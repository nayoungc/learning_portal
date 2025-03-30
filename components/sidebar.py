import streamlit as st
from utils.localization import t, Localization
from utils.session_manager import SessionManager


def render_sidebar():
    """사이드바 렌더링"""
    SessionManager.initialize_session()
    
    # 기본 Streamlit 메뉴 숨기기 및 스타일 적용
    st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        /* 기본 메뉴 숨기기 */
        [data-testid="stSidebarNav"] {display: none !important;}
        
        /* 사이드바의 불필요한 상단 여백 제거 */
        [data-testid="stSidebarUserContent"] {
            padding-top: 0rem;
        }
        
        /* 사이드바 레이블 폰트 크기 통일 */
        [data-testid="stSidebarUserContent"] label {
            font-size: 0.8rem !important;
            font-weight: 400 !important;
        }
        
        /* 불필요한 구분선 숨기기 */
        .sidebar .stRadio ~ hr {
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        # 앱 제목 및 아이콘
        st.markdown('<h2 style="margin-bottom:1rem;">🚀  ' + t('app_title') + '</h1>', unsafe_allow_html=True)
        
        # 국기 아이콘이 포함된 드롭다운 언어 선택
        language_options = {
            "en": "🇺🇸  English",
            "ko": "🇰🇷  한국어"
        }
        
        current_language = st.session_state.get('language', 'en')
        
        # 현재 선택된 언어 표시        
        selected_language = st.selectbox(
            t("select_language"),
            options=list(language_options.keys()),
            format_func=lambda x: language_options[x],
            index=list(language_options.keys()).index(current_language) if current_language in language_options else 0,
        )
        
        if selected_language != current_language:
            Localization.change_language(selected_language)
            st.rerun()
        
        # 테마 설정 - 한 줄에 표시
        if 'theme_mode' not in st.session_state:
            st.session_state.theme_mode = "light"  # 기본값은 라이트 모드
        
        # 테마 선택 라디오 버튼
        theme_mode = st.radio(
            t("theme"),
            options=["light", "dark"],
            format_func=lambda x: t("Light mode") if x == "light" else t("Dark mode"),
            index=0 if st.session_state.theme_mode == "light" else 1,
            horizontal=True,
        )
        
        if theme_mode != st.session_state.theme_mode:
            st.session_state.theme_mode = theme_mode
        
            # 먼저 Python에서 배경색 결정
            bg_color = "black" if theme_mode == "dark" else "white"
            
            # 수정된 스크립트 - JavaScript 조건문 대신 Python에서 계산된 값 사용
            theme_script = f'''
            <script>
                // 테마 변경 전에 오버레이 추가
                const overlay = document.createElement('div');
                overlay.style.position = 'fixed';
                overlay.style.top = '0';
                overlay.style.left = '0';
                overlay.style.width = '100%';
                overlay.style.height = '100%';
                overlay.style.backgroundColor = '{bg_color}';
                overlay.style.opacity = '0';
                overlay.style.zIndex = '9999';
                overlay.style.transition = 'opacity 0.3s ease';
                document.body.appendChild(overlay);
                
                // 오버레이를 약간 보이게 한 후 테마 변경 실행
                setTimeout(() => {{
                    overlay.style.opacity = '0.3';
                    
                    // Streamlit 테마 설정 변경
                    const theme = '{theme_mode}';
                    localStorage.setItem('theme', theme);
                    
                    // 색상 테마 변경 이벤트 발생시키기
                    const event = new Event('streamlit:themeChanged');
                    window.dispatchEvent(event);
                    
                    // 페이지 새로고침 전 잠시 대기
                    setTimeout(() => {{
                        window.location.reload();
                    }}, 300);
                }}, 50);
            </script>
            '''
            st.markdown(theme_script, unsafe_allow_html=True)
            st.rerun()
        
        # 여기 구분선 제거됨 (st.divider()가 있던 위치)
        
        # 메뉴 아이템 정의
        menu_items = [
            {"name": t("home"), "icon": "house", "id": "home"},
            {"name": t("beginner"), "icon": "1-circle", "id": "beginner"},
            {"name": t("intermediate"), "icon": "2-circle", "id": "intermediate"},
            {"name": t("advanced"), "icon": "3-circle", "id": "advanced"},
            {"name": t("mindmap"), "icon": "diagram-3", "id": "mindmap"},
            {"name": t("resources"), "icon": "file-earmark-code", "id": "resources"},
            # {"name": t("kubectl_test"), "icon": "terminal", "id": "kubectl_test"},
            # {"name": t("cheatsheets"), "icon": "card-list", "id": "cheatsheets"},
            {"name": t("analytics"), "icon": "graph-up", "id": "analytics"}
        ]
        
        # 현재 선택된 페이지 인덱스 찾기
        current_page_id = st.session_state.current_page
        default_index = 0
        for i, item in enumerate(menu_items):
            if item["id"] == current_page_id:
                default_index = i
                break
        
        try:
            from streamlit_option_menu import option_menu
            
            # option_menu를 사용한 네비게이션 (AWS 오렌지 색상으로 변경)
            selected = option_menu(
                "Navigation",
                [item["name"] for item in menu_items],
                icons=[item["icon"] for item in menu_items],
                menu_icon="cast",
                default_index=default_index,
                styles={
                    "container": {"padding": "0!important", "margin": "0!important"},
                    "icon": {"color": "#FF9900", "font-size": "16px"}, # AWS 오렌지 색상
                    "nav-link": {"font-size": "0.9rem", "text-align": "left", "margin": "3px 0"},
                    "nav-link-selected": {"background-color": "#FF9900", "color": "white"}, # AWS 오렌지 색상
                    "menu-title": {"display": "none"}  # 메뉴 제목 숨기기
                }
            )
            
            # 선택된 항목이 있으면 페이지 전환
            if selected:
                for item in menu_items:
                    if item["name"] == selected and item["id"] != st.session_state.current_page:
                        SessionManager.set_current_page(item["id"])
                        st.rerun()
            
        except Exception as e:
            # 오류 로깅 후 기본 선택 상자로 대체
            st.warning(f"메뉴 로딩 오류: {str(e)}")
            
            selected_index = 0
            for i, item in enumerate(menu_items):
                if item["id"] == st.session_state.current_page:
                    selected_index = i
                    break
                    
            selected = st.selectbox(
                "메뉴", 
                options=[item["name"] for item in menu_items],
                index=selected_index
            )
            
            selected_id = next(
                (item["id"] for item in menu_items if item["name"] == selected), 
                "home"
            )
            
            # 현재 페이지 설정
            if selected_id != st.session_state.current_page:
                SessionManager.set_current_page(selected_id)
                st.rerun()
        
        # 하단 정보 - 가운데 정렬 (이 구분선은 그대로 유지)
        st.sidebar.divider()
        st.markdown("""
        <div style="text-align: center; color: #6c757d; font-size: 0.8rem; padding: 0.5rem 0;">
            © 2025 AWS EKS Portal
        </div>
        """, unsafe_allow_html=True)