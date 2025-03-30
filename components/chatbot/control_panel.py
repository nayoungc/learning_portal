import streamlit as st
from utils.localization import t

def render_control_panel():
    """챗봇 제어 버튼 영역 컴포넌트"""
    
    # 버튼 스타일 추가
    st.markdown("""
    <style>
    div[data-testid="column"] > div[data-testid="stVerticalBlock"] > div[data-testid="element-container"] > div {
        display: flex;
        justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 컬럼을 중첩하지 않고 직접 반환
    cols = st.columns(5)
    
    with cols[1]:
        reset_clicked = st.button(
            "🔄 초기화", 
            key="reset_chat", 
            help="대화 기록을 초기화합니다",
            type="primary"
        )
    
    with cols[3]:
        commands_clicked = st.button(
            "📋 명령어", 
            key="toggle_commands", 
            help="kubectl 명령어 가이드를 표시합니다"
        )
    
    return reset_clicked, commands_clicked