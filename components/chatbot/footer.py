import streamlit as st


def render_chatbot_footer():
    """챗봇 푸터 컴포넌트"""
    st.markdown("""
    <style>
    .chatbot-footer {
        padding: 10px 18px;
        border-top: 1px solid #e9ecef;
        font-size: 0.7rem;
        color: #6c757d;
        text-align: right;
        background-color: #FAFAFA;
        border-radius: 0 0 10px 10px;
    }
    
    .powered-by {
        font-weight: 500;
    }
    
    .aws-text {
        color: #EA4335;
    }
    </style>
    
    <div class="chatbot-footer">
        <span class="powered-by">Powered by <span class="aws-text">AWS Bedrock</span> | Claude 3 Sonnet</span>
    </div>
    """, unsafe_allow_html=True)