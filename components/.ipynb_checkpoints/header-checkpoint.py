import streamlit as st
from utils.localization import t

def render_header():
    """헤더 컴포넌트 - 상단 여백 최소화 및 한 줄 레이아웃"""
    
    # 헤더 스타일 적용
    st.markdown("""
    <style>
    /* 헤더 컨테이너 - 여백 축소 */
    .header-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.5rem 0;
        margin-bottom: 0.8rem;
        /* border-bottom 제거 */
    }
    
    /* 페이지 제목 */
    .page-title {
        display: flex;
        align-items: center;
    }
    
    .logo {
        width: 40px;
        height: 40px;
        background-color: #fb8500;
        border-radius: 6px;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-right: 12px;
    }
    
    .title-text {
        font-size: 1.3rem;
        font-weight: 600;
        color: #333;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 현재 페이지 이름 가져오기
    current_page = st.session_state.get("current_page", "home")
    page_titles = {
        "home": t("home_title"),
        "beginner": t("beginner_title"),
        "intermediate": t("intermediate_title"),
        "advanced": t("advanced_title"),
        "mindmap": t("mindmap_title"),
        "resources": t("resources_title"),
        "analytics": t("analytics_title")
    }
    
    # 페이지 제목 설정
    page_title = page_titles.get(current_page, t("home_title"))
    
    # 컬럼 레이아웃으로 타이틀과 토글 버튼 한 행에 배치
    col1, col2 = st.columns([6, 1])
    
    with col1:
        st.markdown(f"""
            <div class="page-title">
                <div class="logo">EKS</div>
                <div class="title-text">{page_title}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # AI 토글 버튼
        chat_visible = st.toggle(
            label="Chatbot", 
            value=st.session_state.get("chat_visible", True),
            key="chat_toggle"
        )
        
        if chat_visible != st.session_state.get("chat_visible", True):
            st.session_state.chat_visible = chat_visible
            st.rerun()