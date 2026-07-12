import streamlit as st

def render_summary(summary_text: str):
    """
    Display the summary in a purple‑themed container.
    Optionally shows a 'Regenerate' button (you can pass a callback).
    """
    if not summary_text:
        return

    st.markdown("""
    <div style="margin: 2rem 0 1rem 0;">
        <h3 style="color: #6a0ffe; font-weight: 600;">📋 Summary</h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="
        background: #f8f6ff;
        border-radius: 16px;
        padding: 1.5rem;
        border-left: 4px solid #7c3aed;
        box-shadow: 0 4px 12px rgba(108, 60, 225, 0.08);
        color: #2d1b69;
        line-height: 1.7;
        font-size: 1rem;
        margin-bottom: 1rem;
    ">
        {summary_text}
    </div>
    """, unsafe_allow_html=True)
