import streamlit as st
from utils.localization import t
from services.analytics.usage_tracker import UsageTracker

def render_beginner():
    """초급 과정 메인 페이지 - 개선된 디자인 및 이동 경로 추가"""
    
    # 사용 추적
    UsageTracker.track_page_view("beginner")
    
    # 공통 스타일 정의 - 학습 경로 네비게이션 스타일 추가
    st.markdown("""
    <style>
    /* 색상 변수 */
    :root {
        --blue-color: #4361ee;
        --blue-light: #e6f0ff;
        --divider-color: #e0e0e0;  /* 회색 구분선 */
        --yellow-color: #ffb703;  /* 중급 색상 */
        --red-color: #e63946;    /* 고급 색상 */
        --nav-bg-color: #f8f9fa;
    }
    
    /* 페이지 제목 - "기초"를 더 크게 */
    h1 {
        font-size: 2.2rem !important; 
        margin-bottom: 20px !important;
    }
    
    /* 학습 경로 네비게이션 */
    .learning-path-nav {
        display: flex;
        background-color: var(--nav-bg-color);
        border-radius: 8px;
        padding: 8px;
        margin-bottom: 20px;
        align-items: center;
    }
    
    .nav-item {
        flex: 1;
        text-align: center;
        padding: 8px 0;
        position: relative;
    }
    
    .nav-item:not(:last-child):after {
        content: "→";
        position: absolute;
        right: -5px;
        top: 50%;
        transform: translateY(-50%);
        color: #999;
    }
    
    .current {
        font-weight: bold;
        background-color: var(--blue-light);
        border-radius: 4px;
    }
    
    .beginner-nav {
        color: var(--blue-color);
    }
    
    .intermediate-nav {
        color: var(--yellow-color);
    }
    
    .advanced-nav {
        color: var(--red-color);
    }
    
    /* 관련 모듈 링크 스타일 */
    .related-module-link {
        margin-top: 10px;
        padding: 8px;
        background-color: var(--blue-light);
        border-radius: 4px;
        font-size: 0.85rem;
    }
    
    .related-module-link a {
        color: var(--blue-color);
        text-decoration: none;
        font-weight: 600;
    }
    
    .related-module-link a:hover {
        text-decoration: underline;
    }
    
    /* 섹션 제목 통일 - "학습 모듈", "학습 내용", "개념 정리 및 복습" - 더 크게 */
    .section-title {
        font-size: 1.8rem !important;
        font-weight: 600 !important;
        margin-top: 30px !important;
        margin-bottom: 20px !important;
        color: #333 !important;
        padding-bottom: 8px !important;
        border-bottom: 2px solid var(--divider-color) !important;  /* 회색 구분선으로 변경 */
    }
    
    /* 모듈 카드 스타일 - 높이 고정 및 일관성 유지 */
    .module-card {
        background-color: white;
        border-radius: 12px;
        border-top: 5px solid var(--blue-color);
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        padding: 15px;
        margin-bottom: 20px;
        height: 280px !important; /* 높이 증가 - 관련 모듈 링크 공간 확보 */
        position: relative;
        overflow: hidden;
    }
    
    /* 모듈 헤더 */
    .module-header {
        display: flex;
        align-items: center;
        margin-bottom: 12px;
    }
    
    /* 모듈 아이콘 */
    .module-icon {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background-color: var(--blue-color);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-right: 12px;
        flex-shrink: 0;
    }
    
    /* 모듈 제목 - "컨테이너 기초", "EKS 기초" 등을 더 크게 */
    .module-title {
        font-size: 1.5rem !important;
        font-weight: 600;
        color: var(--blue-color);
        margin: 0;
    }
    
    /* 모듈 설명 */
    .module-desc {
        font-size: 0.9rem;
        color: #555;
        margin-bottom: 35px;
        line-height: 1.5;
    }
    
    /* 주요 내용 리스트 */
    .topic-list {
        position: absolute;
        bottom: 50px; /* 관련 모듈 링크 공간 확보 */
        left: 15px;
        right: 15px;
        background-color: #f8f9fa;
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 0.85rem;
    }
    
    .topic-title {
        font-weight: 600;
        margin-bottom: 4px;
        font-size: 0.85rem;
    }
    
    .topic-item {
        margin: 0;
        padding: 0;
        list-style-type: none;
        display: flex;
        flex-wrap: wrap;
    }
    
    .topic-item li {
        margin-right: 12px;
        padding-left: 10px;
        position: relative;
        font-size: 0.8rem;
    }
    
    .topic-item li:before {
        content: "•";
        position: absolute;
        left: 0;
        color: var(--blue-color);
    }
    
    /* 인트로 카드 */
    .intro-card {
        background-color: var(--blue-light);
        border-left: 4px solid var(--blue-color);
        padding: 15px;
        border-radius: 6px;
        margin-bottom: 20px;
        font-size: 0.9rem;
    }
    
    /* 로드맵 섹션 */
    .roadmap-section {
        margin: 25px 0;
    }
    
    /* 탭 스타일링 수정 - 모든 색상을 파란색으로 통일 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 10px 16px;
        border-radius: 4px 4px 0 0;
        background-color: transparent !important;
        color: #333 !important;
        border: none !important;  /* 기본 테두리 제거 */
    }
    
    /* 탭 호버 효과 - 파란색으로 통일 */
    .stTabs [data-baseweb="tab"]:hover {
        color: var(--blue-color) !important;
        border-bottom: 2px solid var(--blue-color) !important;
    }
    
    /* 선택된 탭 스타일 - 파란색으로 통일 */
    .stTabs [aria-selected="true"] {
        color: var(--blue-color) !important;
        border-bottom: 2px solid var(--blue-color) !important;
        font-weight: 600 !important;
    }
    
    /* 다른 탭 관련 요소에 적용될 수 있는 기본 색상 덮어쓰기 */
    .stTabs [data-baseweb="tab"] * {
        color: inherit !important;
    }
    
    /* 탭 콘텐츠 */
    .tab-content {
        padding: 20px 5px;
        font-size: 0.95rem;
    }
    
    /* 탭 내용 제목 스타일 */
    .tab-content h3 {
        font-size: 1.5rem !important;
        margin-top: 25px !important;
        margin-bottom: 15px !important;
        color: var(--blue-color) !important;
        padding-bottom: 8px !important;
        border-bottom: 1px solid var(--divider-color) !important;  /* 회색 구분선 */
    }
    
    .tab-content h4 {
        font-size: 1.2rem !important;
        margin-top: 20px !important;
        margin-bottom: 10px !important;
        color: #444 !important;
    }
    
    /* 다음 학습 추천 섹션 */
    .next-learning {
        margin-top: 30px;
        padding: 15px;
        background-color: var(--blue-light);
        border-radius: 6px;
        border-left: 4px solid var(--blue-color);
    }
    
    .next-learning h4 {
        margin-top: 0 !important;
        color: var(--blue-color) !important;
    }
    
    .next-learning ul {
        margin-bottom: 0;
    }
    
    /* 주제별 구분선 - 탭 내용용 */
    .topic-divider {
        height: 1px;
        background-color: var(--divider-color);
        margin: 25px 0;
        width: 100%;
        display: block;
    }
    
    /* 복습 섹션 */
    .review-section {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 20px;
        margin-top: 30px;
        border-left: 4px solid var(--blue-color);
    }
    
    .review-title {
        font-size: 1.6rem !important;
        font-weight: 600;
        color: #333;
        margin-bottom: 15px;
        padding-bottom: 8px;
        border-bottom: 1px solid var(--divider-color);
    }
    
    .review-content {
        font-size: 0.95rem;
    }
    
    /* 복습 섹션 내 소제목 */
    .review-content h4 {
        font-size: 1.3rem !important;
        color: var(--blue-color) !important;
        margin-top: 20px !important;
        margin-bottom: 12px !important;
        padding-top: 15px !important;
        border-top: 1px solid var(--divider-color) !important;  /* 회색 구분선 */
    }
    
    /* 복습 섹션 내 리스트 */
    .review-content ul {
        padding-left: 20px !important;
        margin-bottom: 15px !important;
    }
    
    .review-content li {
        margin-bottom: 6px !important;
    }
    
    /* 코드 블록 */
    .code-block {
        background-color: #f1f3f5;
        padding: 12px;
        border-radius: 4px;
        font-family: monospace;
        font-size: 0.9rem;
        margin: 15px 0;
        overflow-x: auto;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 학습 경로 네비게이션 추가
    st.markdown("""
    <div class="learning-path-nav">
        <div class="nav-item current">
            <span class="beginner-nav">기본 과정</span>
        </div>
        <div class="nav-item">
            <a href="/?page=intermediate" class="intermediate-nav">중급 과정</a>
        </div>
        <div class="nav-item">
            <a href="/?page=advanced" class="advanced-nav">고급 과정</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 인트로 설명
    st.markdown("""
    <div class="intro-card">
        쿠버네티스와 EKS를 처음 시작하는 분들을 위한 기초 개념과 실습 가이드입니다.
        기본 용어, 설치 방법, 간단한 애플리케이션 배포 방법 등을 배울 수 있습니다.
    </div>
    """, unsafe_allow_html=True)
    
    # 모듈 정의 - 내용 정리 및 학습 경로 추가
    modules = [
        {
            "id": "container_basics",
            "title": "컨테이너 기초",
            "icon": "D",
            "description": "Docker 개념과 기본 명령어, 컨테이너와 가상머신 비교, 이미지 빌드 기초를 배웁니다.",
            "topics": ["Docker 기본 개념", "Dockerfile 작성", "이미지 빌드 및 관리"],
            "next_modules": {
                "intermediate": "k8s_advanced"
            }
        },
        {
            "id": "kubernetes_intro",
            "title": "Kubernetes 입문",
            "icon": "K",
            "description": "Kubernetes 아키텍처, Pod와 Service 개념, kubectl 기본 명령어를 학습합니다.",
            "topics": ["Kubernetes 구성요소", "Pod 생명주기", "Service 유형", "kubectl 기본 명령어"],
            "next_modules": {
                "intermediate": "k8s_advanced"
            }
        },
        {
            "id": "eks_basics",
            "title": "EKS 기초",
            "icon": "E",
            "description": "AWS 계정 설정, IAM 기초, EKS 클러스터 생성, 기본 노드 그룹 관리 방법을 알아봅니다.",
            "topics": ["AWS 계정 설정", "eksctl 설치 및 사용", "EKS 클러스터 생성", "노드 그룹 관리"],
            "next_modules": {
                "intermediate": "eks_management"
            }
        },
        {
            "id": "storage_basics",
            "title": "기본 스토리지",
            "icon": "S",
            "description": "Kubernetes의 스토리지 개념과 영구 볼륨 관리 방법을 학습합니다.",
            "topics": ["볼륨 타입", "PersistentVolume(PV)", "PersistentVolumeClaim(PVC)", "StorageClass"],
            "next_modules": {
                "intermediate": "eks_storage"
            }
        },
        {
            "id": "helm_basics",
            "title": "Helm 기초",
            "icon": "H",
            "description": "Helm의 기본 개념과 명령어를 배우고 간단한 차트를 설치합니다.",
            "topics": ["Helm 개요", "기본 명령어", "차트 설치 및 관리"],
            "next_modules": {
                "intermediate": "helm_basics"
            }
        },
        {
            "id": "serverless_intro",
            "title": "서버리스 EKS 소개",
            "icon": "F",
            "description": "AWS Fargate와 서버리스 Kubernetes의 기본 개념을 배웁니다.",
            "topics": ["Fargate 개요", "EKS + Fargate 구성", "기본 사용 사례"],
            "next_modules": {
                "intermediate": "eks_management"
            }
        },
        {
            "id": "basic_projects",
            "title": "기본 실습 프로젝트",
            "icon": "P",
            "description": "첫 번째 EKS 클러스터 배포, 정적 웹사이트 배포 실습을 진행합니다.",
            "topics": ["Hello World 애플리케이션 배포", "WordPress 배포"],
            "next_modules": {
                "intermediate": "intermediate_projects"
            }
        }
    ]
    
    # 모듈 카드 표시
    st.markdown("<h2 class='section-title'>학습 모듈</h2>", unsafe_allow_html=True)
    
    # 2열 레이아웃으로 모듈 카드 표시
    for i in range(0, len(modules), 2):
        cols = st.columns(2)
        
        for j in range(2):
            if i + j < len(modules):
                module = modules[i + j]
                with cols[j]:
                    # 관련 모듈 링크 추가
                    next_module_html = ""
                    if "next_modules" in module and "intermediate" in module["next_modules"]:
                        next_id = module["next_modules"]["intermediate"]
                        next_title = next_id.replace("_", " ").title()
                        next_module_html = f"""
                        <div class="related-module-link">
                            <span>다음 단계: </span>
                            <a href="/?page=intermediate#{next_id}">{next_title} →</a>
                        </div>
                        """
                    
                    st.markdown(f"""
                        <div class="module-card">
                            <div class="module-header">
                                <div class="module-icon">{module["icon"]}</div>
                                <h3 class="module-title">{module["title"]}</h3>
                            </div>
                            <p class="module-desc">{module["description"]}</p>
                            <div class="topic-list">
                                <div class="topic-title">주요 내용:</div>
                                <ul class="topic-item">
                                    {"".join([f"<li>{topic}</li>" for topic in module["topics"]])}
                                </ul>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
    
    # 탭 인터페이스로 각 모듈의 세부 내용 표시
    st.markdown("<h2 class='section-title'>학습 내용</h2>", unsafe_allow_html=True)
    
    tabs = st.tabs([module["title"] for module in modules])
    
    # 컨테이너 기초 탭
    with tabs[0]:
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        st.markdown("### Docker 컨테이너 개념")
        st.markdown("""
        Docker는 애플리케이션을 개발, 배포, 실행하기 위한 오픈소스 플랫폼입니다. 
        
        주요 개념:
        - **컨테이너**: 애플리케이션 및 종속성을 패키지화한 독립적인 실행 단위
        - **이미지**: 컨테이너 실행에 필요한 파일 시스템과 설정의 불변 스냅샷
        - **Docker Engine**: 컨테이너를 빌드하고 실행하는 런타임 환경
        - **Docker Hub**: 공용 이미지를 공유하고 검색할 수 있는 레지스트리
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)  # 주제 구분선 추가
        
        st.markdown("#### 컨테이너와 가상머신 비교")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**컨테이너**")
            st.markdown("""
            - 호스트 OS 커널 공유
            - 가볍고 빠른 시작
            - 적은 리소스 사용
            - 이식성과 확장성 뛰어남
            """)
        
        with col2:
            st.markdown("**가상머신**")
            st.markdown("""
            - 독립된 OS 커널 실행
            - 더 무겁고 시작 느림
            - 더 많은 리소스 사용
            - 완전한 격리와 보안
            """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)  # 주제 구분선 추가
        
        st.markdown("### 기본 Docker 명령어")
        st.markdown("""
        ```bash
        # 이미지 다운로드
        docker pull nginx
        
        # 컨테이너 실행
        docker run -d -p 8080:80 --name my-nginx nginx
        
        # 컨테이너 목록 보기
        docker ps
        
        # 컨테이너 중지
        docker stop my-nginx
        
        # 컨테이너 제거
        docker rm my-nginx
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)  # 주제 구분선 추가
        
        st.markdown("### Dockerfile 작성하기")
        st.markdown("""
        Dockerfile은 이미지 빌드에 필요한 명령어를 포함한 텍스트 파일입니다.
        
        ```dockerfile
        # 기본 이미지 지정
        FROM node:14-alpine
    
        # 작업 디렉토리 설정
        WORKDIR /app
    
        # 의존성 파일 복사 및 설치
        COPY package*.json ./
        RUN npm install
    
        # 소스 코드 복사
        COPY . .
    
        # 포트 설정
        EXPOSE 3000
    
        # 시작 명령어
        CMD ["npm", "start"]
        ```
    
        이미지 빌드 명령어:
        ```bash
        docker build -t my-app:1.0 .
        ```
        """)

        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)  # 주제 구분선 추가
        # 다음 학습 추천 섹션 추가
        st.markdown("""
        <div class="next-learning">
            <h4>다음 학습 추천</h4>
            <ul>
                <li>컨테이너 개념을 이해했다면, <a href="/?page=intermediate#k8s_advanced">Kubernetes 심화</a> 모듈에서 컨테이너 오케스트레이션에 대해 더 알아보세요.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Kubernetes 입문 탭
    with tabs[1]:
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        st.markdown("### Kubernetes 기본 개념")
        st.markdown("""
        Kubernetes는 컨테이너화된 애플리케이션의 배포, 확장, 관리를 자동화하는 오픈소스 컨테이너 오케스트레이션 플랫폼입니다.

        #### 주요 구성 요소
        - **마스터 노드**: API 서버, 스케줄러, 컨트롤러 관리자, etcd를 포함
        - **워커 노드**: kubelet, kube-proxy, 컨테이너 런타임을 실행
        - **Pod**: 쿠버네티스에서 가장 작은 배포 단위로, 하나 이상의 컨테이너 포함
        - **Service**: Pod 집합에 대한 안정적인 네트워크 엔드포인트 제공
        - **Deployment**: Pod와 ReplicaSet을 관리하여 애플리케이션 업데이트 및 스케일링
        """)
        
        st.markdown("### YAML 매니페스트 기초")
        st.markdown("""
        Kubernetes 리소스는 YAML 매니페스트 파일로 정의됩니다.
        
        **간단한 Pod 매니페스트**:
        ```yaml
        apiVersion: v1
        kind: Pod
        metadata:
          name: nginx-pod
          labels:
            app: nginx
        spec:
          containers:
          - name: nginx
            image: nginx:latest
            ports:
            - containerPort: 80
        ```
        
        **Deployment 매니페스트**:
        ```yaml
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: nginx-deployment
          labels:
            app: nginx
        spec:
          replicas: 3
          selector:
            matchLabels:
              app: nginx
          template:
            metadata:
              labels:
                app: nginx
            spec:
              containers:
              - name: nginx
                image: nginx:latest
                ports:
                - containerPort: 80
        ```
        """)
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)  # 주제 구분선 추가
        st.markdown("### 기본 kubectl 명령어")
        st.markdown("""
        ```bash
        # 클러스터 정보 확인
        kubectl cluster-info

        # Pod 생성
        kubectl apply -f pod.yaml

        # Pod 목록 확인
        kubectl get pods

        # Pod 세부 정보 확인
        kubectl describe pod nginx-pod

        # Pod 로그 확인
        kubectl logs nginx-pod

        # Pod 내 명령어 실행
        kubectl exec -it nginx-pod -- /bin/bash

        # 리소스 삭제
        kubectl delete pod nginx-pod
        ```
        """)
        
        # 다음 학습 추천 섹션 추가
        st.markdown("""
        <div class="next-learning">
            <h4>다음 학습 추천</h4>
            <ul>
                <li>Kubernetes의 기본 개념을 이해했다면, <a href="/?page=intermediate#k8s_advanced">Kubernetes 심화</a> 모듈에서 더 고급 기능을 학습해 보세요.</li>
                <li>실전 배포를 학습하려면 <a href="/?page=beginner#basic_projects">기본 실습 프로젝트</a> 모듈을 확인하세요.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # EKS 기초 탭
    with tabs[2]:
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        st.markdown("### AWS EKS 소개")
        st.markdown("""
        Amazon Elastic Kubernetes Service(EKS)는 AWS에서 제공하는 관리형 Kubernetes 서비스입니다.

        **주요 특징**:
        - AWS가 관리하는 Kubernetes 컨트롤 플레인
        - AWS 서비스와의 긴밀한 통합(IAM, VPC, ELB 등)
        - 고가용성 구성
        - 자동 업데이트 및 패치
        """)

        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)  # 주제 구분선 추가
        st.markdown("### EKS 클러스터 생성 준비")
        st.markdown("""
        #### 필수 도구 설치

        1. **AWS CLI** - AWS 서비스를 명령줄에서 관리
           ```bash
           # MacOS
           brew install awscli
           
           # Windows
           choco install awscli
           
           # Linux
           pip install awscli
           ```

        2. **eksctl** - EKS 클러스터 생성 및 관리 도구
           ```bash
           # MacOS
           brew install eksctl
           
           # Windows
           choco install eksctl
           
           # Linux
           curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_\\$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
           sudo mv /tmp/eksctl /usr/local/bin
           ```

        3. **kubectl** - Kubernetes 클러스터 관리 도구
           ```bash
           # MacOS
           brew install kubectl
           
           # Windows
           choco install kubernetes-cli
           
           # Linux
           curl -LO "https://dl.k8s.io/release/stable.txt"
           curl -LO "https://dl.k8s.io/release/\\$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
           chmod +x kubectl
           sudo mv kubectl /usr/local/bin/
           ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)  # 주제 구분선 추가
        st.markdown("### EKS 클러스터 생성")
        st.markdown("""
        **eksctl을 사용한 클러스터 생성**:
        ```bash
        eksctl create cluster \\
          --name my-eks-cluster \\
          --version 1.27 \\
          --region us-west-2 \\
          --nodegroup-name my-nodes \\
          --node-type t3.medium \\
          --nodes 3 \\
          --nodes-min 1 \\
          --nodes-max 4
        ```

        **AWS 콘솔을 통한 생성**:
        1. AWS EKS 콘솔에 접속
        2. 'Create cluster' 선택
        3. 클러스터 이름, 역할, 네트워킹 설정
        4. 노드 그룹 생성
        """)

        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)  # 주제 구분선 추가
        st.markdown("### EKS 노드 그룹 관리")
        st.markdown("""
        노드 그룹은 EKS 클러스터에서 워커 노드로 작동하는 EC2 인스턴스 그룹입니다.

        **노드 그룹 추가**:
        ```bash
        eksctl create nodegroup \\
          --cluster my-eks-cluster \\
          --name my-new-nodes \\
          --node-type t3.large \\
          --nodes 3
        ```

        **노드 그룹 스케일링**:
        ```bash
        eksctl scale nodegroup \\
          --cluster my-eks-cluster \\
          --name my-nodes \\
          --nodes 5
        ```

        **노드 그룹 삭제**:
        ```bash
        eksctl delete nodegroup \\
          --cluster my-eks-cluster \\
          --name my-nodes
        ```
        """)
        
        # 다음 학습 추천 섹션 추가
        st.markdown("""
        <div class="next-learning">
            <h4>다음 학습 추천</h4>
            <ul>
                <li>EKS 기초를 이해했다면, <a href="/?page=intermediate#eks_management">EKS 관리와 운영</a> 모듈에서 더 심화된 내용을 학습하세요.</li>
                <li>서버리스 옵션에 대해 알아보려면 <a href="/?page=beginner#serverless_intro">서버리스 EKS 소개</a> 모듈을 확인하세요.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 기본 스토리지 탭 (중급에서 이동)
    with tabs[3]:
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        st.markdown("### Kubernetes의 스토리지 개념")
        st.markdown("""
        Kubernetes에서 스토리지는 컨테이너의 데이터를 영구적으로 저장하기 위한 메커니즘을 제공합니다.

        **스토리지 주요 개념**:
        - **임시 볼륨**: Pod가 실행되는 동안만 존재하는 휘발성 스토리지
        - **영구 볼륨(PV)**: 클러스터의 리소스로 관리되는 스토리지
        - **영구 볼륨 클레임(PVC)**: 사용자가 요청하는 스토리지 요구사항
        - **스토리지 클래스**: 스토리지 프로비저닝 방법을 정의
        """)

        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)  # 주제 구분선 추가
        st.markdown("### Volume 유형")
        st.markdown("""
        **임시 볼륨(emptyDir)**:
        ```yaml
        apiVersion: v1
        kind: Pod
        metadata:
          name: test-pod
        spec:
          containers:
          - name: test-container
            image: nginx
            volumeMounts:
            - mountPath: /cache
              name: cache-volume
          volumes:
          - name: cache-volume
            emptyDir: {}
        ```
        
        **호스트 경로(hostPath)**:
        ```yaml
        apiVersion: v1
        kind: Pod
        metadata:
          name: test-pod
        spec:
          containers:
          - name: test-container
            image: nginx
            volumeMounts:
            - mountPath: /data
              name: host-volume
          volumes:
          - name: host-volume
            hostPath:
              path: /data
              type: DirectoryOrCreate
        ```
        """)
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)  # 주제 구분선 추가
        st.markdown("### PersistentVolume(PV)와 PersistentVolumeClaim(PVC)")
        st.markdown("""
        **영구 볼륨(PV)** 예제:
        ```yaml
        apiVersion: v1
        kind: PersistentVolume
        metadata:
          name: pv-example
        spec:
          capacity:
            storage: 10Gi
          accessModes:
            - ReadWriteOnce
          persistentVolumeReclaimPolicy: Retain
          hostPath:
            path: /mnt/data
        ```
        
        **영구 볼륨 클레임(PVC)** 예제:
        ```yaml
        apiVersion: v1
        kind: PersistentVolumeClaim
        metadata:
          name: pvc-example
        spec:
          accessModes:
            - ReadWriteOnce
          resources:
            requests:
              storage: 5Gi
        ```
        
        **Pod에서 PVC 사용** 예제:
        ```yaml
        apiVersion: v1
        kind: Pod
        metadata:
          name: pvc-pod
        spec:
          containers:
          - name: app
            image: nginx
            volumeMounts:
            - mountPath: "/usr/share/nginx/html"
              name: mypd
          volumes:
          - name: mypd
            persistentVolumeClaim:
              claimName: pvc-example
        ```
        """)
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)  # 주제 구분선 추가
        st.markdown("### StorageClass")
        st.markdown("""
        **StorageClass**는 관리자가 제공하는 스토리지 클래스를 설명합니다. 다른 클래스는 서비스 수준, 백업 정책, 클러스터 관리자가 결정한 임의의 정책에 매핑될 수 있습니다.

        ```yaml
        apiVersion: storage.k8s.io/v1
        kind: StorageClass
        metadata:
          name: standard
        provisioner: kubernetes.io/aws-ebs
        parameters:
          type: gp2
        reclaimPolicy: Retain
        allowVolumeExpansion: true
        ```
        """)
        
        # 다음 학습 추천 섹션 추가
        st.markdown("""
        <div class="next-learning">
            <h4>다음 학습 추천</h4>
            <ul>
                <li>Kubernetes 스토리지의 기본 개념을 이해했다면, <a href="/?page=intermediate#eks_storage">EKS 스토리지 관리</a> 모듈에서 EBS, EFS 등 AWS 스토리지 서비스와의 통합을 학습하세요.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Helm 기초 탭 (중급에서 이동)
    with tabs[4]:
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        st.markdown("### Helm 소개")
        st.markdown("""
        **Helm**은 Kubernetes 애플리케이션을 패키징, 구성 및 배포하기 위한 패키지 관리자입니다.
        
        **주요 개념**:
        - **차트(Chart)**: Helm 패키지로, Kubernetes 리소스를 설치하는 데 필요한 모든 리소스 정의를 포함
        - **저장소(Repository)**: 차트를 수집하고 공유하는 장소
        - **릴리스(Release)**: 클러스터에서 실행 중인 차트의 인스턴스
        """)
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)  # 주제 구분선 추가
        st.markdown("### Helm 설치")
        st.markdown("""
        ```bash
        # MacOS
        brew install helm
        
        # Windows
        choco install kubernetes-helm
        
        # Linux
        curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
        ```
        """)
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)  # 주제 구분선 추가
        st.markdown("### 기본 Helm 명령어")
        st.markdown("""
        **저장소 관리**:
        ```bash
        # 저장소 추가
        helm repo add stable https://charts.helm.sh/stable
        
        # 저장소 목록 보기
        helm repo list
        
        # 저장소 업데이트
        helm repo update
        ```
        
        **차트 검색 및 정보 확인**:
        ```bash
        # 차트 검색
        helm search repo nginx
        
        # 차트 정보 확인
        helm show chart bitnami/nginx
        helm show values bitnami/nginx
        ```
        
        **차트 설치 및 관리**:
        ```bash
        # 차트 설치
        helm install my-release bitnami/nginx
        
        # 설치된 릴리스 목록 확인
        helm list
        
        # 릴리스 업그레이드
        helm upgrade my-release bitnami/nginx --set replicaCount=3
        
        # 릴리스 제거
        helm uninstall my-release
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)  # 주제 구분선 추가
        st.markdown("### 간단한 Helm 차트 구성")
        st.markdown("""
        기본적인 Helm 차트 디렉토리 구조:
        
        ```
        mychart/
        ├── Chart.yaml          # 차트에 대한 메타데이터
        ├── values.yaml         # 차트의 기본 구성 값
        ├── templates/          # Kubernetes 리소스 템플릿
        │   ├── deployment.yaml
        │   └── service.yaml
        └── charts/             # 의존성 차트 (선택 사항)
        ```
        """)
        
        # 다음 학습 추천 섹션 추가
        st.markdown("""
        <div class="next-learning">
            <h4>다음 학습 추천</h4>
            <ul>
                <li>Helm의 기본 개념과 명령어를 이해했다면, <a href="/?page=intermediate#helm_basics">Helm & 패키지 관리</a> 모듈에서 더 심화된 내용과 차트 사용자 정의 방법을 학습하세요.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 서버리스 EKS 소개 탭 (새로 추가)
    with tabs[5]:
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        st.markdown("### AWS Fargate 개요")
        st.markdown("""
        **AWS Fargate**는 컨테이너를 위한 서버리스 컴퓨팅 엔진으로, 서버를 프로비저닝하고 관리할 필요 없이 컨테이너를 실행할 수 있습니다.
        
        **주요 특징**:
        - 서버 관리 작업 불필요
        - 사용한 리소스에 대해서만 비용 지불
        - 각 애플리케이션 격리를 통한 보안 강화
        - EC2 인스턴스와 달리 컨테이너별 리소스 할당
        """)

        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)  # 주제 구분선 추가
        st.markdown("### EKS와 Fargate 통합")
        st.markdown("""
        Amazon EKS와 Fargate를 함께 사용하면 Kubernetes Pod를 서버리스 방식으로 실행할 수 있습니다.
        
        **작동 방식**:
        1. EKS 클러스터에 Fargate 프로필을 생성
        2. 프로필은 특정 네임스페이스와 레이블을 기준으로 어떤 Pod가 Fargate에서 실행될지 결정
        3. 프로필에 맞는 Pod가 생성되면 EKS는 해당 Pod를 Fargate에 자동으로 스케줄링
        """)

        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)  # 주제 구분선 추가
        st.markdown("### 첫 번째 Fargate 프로필 생성")
        st.markdown("""
        ```bash
        # eksctl을 사용한 Fargate 프로필 생성
        eksctl create fargateprofile \\
          --cluster my-eks-cluster \\
          --name fp-default \\
          --namespace default
        ```
        
        **AWS 콘솔을 통한 생성**:
        1. EKS 콘솔에서 클러스터 선택
        2. 'Compute' 탭으로 이동
        3. 'Add Fargate Profile' 선택
        4. 프로필 이름, 포드 실행 역할, 서브넷, 네임스페이스 선택기 구성
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)  # 주제 구분선 추가
        st.markdown("### Fargate 사용 사례")
        st.markdown("""
        **적합한 워크로드**:
        - 배치 처리
        - 웹 애플리케이션
        - 마이크로서비스
        - 데이터 처리 애플리케이션
        
        **적합하지 않은 워크로드**:
        - 매우 낮은 지연 시간이 필요한 애플리케이션
        - GPU가 필요한 워크로드
        - 특정 하드웨어 기능이 필요한 경우
        - DaemonSet을 활용하는 워크로드
        """)

        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)  # 주제 구분선 추가
        st.markdown("### Fargate로 샘플 애플리케이션 배포")
        st.markdown("""
        ```yaml
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: nginx-fargate
          namespace: default
        spec:
          replicas: 2
          selector:
            matchLabels:
              app: nginx
          template:
            metadata:
              labels:
                app: nginx
            spec:
              containers:
              - name: nginx
                image: nginx:latest
                ports:
                - containerPort: 80
        ```
        
        ```bash
        # 배포 적용
        kubectl apply -f nginx-deployment.yaml
        
        # Pod가 Fargate에서 실행되는지 확인
        kubectl get pods -o wide
        ```
        """)
        
        # 다음 학습 추천 섹션 추가
        st.markdown("""
        <div class="next-learning">
            <h4>다음 학습 추천</h4>
            <ul>
                <li>Fargate의 기본 개념을 이해했다면, <a href="/?page=intermediate#eks_management">EKS 관리와 운영</a> 모듈에서 더 심화된 Fargate 프로필 설정을 학습하세요.</li>
                <li>고급 사용자는 <a href="/?page=advanced">고급 과정</a>에서 서버리스 Kubernetes 심화 모듈을 확인하세요.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 기본 실습 프로젝트 탭 (모니터링 부분 제외)
    with tabs[6]:
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        st.markdown("### Hello World 애플리케이션 배포")
        st.markdown("""
        간단한 웹 애플리케이션을 EKS에 배포하는 실습입니다.

        **1. Deployment 매니페스트 작성 (hello-app.yaml)**:
        ```yaml
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: hello-app
        spec:
          replicas: 3
          selector:
            matchLabels:
              app: hello-app
          template:
            metadata:
              labels:
                app: hello-app
            spec:
              containers:
              - name: hello-app
                image: paulbouwer/hello-kubernetes:1.8
                ports:
                - containerPort: 8080
        
        ---
        apiVersion: v1
        kind: Service
        metadata:
          name: hello-app
        spec:
          type: LoadBalancer
          ports:
          - port: 80
            targetPort: 8080
          selector:
            app: hello-app
        ```

        **2. 애플리케이션 배포**:
        ```bash
        kubectl apply -f hello-app.yaml
        ```

        **3. 배포 상태 확인**:
        ```bash
        kubectl get deployments
        kubectl get pods
        kubectl get services
        ```

        **4. 애플리케이션 접속**:
        서비스의 EXTERNAL-IP를 브라우저에 입력하여 접속
        ```bash
        kubectl get services hello-app
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)  # 주제 구분선 추가
        st.markdown("### WordPress 배포")
        st.markdown("""
        WordPress와 MySQL을 EKS에 배포하는 실습입니다.

        **1. WordPress와 MySQL PVC 생성 (wordpress-pvc.yaml)**:
        ```yaml
        apiVersion: v1
        kind: PersistentVolumeClaim
        metadata:
          name: mysql-pvc
        spec:
          accessModes:
            - ReadWriteOnce
          resources:
            requests:
              storage: 20Gi
              
        ---
        apiVersion: v1
        kind: PersistentVolumeClaim
        metadata:
          name: wordpress-pvc
        spec:
          accessModes:
            - ReadWriteOnce
          resources:
            requests:
              storage: 20Gi
        ```

        **2. MySQL Deployment (mysql-deployment.yaml)**:
        ```yaml
        apiVersion: v1
        kind: Secret
        metadata:
          name: mysql-secret
        type: Opaque
        data:
          password: cGFzc3dvcmQ=  # 'password'를 base64로 인코딩
        
        ---
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: mysql
        spec:
          replicas: 1
          selector:
            matchLabels:
              app: mysql
          template:
            metadata:
              labels:
                app: mysql
            spec:
              containers:
              - name: mysql
                image: mysql:5.7
                ports:
                - containerPort: 3306
                env:
                - name: MYSQL_ROOT_PASSWORD
                  valueFrom:
                    secretKeyRef:
                      name: mysql-secret
                      key: password
                volumeMounts:
                - name: mysql-data
                  mountPath: /var/lib/mysql
              volumes:
              - name: mysql-data
                persistentVolumeClaim:
                  claimName: mysql-pvc
                  
        ---
        apiVersion: v1
        kind: Service
        metadata:
          name: mysql
        spec:
          ports:
          - port: 3306
          selector:
            app: mysql
          clusterIP: None
        ```

        **3. WordPress Deployment (wordpress-deployment.yaml)**:
        ```yaml
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: wordpress
        spec:
          replicas: 2
          selector:
            matchLabels:
              app: wordpress
          template:
            metadata:
              labels:
                app: wordpress
            spec:
              containers:
              - name: wordpress
                image: wordpress:latest
                ports:
                - containerPort: 80
                env:
                - name: WORDPRESS_DB_HOST
                  value: mysql
                - name: WORDPRESS_DB_PASSWORD
                  valueFrom:
                    secretKeyRef:
                      name: mysql-secret
                      key: password
                volumeMounts:
                - name: wordpress-data
                  mountPath: /var/www/html
              volumes:
              - name: wordpress-data
                persistentVolumeClaim:
                  claimName: wordpress-pvc
                  
        ---
        apiVersion: v1
        kind: Service
        metadata:
          name: wordpress
        spec:
          type: LoadBalancer
          ports:
          - port: 80
          selector:
            app: wordpress
        ```

        **4. 리소스 배포**:
        ```bash
        kubectl apply -f wordpress-pvc.yaml
        kubectl apply -f mysql-deployment.yaml
        kubectl apply -f wordpress-deployment.yaml
        ```

        **5. 배포 확인 및 접속**:
        ```bash
        kubectl get deployments
        kubectl get pods
        kubectl get services wordpress
        ```
        """)
        
        # 다음 학습 추천 섹션 추가
        st.markdown("""
        <div class="next-learning">
            <h4>다음 학습 추천</h4>
            <ul>
                <li>기본 프로젝트를 완료했다면, <a href="/?page=intermediate#intermediate_projects">중급 실습 프로젝트</a>에서 마이크로서비스 배포와 CI/CD 파이프라인 구축을 배워보세요.</li>
                <li>클러스터 모니터링에 관심이 있다면, <a href="/?page=intermediate#monitoring_basics">모니터링 기초</a> 모듈을 확인하세요.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 복습 섹션
    st.markdown("<h2 class='section-title'>개념 정리 및 복습</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="review-section">
        <h3 class="review-title">초급 과정 요약</h3>
        <div class="review-content">
            <p>EKS와 Kubernetes 초급 과정에서 배운 핵심 개념과 명령어를 정리합니다.</p>
            
            <h4>1. 컨테이너 기초</h4>
            <ul>
                <li><strong>컨테이너</strong>: 애플리케이션과 종속성을 함께 패키징한 독립적 실행 단위</li>
                <li><strong>이미지</strong>: 컨테이너 실행에 필요한 파일 시스템과 설정의 불변 스냅샷</li>
                <li><strong>Docker Engine</strong>: 컨테이너를 관리하는 런타임 환경</li>
                <li><strong>Dockerfile</strong>: 이미지를 빌드하기 위한 설명서</li>
            </ul>
            
            <h4>2. Kubernetes 기초</h4>
            <ul>
                <li><strong>Pod</strong>: Kubernetes의 기본 배포 단위, 하나 이상의 컨테이너 포함</li>
                <li><strong>Service</strong>: Pod에 안정적인 네트워크 엔드포인트 제공</li>
                <li><strong>Deployment</strong>: Pod의 선언적 업데이트와 스케일링 관리</li>
                <li><strong>kubectl</strong>: Kubernetes 클러스터 관리 CLI 도구</li>
            </ul>
            
            <h4>3. EKS 설정 및 관리</h4>
            <ul>
                <li><strong>eksctl</strong>: EKS 클러스터 생성 및 관리 도구</li>
                <li><strong>노드 그룹</strong>: Kubernetes 워커 노드로 작동하는 EC2 인스턴스 집합</li>
                <li><strong>IAM 역할</strong>: EKS 클러스터와 노드에 권한 부여</li>
                <li><strong>AWS VPC</strong>: EKS 클러스터의 네트워크 환경</li>
            </ul>
            
            <h4>4. 스토리지 기초</h4>
            <ul>
                <li><strong>영구 볼륨(PV)</strong>: 클러스터의 스토리지 리소스</li>
                <li><strong>영구 볼륨 클레임(PVC)</strong>: 사용자가 PV에 접근하기 위한 요청</li>
                <li><strong>스토리지 클래스</strong>: PV를 동적으로 프로비저닝하는 방법</li>
            </ul>
            
            <h4>5. Helm 기본</h4>
            <ul>
                <li><strong>차트(Chart)</strong>: Kubernetes 애플리케이션 패키지</li>
                <li><strong>릴리스(Release)</strong>: 클러스터에 설치된 차트 인스턴스</li>
                <li><strong>저장소(Repository)</strong>: 차트를 저장하고 공유하는 장소</li>
            </ul>
            
            <h4>6. 서버리스 EKS</h4>
            <ul>
                <li><strong>Fargate</strong>: 서버리스 컨테이너 컴퓨팅 엔진</li>
                <li><strong>Fargate 프로필</strong>: 어떤 Pod가 Fargate에서 실행될지 정의</li>
                <li><strong>사용 사례</strong>: 배치 처리, 웹 애플리케이션, 마이크로서비스</li>
            </ul>
            
            <h4>자주 사용하는 kubectl 명령어 요약</h4>
            <div class="code-block">
            # 리소스 생성/갱신
            kubectl apply -f [파일명.yaml]
            
            # 리소스 조회
            kubectl get [리소스타입] -n [네임스페이스]
            
            # 리소스 상세 정보 확인
            kubectl describe [리소스타입] [리소스명]
            
            # Pod 로그 확인
            kubectl logs [파드명]
            
            # 컨테이너 내부 접속
            kubectl exec -it [파드명] -- /bin/bash
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 중급/고급 과정으로 이동하는 링크 추가
    st.markdown("""
    <div class="next-learning" style="margin-top: 40px;">
        <h4>다음 학습 단계</h4>
        <p>기본 과정을 충분히 이해했다면, 다음 단계로 진행하세요:</p>
        <ul>
            <li><a href="/?page=intermediate">중급 과정으로 이동하기 →</a> (고급 리소스, 관리, 모니터링, CI/CD)</li>
            <li><a href="/?page=advanced">고급 과정 살펴보기 →</a> (CRD, 서비스 메시, 고급 보안, 멀티클러스터)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)