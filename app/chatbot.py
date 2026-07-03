import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")
def build_catalog(assessments):

    catalog = ""

    for assessment in assessments:

        catalog += f"""
Assessment Name: {assessment['name']}
Description: {assessment['description']}
Duration: {assessment['duration']}
Remote Testing: {assessment['remote']}
Adaptive Testing: {assessment['adaptive']}
Categories: {assessment['categories']}
URL: {assessment['url']}

"""

    return catalog


def generate_recommendation(user_query, assessments):

    catalog = ""

    for assessment in assessments:
        catalog = build_catalog(assessments)
    prompt = f"""
You are an SHL Assessment Recommendation Assistant.

Follow these rules strictly:

1. Recommend ONLY assessments from the provided catalog.
2. Never invent assessment names.
3. Never invent URLs.
4. Explain why each recommended assessment is suitable.
5. If multiple assessments match, rank them from best to least suitable.
6. If the user has not provided enough information, ask exactly ONE clarification question.
7. If the request is unrelated to SHL assessments, politely refuse.
8. Keep the response concise and professional.
9. Use only the information provided in the catalog below.

User Requirements:
{user_query}

Available SHL Assessments:

{catalog}

Respond in this format:

Summary:
<2-3 sentence explanation>

Recommendations:
1. Assessment Name
   - Why it matches
   - Duration
   - Remote Support
   - URL

2. Assessment Name
   - Why it matches
   - Duration
   - Remote Support
   - URL
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception:
     result = "### Recommended Assessments\n\n"

     for i, assessment in enumerate(assessments, 1):
        result += (
            f"{i}. {assessment['name']}\n"
            f"Duration: {assessment['duration']}\n"
            f"Remote: {assessment['remote']}\n"
            f"URL: {assessment['url']}\n\n"
        )

    result += (
        "Gemini summary is currently unavailable because the API quota "
        "has been exceeded."
    )

    return result


def generate_comparison(first, second):

    prompt = f"""
You are an SHL Assessment Assistant.

Compare ONLY these two SHL assessments.

Assessment 1

Name: {first['name']}
Description: {first['description']}
Duration: {first['duration']}
Categories: {first['categories']}
Remote: {first['remote']}

Assessment 2

Name: {second['name']}
Description: {second['description']}
Duration: {second['duration']}
Categories: {second['categories']}
Remote: {second['remote']}

Rules:
- Compare only the information provided.
- Do not invent any features.
- Mention similarities and differences.
- Finish with when each assessment is more suitable.
"""

    response = model.generate_content(prompt)

    return response.text


def generate_refusal():

    return (
        "I can only assist with SHL assessment recommendations, "
        "assessment comparisons, and job-description based assessment selection."
    )




