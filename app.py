import streamlit as st
from components.sidebar import render_sidebar
from components.header import render_header
from components.chatbot import render_chatbot
from utils.session_manager import SessionManager
from utils.style_manager import (
    load_global_styles, 
    load_theme_animation, 
    apply_theme_specifics, 
    calculate_content_height
)
from config import Config

def main():
    """메인 애플리케이션 함수 - 채팅창 영역 확장"""

    # 페이지 설정
    st.set_page_config(
        page_title=Config.APP_TITLE,
        page_icon=Config.APP_ICON,
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 레이아웃 간격 조정 스타일 - 채팅창 영역 확장
    st.markdown("""
    <style>
    /* 상단 여백 최소화 */
    #root > div:first-child {
        padding-top: 0 !important;
    }
    .appview-container {
        padding-top: 0 !important;
    }
    .main .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 1rem !important;
    }
    
    /* 사이드바와 메인 영역 간의 간격 최소화 */
    section[data-testid="stSidebar"] {
        margin-right: 0 !important;
        padding-right: 0 !important;
    }
    
    /* 메인 영역 좌측 패딩 최소화 */
    .main .block-container {
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
    }
    
    /* 컬럼 간격 조정 - 넓게 */
    .row-widget.stHorizontal {
        gap: 1.5rem !important;
    }
    
    /* 채팅 컬럼 너비 조정 - 30%로 설정 (기존 25%에서 확대) */
    .row-widget.stHorizontal > div:first-child {
        flex: 0.7 !important;  /* 메인 영역 70% */
    }
    
    .row-widget.stHorizontal > div:last-child {
        flex: 0.3 !important;  /* 채팅 영역 30% */
        min-width: 420px !important;  /* 최소 너비 증가 */
    }
    </style>
    """, unsafe_allow_html=True)

    # 세션 초기화
    SessionManager.initialize_session()
    
    # 스타일 로드
    load_global_styles()
    load_theme_animation()
    apply_theme_specifics()
    
    # 사이드바 렌더링
    render_sidebar()
    
    # 현재 페이지 확인
    current_page = st.session_state.get('current_page', 'home')
    
    # 헤더 렌더링
    render_header()
    
    # 컨텐츠 영역 높이 계산
    content_height = calculate_content_height()
    
    # 레이아웃 설정
    if st.session_state.get('chat_visible', True):
        # 컨텐츠 영역 비율 조정 - 70:30 비율로 변경
        content_width = 0.7
        
        # 간격이 있는 컬럼 생성
        col1, col2 = st.columns([content_width, 1 - content_width])
        
        # 왼쪽 컬럼: 페이지 콘텐츠
        with col1:
            with st.container(height=content_height):
                render_page_content(current_page)
        
        # 오른쪽 컬럼: 챗봇
        with col2:
            render_chatbot()
            
    else:
        # 챗봇이 숨겨진 경우 - 전체 너비에 스크롤 가능한 컨테이너
        with st.container(height=content_height):
            render_page_content(current_page)


def render_page_content(current_page):
    """현재 페이지에 따른 콘텐츠 렌더링 함수"""
    if current_page == "home":
        from pages.home import render_home
        render_home()
    elif current_page == "mindmap":
        from pages.mindmap import render_mindmap
        render_mindmap()
    elif current_page == "beginner":
        from pages.beginner.index import render_beginner
        render_beginner()
    elif current_page == "intermediate":
        from pages.intermediate.index import render_intermediate
        render_intermediate()
    elif current_page == "advanced":
        from pages.advanced.index import render_advanced
        render_advanced()
    elif current_page == "resources":
        from pages.resources.resources import render_resources
        render_resources()
    elif current_page == "analytics":
        from pages.analytics import render_analytics
        render_analytics()
    else:
        st.warning("요청한 페이지를 찾을 수 없습니다.")
        from pages.home import render_home
        render_home()


if __name__ == "__main__":
    main()