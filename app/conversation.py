from pyexpat.errors import messages
import re

from app.query_analyzer import analyze_query


class ConversationManager:

    ROLE_KEYWORDS = [
        "developer", "engineer", "analyst", "manager", "sales",
        "marketing", "graduate", "intern", "accountant", "hr",
        "recruiter", "support"
    ]

    def build_state(self, messages):

        state = {
            # Conversation
          "intent": "recommend",      # recommend | compare | refine | refuse

           # Candidate information
          "role": None,
          "experience": None,
          "skills": [],
          "job_level": None,

          # Assessment filters
          "categories": [],
          "remote": None,
          "adaptive": None,
          "duration": None,

          # Comparison
          "assessment_names": [],

           # Conversation
           "raw_query": "",
           "last_recommendations": []
        }

        last_assistant_question = None

        for message in messages:

            if message.role == "assistant":
                last_assistant_question = message.content
                continue

            if message.role != "user":
                continue

            text = message.content.lower()
            state["raw_query"] += " " + message.content
            
            for role in self.ROLE_KEYWORDS:
                if role in text:
                    state["role"] = role

            exp = re.search(r"(\d+)\s*(year|years)", text)
            if exp:
                state["experience"] = exp.group(1)
            elif last_assistant_question and "experience" in last_assistant_question.lower():
                bare_num = re.search(r"\d+", text)
                if bare_num:
                    state["experience"] = bare_num.group(0)

            if "remote" in text or "online" in text:
                state["remote"] = "yes"

            duration = re.search(r"(\d+)\s*(minute|min)", text)
            if duration:
                state["duration"] = duration.group(1)

            if "graduate" in text:
                state["job_level"] = "graduate"
            elif "manager" in text:
                state["job_level"] = "manager"
            elif "director" in text:
                state["job_level"] = "director"

    # -----------------------------
    # Analyze latest user message
    # -----------------------------
        latest_user_message = ""

        for message in reversed(messages):
            if message.role == "user":
                latest_user_message = message.content
                break

        analysis = analyze_query(latest_user_message)
    
        state["intent"] = analysis["intent"]
        state["assessment_names"] = analysis["comparison"]

        return state
        
    

    def needs_clarification(self, state):
        if state["intent"] == "compare":
            return False

        return state["role"] is None


    def get_clarification_question(self, state):
        if state["intent"] == "compare":
            return None

        if state["role"] is None:
            return "What role are you hiring for?"

        if state["experience"] is None:
            return "How many years of experience should the candidate have?"

        return None