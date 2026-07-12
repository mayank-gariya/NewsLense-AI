import streamlit as st

def render_entities(entities: list):
    """
    Display named entities as purple‑themed chips in a grid.
    Expects a list of dicts with keys: 'text' (string) and 'label' (string).
    Optional: 'score' (float) if available.
    """
    if not entities:
        return

    st.markdown("""
    <div style="margin: 2rem 0 1rem 0;">
        <h3 style="color: #6a0ffe; font-weight: 600;">🏷️ Named Entities</h3>
    </div>
    """, unsafe_allow_html=True)

    # Color palette for common entity types
    entity_colors = {
        "PERSON": "#dc2626",    # red
        "ORG": "#d97706",       # amber
        "GPE": "#0891b2",       # cyan
        "LOC": "#0891b2",       # cyan (same as GPE)
        "DATE": "#7c3aed",      # purple
        "TIME": "#7c3aed",      # purple
        "MONEY": "#059669",     # green
        "PERCENT": "#059669",   # green
        "FAC": "#6b7280",       # gray
        "PRODUCT": "#8b5cf6",   # violet
        "EVENT": "#ec4899",     # pink
        "LAW": "#f59e0b",       # yellow
        "LANGUAGE": "#3b82f6",  # blue
        "WORK_OF_ART": "#f472b6", # pink
    }
    default_color = "#6a0ffe"   

    # Create a 3‑column grid
    cols = st.columns(3)

    for i, entity in enumerate(entities):
        text = entity.get("text", "")
        label = entity.get("label", "Unknown")
        # Optional score
        score = entity.get("score")

        color = entity_colors.get(label, default_color)

        # Build the chip HTML
        chip_html = f"""
        <div style="
            background: white;
            border-radius: 12px;
            padding: 0.5rem 0.75rem;
            margin-bottom: 0.6rem;
            box-shadow: 0 2px 8px rgba(108, 60, 225, 0.08);
            border-left: 4px solid {color};
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: transform 0.15s;
        ">
            <span style="font-weight: 500; color: #2d1b69; font-size: 0.9rem;">{text}</span>
            <span style="
                background: {color}20;
                color: {color};
                font-size: 0.65rem;
                font-weight: 600;
                padding: 0.1rem 0.5rem;
                border-radius: 20px;
                white-space: nowrap;
                text-transform: uppercase;
            ">{label}</span>
        </div>
        """

        with cols[i % 3]:
            st.markdown(chip_html, unsafe_allow_html=True)