import streamlit as st
from src.api.g_news_client_backend import GNewsClient
from src.Ai_Feats.header import render_header
from config import Config
from pathlib import Path
from src.ui.ai_news_rendering import ai_news
from src.ui.keyword_render import render_keywords
from src.ui.summary_render import render_summary
from src.ui.sentiment_render import render_sentiment
from src.ui.topic_render import render_topic
from src.ui.entities_render import render_entities
from src.ui.question_answer_render import render_qa_conversation
from src.ui.sidebar_render import render_sidebar

st.set_page_config(page_title="NewsLens · AI Features", page_icon="🤖", layout="wide")

# ---- LOAD CSS ----
def load_css():
    css_path = Path(__file__).parent.parent / "styles" / "custom.css"
    if css_path.exists():
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    # Inline styles for this page
    st.markdown("""
    <style>
        .stSelectbox > div > div > div {
            background-color: #0F1115;
            color: white;
            border: 1px solid #2A2F3A;
            border-radius: 12px;
        }
        .ai-tab-card {
            background: #1A1F2B;
            border: 1px solid #2A2F3A;
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1rem;
        }
        .badge-positive { background: #22C55E; color: white; padding: 0.2rem 1rem; border-radius: 20px; }
        .badge-negative { background: #EF4444; color: white; padding: 0.2rem 1rem; border-radius: 20px; }
        .badge-neutral { background: #6B7280; color: white; padding: 0.2rem 1rem; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)
    
load_css()

# ---------- Protected Route ----------
if "token" not in st.session_state:
    st.switch_page("Get_Started.py")

if "profile" not in st.session_state:
    st.switch_page("Get_Started.py")


client = GNewsClient(st.session_state.token)

profile = st.session_state.get("profile")

if profile is None:
    st.switch_page("Get_Started.py")
    st.stop()
    
# ---- SIDEBAR ----
render_sidebar(profile, client)

# ---- FETCH NEWS ----
news_data = client.get_news()


if news_data is None:
    st.error("Unable to connect to backend.")
    st.stop()

if len(news_data) == 0:
    st.warning("No news available.")
    st.stop()
    

# ---- HEADER ----
render_header(title="AI Features", subtitle="Deep-dive AI insights for any article")

# ---- ARTICLE SELECTION ----
titles = {article["title"]: article for article in news_data}

# some basic news cards 
ai_news(news_data)

selected_title = st.selectbox("Select an article to analyze", list(titles.keys()))
article = titles[selected_title]
article_id = article["id"]

# ---- INIT SESSION STATE FOR THIS ARTICLE ----
if f"summary_{article_id}" not in st.session_state:
    st.session_state[f"summary_{article_id}"] = None
if f"qa_history_{article_id}" not in st.session_state:
    st.session_state[f"qa_history_{article_id}"] = []
if f"sentiment_{article_id}" not in st.session_state:
    st.session_state[f"sentiment_{article_id}"] = None
if f"topic_{article_id}" not in st.session_state:
    st.session_state[f"topic_{article_id}"] = None
if f"entities_{article_id}" not in st.session_state:
    st.session_state[f"entities_{article_id}"] = None
if f"keywords_{article_id}" not in st.session_state:
    st.session_state[f"keywords_{article_id}"] = None

# ---- AI TABS ----
st.markdown("---")
tabs = st.tabs([
    "📝 Summary",
    "❓ Q&A",
    "😊 Sentiment",
    "🏷️ Topic",
    "👥 Entities",
    "🔑 Keywords"
])

with tabs[0]:  # Summary
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("Generate Summary", key=f"summ_btn_{article_id}"):
            with st.spinner("Generating summary..."):
                result = client.get_summary(article_id)
                if result:
                    st.session_state[f"summary_{article_id}"] = result.get("summary")
    with col2:
        if st.session_state[f"summary_{article_id}"]:
            if st.button("Copy", key=f"copy_{article_id}"):
                st.write("📋 Copied!")  # Placeholder
            if st.button("Regenerate", key=f"regen_{article_id}"):
                st.session_state[f"summary_{article_id}"] = None
                st.rerun()
    
    summary = st.session_state[f"summary_{article_id}"]
    if summary:
        render_summary(summary) 

with tabs[1]:  # Q&A
    question = st.text_input("Ask a question about this article", key=f"qa_input_{article_id}")
    if st.button("Ask AI", key=f"qa_btn_{article_id}"):
        if question.strip():
            with st.spinner("Thinking..."):
                result = client.get_qa(article_id, question.strip())
                if result:
                    st.session_state[f"qa_history_{article_id}"].append({
                        "question": question.strip(),
                        "answer": result.get("answer"),
                        "confidence": result.get("confidence")
                    })

    # Display chat history
    if st.session_state.get(f"qa_history_{article_id}"):
        history = st.session_state[f"qa_history_{article_id}"]
        render_qa_conversation(history)
        
with tabs[2]:  # Sentiment
    if st.button("Analyze Sentiment", key=f"sent_btn_{article_id}"):
        with st.spinner("Analyzing..."):
            result = client.get_sentiment(article_id)
            if result:
                st.session_state[f"sentiment_{article_id}"] = result
    
    sentiment_data = st.session_state.get(f"sentiment_{article_id}")
    if sentiment_data:
        render_sentiment(sentiment_data)
        

with tabs[3]:  # Topic
    if st.button("Classify Topic", key=f"topic_btn_{article_id}"):
        with st.spinner("Classifying..."):
            result = client.get_topic(article_id)
            if result:
                st.session_state[f"topic_{article_id}"] = result

    if st.session_state.get(f"topic_{article_id}"):
        topic_data = st.session_state[f"topic_{article_id}"]
        render_topic(topic_data) 
        
with tabs[4]:

    col1, col2 = st.columns([3,1])
    with col1:
        if st.button("Extract Entities", key=f"entity_btn_{article_id}"):
            with st.spinner("Extracting entities..."):
                result = client.get_entities(article_id)
                if result:
                    st.session_state[f"entities_{article_id}"] = result

    with col2:
        if st.session_state[f"entities_{article_id}"]:
            if st.button("Regenerate", key=f"entity_regen_{article_id}"):
                st.session_state[f"entities_{article_id}"] = None
                st.rerun()
    
    if st.session_state.get(f"entities_{article_id}"):
        entities = st.session_state[f"entities_{article_id}"]
        render_entities(entities)

with tabs[5]:

    col1, col2 = st.columns([3,1])
    with col1:
        if st.button("Extract Keywords", key=f"keyword_btn_{article_id}"):
            with st.spinner("Finding keywords..."):
                result = client.get_keywords(article_id)
                if result:
                    st.session_state[f"keywords_{article_id}"] = result

    with col2:
        if st.session_state[f"keywords_{article_id}"]:
            if st.button("Regenerate", key=f"keyword_regen_{article_id}"):
                st.session_state[f"keywords_{article_id}"] = None
                st.rerun()

    keywords = st.session_state[f"keywords_{article_id}"]
    
    render_keywords(keywords)
    