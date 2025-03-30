import streamlit as st
from utils.localization import t
from utils.style_manager import calculate_content_height

def render_chatbot():
    """채팅 기본 기능 - 글씨 크기 축소 및 간격 조정"""
    
    # 기본 채팅 상태 초기화
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        
    if 'chat_visible' not in st.session_state:
        st.session_state.chat_visible = True
    
    # 픽셀 단위 높이 계산
    content_height_px = calculate_content_height()
    message_container_height = content_height_px - 120
    
    # 챗봇 스타일 적용
    st.markdown("""
    <style>
    /* 챗봇 컨테이너 스타일 */
    .chat-container {
        border: 1px solid #e9ecef;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        overflow: hidden;
        background-color: #fff;
        height: calc(100vh - 120px);
        display: flex;
        flex-direction: column;
    }
    
    /* 챗봇 헤더 스타일 */
    .chat-header {
        background-color: #4361ee;
        color: white;
        padding: 10px 15px;
        font-size: 0.9rem;
        display: flex;
        align-items: center;
    }
    
    .chat-icon {
        width: 24px;
        height: 24px;
        background: rgba(255,255,255,0.2);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 10px;
    }
    
    /* 메시지 글씨 크기 축소 */
    .stChatMessage {
        font-size: 0.85rem !important;
    }
    
    .stChatMessage [data-testid="stMarkdownContainer"] p {
        font-size: 0.85rem !important;
        line-height: 1.4 !important;
    }
    
    /* 이모티콘과 텍스트 간격 */
    .stChatMessage .stChatMessageContent {
        margin-left: 12px !important;
    }
    
    /* 사용자 메시지 스타일 */
    .stChatMessage.user [data-testid="stChatMessageContent"] {
        background-color: #e3f2fd !important;
        border: 1px solid #bbdefb !important;
        color: #0d47a1 !important;
        border-radius: 12px 12px 2px 12px !important;
    }
    
    /* 어시스턴트 메시지 스타일 */
    .stChatMessage.assistant [data-testid="stChatMessageContent"] {
        background-color: #f5f5f5 !important;
        border: 1px solid #e0e0e0 !important;
        color: #333333 !important;
        border-radius: 12px 12px 12px 2px !important;
    }
    
    /* 채팅 컨테이너 패딩 */
    .stChatMessageContent {
        padding: 10px 12px !important;
    }
    
    /* 채팅 입력창 스타일 */
    .stChatInputContainer {
        padding: 8px 10px !important;
        border-top: 1px solid #e9ecef;
    }
    
    .stChatInputContainer textarea {
        font-size: 0.85rem !important;
        padding: 8px 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 챗봇 헤더
    st.markdown("""
    <div class="chat-header">
        <div class="chat-icon">🤖</div>
        <span>EKS & Kubernetes Assistant</span>
    </div>
    """, unsafe_allow_html=True)
    
    # AI 비활성화 상태인 경우
    if not st.session_state.chat_visible:
        st.warning("AI 어시스턴트가 비활성화되었습니다. 다시 활성화하려면 상단의 토글 버튼을 클릭하세요.")
        return
    
    # 채팅 영역 - 메시지 컨테이너
    with st.container(height=message_container_height):
        # 채팅 메시지 표시
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
        # 메시지가 없는 경우 안내 메시지 표시
        if not st.session_state.messages:
            st.info("""
            👋 안녕하세요! 
            
            AWS EKS와 Kubernetes에 관한 질문이 있으신가요?
            
            학습 자료에 관한 질문이나 실습 문제에 대해 도움을 드릴 수 있습니다.
            """)
    
    # 입력창 영역 - 기본 Streamlit 채팅 입력 사용
    if prompt := st.chat_input("질문을 입력하세요..."):
        # 사용자 메시지 추가
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # 어시스턴트 응답 생성
        assistant_response = "AWS EKS와 Kubernetes에 대한 질문을 해주셔서 감사합니다. 어떤 도움이 필요하신가요? 클라우드 네이티브 환경에서의 배포, 관리, 운영에 관한 질문에 답변해 드리겠습니다."
        
        # 어시스턴트 응답 추가
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        
        # 새로고침하여 모든 메시지를 올바른 순서로 표시
        st.rerun()