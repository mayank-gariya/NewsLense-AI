import streamlit as st
import html

def render_qa_conversation(history):
    if not history:
        return

    st.markdown("""
    <div style="margin: 2rem 0 1rem 0;">
        <h3 style="color: #2d1b69; font-weight: 600;">💬 Conversation</h3>
    </div>
    """, unsafe_allow_html=True)

    for item in reversed(history):
        question = html.escape(item.get("question", ""))
        answer = html.escape(item.get("answer", ""))
        confidence = item.get("confidence")

        # User message
        st.markdown(f"""
        <div style="background:#f8f6ff; border-radius:16px 16px 16px 4px; padding:0.75rem 1rem; margin-bottom:0.5rem; border-left:4px solid #7c3aed; color:#2d1b69; font-weight:500;">
            <span style="font-size:0.85rem; color:#7c6b9e;">You</span><br>
            {question}
        </div>
        """, unsafe_allow_html=True)

        # Assistant message with confidence
        if confidence is not None:
            pct = int(confidence * 100)
            assistant_html = f"""
            <div style="background:white; border-radius:16px 16px 4px 16px; padding:0.75rem 1rem; margin-bottom:1rem; box-shadow:0 2px 8px rgba(108,60,225,0.06); border:1px solid #f0ecff;">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div style="color:#1f2937; line-height:1.6; flex:1;">
                        <span style="font-size:0.85rem; color:#7c6b9e;">Assistant</span><br>
                        {answer}
                    </div>
                    <div style="display:flex; flex-direction:column; align-items:flex-end; margin-left:1rem; min-width:80px;">
                        <span style="font-size:0.65rem; color:#7c6b9e;">Confidence</span>
                        <div style="width:80px; height:4px; background:#ede7ff; border-radius:10px; overflow:hidden; margin-top:0.2rem;">
                            <div style="width:{pct}%; height:100%; background:#7c3aed; border-radius:10px;"></div>
                        </div>
                        <span style="font-size:0.7rem; font-weight:500; color:#2d1b69;">{confidence:.2f}</span>
                    </div>
                </div>
            </div>
            """
        else:
            assistant_html = f"""
            <div style="background:white; border-radius:16px 16px 4px 16px; padding:0.75rem 1rem; margin-bottom:1rem; box-shadow:0 2px 8px rgba(108,60,225,0.06); border:1px solid #f0ecff;">
                <div style="color:#1f2937; line-height:1.6;">
                    <span style="font-size:0.85rem; color:#7c6b9e;">Assistant</span><br>
                    {answer}
                </div>
            </div>
            """

        st.markdown(assistant_html, unsafe_allow_html=True)