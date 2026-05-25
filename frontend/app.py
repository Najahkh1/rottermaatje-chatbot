import sys
from pathlib import Path
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
sys.path.append(str(SRC_DIR))

from services.chatbot_service import ChatbotService


st.set_page_config(
    page_title="RotterMaatje",
    page_icon="🤝",
    layout="centered"
)

st.markdown(
    """
    <style>
    .main-title {
        font-size: 38px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
        color: #2563eb;
    }

    .subtitle {
        text-align: center;
        color: #475569;
        font-size: 17px;
        margin-bottom: 25px;
    }

    .info-box {
        background-color: #2563eb;
        color: white;
        padding: 14px;
        border-radius: 12px;
        margin-bottom: 20px;
        border-left: 5px solid #1d4ed8;
        font-size: 15px;
    }

    .warning-box {
        background-color: #f97316;
        color: white;
        padding: 12px;
        border-radius: 12px;
        margin-bottom: 20px;
        border-left: 5px solid #ea580c;
        font-size: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-title">🤝 RotterMaatje</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Stel je vraag over hulp in Rotterdam</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="info-box">
    RotterMaatje helpt met eenvoudige informatie over eten, douchen, opvang,
    papieren en hulpverlening.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="warning-box">
    Bij direct gevaar of spoed: bel 112.
    RotterMaatje geeft geen medisch of juridisch advies.
    </div>
    """,
    unsafe_allow_html=True
)

if "chatbot" not in st.session_state:
    st.session_state.chatbot = ChatbotService(
        model_name="qwen/qwen3-4b-instruct-2507"
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_question = st.chat_input("Typ hier je vraag...")

if user_question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    with st.chat_message("user"):
        st.write(user_question)

    with st.chat_message("assistant"):

        with st.spinner("RotterMaatje zoekt een antwoord..."):
            answer = st.session_state.chatbot.generate_answer(
                user_question
            )

        st.write(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )