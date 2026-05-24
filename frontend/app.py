import sys
from pathlib import Path
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
sys.path.append(str(SRC_DIR))

from services.chatbot_service import ChatbotService
from safety.safety_rules import detect_language


st.set_page_config(
    page_title="RotterMaatje",
    page_icon="🤝",
    layout="wide"
)

st.title("🤝 RotterMaatje")
st.caption("AI-chatbot met FAQ, RAG, safety rules en meertalige ondersteuning")

with st.sidebar:
    st.header("Instellingen")

    model_choice = st.selectbox(
        "Model",
        ["qwen/qwen3-4b-instruct-2507", "gemma-3-4b-it"]
    )

    st.metric("Retrieval threshold", "0.60")
    st.metric("RAG bronnen", "FAQ + websites")
    st.metric("Safety", "Aan")

    debug_mode = st.toggle("Debug mode", value=True)

if "chatbot" not in st.session_state or st.session_state.model != model_choice:
    st.session_state.chatbot = ChatbotService(model_name=model_choice)
    st.session_state.model = model_choice

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_question = st.chat_input("Stel je vraag aan RotterMaatje...")

if user_question:
    st.session_state.messages.append(
        {"role": "user", "content": user_question}
    )

    with st.chat_message("user"):
        st.write(user_question)

    language = detect_language(user_question)

    with st.chat_message("assistant"):
        with st.spinner("RotterMaatje denkt na..."):
            answer = st.session_state.chatbot.generate_answer(user_question)

        st.write(answer)

        if debug_mode:
            with st.expander("Debug informatie"):
                st.write(f"**Model:** {model_choice}")
                st.write(f"**Gedetecteerde taal:** {language}")
                st.write("**Pipeline:** Safety rules → RAG retrieval → LLM antwoord")
                st.write("**Bronnen:** FAQ + web_sources.json")
                st.write("**Threshold:** 0.60")

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
    