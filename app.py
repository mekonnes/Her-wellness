import streamlit as st
import os
from rag import load_knowledge_base, build_vector_store, get_answer

st.set_page_config(
    page_title="Her Wellness",
    page_icon="✦",
    layout="centered"
)

st.markdown("""
<style>
.stApp { background-color: #0A0A0A; }
.stButton > button {
    background-color: transparent;
    color: #D4AF5A;
    border: 1px solid #4A3A1A;
    border-radius: 3px;
    font-family: Georgia, serif;
    font-size: 13px;
    padding: 10px 16px;
    font-weight: 400;
    letter-spacing: 1px;
}
.stButton > button:hover {
    background-color: #1E1600;
    color: #D4AF5A;
    border-color: #D4AF5A;
}
.stTextInput > div > input {
    background-color: #111111;
    color: #D4AF5A;
    border: 1px solid #4A3A1A;
    border-radius: 3px;
    font-family: Georgia, serif;
    font-size: 14px;
}
.stTextInput > div > input::placeholder {
    color: #4A3A1A;
}
div[data-testid="stSidebar"] {
    background-color: #060606;
    border-right: 1px solid #1E1600;
}
</style>
""", unsafe_allow_html=True)

api_key = os.environ.get("GROQ_API_KEY", "")

@st.cache_resource
def initialize():
    docs = load_knowledge_base()
    vs = build_vector_store(docs)
    return vs

st.markdown("""
<div style='text-align:center; padding:40px 0 28px 0;'>
    <p style='color:#8B7340; font-size:11px; letter-spacing:6px; margin:0 0 14px 0; font-family:Georgia,serif;'>HEALTH EDUCATION FOR BLACK WOMEN</p>
    <h1 style='color:#D4AF5A; font-family:Georgia,serif; font-size:52px; font-weight:400; letter-spacing:8px; margin:0 0 16px 0;'>Her Wellness</h1>
    <div style='width:80px; height:1px; background:#D4AF5A; margin:0 auto;'></div>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='border:none; border-top:1px solid #1E1600; margin:0 0 32px 0;'>", unsafe_allow_html=True)

st.markdown("<p style='color:#8B7340; font-size:11px; letter-spacing:4px; margin-bottom:14px; font-family:Georgia,serif;'>SELECT A HEALTH TOPIC</p>", unsafe_allow_html=True)

topics = {
    "Fibroids": "fibroids",
    "Maternal Health": "maternal health",
    "Mental Health": "mental health",
    "Hypertension": "hypertension",
    "Nutrition": "nutrition",
    "Navigating Healthcare": "navigating healthcare as a Black woman",
}

if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = None

if "answer" not in st.session_state:
    st.session_state.answer = None

if "trigger_answer" not in st.session_state:
    st.session_state.trigger_answer = False

cols = st.columns(3)
for i, (label, value) in enumerate(topics.items()):
    with cols[i % 3]:
        if st.button(label, use_container_width=True, key=f"topic_{i}"):
            st.session_state.selected_topic = value
            st.session_state.answer = None

if st.session_state.selected_topic:
    st.markdown(f"<p style='color:#8B7340; font-size:11px; letter-spacing:3px; margin-top:14px; font-family:Georgia,serif;'>TOPIC — {st.session_state.selected_topic.upper()}</p>", unsafe_allow_html=True)

st.markdown("<hr style='border:none; border-top:1px solid #1E1600; margin:24px 0;'>", unsafe_allow_html=True)

st.markdown("<p style='color:#8B7340; font-size:11px; letter-spacing:4px; margin-bottom:10px; font-family:Georgia,serif;'>YOUR QUESTION</p>", unsafe_allow_html=True)

def on_enter():
    st.session_state.trigger_answer = True

question = st.text_input(
    "Your question",
    placeholder="e.g. What are my treatment options for fibroids?",
    key="question_input",
    label_visibility="collapsed",
    on_change=on_enter
)

st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)

def run_query(q):
    if not api_key:
        st.session_state.answer = "API key not found."
        return
    with st.spinner("Finding the best answer for you..."):
        try:
            vector_store = initialize()
            result = get_answer(q, vector_store, api_key, st.session_state.selected_topic)
            st.session_state.answer = result
        except Exception as e:
            st.session_state.answer = f"Error: {str(e)}"

if st.session_state.trigger_answer and st.session_state.get("question_input", "").strip():
    st.session_state.trigger_answer = False
    run_query(st.session_state.question_input)

if st.button("GET ANSWER", use_container_width=True, key="get_answer"):
    if not question.strip():
        st.warning("Please type a question first.")
    else:
        run_query(question)

if st.session_state.answer:
    st.markdown("<hr style='border:none; border-top:1px solid #1E1600; margin:28px 0 16px 0;'>", unsafe_allow_html=True)
    st.markdown("<p style='color:#8B7340; font-size:11px; letter-spacing:4px; margin-bottom:14px; font-family:Georgia,serif;'>ANSWER</p>", unsafe_allow_html=True)
    st.markdown(f"<div style='background:#111111; border-left:2px solid #D4AF5A; padding:22px 26px; border-radius:3px; color:#E8D5A0; line-height:1.9; font-size:15px; font-family:Georgia,serif;'>{st.session_state.answer}</div>", unsafe_allow_html=True)
    st.markdown("<p style='color:#4A3A1A; font-size:11px; margin-top:14px; letter-spacing:1px;'>This information is for educational purposes only. Always consult a qualified healthcare provider for personal medical advice.</p>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<h2 style='color:#D4AF5A; font-family:Georgia,serif; font-weight:400; letter-spacing:2px;'>About</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#8B7340; font-size:13px; line-height:1.9;'>Her Wellness is an AI-powered health education tool built specifically for Black and African women. All answers are grounded in medically reviewed sources from NIH, CDC, Office on Women's Health, and Black Women's Health Imperative.</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border:none; border-top:1px solid #1E1600;'>", unsafe_allow_html=True)
    st.markdown("<p style='color:#D4AF5A; font-size:11px; letter-spacing:3px;'>CRISIS RESOURCES</p>", unsafe_allow_html=True)
    st.markdown("<p style='color:#8B7340; font-size:13px;'>Call or text <strong style='color:#D4AF5A;'>988</strong> — Suicide & Crisis Lifeline</p>", unsafe_allow_html=True)
    st.markdown("<p style='color:#8B7340; font-size:13px;'>Text HOME to <strong style='color:#D4AF5A;'>741741</strong> — Crisis Text Line</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border:none; border-top:1px solid #1E1600;'>", unsafe_allow_html=True)
    st.markdown("<p style='color:#2A2000; font-size:11px;'>Built with Python, LangChain, FAISS, Groq LLM API, Streamlit</p>", unsafe_allow_html=True)