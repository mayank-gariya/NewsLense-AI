import streamlit as st

def render_keywords(keywords):
    """
    Display keyword data as styled chips in a 3‑column grid.
    Expects a list of dicts with keys: 'text', 'score', 'metadata' (with 'source' and 'entity').
    """
    if not keywords:
        return

    st.markdown("""
    <div style="margin: 2rem 0 1rem 0;">
        <h3 style="color: #6a0ffe; font-weight: 600;">🔑 Keywords</h3>
    </div>
    """, unsafe_allow_html=True)

    # Create 3 columns
    cols = st.columns(3)

    for i, kw in enumerate(keywords):
        text = kw.get('text', '')
        score = kw.get('score', 0.0)
        metadata = kw.get('metadata', {})
        entity = metadata.get('entity', '')
        source = metadata.get('source', '')

        # Color palette for entity types (adjust as you like)
        entity_color_map = {
            'EVENT': '#7c3aed',   # purple
            'GPE': '#0891b2',     # cyan
            'NORP': '#059669',    # green
            'ORG': '#d97706',     # amber
            'PERSON': '#dc2626',  # red
            'YAKE': '#6b7280',    # gray (for YAKE-only entries)
        }
        color = entity_color_map.get(entity, "#5d00ff")

        # Build the chip HTML
        chip_html = f"""
        <div style="
            background: white;
            border-radius: 12px;
            padding: 0.75rem 1rem;
            margin-bottom: 0.75rem;
            box-shadow: 0 2px 8px rgba(108, 60, 225, 0.08);
            border-left: 4px solid {color};
            transition: transform 0.15s;
            height: 100%;
        ">
            <div style="display: flex; flex-direction: column; gap: 0.25rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 600; color: #2d1b69; font-size: 1rem;">{text}</span>
                    <span style="
                        background: {color}20;
                        color: {color};
                        font-size: 0.7rem;
                        font-weight: 600;
                        padding: 0.15rem 0.5rem;
                        border-radius: 20px;
                        white-space: nowrap;
                    ">{entity if entity else 'keyword'}</span>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #6b7280;">
                    <span>score: {score:.4f}</span>
                    <span>{source}</span>
                </div>
            </div>
        </div>
        """

        with cols[i % 3]:
            st.markdown(chip_html, unsafe_allow_html=True)