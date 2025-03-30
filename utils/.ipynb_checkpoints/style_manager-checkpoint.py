import streamlit as st
import os
from pathlib import Path

def load_global_styles():
    """전역 공통 스타일 로드"""
    css_file = Path("styles/styles.css")
    if css_file.exists():
        with open(css_file, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def load_theme_animation():
    """테마 전환 애니메이션 스타일 로드"""
    css_file = Path("styles/theme_animation.css")
    if css_file.exists():
        with open(css_file, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def load_visualization_styles():
    """시각화 요소 스타일 로드"""
    css_file = Path("styles/visualizations.css")
    if css_file.exists():
        with open(css_file, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def load_language_specific_styles():
    """현재 언어에 맞는 언어별 스타일 로드"""
    current_language = st.session_state.get("language", "ko")  # 기본값은 한국어
    lang_css_path = Path(f"styles/language/{current_language}.css")
    
    if lang_css_path.exists():
        with open(lang_css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def apply_theme_specifics():
    """현재 테마에 따른 추가 스타일 적용"""
    current_theme = st.session_state.get("theme_mode", "light")  # 기본값은 라이트 모드
    
    # 테마에 따른 배경색 스타일 설정
    bg_color = "#FFFFFF" if current_theme == "light" else "#111111"
    text_color = "#333333" if current_theme == "light" else "#F0F0F0"
    
    theme_css = f"""
    <style>
    /* {current_theme} 테마 전용 스타일 */
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
        transition: background-color 0.3s ease;
    }}
    </style>
    """
    st.markdown(theme_css, unsafe_allow_html=True)

def load_page_specific_styles(page_name):
    """특정 페이지를 위한 스타일 로드"""
    page_css_path = Path(f"styles/pages/{page_name}.css")
    if page_css_path.exists():
        with open(page_css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def calculate_content_height():
    """현재 페이지에 따라 적절한 컨텐츠 높이 계산 (픽셀 단위)"""
    # 기본 높이: 800px로 증가 (이전보다 크게)
    base_height = 800
    
    # 페이지별로 다른 높이 적용 가능
    current_page = st.session_state.get('current_page', 'home')
    
    # 특정 페이지에 대해 다른 높이를 설정할 수 있음
    page_heights = {
        'mindmap': 950,  # 마인드맵은 더 큰 높이
        'analytics': 950,  # 분석 페이지도 더 큰 높이
    }
    
    return page_heights.get(current_page, base_height)

def calculate_content_height_vh():
    """CSS용 vh 단위의 높이 계산 (문자열)"""
    return "95vh"  # 뷰포트 높이의 95%로 증가

def inject_custom_css(css_code):
    """사용자 정의 CSS 코드 주입"""
    st.markdown(f"<style>{css_code}</style>", unsafe_allow_html=True)

# 초기화 시 사이드바와 메인 영역의 간격을 줄이는 CSS 추가
def remove_padding():
    """페이지 전체 패딩 제거"""
    st.markdown("""
    <style>
    /* 사이드바와 메인 영역 사이 간격 제거 */
    .css-1d391kg, .css-12oz5g7 {
        padding-top: 0 !important;
        padding-right: 0 !important;
        padding-left: 0 !important;
    }
    
    /* 메인 영역의 왼쪽 여백 제거 */
    .block-container {
        margin-left: 0 !important;
        padding-left: 0 !important;
    }
    
    /* 컨테이너 간 여백 제거 */
    .element-container {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)