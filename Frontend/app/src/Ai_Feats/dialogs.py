import streamlit as st
from src.api.gnews_client import GNewsClient
from src.utils.helpers import format_published_date

def show_article_dialog(article):
    """Open a dialog showing full article content."""
    with st.dialog("Full Article", width="large"):
        if article.get("image"):
            st.image(article["image"], use_column_width=True)
        st.header(article.get("title"))
        st.caption(f"Source: {article.get('source', 'Unknown')} | {format_published_date(article.get('published_at'))}")
        st.markdown(article.get("content", "Content not available."))
        if st.button("Close", key="close_article_dialog"):
            st.rerun()

def show_ai_dialog(article):
    """Open a dialog with AI assistant tabs."""
    # Set session state to open dialog
    st.session_state.selected_article = article
    st.session_state.ai_dialog_open = True

def render_ai_tabs(article):
    """
    Render the AI tabs (Summary, Q&A, Sentiment, Topic) for a given article.
    This can be used inside a dialog or a full page.
    """
    client = GNewsClient(st.session_state.token)
    article_id = article["id"]

    # Initialise session state for this article
    if f"summary_{article_id}" not in st.session_state:
        st.session_state[f"summary_{article_id}"] = None
    if f"qa_history_{article_id}" not in st.session_state:
        st.session_state[f"qa_history_{article_id}"] = []
    if f"sentiment_{article_id}" not in st.session_state:
        st.session_state[f"sentiment_{article_id}"] = None
    if f"topic_{article_id}" not in st.session_state:
        st.session_state[f"topic_{article_id}"] = None

    tabs = st.tabs(["📝 Summary", "❓ Q&A", "😊 Sentiment", "🏷️ Topic"])

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
                    st.write("📋 Copied!")  # Placeholder; could use st.write to clipboard
                if st.button("Regenerate", key=f"regen_{article_id}"):
                    st.session_state[f"summary_{article_id}"] = None
                    st.rerun()
        if st.session_state[f"summary_{article_id}"]:
            st.success(st.session_state[f"summary_{article_id}"])

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
        for item in st.session_state[f"qa_history_{article_id}"]:
            st.markdown(f"**Q:** {item['question']}")
            st.markdown(f"**A:** {item['answer']}")
            if item.get("confidence"):
                st.progress(float(item["confidence"]))

    with tabs[2]:  # Sentiment
        if st.button("Analyze Sentiment", key=f"sent_btn_{article_id}"):
            with st.spinner("Analyzing..."):
                result = client.get_sentiment(article_id)
                if result:
                    st.session_state[f"sentiment_{article_id}"] = result
        if st.session_state[f"sentiment_{article_id}"]:
            sent = st.session_state[f"sentiment_{article_id}"]
            label = sent.get("label", "neutral")
            score = sent.get("score", 0)
            color = "green" if label == "positive" else "red" if label == "negative" else "gray"
            st.markdown(f"<span style='background:{color}; padding:0.2rem 1rem; border-radius:20px; color:white;'>{label.upper()}</span>", unsafe_allow_html=True)
            st.write(f"Confidence: {score:.2f}")

    with tabs[3]:  # Topic
        if st.button("Classify Topic", key=f"topic_btn_{article_id}"):
            with st.spinner("Classifying..."):
                result = client.get_topic(article_id)
                if result:
                    st.session_state[f"topic_{article_id}"] = result
        if st.session_state[f"topic_{article_id}"]:
            topic = st.session_state[f"topic_{article_id}"].get("topic", "Unknown")
            st.success(f"🏷️ {topic}")