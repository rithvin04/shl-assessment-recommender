import streamlit as st


def recommendation_card(rec):

    with st.container(border=True):

        st.subheader(rec["name"])

        st.write(f"**Type:** {rec['test_type']}")

        st.link_button(
            "Open SHL Assessment",
            rec["url"]
        )