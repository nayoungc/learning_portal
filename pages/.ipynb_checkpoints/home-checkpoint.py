import streamlit as st
from utils.localization import t
from services.analytics.usage_tracker import UsageTracker

def render_home():
    """홈 페이지 렌더링 - 접근성 경고 해결 및 디자인 개선"""
    
    # 사용 추적
    UsageTracker.track_page_view("home")
    
    # 스타일 정의 - 버튼 텍스트 및 크기 문제 해결
    st.markdown("""
    <style>
    /* 색상 변수 */
    :root {
        --blue-color: #4361ee;
        --blue-light: #e6f0ff;
        --yellow-color: #ffb703;
        --yellow-light: #fff8e6;
        --red-color: #e63946;
        --red-light: #ffebee;
        --orange-color: #fb8500;
        --orange-light: #fff4e6;
        --purple-color: #8338ec;
        --purple-light: #f3e6ff;
        --gray-light: #f8f9fa;
        --green-color: #2a9d8f;      /* 녹색 */
        --green-light: #e0f5f1;      /* 연한 녹색 */
        --hotpink-color: #FF1493;    /* 핫핑크 색상 추가 */
        --hotpink-light: #FFE6F2;    /* 연한 핫핑크 색상 추가 */
    }
    
    /* 인트로 카드 */
    .intro-card {
        background-color: white;
        border: 3px solid var(--orange-color);
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 20px;
    }
    
    .intro-card h1 {
        font-size: 1.8rem;
        margin-bottom: 12px;
        color: var(--orange-color);
    }
    
    .intro-card p {
        font-size: 1rem;
        color: #333;
    }
    
    /* 섹션 헤더 스타일 */
    .section-header {
        font-size: 1.4rem;
        font-weight: 600;
        color: #333;
        margin-top: 30px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* 과정 카드 컨테이너 스타일 - 높이 고정 */
    .course-card {
        padding: 15px;
        border-radius: 12px;
        background-color: white;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        height: 220px !important; /* 높이 고정 */
        display: flex;
        flex-direction: column;
        position: relative;
    }
    
    /* 카드 헤더 영역 */
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
    }
    
    /* 카드 내용 영역 */
    .card-content {
        flex-grow: 1;
    }
    
    /* 버튼 컨테이너 - 하단 가운데 정렬 */
    .button-container {
        position: absolute;
        bottom: 15px;
        left: 0;
        right: 0;
        text-align: center;
        padding: 0 15px;
    }
    
    /* 버튼 스타일 - 글씨가 확실히 보이도록 수정 */
    .stButton > button {
        width: 100% !important;
        border-radius: 30px !important;
        padding: 0.5rem 1rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        margin: 0 !important;
        border: none !important;
        color: white !important;
        text-shadow: 0 1px 1px rgba(0,0,0,0.2) !important;
    }
    
    .stButton > button:hover {
        opacity: 0.9 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
    }
    
    /* 자료실 버튼 (핫핑크 색상) */
    .hotpink-button > button {
        background-color: var(--hotpink-color) !important;
    }
    
    /* 마인드맵 버튼 (녹색) */
    .green-button > button {
        background-color: var(--green-color) !important;
    }
    
    /* 초급 과정 버튼 */
    .beginner-button > button {
        background-color: var(--blue-color) !important;
    }
    
    /* 중급 과정 버튼 */
    .intermediate-button > button {
        background-color: var(--yellow-color) !important;
    }
    
    /* 고급 과정 버튼 */
    .advanced-button > button {
        background-color: var(--red-color) !important;
    }
    
    /* 자가진단 테스트 버튼 */
    .test-button > button {
        background-color: var(--blue-color) !important;
        width: 100% !important;
        margin-top: 20px !important;
    }
    
    /* 자가진단 테스트 디자인 개선 */
    .test-container {
        background-color: var(--gray-light);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    .test-title {
        font-size: 1.2rem;
        color: #333;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .test-description {
        font-size: 0.85rem;
        color: #555;
        margin-bottom: 20px;
        font-style: italic;
    }
    
    /* 테스트 질문 카테고리 */
    .question-category {
        background-color: #e9ecef;
        padding: 10px 15px;
        border-radius: 8px;
        margin: 15px 0 10px 0;
        font-weight: 600;
        font-size: 0.9rem;
        color: #495057;
    }
    
    /* 테스트 질문 스타일 */
    .test-question {
        font-size: 0.85rem;
        color: #333;
        margin-bottom: 8px;
    }
    
    /* 라디오 버튼 글씨 크기 조정 */
    .stRadio div {
        font-size: 0.8rem !important;
    }
    
    .stRadio label {
        font-size: 0.8rem !important;
    }
    
    /* 결과 카드 스타일 */
    .result-card {
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
    }
    
    .beginner-result {
        background-color: var(--blue-light);
        border-left: 5px solid var(--blue-color);
    }
    
    .intermediate-result {
        background-color: var(--yellow-light);
        border-left: 5px solid var(--yellow-color);
    }
    
    .advanced-result {
        background-color: var(--red-light);
        border-left: 5px solid var(--red-color);
    }
    
    /* 결과 타이틀 */
    .result-title {
        font-size: 1.1rem !important;
        margin: 0 0 12px 0 !important;
    }
    
    /* 결과 내용 */
    .result-content {
        font-size: 0.85rem !important;
    }
    
    .result-content li {
        margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 인트로 카드 - 흰색 배경에 파란색 테두리
    st.markdown("""
    <div class="intro-card">
        <h1>AWS EKS와 Kubernetes 전문가 되기</h1>
        <p>클라우드 네이티브 기술을 배우고 실무에 적용할 수 있는 학습 플랫폼입니다.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 자가진단 테스트 - 디자인 개선
    st.markdown("""
    <div class="test-container">
        <div class="test-title">
            <span>📋</span>
            <span>자가진단 테스트</span>
        </div>
        <p class="test-description">
            아래 테스트를 통해 현재 지식 수준을 평가하고 적합한 학습 경로를 찾아보세요.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 자가진단 테스트 내용
    with st.expander("테스트 시작하기"):
        # 세션 상태 초기화
        if 'test_score' not in st.session_state:
            st.session_state.test_score = 0
        
        if 'test_submitted' not in st.session_state:
            st.session_state.test_submitted = False
            
        if 'show_result' not in st.session_state:
            st.session_state.show_result = False
        
        # 테스트 질문 - 카테고리별로 그룹화
        st.markdown('<div class="question-category">1. 컨테이너 기초</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="test-question">Docker 컨테이너와 가상머신(VM)의 차이점을 설명할 수 있나요?</div>', unsafe_allow_html=True)
        docker_q1 = st.radio(
            "Docker 컨테이너와 가상머신 차이점 질문",
            ["아니오, 잘 모릅니다", "기본적인 차이점은 알고 있습니다", "명확하게 차이점을 설명할 수 있습니다"],
            key="docker_q1",
            label_visibility="collapsed"
        )
        
        st.markdown('<div class="test-question">Dockerfile을 작성하고 이미지를 빌드해본 경험이 있나요?</div>', unsafe_allow_html=True)
        docker_q2 = st.radio(
            "Dockerfile 경험 질문",
            ["없습니다", "간단한 Dockerfile을 작성해봤습니다", "복잡한 다단계 빌드도 작성할 수 있습니다"],
            key="docker_q2",
            label_visibility="collapsed"
        )
        
        st.markdown('<div class="question-category">2. Kubernetes 개념</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="test-question">Kubernetes의 기본 구성요소(Pod, Service, Deployment 등)를 이해하고 있나요?</div>', unsafe_allow_html=True)
        k8s_q1 = st.radio(
            "Kubernetes 기본 구성요소 이해 질문",
            ["아니오, 잘 모릅니다", "기본 개념은 알고 있습니다", "자세히 알고 있고 실무에 적용할 수 있습니다"],
            key="k8s_q1",
            label_visibility="collapsed"
        )
        
        st.markdown('<div class="test-question">Kubernetes YAML 매니페스트 파일을 작성하고 적용해본 경험이 있나요?</div>', unsafe_allow_html=True)
        k8s_q2 = st.radio(
            "Kubernetes YAML 파일 경험 질문",
            ["없습니다", "간단한 매니페스트는 작성해봤습니다", "복잡한 매니페스트도 작성할 수 있습니다"],
            key="k8s_q2",
            label_visibility="collapsed"
        )
        
        st.markdown('<div class="question-category">3. AWS 경험</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="test-question">AWS 서비스(EC2, VPC, IAM 등)를 사용해본 경험이 있나요?</div>', unsafe_allow_html=True)
        aws_q1 = st.radio(
            "AWS 서비스 경험 질문",
            ["없습니다", "기본 서비스는 사용해봤습니다", "다양한 서비스를 실무에서 활용합니다"],
            key="aws_q1",
            label_visibility="collapsed"
        )
        
        st.markdown('<div class="test-question">AWS EKS(Elastic Kubernetes Service)를 구축하고 관리해본 경험이 있나요?</div>', unsafe_allow_html=True)
        aws_q2 = st.radio(
            "AWS EKS 경험 질문",
            ["없습니다", "튜토리얼을 따라해본 적이 있습니다", "실무에서 구축/관리한 경험이 있습니다"],
            key="aws_q2",
            label_visibility="collapsed"
        )
        
        st.markdown('<div class="question-category">4. DevOps 경험</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="test-question">CI/CD 파이프라인을 구축하고 운영해본 경험이 있나요?</div>', unsafe_allow_html=True)
        devops_q1 = st.radio(
            "CI/CD 경험 질문",
            ["없습니다", "간단한 파이프라인을 구축해봤습니다", "복잡한 파이프라인을 운영한 경험이 있습니다"],
            key="devops_q1",
            label_visibility="collapsed"
        )
        
        st.markdown('<div class="test-question">GitOps, IaC(Infrastructure as Code) 도구를 사용해본 경험이 있나요?</div>', unsafe_allow_html=True)
        devops_q2 = st.radio(
            "GitOps, IaC 경험 질문",
            ["없습니다", "기본적인 사용법은 알고 있습니다", "실무에서 적극적으로 활용합니다"],
            key="devops_q2",
            label_visibility="collapsed"
        )
        
        # 버튼 컨테이너로 감싸서 버튼 스타일 적용
        st.markdown('<div class="test-button">', unsafe_allow_html=True)
        
        # 결과 계산 버튼 - 명확한 텍스트가 보이는 버튼
        if st.button("학습 수준 확인하기", key="test_result_button"):
            # 점수 계산 (0: 초급, 1: 중급, 2: 고급)
            score = 0
            questions = [docker_q1, docker_q2, k8s_q1, k8s_q2, aws_q1, aws_q2, devops_q1, devops_q2]
            options = [
                ["아니오, 잘 모릅니다", "기본적인 차이점은 알고 있습니다", "명확하게 차이점을 설명할 수 있습니다"],
                ["없습니다", "간단한 Dockerfile을 작성해봤습니다", "복잡한 다단계 빌드도 작성할 수 있습니다"],
                ["아니오, 잘 모릅니다", "기본 개념은 알고 있습니다", "자세히 알고 있고 실무에 적용할 수 있습니다"],
                ["없습니다", "간단한 매니페스트는 작성해봤습니다", "복잡한 매니페스트도 작성할 수 있습니다"],
                ["없습니다", "기본 서비스는 사용해봤습니다", "다양한 서비스를 실무에서 활용합니다"],
                ["없습니다", "튜토리얼을 따라해본 적이 있습니다", "실무에서 구축/관리한 경험이 있습니다"],
                ["없습니다", "간단한 파이프라인을 구축해봤습니다", "복잡한 파이프라인을 운영한 경험이 있습니다"],
                ["없습니다", "기본적인 사용법은 알고 있습니다", "실무에서 적극적으로 활용합니다"]
            ]
            
            for i, q in enumerate(questions):
                if q == options[i][1]:  # 중급 응답
                    score += 1
                elif q == options[i][2]:  # 고급 응답
                    score += 2
            
            # 평균 점수 계산 (0-1.0: 초급, 1.0-1.5: 중급, 1.5-2.0: 고급)
            avg_score = score / len(questions)
            st.session_state.test_score = avg_score
            st.session_state.show_result = True
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 결과 표시 (텍스트 크기 축소)
        if st.session_state.show_result:
            score = st.session_state.test_score
            
            if score < 1.0:
                st.markdown("""
                <div class="result-card beginner-result">
                    <h3 class="result-title" style="color: var(--blue-color);">📊 진단 결과: 초급자 수준</h3>
                    <div class="result-content">
                        <p>컨테이너와 Kubernetes의 기본 개념부터 학습하는 것이 좋겠습니다. 초급 과정에서는:</p>
                        <ul>
                            <li>Docker 컨테이너의 기본 개념과 명령어</li>
                            <li>Kubernetes의 핵심 컴포넌트와 리소스 유형</li>
                            <li>AWS EKS 클러스터 생성 및 기본 관리</li>
                        </ul>
                        <p><b>추천:</b> '기본 과정'부터 시작하세요.</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            elif score < 1.5:
                st.markdown("""
                <div class="result-card intermediate-result">
                    <h3 class="result-title" style="color: var(--yellow-color);">📊 진단 결과: 중급자 수준</h3>
                    <div class="result-content">
                        <p>기본 개념은 이해하고 계시네요. 중급 과정에서 실전 운영 기술을 배우면 좋겠습니다:</p>
                        <ul>
                            <li>Helm 차트를 활용한 애플리케이션 배포</li>
                            <li>CI/CD 파이프라인과 Kubernetes 통합</li>
                            <li>EKS 클러스터 확장 및 모니터링 구성</li>
                        </ul>
                        <p><b>추천:</b> '중급 과정'부터 시작하고 필요에 따라 기본 개념도 복습하세요.</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="result-card advanced-result">
                    <h3 class="result-title" style="color: var(--red-color);">📊 진단 결과: 고급자 수준</h3>
                    <div class="result-content">
                        <p>이미 상당한 지식과 경험을 갖고 계시네요. 고급 과정에서 전문 지식을 더 확장할 수 있습니다:</p>
                        <ul>
                            <li>GitOps 및 Flux/ArgoCD를 활용한 선언적 배포</li>
                            <li>서비스 메시 아키텍처와 Istio 활용법</li>
                            <li>멀티클러스터 관리 및 운영 전략</li>
                        </ul>
                        <p><b>추천:</b> '고급 과정'을 통해 특정 주제에 깊이 있게 집중하세요.</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # 학습 과정 섹션 헤더
    st.markdown('<h3 class="section-header"><span>📚</span> 학습 과정</h3>', unsafe_allow_html=True)
    
    # 학습 과정 - 한 행에 3개 카드, 고정 높이 및 가운데 정렬 버튼
    cols = st.columns(3)
    
    # 기본 과정
    with cols[0]:
        st.markdown("""
            <div class="course-card" style="border-top: 5px solid var(--blue-color);">
                <div class="card-header">
                    <h3 style="color: var(--blue-color); margin: 0;">기본 과정</h3>
                    <span style="background-color: var(--blue-color); color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">초급</span>
                </div>
                <div class="card-content">
                    <p>컨테이너 기초부터 첫 EKS 클러스터 생성까지, 초보자도 쉽게 시작할 수 있습니다.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # 버튼 컨테이너로 감싸서 버튼 스타일 적용
        st.markdown('<div class="beginner-button">', unsafe_allow_html=True)
        if st.button("시작하기 →", key="btn_start_beginner"):
            st.session_state.current_page = "beginner"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 중급 과정
    with cols[1]:
        st.markdown("""
            <div class="course-card" style="border-top: 5px solid var(--yellow-color);">
                <div class="card-header">
                    <h3 style="color: var(--yellow-color); margin: 0;">중급 과정</h3>
                    <span style="background-color: var(--yellow-color); color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">중급</span>
                </div>
                <div class="card-content">
                    <p>EKS 확장, Helm 차트, CI/CD 통합, 모니터링 구성 등 실전 운영 기술을 배웁니다.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # 버튼 컨테이너로 감싸서 버튼 스타일 적용
        st.markdown('<div class="intermediate-button">', unsafe_allow_html=True)
        if st.button("탐색하기 →", key="btn_start_intermediate"):
            st.session_state.current_page = "intermediate"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 고급 과정
    with cols[2]:
        st.markdown("""
            <div class="course-card" style="border-top: 5px solid var(--red-color);">
                <div class="card-header">
                    <h3 style="color: var(--red-color); margin: 0;">고급 과정</h3>
                    <span style="background-color: var(--red-color); color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">고급</span>
                </div>
                <div class="card-content">
                    <p>GitOps, 서비스 메시, 멀티클러스터 관리 등 고급 기술과 아키텍처 패턴을 학습합니다.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # 버튼 컨테이너로 감싸서 버튼 스타일 적용
        st.markdown('<div class="advanced-button">', unsafe_allow_html=True)
        if st.button("도전하기 →", key="btn_start_advanced"):
            st.session_state.current_page = "advanced"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 학습 도구 섹션 헤더
    st.markdown('<h3 class="section-header"><span>🔧</span> 학습 도구</h3>', unsafe_allow_html=True)
    
    # 학습 도구 - 마인드맵과 자료실 (동일한 높이 유지)
    tool_cols = st.columns(2)
    
    # 마인드맵 - 녹색으로 변경
    with tool_cols[0]:
        st.markdown("""
        <div class="course-card" style="height: 250px !important; text-align: center;">
            <div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 15px;">
                <div style="background-color: var(--green-light); color: var(--green-color); width: 70px; height: 70px; display: flex; align-items: center; justify-content: center; border-radius: 50%; font-size: 2rem; font-weight: bold;">
                    M
                </div>
                <h3 style="color: var(--green-color); margin: 15px 0 10px 0;">마인드맵</h3>
            </div>
            <div style="flex-grow: 1;">
                <p style="color: #555; margin-bottom: 0;">시각적으로 개념을 탐색하고 관계를 이해하세요. Kubernetes, EKS, DevOps 도구 간의 연결성을 확인할 수 있습니다.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 녹색 버튼 스타일
        st.markdown('<div class="green-button">', unsafe_allow_html=True)
        if st.button("마인드맵 보기 ↗", key="btn_view_mindmap"):
            st.session_state.current_page = "mindmap"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 자료실 - 핫핑크로 변경
    with tool_cols[1]:
        st.markdown("""
        <div class="course-card" style="height: 250px !important; text-align: center;">
            <div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 15px;">
                <div style="background-color: var(--hotpink-light); color: var(--hotpink-color); width: 70px; height: 70px; display: flex; align-items: center; justify-content: center; border-radius: 50%; font-size: 2rem; font-weight: bold;">
                    R
                </div>
                <h3 style="color: var(--hotpink-color); margin: 15px 0 10px 0;">자료실</h3>
            </div>
            <div style="flex-grow: 1;">
                <p style="color: #555; margin-bottom: 0;">YAML 템플릿과 치트시트로 빠르게 참조하고 활용하세요. 실무에서 바로 사용할 수 있는 자료를 제공합니다.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 핫핑크 버튼 스타일
        st.markdown('<div class="hotpink-button">', unsafe_allow_html=True)
        if st.button("자료 살펴보기 ↗", key="btn_view_resources"):
            st.session_state.current_page = "yaml_templates"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 업데이트 섹션 헤더
    st.markdown('<h3 class="section-header"><span>🔔</span> 최신 업데이트</h3>', unsafe_allow_html=True)
    
    # 업데이트 카드
    st.markdown("""
    <div style="padding: 20px; background-color: white; border-top: 5px solid var(--purple-color); border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <div style="background-color: var(--purple-light); color: var(--purple-color); width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; border-radius: 50%; margin-right: 15px;">
                📢
            </div>
            <h3 style="color: var(--purple-color); margin: 0;">2025년 4월 업데이트</h3>
        </div>
        <ul style="padding-left: 20px; color: #555; line-height: 1.5;">
            <li style="margin-bottom: 6px;">AWS EKS 1.30 버전 관련 콘텐츠 추가</li>
            <li style="margin-bottom: 6px;">GitOps 섹션에 ArgoCD 애플리케이션 예제 추가</li>
            <li style="margin-bottom: 6px;">Istio 서비스 메시 실습 강화</li>
            <li>AI 챗봇 답변 품질 개선</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)