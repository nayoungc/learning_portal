import streamlit as st
from config import Config


class SessionManager:
    """사용자 세션 관리를 위한 클래스"""
    
    @staticmethod
    def initialize_session():
        """세션 상태를 초기화합니다."""
        # 현재 페이지 세션 상태
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'home'
        
        # 언어 세션 상태
        if 'language' not in st.session_state:
            st.session_state.language = 'ko'  # 기본 언어: 한국어
        
        # 테마 세션 상태
        if 'theme_mode' not in st.session_state:
            st.session_state.theme_mode = 'light'  # 기본 테마: 라이트 모드
        
        # 챗봇 관련 세션 상태
        if 'chat_visible' not in st.session_state:
            st.session_state.chat_visible = Config.DEFAULT_CHAT_VISIBLE
        
        if 'chat_width' not in st.session_state:
            st.session_state.chat_width = Config.DEFAULT_CHAT_WIDTH
        
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
            
        # 마인드맵 관련 세션 상태
        if 'mindmap_type' not in st.session_state:
            st.session_state.mindmap_type = Config.MindMapType.KUBERNETES.value
            
        if 'mindmap_zoom' not in st.session_state:
            st.session_state.mindmap_zoom = 1.0
            
        if 'selected_node' not in st.session_state:
            st.session_state.selected_node = None
    
    @staticmethod
    def set_current_page(page_id):
        """현재 페이지를 설정합니다."""
        st.session_state.current_page = page_id
    
    @staticmethod
    def toggle_chat_visibility():
        """챗봇 표시 여부를 토글합니다."""
        st.session_state.chat_visible = not st.session_state.chat_visible
        
    @staticmethod
    def set_mindmap_type(mindmap_type):
        """마인드맵 유형을 설정합니다."""
        st.session_state.mindmap_type = mindmap_type
        
    @staticmethod
    def set_selected_node(node_id):
        """선택된 마인드맵 노드를 설정합니다."""
        st.session_state.selected_node = node_id
