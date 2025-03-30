import json
import os
import streamlit as st
from config import Config


class Localization:
    """국제화 및 현지화를 위한 클래스"""
    
    _translations = {
        'common': {},
        'beginner': {},
        'intermediate': {},
        'advanced': {}
    }
    
    @classmethod
    def load_translations(cls):
        """지원하는 모든 언어의 번역 파일을 로드합니다."""
        categories = ['common', 'beginner', 'intermediate', 'advanced']
        
        for lang in ['en', 'ko']:
            for category in categories:
                file_path = os.path.join(Config.I18N_DIR, category, f"{lang}.json")
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        if lang not in cls._translations[category]:
                            cls._translations[category][lang] = {}
                        cls._translations[category][lang].update(json.load(f))
                else:
                    if cls._translations[category].get(lang) is None:
                        cls._translations[category][lang] = {}
    
    @classmethod
    def change_language(cls, language):
        """표시 언어를 변경합니다."""
        st.session_state.language = language
    
    @classmethod
    def get_text(cls, key, category='common', language=None):
        """지정된 언어로 키에 해당하는 텍스트를 반환합니다."""
        if not cls._translations['common']:  # 아직 로드되지 않았으면 로드
            cls.load_translations()
        
        # 언어가 지정되지 않은 경우 세션 상태의 언어 사용
        language = language or st.session_state.get('language', 'en')
        
        # 먼저 지정된 카테고리에서 검색
        if key in cls._translations.get(category, {}).get(language, {}):
            return cls._translations[category][language][key]
        
        # 지정된 카테고리에 없으면 common에서 검색
        if key in cls._translations.get('common', {}).get(language, {}):
            return cls._translations['common'][language][key]
        
        # 현재 언어에 없으면 영어 버전 시도
        if key in cls._translations.get(category, {}).get('en', {}):
            return cls._translations[category]['en'][key]
        if key in cls._translations.get('common', {}).get('en', {}):
            return cls._translations['common']['en'][key]
        
        # 모든 경우에 실패하면 키 자체 반환
        return key


# 간단한 별칭 함수
def t(key, category='common', language=None):
    return Localization.get_text(key, category, language)
