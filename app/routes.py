from fastapi import APIRouter, Request
from app.retriever import Retriever
from app.conversation import ConversationManager
from app.models import (
    ChatRequest,
    ChatResponse,
    Recommendation
)


from app.chatbot import (
    generate_recommendation,
    generate_comparison,
    generate_refusal
)
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
    


   # -----------------------------
# Compare Assessments
# -----------------------------
    if analysis["intent"] == "compare":
        comparison = retriever.compare(
            analysis["comparison"]
       )

        results = comparison["results"]

        found = [r for r in results if r.get("found")]
        missing = [r["name"] for r in results if not r.get("found")]

        if len(found) != 2:
            reply = ""

            if found:
                reply += f"Found: {found[0]['name']}\n\n"

            if missing:
                reply += f"Not Found: {', '.join(missing)}\n\n"

            reply += (
            "I can only compare assessments that exist in the SHL catalog."
            )

            return ChatResponse(
                reply=reply,
                recommendations=[],
                end_of_conversation=True
           )

        first = found[0]
        second = found[1]

        reply = generate_comparison(
            first,
            second
        )

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
        reply=generate_refusal(),
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
    reply = generate_recommendation(
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
  