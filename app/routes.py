from fastapi import APIRouter, Request

from app.models import (
    ChatRequest,
    ChatResponse,
    Recommendation
)

from app.conversation import ConversationManager
from app.chatbot import generate_response
from app.query_analyzer import analyze_query
router = APIRouter()

manager = ConversationManager()


@router.get("/health")
async def health():
    return {
        "status": "ok"
    }


@router.post("/chat", response_model=ChatResponse)
async def chat(
    body: ChatRequest,
    request: Request
):
    """
    SHL Assessment Chatbot Endpoint
    """

    # Get retriever instance created during FastAPI startup
    
    from app.retriever import Retriever
    if request.app.state.retriever is None:
         print("Loading retriever...")
         request.app.state.retriever = Retriever()
         print("Retriever loaded.")
        
    retriever = request.app.state.retriever


    # Build conversation state from all messages
    state = manager.build_state(body.messages)

    # Combined user query
    user_query = state["raw_query"].strip()
    latest_query = body.messages[-1].content

    analysis = analyze_query(latest_query)
    


    if analysis["intent"] == "compare":
        assessments = retriever.compare_assessments(
           analysis["comparison"]
        )
        if len(assessments) < 2:
            return ChatResponse(
                reply="I couldn't find both assessments to compare.",
                recommendations=[],
                end_of_conversation=True
            )

        first = assessments[0]
        second = assessments[1]

        reply = f"""
Comparison of {first['name']} and {second['name']}

Test Type:
• {first['name']}: {first['categories']}
• {second['name']}: {second['categories']}

Duration:
• {first['name']}: {first['duration']}
• {second['name']}: {second['duration']}

Remote:
• {first['name']}: {first['remote']}
• {second['name']}: {second['remote']}

Adaptive:
• {first['name']}: {first['adaptive']}
• {second['name']}: {second['adaptive']}

Description:

• {first['name']}:
{first['description']}

• {second['name']}:
{second['description']}
"""

        return ChatResponse(
            reply=reply,
            recommendations=[],
            end_of_conversation=True
         )
        
    # -----------------------------
    # Refuse Off-topic Queries
    # -----------------------------
    if analysis["intent"] == "refuse":

        return ChatResponse(
            reply=(
                "I can only assist with SHL assessment recommendations, "
                "comparisons, and refinements. I can't help with unrelated "
                "questions, legal advice, or general hiring advice."
            ),
            recommendations=[],
            end_of_conversation=True
        )
    
    # Ask clarification question if required
    clarification = manager.get_clarification_question(state)

    if clarification:
        return ChatResponse(
            reply=clarification,
            recommendations=[],
            end_of_conversation=False
        )
    
    # Retrieve top assessments
    results = retriever.search(
        query=user_query,
        top_k=5
    )
   
    # No results found
    if len(results) == 0:

        return ChatResponse(
            reply="Sorry, I couldn't find a suitable SHL assessment for your requirements.",
            recommendations=[],
            end_of_conversation=True
        )

    # Generate Gemini response
    reply = generate_response(
        user_query=user_query,
        assessments=results
    )

    # Build recommendation list
    recommendations = []

    for assessment in results:

        categories = assessment.get("categories", "")

        if isinstance(categories, list):
            test_type = ", ".join(categories)
        else:
            test_type = str(categories)

        recommendations.append(
            Recommendation(
                name=assessment["name"],
                url=assessment["url"],
                test_type=test_type
            )
        )

    return ChatResponse(
        reply=reply,
        recommendations=recommendations,
        end_of_conversation=True
    )
  