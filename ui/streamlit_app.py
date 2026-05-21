import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import streamlit as st
from app.agent import run_agent

st.set_page_config(page_title="Text-to-SQL Agent")

st.title("🧠 Agentic Text-to-SQL System")

question = st.text_input("Enter your SQL question")

if st.button("Run Agent"):

    if question:

        with st.spinner("Thinking like SQL expert agent Please Wait..."):

            response = run_agent(question)

        st.subheader("📌 Decomposition")
        st.json(response["decomposition"])

        st.subheader("⚡ Generated SQL")
        st.code(response["sql"], language="sql")

        st.subheader("📊 Result")
        st.json(response["result"])

        st.subheader("🧾 Summary")
        st.write(response["summary"])

        st.success(response["status"])