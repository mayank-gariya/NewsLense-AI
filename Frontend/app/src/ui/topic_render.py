import streamlit as st

def render_topic(topic_data: dict):
    """
    Display the detected topic in a purple‑themed chip/card.
    Expects a dict with key 'topic' (string), optionally 'confidence' (float).
    """
    if not topic_data:
        return

    topic = topic_data.get("topic", "Unknown")
    confidence = topic_data.get("confidence")  # optional

    # Build the display
    st.markdown("""
    <div style="margin: 2rem 0 1rem 0;">
        <h3 style="color: #6a0ffe; font-weight: 600;">🏷️ Detected Topic</h3>
    </div>
    """, unsafe_allow_html=True)

    # Main card
    if confidence is not None:
        # Show with confidence bar
        st.markdown(f"""
        <div style="
            background: white;
            border-radius: 16px;
            padding: 1rem 1.5rem;
            box-shadow: 0 4px 12px rgba(108, 60, 225, 0.08);
            border: 1px solid #f0ecff;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 1rem;
        ">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <span style="font-size: 1.5rem;">🔖</span>
                <span style="font-weight: 600; color: #6a0ffe; font-size: 1.1rem;">{topic}</span>
            </div>
            <div style="display: flex; align-items: center; gap: 1rem;">
                <span style="color: #7c6b9e; font-size: 0.85rem;">Confidence</span>
                <div style="width: 100px; height: 6px; background: #ede7ff; border-radius: 10px; overflow: hidden;">
                    <div style="width: {confidence*100:.0f}%; height: 100%; background: #7c3aed; border-radius: 10px;"></div>
                </div>
                <span style="font-weight: 500; color: #2d1b69;">{confidence:.2f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="
            background: white;
            border-radius: 16px;
            padding: 1rem 1.5rem;
            box-shadow: 0 4px 12px rgba(108, 60, 225, 0.08);
            border: 1px solid #f0ecff;
            display: inline-block;
        ">
            <span style="font-size: 1.5rem;">🔖</span>
            <span style="font-weight: 600; color: #2d1b69; font-size: 1.1rem; margin-left: 0.5rem;">{topic}</span>
        </div>
        """, unsafe_allow_html=True)