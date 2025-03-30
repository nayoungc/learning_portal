import streamlit as st
from utils.localization import t
from utils.mindmap_generator import render_interactive_mindmap
from utils.session_manager import SessionManager


def render_mindmap_viewer(mindmap_type, zoom_level=1.0, max_depth=None):
    """마인드맵 뷰어 컴포넌트"""
    # 마인드맵 컨트롤 UI
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        if st.button("➖", help=t("zoom_out"), key="zoom_out"):
            if st.session_state.mindmap_zoom > 0.5:
                st.session_state.mindmap_zoom -= 0.1
                st.rerun()
    
    with col2:
        st.write("")  # 빈 공간
        
    with col3:
        if st.button("➕", help=t("zoom_in"), key="zoom_in"):
            if st.session_state.mindmap_zoom < 2.0:
                st.session_state.mindmap_zoom += 0.1
                st.rerun()
    
    # 컨테이너에 마인드맵 렌더링
    with st.container():
        st.markdown('<div class="mindmap-container">', unsafe_allow_html=True)
        
        # 마인드맵 렌더링 및 노드 정보 반환
        node_info = render_interactive_mindmap(
            mindmap_type, 
            zoom_level=st.session_state.mindmap_zoom, 
            max_depth=max_depth,
            selected_node=st.session_state.get("selected_node")
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 선택된 노드가 있으면 정보 표시
    if st.session_state.get("selected_node") and node_info:
        selected_info = node_info.get(st.session_state.selected_node, {})
        if selected_info:
            st.markdown('<div class="node-info-panel">', unsafe_allow_html=True)
            st.subheader(selected_info.get('name', ''))
            st.markdown(selected_info.get('description', ''))
            
            # 링크가 있으면 페이지 이동 버튼 표시
            link = selected_info.get('link', '')
            if link:
                if st.button("이 주제 학습하기"):
                    # 링크 처리 (예: 페이지 전환)
                    page_id, section = link.lstrip('/').split('#') if '#' in link else (link.lstrip('/'), None)
                    SessionManager.set_current_page(page_id)
                    st.rerun()
                    
            st.markdown('</div>', unsafe_allow_html=True)
    
    return node_info
