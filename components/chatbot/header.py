import streamlit as st
from utils.localization import t


def render_chatbot_header():
    """챗봇 헤더 컴포넌트"""
    st.markdown("""
    <style>
    .chatbot-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 18px;
        border-bottom: 1px solid #f0f0f0;
        background: linear-gradient(to right, #FFFFFF, #F8F9FA);
        border-radius: 10px 10px 0 0;
        margin-top: 0;
    }
    
    .chatbot-title {
        display: flex;
        align-items: center;
    }
    
    .chatbot-icon {
        font-size: 1.5rem;
        margin-right: 10px;
        color: #326CE5;
    }
    
    .chatbot-name {
        font-size: 1.15rem;
        font-weight: 600;
        color: #333;
    }
    
    .chatbot-status {
        background-color: #EA4335;
        color: #FFFFFF;
        border-radius: 20px;
        padding: 3px 10px;
        font-size: 0.7rem;
        font-weight: bold;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    
    <div class="chatbot-header">
        <div class="chatbot-title">
            <div class="chatbot-icon">🤖</div>
            <div class="chatbot-name">EKS & K8s Expert</div>
        </div>
        <div class="chatbot-status">ONLINE</div>
    </div>
    """, unsafe_allow_html=True)