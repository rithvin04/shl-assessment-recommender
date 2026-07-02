import streamlit as st

from api import send_message
from components import recommendation_card

with st.sidebar:

    st.title("SHL Assistant")

    if st.button("🗑️ New Chat"):

        st.session_state.messages = []

        st.rerun()

    st.divider()

    st.success("Backend Connected")

st.set_page_config(
    page_title="SHL Assessment Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 SHL Assessment Recommendation Assistant")

st.caption("Find the best SHL assessments using AI.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input(
    "Describe the role you are hiring for..."
)

if prompt:

    # Add user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Send to backend
    with st.spinner("Finding the best assessments..."):

        response = send_message(
            st.session_state.messages
        )

    # Display assistant reply
    with st.chat_message("assistant"):

        st.markdown(response["reply"])

        if response["recommendations"]:

            st.markdown("---")

            st.subheader("Recommended Assessments")

            for rec in response["recommendations"]:
                recommendation_card(rec)

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response["reply"]
        }
    )