import streamlit as st
from utils.localization import t
from services.analytics.usage_tracker import UsageTracker

def render_advanced():
    """고급 과정 메인 페이지 - 개선된 디자인 및 이동 경로 추가"""
    
    # 사용 추적
    UsageTracker.track_page_view("advanced")
    
    # 공통 스타일 정의 - HTML 렌더링 문제 해결을 위한 코드 수정
    st.markdown("""
    <style>
    /* 색상 변수 */
    :root {
        --red-color: #e63946;
        --red-light: #fde9e8;
        --divider-color: #e0e0e0;  /* 회색 구분선 */
        --blue-color: #4361ee;     /* 기본 색상 */
        --yellow-color: #ffb703;   /* 중급 색상 */
        --nav-bg-color: #f8f9fa;
    }

    /* 페이지 제목 - "고급"을 더 크게 */
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
        background-color: var(--red-light);
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
        background-color: var(--red-light);
        border-radius: 4px;
        font-size: 0.85rem;
    }
    
    .related-module-link a {
        color: var(--red-color);
        text-decoration: none;
        font-weight: 600;
    }
    
    .related-module-link a:hover {
        text-decoration: underline;
    }
    
    /* 선수 지식 표시 */
    .prerequisite {
        margin-top: 5px;
        margin-bottom: 5px;
        font-size: 0.8rem;
        color: #666;
        font-style: italic;
        padding: 3px 0;
    }
    
    .prerequisite a {
        color: var(--yellow-color);
        text-decoration: none;
    }
    
    .prerequisite a:hover {
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
        border-bottom: 2px solid var(--divider-color) !important;
    }

    /* 모듈 카드 스타일 - 높이 고정 및 일관성 유지 */
    .module-card {
        background-color: white;
        border-radius: 12px;
        border-top: 5px solid var(--red-color);
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        padding: 15px;
        margin-bottom: 20px;
        height: 300px !important; /* 높이 증가 - 관련 모듈 링크 공간 확보 */
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
        background-color: var(--red-color);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-right: 12px;
        flex-shrink: 0;
    }

    /* 모듈 제목 */
    .module-title {
        font-size: 1.5rem !important;
        font-weight: 600;
        color: var(--red-color);
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
        color: var(--red-color);
    }

    /* 인트로 카드 */
    .intro-card {
        background-color: var(--red-light);
        border-left: 4px solid var(--red-color);
        padding: 15px;
        border-radius: 6px;
        margin-bottom: 20px;
        font-size: 0.9rem;
    }

    /* 로드맵 섹션 */
    .roadmap-section {
        margin: 25px 0;
    }

    /* 탭 스타일링 수정 */
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

    /* 탭 호버 효과 */
    .stTabs [data-baseweb="tab"]:hover {
        color: var(--red-color) !important;
        border-bottom: 2px solid var(--red-color) !important;
    }

    /* 선택된 탭 스타일 */
    .stTabs [aria-selected="true"] {
        color: var(--red-color) !important;
        border-bottom: 2px solid var(--red-color) !important;
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

    /* 다음 학습 추천 섹션 */
    .next-learning {
        margin-top: 30px;
        padding: 15px;
        background-color: var(--red-light);
        border-radius: 6px;
        border-left: 4px solid var(--red-color);
    }
    
    .next-learning h4 {
        margin-top: 0 !important;
        color: var(--red-color) !important;
    }
    
    .next-learning ul {
        margin-bottom: 0;
    }

    /* 탭 내용 제목 스타일 */
    .tab-content h3 {
        font-size: 1.5rem !important;
        margin-top: 25px !important;
        margin-bottom: 15px !important;
        color: var(--red-color) !important;
        padding-bottom: 8px !important;
        border-bottom: 1px solid var(--divider-color) !important;  /* 회색 구분선 */
    }

    .tab-content h4 {
        font-size: 1.2rem !important;
        margin-top: 20px !important;
        margin-bottom: 10px !important;
        color: #444 !important;
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
        border-left: 4px solid var(--red-color);
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
        color: var(--red-color) !important;
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
    
    # 페이지 제목
    st.markdown(f"<h1>{t('advanced')}</h1>", unsafe_allow_html=True)
    
    # 학습 경로 네비게이션 추가
    st.markdown("""
    <div class="learning-path-nav">
        <div class="nav-item">
            <a href="/?page=beginner" class="beginner-nav">기본 과정</a>
        </div>
        <div class="nav-item">
            <a href="/?page=intermediate" class="intermediate-nav">중급 과정</a>
        </div>
        <div class="nav-item current">
            <span class="advanced-nav">고급 과정</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 인트로 설명
    st.markdown("""
    <div class="intro-card">
        Kubernetes와 EKS에 대한 심층적인 지식을 갖춘 사용자를 위한 고급 주제입니다.
        복잡한 배포 전략, 멀티클러스터 관리, 서비스 메시, 보안 강화 등을 다룹니다.
    </div>
    """, unsafe_allow_html=True)
    
    # 모듈 정의 - 내용 정리 및 학습 경로 추가
    modules = [
        {
            "id": "k8s_advanced",
            "title": "고급 Kubernetes",
            "icon": "K",
            "description": "Kubernetes의 고급 기능과 확장성 기능을 탐구합니다. CRD, 커스텀 컨트롤러, 어피니티 등을 다룹니다.",
            "topics": ["CRD & 오퍼레이터 패턴", "커스텀 컨트롤러 개발", "고급 스케줄링", "멀티클러스터 관리"],
            "prerequisites": ["k8s_advanced"]
        },
        {
            "id": "gitops_cicd",
            "title": "GitOps와 고급 CI/CD",
            "icon": "G",
            "description": "GitOps 원칙을 기반으로 한 고급 배포 전략을 학습합니다. ArgoCD, FluxCD 등의 도구를 다룹니다.",
            "topics": ["ArgoCD 고급 설정", "FluxCD 구현", "카나리/블루-그린 배포", "프로그레시브 딜리버리"],
            "prerequisites": ["cicd_basics"]
        },
        {
            "id": "networking",
            "title": "네트워킹 고급",
            "icon": "N",
            "description": "Kubernetes 네트워킹의 심층적인 측면과 고급 네트워크 관리 기술을 학습합니다.",
            "topics": ["Calico CNI 고급 설정", "네트워크 정책", "서비스 메시(Istio) 심화", "멀티클러스터 네트워킹"],
            "prerequisites": ["service_mesh_intro"]
        },
        {
            "id": "security",
            "title": "보안 강화",
            "icon": "S",
            "description": "EKS와 Kubernetes 환경의 보안을 강화하는 방법을 심층적으로 학습합니다.",
            "topics": ["Pod 보안 정책", "이미지 스캐닝", "런타임 보안", "Secret 관리 전략"],
            "prerequisites": ["eks_storage"]
        },
        {
            "id": "multi_cluster",
            "title": "멀티클러스터 관리",
            "icon": "M",
            "description": "여러 EKS 클러스터를 효율적으로 관리하고 연결하는 방법을 배웁니다.",
            "topics": ["멀티클러스터 아키텍처", "클러스터 간 연결", "리소스 동기화", "전역 워크로드 배포"],
            "prerequisites": ["eks_management", "k8s_advanced"]
        },
        {
            "id": "disaster_recovery",
            "title": "재해 복구 및 백업",
            "icon": "D",
            "description": "EKS 클러스터의 재해 복구 전략과 데이터 백업 방법을 학습합니다.",
            "topics": ["백업 솔루션(Velero)", "다중 리전 DR 설계", "백업/복구 자동화", "고가용성 아키텍처"],
            "prerequisites": ["eks_storage"]
        },
        {
            "id": "observability",
            "title": "고급 관찰성",
            "icon": "O",
            "description": "분산 시스템 모니터링을 위한 고급 도구와 기술을 다룹니다.",
            "topics": ["분산 추적(Jaeger)", "EFK 스택 구성", "사용자 정의 메트릭", "용량 계획"],
            "prerequisites": ["monitoring_basics"]
        },
        {
            "id": "ai_ml_workloads",
            "title": "AI/ML 워크로드",
            "icon": "A",
            "description": "EKS에서 AI/ML 워크로드를 효율적으로 실행하기 위한 방법을 배웁니다.",
            "topics": ["Kubeflow 배포", "GPU 노드 관리", "분산 학습 구성", "ML 파이프라인 자동화"],
            "prerequisites": ["eks_management", "serverless_advanced"]
        },
        {
            "id": "cost_optimization",
            "title": "비용 최적화 전략",
            "icon": "C",
            "description": "EKS 클러스터 운영 비용을 최적화하는 전략과 방법을 학습합니다.",
            "topics": ["스팟 인스턴스 활용", "리소스 요청 최적화", "비용 할당 태그", "워크로드 스케줄링"],
            "prerequisites": ["scaling_eks", "serverless_advanced"]
        },
        {
            "id": "advanced_projects",
            "title": "고급 실습 프로젝트",
            "icon": "P",
            "description": "복잡한 실제 시나리오를 통해 고급 개념을 실습합니다.",
            "topics": ["다중 영역 HA 아키텍처", "GitOps 기반 멀티클러스터", "서비스 메시 구현"],
            "prerequisites": ["intermediate_projects"]
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
                    # 선수 지식 표시 - HTML이 올바르게 렌더링되도록 수정
                    prereq_html = ""
                    if "prerequisites" in module and module["prerequisites"]:
                        prereq_links = []
                        for prereq in module["prerequisites"]:
                            link_text = ""
                            level = ""
                            if prereq in ["kubernetes_intro", "eks_basics", "storage_basics", "serverless_intro", "helm_basics", "basic_projects"]:
                                prereq_title = prereq.replace("_", " ").title()
                                link_text = f'<a href="/?page=beginner#{prereq}">{prereq_title}</a>'
                                level = "기본 과정"
                            else:
                                prereq_title = prereq.replace("_", " ").title()
                                link_text = f'<a href="/?page=intermediate#{prereq}">{prereq_title}</a>'
                                level = "중급 과정"
                            prereq_links.append(f"{link_text} ({level})")
                        
                        prereq_html = f"""
                        <div class="prerequisite">
                            선수 지식: {", ".join(prereq_links)}
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
    
    # 고급 Kubernetes 탭
    with tabs[0]:
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        st.markdown("### Custom Resource Definition(CRD) 및 Operator 패턴")
        st.markdown("""
        **CRD(Custom Resource Definition)**를 사용하면 Kubernetes API를 확장하여 사용자 정의 리소스를 만들 수 있습니다.
        
        **간단한 CRD 정의 예시**:
        ```yaml
        apiVersion: apiextensions.k8s.io/v1
        kind: CustomResourceDefinition
        metadata:
          name: backups.stable.example.com
        spec:
          group: stable.example.com
          versions:
            - name: v1
              served: true
              storage: true
              schema:
                openAPIV3Schema:
                  type: object
                  properties:
                    spec:
                      type: object
                      properties:
                        source:
                          type: string
                        schedule:
                          type: string
                        retention:
                          type: integer
          scope: Namespaced
          names:
            plural: backups
            singular: backup
            kind: Backup
            shortNames:
            - bk
        ```

        **Operator 패턴**은 Kubernetes 컨트롤러와 CRD를 결합하여 특정 애플리케이션의 운영 지식을 소프트웨어로 인코딩하는 방식입니다.
        
        Operator는 다음과 같은 구성 요소로 이루어집니다:
        1. **CRD**: 커스텀 리소스 정의
        2. **컨트롤러**: 리소스의 상태를 감시하고 조작하는 로직
        3. **리콘실리에이션 루프**: 실제 상태를 원하는 상태로 조정하는 프로세스
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### 커스텀 컨트롤러 개발")
        st.markdown("""
        **Kubebuilder**를 사용한 커스텀 컨트롤러 개발 과정:
        
        ```bash
        # 프로젝트 생성
        kubebuilder init --domain example.com --repo github.com/example/backup-operator

        # API 리소스 생성
        kubebuilder create api --group backup --version v1 --kind Backup
        ```

        **컨트롤러의 조정 함수 예시**:
        ```go
        func (r *BackupReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
            log := r.Log.WithValues("backup", req.NamespacedName)
            
            // 리소스 객체 가져오기
            var backup backupv1.Backup
            if err := r.Get(ctx, req.NamespacedName, &backup); err != nil {
                if errors.IsNotFound(err) {
                    return ctrl.Result{}, nil
                }
                log.Error(err, "Unable to fetch Backup")
                return ctrl.Result{}, err
            }
            
            // 백업 작업 수행 로직
            if backup.Status.State == "" {
                backup.Status.State = "InProgress"
                if err := r.Status().Update(ctx, &backup); err != nil {
                    return ctrl.Result{}, err
                }
                
                // 백업 실행
                if err := performBackup(backup.Spec.Source); err != nil {
                    backup.Status.State = "Failed"
                    backup.Status.Error = err.Error()
                    r.Status().Update(ctx, &backup)
                    return ctrl.Result{}, err
                }
                
                backup.Status.State = "Completed"
                backup.Status.CompletionTime = metav1.Now()
                if err := r.Status().Update(ctx, &backup); err != nil {
                    return ctrl.Result{}, err
                }
            }
            
            return ctrl.Result{}, nil
        }
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### 고급 스케줄링 기법")
        st.markdown("""
        **노드 어피니티(Node Affinity)** - 특정 노드 특성에 기반한 스케줄링
        
        ```yaml
        apiVersion: v1
        kind: Pod
        metadata:
          name: with-node-affinity
        spec:
          affinity:
            nodeAffinity:
              requiredDuringSchedulingIgnoredDuringExecution:
                nodeSelectorTerms:
                - matchExpressions:
                  - key: kubernetes.io/e2e-az-name
                    operator: In
                    values:
                    - us-west-1a
                    - us-west-1b
              preferredDuringSchedulingIgnoredDuringExecution:
              - weight: 1
                preference:
                  matchExpressions:
                  - key: another-node-label-key
                    operator: In
                    values:
                    - another-node-label-value
          containers:
          - name: with-node-affinity
            image: nginx
        ```
        
        **팟 어피니티(Pod Affinity)** - 다른 Pod와의 관계에 기반한 스케줄링
        
        ```yaml
        apiVersion: v1
        kind: Pod
        metadata:
          name: with-pod-affinity
        spec:
          affinity:
            podAffinity:
              requiredDuringSchedulingIgnoredDuringExecution:
              - labelSelector:
                  matchExpressions:
                  - key: security
                    operator: In
                    values:
                    - S1
                topologyKey: topology.kubernetes.io/zone
            podAntiAffinity:
              preferredDuringSchedulingIgnoredDuringExecution:
              - weight: 100
                podAffinityTerm:
                  labelSelector:
                    matchExpressions:
                    - key: security
                      operator: In
                      values:
                      - S2
                  topologyKey: topology.kubernetes.io/zone
          containers:
          - name: with-pod-affinity
            image: nginx
        ```
        
        **Taint와 Toleration** - 특정 노드에 Pod가 스케줄링되지 않도록 제한
        
        ```bash
        # 노드에 taint 추가
        kubectl taint nodes node1 key=value:NoSchedule
        ```
        
        ```yaml
        apiVersion: v1
        kind: Pod
        metadata:
          name: tolerating-pod
        spec:
          tolerations:
          - key: "key"
            operator: "Equal"
            value: "value"
            effect: "NoSchedule"
          containers:
          - name: nginx
            image: nginx
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### 멀티클러스터 관리와 Federation")
        st.markdown("""
        **Kubefed (Kubernetes Federation)**를 사용하여 여러 클러스터를 중앙에서 관리할 수 있습니다.

        **Federation 설치**:
        ```bash
        # Kubefed CLI 설치
        curl -LO https://github.com/kubernetes-sigs/kubefed/releases/download/v0.8.1/kubefedctl-0.8.1-linux-amd64.tgz
        tar -xvf kubefedctl-0.8.1-linux-amd64.tgz
        chmod +x kubefedctl
        sudo mv kubefedctl /usr/local/bin/
        
        # Federation 컨트롤 플레인 설치
        kubefedctl install
        ```

        **클러스터 조인**:
        ```bash
        # 클러스터 컨텍스트 가져오기
        kubectl config get-contexts
        
        # Federation에 클러스터 조인
        kubefedctl join cluster1 --cluster-context cluster1 --host-cluster-context host-cluster
        kubefedctl join cluster2 --cluster-context cluster2 --host-cluster-context host-cluster
        ```

        **FederatedDeployment 예제**:
        ```yaml
        apiVersion: types.kubefed.io/v1beta1
        kind: FederatedDeployment
        metadata:
          name: test-deployment
          namespace: test-namespace
        spec:
          template:
            metadata:
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
                  - image: nginx
                    name: nginx
          placement:
            clusters:
            - name: cluster1
            - name: cluster2
          overrides:
          - clusterName: cluster2
            clusterOverrides:
            - path: "/spec/replicas"
              value: 5
        ```
        """)
        
        # 다음 학습 추천 섹션 추가
        st.markdown("""
        <div class="next-learning">
            <h4>관련 학습 리소스</h4>
            <ul>
                <li>Kubernetes 확장에 관심이 있다면 <a href="/?page=advanced#multi_cluster">멀티클러스터 관리</a> 모듈을 함께 학습하세요.</li>
                <li>CRD 기반 보안 정책을 구현하려면 <a href="/?page=advanced#security">보안 강화</a> 모듈을 참고하세요.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # GitOps와 고급 CI/CD 탭
    with tabs[1]:
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        st.markdown("### GitOps 심화 개념")
        st.markdown("""
        **GitOps**는 Git을 단일 진실 원천으로 사용하여 인프라 및 애플리케이션을 관리하는 방법론입니다.

        **GitOps 고급 원칙**:
        - **불변 인프라**: 변경 대신 항상 새 인프라 배포
        - **선언적 상태**: 모든 시스템 상태는 Git 저장소에 선언적으로 정의
        - **시스템 드리프트 감지 및 수정**: 시스템이 선언된 상태에서 벗어나면 자동 복구
        - **점진적 배포**: 변경사항을 단계적으로 배포하고 롤백 준비
        - **감사성**: 모든 변경이 Git에 추적되므로 전체 변경 기록 유지
        
        **내부 루프와 외부 루프**:
        - **내부 루프**: 개발자 중심의 워크플로우 (개발, 테스트, 코드 리뷰)
        - **외부 루프**: 운영 중심의 워크플로우 (배포, 모니터링, 알림, 롤백)
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### ArgoCD 고급 설정")
        st.markdown("""
        **ArgoCD**는 GitOps 방식으로 애플리케이션을 Kubernetes에 지속적으로 배포하기 위한 선언적 도구입니다.

        **애플리케이션 동기화 정책 고급 설정**:
        ```yaml
        apiVersion: argoproj.io/v1alpha1
        kind: Application
        metadata:
          name: complex-app
          namespace: argocd
          finalizers:
            - resources-finalizer.argocd.argoproj.io
        spec:
          project: production
          source:
            repoURL: https://github.com/organization/app-configs.git
            targetRevision: HEAD
            path: overlays/production
          destination:
            server: https://kubernetes.default.svc
            namespace: production
          syncPolicy:
            automated:
              prune: true
              selfHeal: true
              allowEmpty: false
            syncOptions:
              - Validate=true
              - CreateNamespace=true
              - PrunePropagationPolicy=foreground
              - PruneLast=true
            retry:
              limit: 5
              backoff:
                duration: 5s
                factor: 2
                maxDuration: 3m
          ignoreDifferences:
          - group: apps
            kind: Deployment
            jsonPointers:
            - /spec/replicas
    **AppProject 리소스를 통한 권한 제어**:
    ```yaml
    apiVersion: argoproj.io/v1alpha1
    kind: AppProject
    metadata:
      name: production
      namespace: argocd
    spec:
      description: Production Environment
      sourceRepos:
      - 'https://github.com/organization/*'
      
      # 클러스터 및 네임스페이스 제한
      destinations:
      - namespace: production
        server: https://kubernetes.default.svc
      - namespace: monitoring
        server: https://kubernetes.default.svc
      
      # 역할 정의
      roles:
      - name: project-admin
        description: Project admins
        policies:
        - p, proj:production:project-admin, applications, *, production/*, allow
        groups:
        - production-admins

      # 리소스 제한
      clusterResourceWhitelist:
      - group: '*'
        kind: Namespace
      - group: 'networking.k8s.io'
        kind: Ingress
      
      # 네임스페이스 리소스 제한
      namespaceResourceWhitelist:
      - group: '*'
        kind: '*'
        
      # 오프젝트 시그니처 검증 활성화
      signatureKeys:
      - keyID: ABCDEF1234567890
    ```
    """)
    
    st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
    
    st.markdown("### Flux CD 구현")
    st.markdown("""
    **Flux CD**는 Weaveworks에서 개발한 GitOps 도구로, Git 저장소의 변경 사항을 클러스터에 자동으로 동기화합니다.

    **Flux CLI 설치**:
    ```bash
    # Flux CLI 설치
    curl -s https://fluxcd.io/install.sh | bash
    
    # 클러스터에 Flux 구성요소 설치
    flux bootstrap github \\
      --owner=my-github-username \\
      --repository=my-flux-config \\
      --branch=main \\
      --path=clusters/production \\
      --personal
    ```

    **소스 리포지토리 정의**:
    ```yaml
    apiVersion: source.toolkit.fluxcd.io/v1beta2
    kind: GitRepository
    metadata:
      name: app-config
      namespace: flux-system
    spec:
      interval: 1m
      url: https://github.com/my-org/app-config
      ref:
        branch: main
      secretRef:
        name: github-credentials
    ```

    **Kustomization 리소스 정의**:
    ```yaml
    apiVersion: kustomize.toolkit.fluxcd.io/v1beta2
    kind: Kustomization
    metadata:
      name: app-config
      namespace: flux-system
    spec:
      interval: 5m0s
      path: ./overlays/production
      prune: true
      sourceRef:
        kind: GitRepository
        name: app-config
      validation: client
      healthChecks:
      - apiVersion: apps/v1
        kind: Deployment
        name: app-backend
        namespace: production
    ```

    **이미지 자동 업데이트 구성**:
    ```yaml
    apiVersion: image.toolkit.fluxcd.io/v1beta1
    kind: ImageRepository
    metadata:
      name: app-images
      namespace: flux-system
    spec:
      image: docker.io/myorg/app
      interval: 1m0s
    ---
    apiVersion: image.toolkit.fluxcd.io/v1beta1
    kind: ImagePolicy
    metadata:
      name: app-policy
      namespace: flux-system
    spec:
      imageRepositoryRef:
        name: app-images
      policy:
        semver:
          range: '>=1.0.0 <2.0.0'
    ---
    apiVersion: image.toolkit.fluxcd.io/v1beta1
    kind: ImageUpdateAutomation
    metadata:
      name: app-image-update
      namespace: flux-system
    spec:
      interval: 1m0s
      sourceRef:
        kind: GitRepository
        name: app-config
      git:
        checkout:
          ref:
            branch: main
        commit:
          author:
            name: Flux
            email: flux@example.com
          messageTemplate: 'Update image to {{.NewTag}}'
        push:
          branch: main
      update:
        path: ./base/deployment.yaml
        strategy: Setters
    ```
    """)
    
    st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
    
    st.markdown("### 고급 배포 전략")
    st.markdown("""
    **카나리 배포** - 신규 버전을 일부 트래픽에만 점진적으로 노출하는 방식

    **Argo Rollouts를 사용한 카나리 배포 예시**:
    ```yaml
    apiVersion: argoproj.io/v1alpha1
    kind: Rollout
    metadata:
      name: example-rollout
    spec:
      replicas: 10
      strategy:
        canary:
          steps:
          - setWeight: 20
          - pause: {duration: 10m}
          - setWeight: 40
          - pause: {duration: 10m}
          - setWeight: 60
          - pause: {duration: 10m}
          - setWeight: 80
          - pause: {duration: 10m}
          # 메트릭 기반 분석
          analysis:
            templates:
            - templateName: success-rate
            args:
            - name: service-name
              value: canary-demo
      revisionHistoryLimit: 2
      selector:
        matchLabels:
          app: canary-demo
      template:
        metadata:
          labels:
            app: canary-demo
        spec:
          containers:
          - name: canary-demo
            image: argoproj/rollouts-demo:blue
            ports:
            - name: http
              containerPort: 8080
              protocol: TCP
            resources:
              requests:
                memory: 32Mi
                cpu: 5m
    ```

    **블루/그린 배포** - 동일한 두 환경을 준비하고 한 번에 트래픽 전환

    ```yaml
    apiVersion: argoproj.io/v1alpha1
    kind: Rollout
    metadata:
      name: bluegreen-rollout
    spec:
      replicas: 3
      revisionHistoryLimit: 2
      selector:
        matchLabels:
          app: bluegreen-demo
      template:
        metadata:
          labels:
            app: bluegreen-demo
        spec:
          containers:
          - name: bluegreen-demo
            image: argoproj/rollouts-demo:blue
            ports:
            - name: http
              containerPort: 8080
              protocol: TCP
            resources:
              requests:
                memory: 32Mi
                cpu: 5m
      strategy:
        blueGreen:
          activeService: bluegreen-demo-active
          previewService: bluegreen-demo-preview
          autoPromotionEnabled: false
          autoPromotionSeconds: 600  # 10분 후 자동 승격
          prePromotionAnalysis:
            templates:
            - templateName: smoke-tests
          postPromotionAnalysis:
            templates:
            - templateName: success-rate
            args:
            - name: service-name
              value: bluegreen-demo-active
          scaleDownDelaySeconds: 300  # 이전 버전 5분 유지 후 스케일 다운
    ```
    """)
    
    st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
    
    st.markdown("### 프로그레시브 딜리버리")
    st.markdown("""
    **프로그레시브 딜리버리**는 새로운 기능 릴리스의 위험을 줄이기 위한 현대적인 배포 방식입니다.

    **주요 테크닉**:

    **1. 특성 플래그 (Feature Flags)**:
    - 코드에 조건부 기능 포함
    - 런타임에 기능 활성화/비활성화 가능
    - 특정 사용자 세그먼트에 점진적으로 기능 노출
    
    ```java
    // 특성 플래그 구현 예
    if (featureFlags.isEnabled("new-ui-design")) {
        return renderNewUI();
    } else {
        return renderOldUI();
    }
    ```

    **2. A/B 테스팅**:
    - 두 가지 버전의 기능을 동시에 사용자에게 제공
    - 메트릭을 통해 어떤 버전이 더 나은지 판단
    - 데이터 기반 의사결정 가능

    **3. 점진적 롤아웃**:
    - 지역/데이터센터 기반 점진적 확장
    - 사용자 세그먼트 기반 단계적 배포
    - 문제 발생 시 영향 범위 최소화
    
    **Flagger를 사용한 메트릭 기반 카나리 배포**:
    ```yaml
    apiVersion: flagger.app/v1beta1
    kind: Canary
    metadata:
      name: app-canary
      namespace: production
    spec:
      targetRef:
        apiVersion: apps/v1
        kind: Deployment
        name: app
      progressDeadlineSeconds: 600
      service:
        port: 80
        targetPort: 8080
        gateways:
        - public-gateway
        hosts:
        - app.example.com
      analysis:
        interval: 30s
        threshold: 10
        maxWeight: 50
        stepWeight: 5
        metrics:
        - name: request-success-rate
          threshold: 99
          interval: 1m
        - name: request-duration
          threshold: 500
          interval: 1m
        webhooks:
        - name: acceptance-test
          type: pre-rollout
          url: http://flagger-loadtester.test/
          timeout: 30s
          metadata:
            type: bash
            cmd: "curl -s http://app-canary.production/health | grep OK"
        - name: load-test
          type: rollout
          url: http://flagger-loadtester.test/
          timeout: 30s
          metadata:
            type: cmd
            cmd: "hey -z 1m -q 10 -c 2 http://app-canary.production/"
    ```
    """)
    
    # 다음 학습 추천 섹션 추가
    st.markdown("""
    <div class="next-learning">
        <h4>관련 학습 리소스</h4>
        <ul>
            <li>멀티클러스터 환경에서의 GitOps 적용은 <a href="/?page=advanced#multi_cluster">멀티클러스터 관리</a> 모듈을 참고하세요.</li>
            <li>고급 배포 전략과 서비스 메시를 통합하려면 <a href="/?page=advanced#networking">네트워킹 고급</a> 모듈을 확인하세요.</li>
            <li>실제 고급 배포 전략을 적용하는 실습은 <a href="/?page=advanced#advanced_projects">고급 실습 프로젝트</a> 모듈에서 진행할 수 있습니다.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

    # 네트워킹 고급 탭
    with tabs[2]:
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        st.markdown("### Calico CNI 고급 설정")
        st.markdown("""
        **Calico**는 컨테이너, VM, 호스트 워크로드를 위한 오픈소스 네트워킹 및 네트워크 보안 솔루션입니다.
        
        **BGP(Border Gateway Protocol) 피어링 설정**:
        ```yaml
        apiVersion: projectcalico.org/v3
        kind: BGPPeer
        metadata:
          name: bgppeer-global
        spec:
          peerIP: 192.168.1.1
          asNumber: 64512
        ```
    
        **IP 풀 설정**:
        ```yaml
        apiVersion: projectcalico.org/v3
        kind: IPPool
        metadata:
          name: high-performance-pool
        spec:
          cidr: 192.168.0.0/16
          blockSize: 26
          ipipMode: Always
          natOutgoing: true
          nodeSelector: "nodetype == 'compute'"
        ```
    
        **Calico 기반 대역폭 제한**:
        ```yaml
        apiVersion: projectcalico.org/v3
        kind: NetworkPolicy
        metadata:
          name: limit-app-bandwidth
          namespace: app
        spec:
          selector: app == 'bandwidth-hungry'
          ingress:
          - action: Allow
            source:
              selector: role == 'frontend'
            destination:
              selector: role == 'api'
              ports:
              - 8080
          egress:
          - action: Allow
          types:
          - Ingress
          - Egress
        ```
        
        **BGP 구성 확인**:
        ```bash
        # calicoctl 설치
        curl -L https://github.com/projectcalico/calico/releases/download/v3.25.0/calicoctl-linux-amd64 -o calicoctl
        chmod +x calicoctl
        
        # BGP 피어 상태 확인
        calicoctl node status
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### 고급 네트워크 정책")
        st.markdown("""
        **Kubernetes NetworkPolicy**를 사용한 고급 네트워크 격리 구현 방법입니다.
    
        **마이크로서비스 계층화된 네트워크 정책**:
        ```yaml
        # frontend 마이크로서비스 정책
        apiVersion: networking.k8s.io/v1
        kind: NetworkPolicy
        metadata:
          name: frontend-policy
          namespace: microservices
        spec:
          podSelector:
            matchLabels:
              app: frontend
          policyTypes:
          - Ingress
          - Egress
          ingress:
          - from:
            - ipBlock:
                cidr: 0.0.0.0/0
                except:
                - 10.0.0.0/24  # 보호된 내부 네트워크 제외
            ports:
            - protocol: TCP
              port: 80
            - protocol: TCP
              port: 443
          egress:
          - to:
            - podSelector:
                matchLabels:
                  app: api-gateway
            ports:
            - protocol: TCP
              port: 8080
        ---
        # API 게이트웨이 정책
        apiVersion: networking.k8s.io/v1
        kind: NetworkPolicy
        metadata:
          name: api-gateway-policy
          namespace: microservices
        spec:
          podSelector:
            matchLabels:
              app: api-gateway
          policyTypes:
          - Ingress
          - Egress
          ingress:
          - from:
            - podSelector:
                matchLabels:
                  app: frontend
            ports:
            - protocol: TCP
              port: 8080
          egress:
          - to:
            - podSelector:
                matchLabels:
                  tier: backend
            ports:
            - protocol: TCP
              port: 8080
        ---
        # 백엔드 서비스 정책
        apiVersion: networking.k8s.io/v1
        kind: NetworkPolicy
        metadata:
          name: backend-policy
          namespace: microservices
        spec:
          podSelector:
            matchLabels:
              tier: backend
          policyTypes:
          - Ingress
          - Egress
          ingress:
          - from:
            - podSelector:
                matchLabels:
                  app: api-gateway
            ports:
            - protocol: TCP
              port: 8080
          egress:
          - to:
            - podSelector:
                matchLabels:
                  app: database
                  app: cache
            ports:
            - protocol: TCP
              port: 5432
            - protocol: TCP
              port: 6379
        ```
    
        **네임스페이스 간 통신 정책**:
        ```yaml
        # dev 네임스페이스에서만 test 네임스페이스로의 접근 허용
        apiVersion: networking.k8s.io/v1
        kind: NetworkPolicy
        metadata:
          name: allow-from-dev-to-test
          namespace: test
        spec:
          podSelector: {}  # 네임스페이스의 모든 Pod에 적용
          policyTypes:
          - Ingress
          ingress:
          - from:
            - namespaceSelector:
                matchLabels:
                  name: dev
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### 서비스 메시(Istio) 고급 설정")
        st.markdown("""
        **고급 트래픽 관리**:
        
        **가중치 기반 라우팅**:
        ```yaml
        apiVersion: networking.istio.io/v1alpha3
        kind: VirtualService
        metadata:
          name: reviews
        spec:
          hosts:
          - reviews
          http:
          - route:
            - destination:
                host: reviews
                subset: v1
              weight: 75
            - destination:
                host: reviews
                subset: v2
              weight: 25
        ```
        
        **조건부 라우팅**:
        ```yaml
        apiVersion: networking.istio.io/v1alpha3
        kind: VirtualService
        metadata:
          name: reviews
        spec:
          hosts:
          - reviews
          http:
          - match:
            - headers:
                end-user:
                  exact: alpha-tester
            route:
            - destination:
                host: reviews
                subset: v3
          - route:
            - destination:
                host: reviews
                subset: v1
        ```
        
        **장애 주입**:
        ```yaml
        apiVersion: networking.istio.io/v1alpha3
        kind: VirtualService
        metadata:
          name: ratings
        spec:
          hosts:
          - ratings
          http:
          - fault:
              delay:
                percentage:
                  value: 10.0
                fixedDelay: 7s
            route:
            - destination:
                host: ratings
                subset: v1
        ```
        
        **서킷 브레이커**:
        ```yaml
        apiVersion: networking.istio.io/v1alpha3
        kind: DestinationRule
        metadata:
          name: reviews
        spec:
          host: reviews
          trafficPolicy:
            outlierDetection:
              consecutive5xxErrors: 5
              interval: 30s
              baseEjectionTime: 60s
              maxEjectionPercent: 100
          subsets:
          - name: v1
            labels:
              version: v1
        ```
        
        **상호 TLS(mTLS) 엄격 모드**:
        ```yaml
        apiVersion: security.istio.io/v1beta1
        kind: PeerAuthentication
        metadata:
          name: default
          namespace: istio-system
        spec:
          mtls:
            mode: STRICT
        ```
        
        **세분화된 인증 정책**:
        ```yaml
        apiVersion: security.istio.io/v1beta1
        kind: AuthorizationPolicy
        metadata:
          name: httpbin
          namespace: foo
        spec:
          selector:
            matchLabels:
              app: httpbin
          rules:
          - from:
            - source:
                principals: ["cluster.local/ns/default/sa/sleep"]
            to:
            - operation:
                methods: ["GET"]
                paths: ["/info*"]
          - from:
            - source:
                namespaces: ["dev"]
            to:
            - operation:
                methods: ["POST"]
                paths: ["/data"]
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### 멀티클러스터 네트워킹")
        st.markdown("""
        **클러스터 간 통신** 설정을 통해 서로 다른 지역에 있는 Kubernetes 클러스터 간의 통신을 구성합니다.
        
        **Istio 멀티클러스터 설정**:
        ```bash
        # 프라이머리 클러스터 설정 (클러스터 1)
        istioctl install --set profile=minimal \\
          --set values.global.meshID=mesh1 \\
          --set values.global.multiCluster.clusterName=cluster1 \\
          --set values.global.network=network1
        
        # 리모트 클러스터 설정 (클러스터 2)
        istioctl install --set profile=minimal \\
          --set values.global.meshID=mesh1 \\
          --set values.global.multiCluster.clusterName=cluster2 \\
          --set values.global.network=network2
        ```
        
        **클러스터 간 서비스 디스커버리 활성화**:
        ```bash
        # 리모트 시크릿 생성 (클러스터 1에서)
        istioctl x create-remote-secret --name=cluster2 --context="\${CTX_CLUSTER2}" | \\
          kubectl apply -f - --context="\${CTX_CLUSTER1}"
        
        # 반대 방향 리모트 시크릿 생성 (클러스터 2에서)
        istioctl x create-remote-secret --name=cluster1 --context="\${CTX_CLUSTER1}" | \\
          kubectl apply -f - --context="\${CTX_CLUSTER2}"
        ```
        
        **멀티클러스터 서비스 메시 테스트**:
        ```bash
        # 클러스터 1에서 테스트 서비스 배포
        kubectl --context="\${CTX_CLUSTER1}" apply -f samples/helloworld/helloworld.yaml -l service=helloworld
        kubectl --context="\${CTX_CLUSTER1}" apply -f samples/helloworld/helloworld.yaml -l version=v1
        
        # 클러스터 2에서 테스트 서비스 배포
        kubectl --context="\${CTX_CLUSTER2}" apply -f samples/helloworld/helloworld.yaml -l service=helloworld
        kubectl --context="\${CTX_CLUSTER2}" apply -f samples/helloworld/helloworld.yaml -l version=v2
        
        # sleep 서비스로 테스트
        kubectl --context="\${CTX_CLUSTER1}" apply -f samples/sleep/sleep.yaml
        
        # 클러스터 2의 서비스를 클러스터 1에서 호출
        kubectl exec --context="\${CTX_CLUSTER1}" -n default -c sleep \\
          "\$(kubectl get pod --context="\${CTX_CLUSTER1}" -n default -l app=sleep -o jsonpath='{.items[0].metadata.name}')" \\
          -- curl -sS helloworld.default:5000/hello
        ```
        
        **멀티클러스터 인그레스 게이트웨이 설정**:
        ```yaml
        apiVersion: networking.istio.io/v1alpha3
        kind: Gateway
        metadata:
          name: cross-cluster-gateway
        spec:
          selector:
            istio: ingressgateway
          servers:
          - port:
              number: 80
              name: http
              protocol: HTTP
            hosts:
            - "*.global"
        ```
        """)
        
        # 다음 학습 추천 섹션 추가
        st.markdown("""
        <div class="next-learning">
            <h4>관련 학습 리소스</h4>
            <ul>
                <li>서비스 메시와 멀티클러스터 전략을 함께 적용하려면 <a href="/?page=advanced#multi_cluster">멀티클러스터 관리</a> 모듈을 살펴보세요.</li>
                <li>네트워크 보안을 강화하려면 <a href="/?page=advanced#security">보안 강화</a> 모듈을 함께 학습하세요.</li>
                <li>서비스 메시 기반 관찰성 향상에 대해서는 <a href="/?page=advanced#observability">고급 관찰성</a> 모듈을 참고하세요.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 보안 강화 탭
    with tabs[3]:
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        st.markdown("### Pod Security Standards")
        st.markdown("""
        **Pod Security Standards**는 Pod Security Policy(PSP)를 대체하는 Kubernetes의 보안 표준입니다.
    
        **세 가지 정책 수준**:
        1. **Privileged**: 제한 없음 - 모든 권한 허용
        2. **Baseline**: 알려진 권한 에스컬레이션 방지
        3. **Restricted**: 강화된 보안 강제
    
        **Pod Security Admission 설정 예시**:
        ```yaml
        apiVersion: apiserver.config.k8s.io/v1
        kind: AdmissionConfiguration
        plugins:
        - name: PodSecurity
          configuration:
            defaults:
              enforce: "baseline"
              enforce-version: "latest"
              audit: "restricted"
              audit-version: "latest"
              warn: "restricted"
              warn-version: "latest"
            exemptions:
              usernames: ["system:serviceaccount:kube-system:replicaset-controller"]
              namespaces: ["kube-system"]
        ```
    
        **네임스페이스 레벨에서 Pod Security Standards 적용**:
        ```bash
        kubectl label namespace default \\
          pod-security.kubernetes.io/enforce=baseline \\
          pod-security.kubernetes.io/audit=restricted \\
          pod-security.kubernetes.io/warn=restricted
        ```
        
        **강화된 보안 정책 적용**:
        ```yaml
        # 프로덕션 네임스페이스에 엄격한 보안 정책 적용
        apiVersion: v1
        kind: Namespace
        metadata:
          name: production
          labels:
            pod-security.kubernetes.io/enforce: restricted
            pod-security.kubernetes.io/enforce-version: latest
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### 이미지 스캐닝 및 Supply Chain 보안")
        st.markdown("""
        **Amazon ECR 이미지 스캐닝** 설정:
        ```bash
        # 저장소 생성 시 스캔 활성화
        aws ecr create-repository --repository-name my-repo --image-scanning-configuration scanOnPush=true
        
        # 기존 저장소에 스캔 활성화
        aws ecr put-image-scanning-configuration --repository-name my-repo --image-scanning-configuration scanOnPush=true
        ```
        
        **Trivy를 사용한 이미지 취약점 스캐닝**:
        ```bash
        # Trivy 설치
        brew install trivy
        
        # 이미지 스캔하기
        trivy image my-registry/my-app:latest
        ```
    
        **Supply Chain 보안 강화**:
        
        **Cosign을 사용한 이미지 서명과 검증**:
        ```bash
        # 키 생성
        cosign generate-key-pair
        
        # 이미지 서명
        cosign sign --key cosign.key my-registry/my-app:latest
        
        # 이미지 검증
        cosign verify --key cosign.pub my-registry/my-app:latest
        ```
        
        **SLSA 프레임워크 준수를 위한 체크리스트**:
        - 소스 코드 버전 관리 및 접근 제어
        - 빌드 과정 문서화 및 자동화
        - 빌드 프로비넌스 생성 및 검증
        - 이미지 서명과 검증
        - 배포 전 보안 게이트 구현
        
        **GitOps 파이프라인 보안 강화**:
        ```yaml
        # Flux에 Cosign 검증 추가
        apiVersion: image.toolkit.fluxcd.io/v1beta2
        kind: ImagePolicy
        metadata:
          name: secure-app
          namespace: flux-system
        spec:
          imageRepositoryRef:
            name: secure-app
          verify:
            provider: cosign
            secretRef:
              name: cosign-public-key
          policy:
            semver:
              range: '>=1.0.0'
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### 런타임 보안")
        st.markdown("""
        **Falco**: 컨테이너 런타임 보안 모니터링 도구
    
        **Falco 설치 및 구성**:
        ```bash
        # Helm으로 설치
        helm repo add falcosecurity https://falcosecurity.github.io/charts
        helm repo update
        
        helm install falco falcosecurity/falco \\
          --namespace falco \\
          --create-namespace
        ```
    
        **Falco 룰 설정**:
        ```yaml
        # Custom Falco rules
        customRules:
          rules-custom.yaml: |-
            - rule: Terminal shell in container
              desc: A shell was spawned by a non-shell program in a container
              condition: >
                container.id != host and
                proc.name = bash and
                container.image.repository != "bash" and
                not proc.pname in (bash, sh, docker)
              output: >
                Shell spawned in a container (user=%user.name container_id=%container.id
                container_name=%container.name shell=%proc.name parent=%proc.pname cmdline=%proc.cmdline)
              priority: WARNING
              tags: [container, shell]
        ```
    
        **SecurityContext 설정**:
        ```yaml
        apiVersion: v1
        kind: Pod
        metadata:
          name: secured-pod
        spec:
          securityContext:
            runAsUser: 1000
            runAsGroup: 3000
            fsGroup: 2000
          containers:
          - name: secure-app
            image: secure-app:latest
            securityContext:
              allowPrivilegeEscalation: false
              privileged: false
              readOnlyRootFilesystem: true
              runAsNonRoot: true
              capabilities:
                drop:
                - ALL
        ```
        
        **AppArmor 프로필 적용**:
        ```yaml
        apiVersion: v1
        kind: Pod
        metadata:
          name: apparmor-pod
          annotations:
            container.apparmor.security.beta.kubernetes.io/secure-app: localhost/k8s-apparmor-example-deny-write
        spec:
          containers:
          - name: secure-app
            image: secure-app:latest
        ```
        
        **Seccomp 프로필 적용**:
        ```yaml
        apiVersion: v1
        kind: Pod
        metadata:
          name: seccomp-pod
        spec:
          securityContext:
            seccompProfile:
              type: Localhost
              localhostProfile: profiles/audit.json
          containers:
          - name: secure-app
            image: secure-app:latest
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### Secret 관리 전략")
        st.markdown("""
        **HashiCorp Vault 통합**:
        
        **Vault 설치 및 설정**:
        ```bash
        # Helm으로 Vault 설치
        helm repo add hashicorp https://helm.releases.hashicorp.com
        helm install vault hashicorp/vault \\
          --namespace vault \\
          --create-namespace
        
        # Vault 초기화
        kubectl exec -n vault vault-0 -- vault operator init
        
        # Vault 봉인 해제
        kubectl exec -n vault vault-0 -- vault operator unseal <KEY_1>
        kubectl exec -n vault vault-0 -- vault operator unseal <KEY_2>
        kubectl exec -n vault vault-0 -- vault operator unseal <KEY_3>
        ```
        
        **Kubernetes 인증 설정**:
        ```bash
        # Vault에 로그인
        kubectl exec -it -n vault vault-0 -- /bin/sh
        vault login
        
        # Kubernetes 인증 활성화
        vault auth enable kubernetes
        
        # Kubernetes 인증 설정
        vault write auth/kubernetes/config \\
          kubernetes_host="https://\$KUBERNETES_SERVICE_HOST:\$KUBERNETES_SERVICE_PORT" \\
          token_reviewer_jwt="\$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" \\
          kubernetes_ca_cert=@/var/run/secrets/kubernetes.io/serviceaccount/ca.crt
        ```
        
        **애플리케이션 정책 생성**:
        ```bash
        # KV 시크릿 엔진 활성화
        vault secrets enable -path=secret kv-v2
        
        # 시크릿 저장
        vault kv put secret/myapp/config \\
          db.password="supersecret" \\
          api.key="key-12345"
        
        # 애플리케이션 정책 생성
        vault policy write myapp - <<EOF
        path "secret/data/myapp/*" {
          capabilities = ["read"]
        }
        EOF
        
        # Kubernetes 역할 생성
        vault write auth/kubernetes/role/myapp \\
          bound_service_account_names=myapp-sa \\
          bound_service_account_namespaces=default \\
          policies=myapp \\
          ttl=1h
        ```
        
        **Vault Agent Injector 활용**:
        ```yaml
        apiVersion: v1
        kind: Pod
        metadata:
          name: vault-agent-example
          annotations:
            vault.hashicorp.com/agent-inject: 'true'
            vault.hashicorp.com/agent-inject-secret-db-creds: 'secret/myapp/config'
            vault.hashicorp.com/agent-inject-template-db-creds: |
              {{- with secret "secret/myapp/config" -}}
              export DB_PASSWORD="{{ .Data.data.db.password }}"
              export API_KEY="{{ .Data.data.api.key }}"
              {{- end -}}
            vault.hashicorp.com/role: 'myapp'
        spec:
          serviceAccountName: myapp-sa
          containers:
          - name: app
            image: myapp:latest
            command: ["sh", "-c", "source /vault/secrets/db-creds && ./start.sh"]
        ```
        """)
        
        # 다음 학습 추천 섹션 추가
        st.markdown("""
        <div class="next-learning">
            <h4>관련 학습 리소스</h4>
            <ul>
                <li>보안을 위한 관찰성 향상 방법은 <a href="/?page=advanced#observability">고급 관찰성</a> 모듈을 참고하세요.</li>
                <li>안전한 멀티클러스터 환경 구성은 <a href="/?page=advanced#multi_cluster">멀티클러스터 관리</a> 모듈에서 배울 수 있습니다.</li>
                <li>재해 복구와 보안을 통합하는 방법은 <a href="/?page=advanced#disaster_recovery">재해 복구 및 백업</a> 모듈을 확인하세요.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
    # 멀티클러스터 관리 탭 (신규 추가)
    with tabs[4]:
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        st.markdown("### 멀티클러스터 아키텍처 설계")
        st.markdown("""
        **멀티클러스터 도입 이유**:
        - **고가용성**: 지리적 분산을 통한 재해 복구
        - **확장성**: 클러스터 당 한계 극복
        - **리소스 격리**: 테넌트 간, 환경 간 격리
        - **지역 최적화**: 사용자와 가까운 곳에서 서비스 제공
        - **규제 준수**: 데이터 레지던시 요구사항 충족
        
        **멀티클러스터 패턴**:
        
        **1. 지역 기반 분산 (Region-Based)**
        ```
        ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
        │  EKS Cluster A  │  │  EKS Cluster B  │  │  EKS Cluster C  │
        │   (us-east-1)   │  │   (eu-west-1)   │  │  (ap-south-1)   │
        └─────────────────┘  └─────────────────┘  └─────────────────┘
                   │                 │                  │
                   └──────────┬──────┴──────────┐
                              ▼                 ▼
                      ┌───────────────┐  ┌───────────────┐
                      │Global Database│  │  Global DNS   │
                      └───────────────┘  └───────────────┘
        ```
        
        **2. 환경 기반 분리 (Environment-Based)**
        ```
        ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
        │   Production    │  │    Staging      │  │   Development   │
        │  EKS Cluster    │  │  EKS Cluster    │  │  EKS Cluster    │
        └─────────────────┘  └─────────────────┘  └─────────────────┘
                    │                │                 │
                    └────────────────┼─────────────────┘
                                     ▼
                             ┌──────────────┐
                             │   CI/CD      │
                             │  Pipeline    │
                             └──────────────┘
        ```
        
        **3. 워크로드 기반 분리 (Workload-Based)**
        ```
        ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
        │  ML Workloads   │  │ User Services   │  │ Data Processing │
        │  EKS Cluster    │  │  EKS Cluster    │  │  EKS Cluster    │
        └─────────────────┘  └─────────────────┘  └─────────────────┘
                    │                │                 │
                    └────────────────┼─────────────────┘
                                     ▼
                             ┌──────────────┐
                             │ Shared       │
                             │ Services     │
                             └──────────────┘
        ```
        
        **4. 소유권 기반 분리 (Ownership-Based)**
        ```
        ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
        │  Team Alpha's   │  │  Team Beta's    │  │  Team Gamma's   │
        │  EKS Cluster    │  │  EKS Cluster    │  │  EKS Cluster    │
        └─────────────────┘  └─────────────────┘  └─────────────────┘
                    │                │                 │
                    └────────────────┼─────────────────┘
                                     ▼
                             ┌──────────────┐
                             │  Platform    │
                             │  Services    │
                             └──────────────┘
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### 클러스터간 연결 및 통신")
        st.markdown("""
        **VPC 피어링**을 통한 클러스터 간 직접 통신 설정:
        ```bash
        # 피어링 연결 생성 (AWS CLI)
        aws ec2 create-vpc-peering-connection \\
          --vpc-id vpc-1234abcd \\  # 클러스터 A의 VPC
          --peer-vpc-id vpc-5678efgh  # 클러스터 B의 VPC
        
        # 피어링 연결 수락
        aws ec2 accept-vpc-peering-connection \\
          --vpc-peering-connection-id pcx-1234567890abcdef0
        
        # 라우팅 테이블 업데이트 (클러스터 A → 클러스터 B)
        aws ec2 create-route \\
          --route-table-id rtb-12345678 \\
          --destination-cidr-block 10.1.0.0/16 \\
          --vpc-peering-connection-id pcx-1234567890abcdef0
        
        # 라우팅 테이블 업데이트 (클러스터 B → 클러스터 A)
        aws ec2 create-route \\
          --route-table-id rtb-87654321 \\
          --destination-cidr-block 10.0.0.0/16 \\
          --vpc-peering-connection-id pcx-1234567890abcdef0
        ```
        
        **AWS Transit Gateway**를 통한 중앙 집중식 라우팅:
        ```bash
        # Transit Gateway 생성
        aws ec2 create-transit-gateway \\
          --description "EKS Multi-Cluster Transit Gateway"
        
        # VPC 연결
        aws ec2 create-transit-gateway-vpc-attachment \\
          --transit-gateway-id tgw-1234567890abcdef0 \\
          --vpc-id vpc-1234abcd \\
          --subnet-ids subnet-123abc subnet-456def
        
        # 추가 VPC 연결
        aws ec2 create-transit-gateway-vpc-attachment \\
          --transit-gateway-id tgw-1234567890abcdef0 \\
          --vpc-id vpc-5678efgh \\
          --subnet-ids subnet-789ghi subnet-012jkl
        ```
        
        **클러스터 DNS 통합**:
        ```yaml
        apiVersion: v1
        kind: Service
        metadata:
          name: external-service
          namespace: default
          annotations:
            external-dns.alpha.kubernetes.io/hostname: api.example.com
        spec:
          type: ExternalName
          externalName: api-service.cluster2.svc.cluster.local
          ports:
          - port: 80
        ```
        
        **Multi-Cluster Service**:
        ```yaml
        apiVersion: multicluster.x-k8s.io/v1alpha1
        kind: ServiceExport
        metadata:
          name: api-service
          namespace: default
        ---
        apiVersion: multicluster.x-k8s.io/v1alpha1
        kind: ServiceImport
        metadata:
          name: api-service
          namespace: default
        spec:
          type: ClusterSetIP
          ports:
          - port: 80
            protocol: TCP
          ips:
          - 10.0.1.15  # Service CIDR in source cluster
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### 중앙 집중식 관리 도구")
        st.markdown("""
        **Rancher**를 사용한 여러 EKS 클러스터 관리:
        ```bash
        # Rancher 설치
        helm repo add rancher-stable https://releases.rancher.com/server-charts/stable
        
        helm install rancher rancher-stable/rancher \\
          --namespace cattle-system \\
          --create-namespace \\
          --set hostname=rancher.my-domain.com \\
          --set replicas=3
        
        # EKS 클러스터 가져오기 (Rancher UI에서 또는 CLI로)
        rancher clusters import --kubeconfig=cluster1.yaml
        ```
        
        **Argo CD를 통한 멀티클러스터 GitOps**:
        ```yaml
        # ApplicationSet을 사용하여 여러 클러스터에 동일한 애플리케이션 배포
        apiVersion: argoproj.io/v1alpha1
        kind: ApplicationSet
        metadata:
          name: guestbook
          namespace: argocd
        spec:
          generators:
          - clusters: {}  # 등록된 모든 클러스터 대상
          template:
            metadata:
              name: '{{name}}-guestbook'  # 클러스터 이름으로 생성
            spec:
              project: default
              source:
                repoURL: https://github.com/argoproj/argocd-example-apps.git
                targetRevision: HEAD
                path: guestbook
              destination:
                server: '{{server}}'  # 클러스터 API 서버
                namespace: guestbook
              syncPolicy:
                automated:
                  prune: true
                  selfHeal: true
        ```
        
        **Crossplane**을 통한 리소스 프로비저닝:
        ```yaml
        # Crossplane Provider 설정
        apiVersion: pkg.crossplane.io/v1
        kind: Provider
        metadata:
          name: provider-aws
        spec:
          package: "crossplane/provider-aws:v0.24.1"
          controllerConfigRef:
            name: aws-config
        ---
        # EKS 클러스터 프로비저닝 정의
        apiVersion: eks.aws.crossplane.io/v1beta1
        kind: Cluster
        metadata:
          name: sample-eks-cluster
        spec:
          forProvider:
            region: us-west-2
            version: "1.22"
            roleArn: arn:aws:iam::123456789:role/eksClusterRole
            resourcesVpcConfig:
              subnetIds:
                - subnet-01234567890abcdef
                - subnet-0987654321fedcba
              endpointPrivateAccess: true
              endpointPublicAccess: true
          writeConnectionSecretToRef:
            name: eks-cluster-conn
            namespace: crossplane-system
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### 워크로드 페더레이션과 마이그레이션")
        st.markdown("""
        **KubeFed (Kubernetes Cluster Federation)**을 사용한 워크로드 페더레이션:
        ```bash
        # KubeFed 설치
        helm repo add kubefed-charts https://raw.githubusercontent.com/kubernetes-sigs/kubefed/master/charts
        helm repo update
        
        helm install kubefed kubefed-charts/kubefed \\
          --namespace kube-federation-system \\
          --create-namespace \\
          --version=0.8.1
        ```
        
        **FederatedDeployment 예제**:
        ```yaml
        apiVersion: types.kubefed.io/v1beta1
        kind: FederatedDeployment
        metadata:
          name: test-deployment
          namespace: test-namespace
        spec:
          template:
            metadata:
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
                  - image: nginx
                    name: nginx
          placement:
            clusters:
            - name: cluster1
            - name: cluster2
            - name: cluster3
          overrides:
          - clusterName: cluster2
            clusterOverrides:
            - path: "/spec/replicas"
              value: 5
          - clusterName: cluster3
            clusterOverrides:
            - path: "/spec/template/spec/containers/0/image"
              value: "nginx:alpine"
        ```
        
        **Velero**를 사용한 워크로드 마이그레이션:
        ```bash
        # Velero 설치 (소스 클러스터)
        velero install \\
          --provider aws \\
          --plugins velero/velero-plugin-for-aws:v1.2.0 \\
          --bucket velero-backup \\
          --backup-location-config region=us-west-2 \\
          --snapshot-location-config region=us-west-2 \\
          --secret-file ./credentials-velero
        
        # 애플리케이션 백업
        velero backup create app-backup --include-namespaces app1,app2
        
        # Velero 설치 (대상 클러스터)
        velero install \\
          --provider aws \\
          --plugins velero/velero-plugin-for-aws:v1.2.0 \\
          --bucket velero-backup \\
          --backup-location-config region=us-west-2 \\
          --snapshot-location-config region=us-west-2 \\
          --secret-file ./credentials-velero
        
        # 애플리케이션 복원
        velero restore create --from-backup app-backup
        ```
        """)
        
        # 다음 학습 추천 섹션 추가
        st.markdown("""
        <div class="next-learning">
            <h4>관련 학습 리소스</h4>
            <ul>
                <li>멀티클러스터 환경의 보안을 강화하려면 <a href="/?page=advanced#security">보안 강화</a> 모듈을 참고하세요.</li>
                <li>멀티클러스터 환경의 관찰성을 확보하려면 <a href="/?page=advanced#observability">고급 관찰성</a> 모듈을 확인하세요.</li>
                <li>멀티클러스터 재해 복구에 대해서는 <a href="/?page=advanced#disaster_recovery">재해 복구 및 백업</a> 모듈을 참조하세요.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 재해 복구 및 백업 탭 (신규 추가)
    with tabs[5]:
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        st.markdown("### EKS 백업 솔루션")
        st.markdown("""
        **Velero**는 Kubernetes 클러스터 자원과 영구 볼륨 데이터를 백업 및 복원하는 오픈소스 도구입니다.
        
        **Velero 설치 및 설정**:
        ```bash
        # AWS IAM 정책 생성
        cat > velero-policy.json << EOF
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "ec2:DescribeVolumes",
                        "ec2:DescribeSnapshots",
                        "ec2:CreateTags",
                        "ec2:CreateVolume",
                        "ec2:CreateSnapshot",
                        "ec2:DeleteSnapshot"
                    ],
                    "Resource": "*"
                },
                {
                    "Effect": "Allow",
                    "Action": [
                        "s3:GetObject",
                        "s3:DeleteObject",
                        "s3:PutObject",
                        "s3:AbortMultipartUpload",
                        "s3:ListMultipartUploadParts"
                    ],
                    "Resource": [
                        "arn:aws:s3:::velero-bucket/*"
                    ]
                },
                {
                    "Effect": "Allow",
                    "Action": [
                        "s3:ListBucket"
                    ],
                    "Resource": [
                        "arn:aws:s3:::velero-bucket"
                    ]
                }
            ]
        }
        EOF
        
        aws iam create-policy \\
          --policy-name VeleroAccessPolicy \\
          --policy-document file://velero-policy.json
        
        # AWS 자격 증명 파일 생성
        cat > credentials-velero << EOF
        [default]
        aws_access_key_id=<AWS_ACCESS_KEY_ID>
        aws_secret_access_key=<AWS_SECRET_ACCESS_KEY>
        EOF
        
        # Velero CLI 설치
        brew install velero
        
        # Velero 설치 (AWS S3 백업 저장소 사용)
        velero install \\
          --provider aws \\
          --plugins velero/velero-plugin-for-aws:v1.3.0 \\
          --bucket velero-eks-backup \\
          --backup-location-config region=us-west-2,s3ForcePathStyle="true" \\
          --snapshot-location-config region=us-west-2 \\
          --secret-file ./credentials-velero
        ```
        
        **Velero 백업 및 복원 작업**:
        ```bash
        # 네임스페이스 백업
        velero backup create app-namespace-backup --include-namespaces app
        
        # 특정 리소스 백업
        velero backup create app-config-backup \\
          --include-resources configmaps,secrets \\
          --selector app=myapp
        
        # 예약 백업 생성
        velero schedule create daily-backup \\
          --schedule="0 1 * * *" \\
          --include-namespaces app,frontend,backend
        
        # 백업 상태 확인
        velero backup describe app-namespace-backup
        
        # 백업에서 복원
        velero restore create --from-backup app-namespace-backup
        
        # 다른 네임스페이스로 복원
        velero restore create --from-backup app-namespace-backup \\
          --namespace-mappings app:app-restore
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### 다중 리전 DR 설계")
        st.markdown("""
        **다중 리전 재해 복구(DR) 전략**을 위한 여러 접근법을 살펴봅니다.
        
        **DR 전략 유형**:
        
        **1. Cold Standby (Backup & Restore)**
        - 가장 저렴한 DR 전략
        - RPO(Recovery Point Objective): 수 시간에서 하루
        - RTO(Recovery Time Objective): 수 시간
        - Velero를 사용하여 주기적으로 백업 수행
        - 백업으로부터 DR 리전의 새 클러스터에 복원
        
        ```bash
        # 재해 복구 프로세스 (Cold Standby)
        
        # 1. DR 리전에 새 EKS 클러스터 생성
        eksctl create cluster \\
          --name eks-dr-cluster \\
          --region us-east-1 \\
          --version 1.23 \\
          --nodegroup-name standard-nodes \\
          --node-type m5.xlarge \\
          --nodes 3 \\
          --nodes-min 3 \\
          --nodes-max 5
        
        # 2. DR 클러스터에 Velero 설치
        velero install \\
          --provider aws \\
          --plugins velero/velero-plugin-for-aws:v1.3.0 \\
          --bucket velero-eks-backup \\
          --backup-location-config region=us-west-2 \\
          --snapshot-location-config region=us-west-2 \\
          --secret-file ./credentials-velero
        
        # 3. 최신 백업에서 애플리케이션 복원
        velero restore create --from-backup latest-backup
        ```
        
        **2. Warm Standby (Pilot Light)**
        - DR 리전에 최소한의 인프라를 계속 실행
        - RPO: 수 분에서 수 시간
        - RTO: 수 분에서 수 시간
        - 핵심 데이터의 비동기적 복제
        - 리소스 요구사항이 적은 대기 클러스터 유지
        
        ```bash
        # 파일럿 라이트 접근 방식
        
        # 1. DR 리전에 작은 크기의 클러스터 유지
        eksctl create cluster \\
          --name eks-dr-cluster \\
          --region us-east-1 \\
          --version 1.23 \\
          --nodegroup-name minimal-nodes \\
          --node-type t3.medium \\
          --nodes 2 \\
          --nodes-min 2 \\
          --nodes-max 5
        
        # 2. 핵심 구성요소만 배포 (DB 복제 및 데이터 동기화 설정 포함)
        helm install core-infrastructure ./core-infra-chart
        
        # 3. 재해 발생 시:
        # - 노드 그룹 확장
        eksctl scale nodegroup --cluster=eks-dr-cluster --nodes=5 --name=minimal-nodes
        
        # - 모든 애플리케이션 구성요소 배포
        helm install full-app ./full-app-chart
        
        # - 트래픽 전환 (Route 53 또는 기타 DNS 서비스 사용)
        aws route53 change-resource-record-sets --hosted-zone-id Z123456 --change-batch file://failover.json
        ```
        
        **3. Hot Standby**
        - 완전한 환경이 항상 실행 중
        - RPO: 거의 0 또는 수 분
        - RTO: 수 분 이내
        - 두 리전 모두에서 동일한 애플리케이션 실행
        - 데이터 동기화 유지
        - 즉시 장애 조치 가능
        
        ```bash
        # Global Accelerator를 사용한 다중 리전 부하 분산
        aws globalaccelerator create-accelerator \\
          --name eks-ha-accelerator \\
          --ip-address-type IPV4 \\
          --enabled
        
        aws globalaccelerator create-listener \\
          --accelerator-arn arn:aws:globalaccelerator::ACCOUNT_ID:accelerator/ACCELERATOR_ID \\
          --protocol TCP \\
          --port-ranges FromPort=80,ToPort=80
        
        aws globalaccelerator create-endpoint-group \\
          --listener-arn arn:aws:globalaccelerator::ACCOUNT_ID:accelerator/ACCELERATOR_ID/listener/LISTENER_ID \\
          --endpoint-group-region us-west-2 \\
          --traffic-dial-percentage 60
        
        aws globalaccelerator create-endpoint-group \\
          --listener-arn arn:aws:globalaccelerator::ACCOUNT_ID:accelerator/ACCELERATOR_ID/listener/LISTENER_ID \\
          --endpoint-group-region us-east-1 \\
          --traffic-dial-percentage 40
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### 고가용성 아키텍처 설계")
        st.markdown("""
        **다중 가용 영역(AZ) 아키텍처** - 단일 리전 내에서 고가용성 보장
        
        **EKS 클러스터의 HA 설정**:
        ```bash
        # 다중 AZ 노드 그룹 생성
        eksctl create nodegroup \\
          --cluster my-eks-cluster \\
          --name multi-az-nodes \\
          --nodes 3 \\
          --nodes-min 3 \\
          --nodes-max 9 \\
          --node-type m5.large \\
          --node-ami auto \\
          --node-labels "failure-domain=distributed" \\
          --asg-access \\
          --zones us-west-2a,us-west-2b,us-west-2c
        ```
        
        **Pod 분산 설정**:
        ```yaml
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: ha-app
        spec:
          replicas: 6  # 여러 AZ에 걸쳐 분산
          selector:
            matchLabels:
              app: ha-app
          template:
            metadata:
              labels:
                app: ha-app
            spec:
              topologySpreadConstraints:
              - maxSkew: 1  # AZ 당 차이의 최대값
                topologyKey: topology.kubernetes.io/zone  # AZ를 기준으로 분산
                whenUnsatisfiable: ScheduleAnyway  # 제약 조건을 만족할 수 없을 때도 스케줄링
                labelSelector:
                  matchLabels:
                    app: ha-app
              # 노드 안티-어피니티로 동일 노드 회피
              affinity:
                podAntiAffinity:
                  preferredDuringSchedulingIgnoredDuringExecution:
                  - weight: 100
                    podAffinityTerm:
                      labelSelector:
                        matchExpressions:
                        - key: app
                          operator: In
                          values:
                          - ha-app
                      topologyKey: kubernetes.io/hostname
              containers:
              - name: ha-app
                image: ha-app:latest
                resources:
                  limits:
                    memory: "128Mi"
                    cpu: "500m"
        ```
        
        **AWS Load Balancer Controller를 통한 연결성 보장**:
        ```yaml
        apiVersion: v1
        kind: Service
        metadata:
          name: ha-app-service
          annotations:
            service.beta.kubernetes.io/aws-load-balancer-type: nlb
            service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"
        spec:
          type: LoadBalancer
          selector:
            app: ha-app
          ports:
          - port: 80
            targetPort: 8080
        ```
        
        **고가용성 StatefulSet 구성**:
        ```yaml
        apiVersion: apps/v1
        kind: StatefulSet
        metadata:
          name: ha-database
        spec:
          serviceName: "ha-database"
          replicas: 3
          selector:
            matchLabels:
              app: ha-database
          template:
            metadata:
              labels:
                app: ha-database
            spec:
              topologySpreadConstraints:
              - maxSkew: 1
                topologyKey: topology.kubernetes.io/zone
                whenUnsatisfiable: DoNotSchedule
                labelSelector:
                  matchLabels:
                    app: ha-database
              containers:
              - name: database
                image: mongo:4.4
                ports:
                - containerPort: 27017
                  name: db-port
                volumeMounts:
                - name: data
                  mountPath: /data/db
          volumeClaimTemplates:
          - metadata:
              name: data
            spec:
              accessModes: [ "ReadWriteOnce" ]
              storageClassName: "gp2-az-spread"
              resources:
                requests:
                  storage: 10Gi
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### 백업 및 복구 자동화")
        st.markdown("""
        **GitOps 기반 백업 구성 및 자동화**:
        
        **1. Velero CRD 기반 백업 관리**:
        ```yaml
        # 예약 백업 정의
        apiVersion: velero.io/v1
        kind: Schedule
        metadata:
          name: daily-cluster-backup
          namespace: velero
        spec:
          schedule: "0 1 * * *"  # 매일 01:00에 실행
          template:
            includedNamespaces:
            - "*"
            excludedNamespaces:
            - kube-system
            - velero
            includeClusterResources: true
            storageLocation: default
            ttl: 720h  # 30일 보관
        ```
        
        **2. AWS 기반 백업 검증 및 테스트**:
        ```yaml
        apiVersion: batch/v1
        kind: CronJob
        metadata:
          name: backup-validation
          namespace: velero
        spec:
          schedule: "0 3 * * *"  # 매일 03:00에 실행
          jobTemplate:
            spec:
              template:
                spec:
                  containers:
                  - name: velero-cli
                    image: velero/velero:v1.8.0
                    command:
                    - /bin/sh
                    - -c
                    - |
                      # 최근 백업 검증
                      LATEST_BACKUP=\$(velero backup get --output json | jq -r '.items[0].metadata.name')
                      echo "Validating backup: \$LATEST_BACKUP"
                      
                      # 테스트 복원 (별도 네임스페이스에)
                      velero restore create --from-backup \$LATEST_BACKUP \
                        --namespace-mappings default:backup-test \
                        --include-resources deployments,services \
                        --selector app=critical-app \
                        --wait
                      
                      # 복원 검증
                      if kubectl get -n backup-test deployment critical-app; then
                        echo "Backup validation successful!"
                        # 알림 전송 (Slack, SNS 등)
                      else
                        echo "Backup validation failed!"
                        # 실패 알림 전송
                      fi
                      
                      # 테스트 네임스페이스 정리
                      kubectl delete namespace backup-test
                    volumeMounts:
                    - name: cloud-credentials
                      mountPath: /credentials
                    env:
                    - name: KUBECONFIG
                      value: /root/.kube/config
                    - name: CLOUD_CREDENTIALS_FILE
                      value: /credentials/cloud
                  volumes:
                  - name: cloud-credentials
                    secret:
                      secretName: velero-credentials
                  restartPolicy: OnFailure
                  serviceAccountName: velero
        ```
        
        **3. 재해 복구 훈련 자동화**:
        ```bash
        #!/bin/bash
        # dr-drill.sh - DR 훈련 스크립트
        
        # 1. 임시 DR 클러스터 생성
        echo "Creating temporary DR cluster..."
        eksctl create cluster \\
          --name eks-dr-drill-\$(date +%Y%m%d) \\
          --region us-east-1 \\
          --version 1.23 \\
          --nodegroup-name drill-nodes \\
          --node-type m5.large \\
          --nodes 3 \\
          --auto-kubeconfig
        
        # 2. Velero 설치 및 백업 스토어 연결
        echo "Installing Velero on DR cluster..."
        velero install \\
          --provider aws \\
          --plugins velero/velero-plugin-for-aws:v1.3.0 \\
          --bucket velero-eks-backup \\
          --backup-location-config region=us-west-2 \\
          --snapshot-location-config region=us-west-2 \\
          --secret-file ./credentials-velero
        
        # 3. 최신 백업에서 복원
        echo "Restoring from latest backup..."
        LATEST_BACKUP=\$(velero backup get --output json | jq -r '.items[0].metadata.name')
        velero restore create --from-backup \$LATEST_BACKUP
        
        # 4. 복원 검증
        echo "Validating restoration..."
        kubectl get pods --all-namespaces
        kubectl get deployments --all-namespaces
        
        # 5. 애플리케이션 테스트
        echo "Running application tests..."
        ./run-app-tests.sh
        
        # 6. 결과 보고
        echo "Generating DR drill report..."
        ./generate-dr-report.sh
        
        # 7. 정리
        echo "Cleaning up temporary DR cluster..."
        eksctl delete cluster --name eks-dr-drill-\$(date +%Y%m%d) --region us-east-1
        ```
        """)
        
        # 다음 학습 추천 섹션 추가
        st.markdown("""
        <div class="next-learning">
            <h4>관련 학습 리소스</h4>
            <ul>
                <li>재해 복구를 위한 멀티클러스터 설계는 <a href="/?page=advanced#multi_cluster">멀티클러스터 관리</a> 모듈을 참고하세요.</li>
                <li>백업 및 복구 작업의 모니터링 방법은 <a href="/?page=advanced#observability">고급 관찰성</a> 모듈을 확인하세요.</li>
                <li>DR 전략과 함께 비용 최적화를 고려하려면 <a href="/?page=advanced#cost_optimization">비용 최적화 전략</a> 모듈이 도움이 됩니다.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 고급 관찰성 탭
    with tabs[6]:
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        st.markdown("### 분산 트레이싱")
        st.markdown("""
        **분산 트레이싱**은 마이크로서비스 환경에서 요청의 전체 경로를 추적하는 기술입니다.
    
        **Jaeger를 이용한 분산 트레이싱**:
        ```bash
        # Jaeger All-in-One 설치
        kubectl apply -f https://github.com/jaegertracing/jaeger-operator/releases/download/v1.35.0/jaeger-operator.yaml
        
        # Jaeger 인스턴스 생성
        cat <<EOF | kubectl apply -f -
        apiVersion: jaegertracing.io/v1
        kind: Jaeger
        metadata:
          name: my-jaeger
        spec:
          strategy: production
          storage:
            type: elasticsearch
            elasticsearch:
              nodeCount: 3
              redundancyPolicy: ZeroRedundancy
              resources:
                requests:
                  cpu: 1
                  memory: 2Gi
                limits:
                  memory: 2Gi
          ingress:
            enabled: true
            hosts:
              - jaeger.example.com
        EOF
        ```
    
        **애플리케이션에 Jaeger 통합 (Java 예시)**:
        ```java
        // Maven 의존성 추가
        // <dependency>
        //   <groupId>io.opentracing.contrib</groupId>
        //   <artifactId>opentracing-spring-jaeger-web-starter</artifactId>
        //   <version>3.3.1</version>
        // </dependency>
    
        // application.properties 구성
        opentracing.jaeger.service-name=order-service
        opentracing.jaeger.udp-sender.host=jaeger-agent.observability
        opentracing.jaeger.udp-sender.port=6831
        opentracing.jaeger.sampler-type=const
        opentracing.jaeger.sampler-param=1
    
        // 스프링 컨트롤러에서 트레이싱 사용
        @RestController
        public class OrderController {
          
          private final Tracer tracer;
          private final OrderService orderService;
          
          public OrderController(Tracer tracer, OrderService orderService) {
            this.tracer = tracer;
            this.orderService = orderService;
          }
          
          @GetMapping("/orders/{id}")
          public Order getOrder(@PathVariable Long id) {
            Span span = tracer.buildSpan("get-order-details").start();
            try (Scope scope = tracer.activateSpan(span)) {
              span.setTag("order.id", id);
              Order order = orderService.getOrderById(id);
              span.setTag("order.status", order.getStatus());
              return order;
            } finally {
              span.finish();
            }
          }
        }
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### EFK 스택 구성")
        st.markdown("""
        **EFK 스택(Elasticsearch, Fluent Bit, Kibana)**은 로그 수집, 저장, 시각화를 위한 통합 솔루션입니다.
    
        **Elasticsearch와 Kibana 설치 (ECK 이용)**:
        ```bash
        # ECK 오퍼레이터 설치
        kubectl apply -f https://download.elastic.co/downloads/eck/2.5.0/crds.yaml
        kubectl apply -f https://download.elastic.co/downloads/eck/2.5.0/operator.yaml
        
        # Elasticsearch 클러스터 생성
        cat <<EOF | kubectl apply -f -
        apiVersion: elasticsearch.k8s.elastic.co/v1
        kind: Elasticsearch
        metadata:
          name: logging
          namespace: observability
        spec:
          version: 8.5.1
          nodeSets:
          - name: default
            count: 3
            config:
              node.store.allow_mmap: false
              node.roles: ["master", "data"]
              xpack.security.authc.anonymous.roles: monitoring_user
            podTemplate:
              spec:
                containers:
                - name: elasticsearch
                  resources:
                    limits:
                      memory: 4Gi
                    requests:
                      cpu: 1
                      memory: 2Gi
        EOF
        
        # Kibana 인스턴스 생성
        cat <<EOF | kubectl apply -f -
        apiVersion: kibana.k8s.elastic.co/v1
        kind: Kibana
        metadata:
          name: logging
          namespace: observability
        spec:
          version: 8.5.1
          count: 1
          elasticsearchRef:
            name: logging
        EOF
        ```
    
        **고급 Fluent Bit 설정 및 파싱 규칙**:
        ```yaml
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: fluent-bit-config
          namespace: observability
        data:
          fluent-bit.conf: |
            [SERVICE]
                Flush               5
                Daemon              off
                Log_Level           info
                Parsers_File        parsers.conf
                HTTP_Server         On
                HTTP_Listen         0.0.0.0
                HTTP_Port           2020
            
            # 여러 입력 소스 구성
            [INPUT]
                Name                tail
                Tag                 kube.*
                Path                /var/log/containers/*_app_*.log
                Parser              docker
                DB                  /var/log/flb_app.db
                Mem_Buf_Limit       5MB
                Skip_Long_Lines     On
                Refresh_Interval    10
                
            [INPUT]
                Name                tail
                Tag                 kube.system.*
                Path                /var/log/containers/*_kube-system_*.log
                Parser              docker
                DB                  /var/log/flb_system.db
                Mem_Buf_Limit       5MB
            
            # Kubernetes 메타데이터 추가
            [FILTER]
                Name                kubernetes
                Match               kube.*
                Merge_Log           On
                Keep_Log            Off
                K8S-Logging.Parser  On
                K8S-Logging.Exclude Off
            
            # JSON 로그 파싱
            [FILTER]
                Name                parser
                Match               kube.app.*
                Key_Name            log
                Parser              json
                Reserve_Data        On
            
            # 특정 필드에 따른 로그 필터링
            [FILTER]
                Name                grep
                Match               kube.app.*
                Regex               level INFO|WARN|ERROR|FATAL
            
            # Elasticsearch 출력 설정 
            [OUTPUT]
                Name                es
                Match               kube.*
                Host                logging-es-http
                Port                9200
                Index               kubernetes_%Y.%m.%d
                Suppress_Type_Name  On
                HTTP_User           elastic
                HTTP_Passwd         \${ELASTICSEARCH_PASSWORD}
                tls                 On
                tls.verify          Off
                Logstash_Format     On
                Retry_Limit         False
                
          parsers.conf: |
            [PARSER]
                Name                docker
                Format              json
                Time_Key            time
                Time_Format         %Y-%m-%dT%H:%M:%S.%L
                Time_Keep           On
            
            # JSON 로그 파서
            [PARSER]
                Name                json
                Format              json
                Time_Key            timestamp
                Time_Format         %Y-%m-%dT%H:%M:%S.%LZ
                Time_Keep           On
                
            # 멀티라인 로그 파서 (자바 스택 트레이스)
            [PARSER]
                Name                java_multiline
                Format              regex
                Regex               ^(?<time>[^ ]* {1,2}[^ ]*) (?<level>[A-Z]+) (?<message>.*(?:\n.*)*)
                Time_Key            time
                Time_Format         %Y-%m-%d %H:%M:%S,%L
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### 사용자 정의 메트릭")
        st.markdown("""
        **Prometheus와 함께 사용자 정의 메트릭**을 설정하고 활용하는 방법입니다.
    
        **서비스 모니터 설정**:
        ```yaml
        apiVersion: monitoring.coreos.com/v1
        kind: ServiceMonitor
        metadata:
          name: custom-app-monitor
          namespace: monitoring
          labels:
            app: custom-app
            release: prometheus
        spec:
          selector:
            matchLabels:
              app: custom-app
          endpoints:
          - port: metrics
            interval: 15s
            path: /metrics
          namespaceSelector:
            matchNames:
            - default
            - app
        ```
    
        **PrometheusRule을 통한 알림 규칙 정의**:
        ```yaml
        apiVersion: monitoring.coreos.com/v1
        kind: PrometheusRule
        metadata:
          name: custom-app-alerts
          namespace: monitoring
          labels:
            app: custom-app
            release: prometheus
        spec:
          groups:
          - name: custom-app.rules
            rules:
            - alert: CustomAppHighErrorRate
              expr: |
                sum(rate(custom_app_http_requests_total{status=~"5.."}[5m])) by (service, namespace)
                  /
                sum(rate(custom_app_http_requests_total[5m])) by (service, namespace)
                  > 0.05
              for: 5m
              labels:
                severity: critical
                team: backend
              annotations:
                summary: "High HTTP error rate on {{ \$labels.service }}"
                description: "{{ \$labels.service }} in {{ \$labels.namespace }} namespace has error rate above 5% (current value: {{ \$value | printf \"%.2f%%\" }})"
                runbook_url: "https://wiki.example.com/alerts/high-error-rate"
            - alert: CustomAppHighLatency
              expr: |
                histogram_quantile(0.95, sum(rate(custom_app_request_duration_seconds_bucket[5m])) by (le, service, namespace))
                  > 0.5
              for: 10m
              labels:
                severity: warning
                team: backend
              annotations:
                summary: "High latency on {{ \$labels.service }}"
                description: "{{ \$labels.service }} in {{ \$labels.namespace }} namespace has 95th percentile latency above 500ms (current value: {{ \$value | printf \"%.2fs\" }})"
                dashboard_url: "https://grafana.example.com/d/custom-app/custom-app-dashboard?var-service={{ \$labels.service }}"
        ```
    
        **Java/Spring 애플리케이션 사용자 정의 메트릭 추가**:
        ```java
        // Maven 의존성
        // <dependency>
        //   <groupId>io.micrometer</groupId>
        //   <artifactId>micrometer-registry-prometheus</artifactId>
        // </dependency>
        
        @Service
        public class OrderServiceImpl implements OrderService {
            
            private final MeterRegistry meterRegistry;
            private final Counter orderCounter;
            private final DistributionSummary orderSizeHistogram;
            private final Timer orderProcessingTimer;
            
            public OrderServiceImpl(MeterRegistry meterRegistry) {
                this.meterRegistry = meterRegistry;
                
                // 주문 횟수 카운터
                this.orderCounter = Counter.builder("orders.created")
                    .description("Total number of orders created")
                    .tag("region", "us-west")
                    .register(meterRegistry);
                
                // 주문 크기 히스토그램
                this.orderSizeHistogram = DistributionSummary.builder("orders.size")
                    .description("Distribution of order sizes")
                    .baseUnit("items")
                    .publishPercentiles(0.5, 0.95, 0.99)
                    .register(meterRegistry);
                
                // 주문 처리 시간 타이머
                this.orderProcessingTimer = Timer.builder("orders.processing.time")
                    .description("Order processing time")
                    .tag("process", "checkout")
                    .publishPercentiles(0.5, 0.95, 0.99)
                    .register(meterRegistry);
            }
            
            @Override
            public Order createOrder(OrderRequest request) {
                return orderProcessingTimer.record(() -> {
                    // 주문 생성 로직
                    Order order = new Order(/* ... */);
                    
                    // 메트릭 기록
                    orderCounter.increment();
                    orderSizeHistogram.record(request.getItems().size());
                    
                    // 주문 상태에 따른 게이지 업데이트
                    meterRegistry.gauge(
                        "orders.pending", 
                        Tags.of("status", "pending"),
                        orderRepository.countByStatus("PENDING")
                    );
                    
                    return order;
                });
            }
        }
        ```
    
        **Grafana 대시보드 정의 (JSON)**:
        ```json
        {
          "annotations": { },
          "editable": true,
          "gnetId": null,
          "graphTooltip": 0,
          "id": 10,
          "links": [ ],
          "panels": [
            {
              "datasource": "Prometheus",
              "fieldConfig": {
                "defaults": {
                  "color": { "mode": "palette-classic" },
                  "mappings": [ ],
                  "thresholds": {
                    "mode": "absolute",
                    "steps": [
                      { "color": "green", "value": null },
                      { "color": "red", "value": 80 }
                    ]
                  }
                }
              },
              "options": {
                "displayMode": "gradient",
                "orientation": "auto",
                "reduceOptions": {
                  "calcs": [ "lastNotNull" ],
                  "fields": "",
                  "values": false
                },
                "showUnfilled": true
              },
              "pluginVersion": "7.5.5",
              "targets": [
                {
                  "expr": "sum(rate(orders_created_total[5m])) by (region)",
                  "interval": "",
                  "legendFormat": "{{region}}",
                  "refId": "A"
                }
              ],
              "title": "Orders Created per Second",
              "type": "bargauge"
            },
            {
              "datasource": "Prometheus",
              "fieldConfig": { },
              "options": { },
              "targets": [
                {
                  "expr": "histogram_quantile(0.95, sum(rate(orders_processing_time_seconds_bucket[5m])) by (le))",
                  "interval": "",
                  "legendFormat": "95th percentile",
                  "refId": "A"
                },
                {
                  "expr": "histogram_quantile(0.50, sum(rate(orders_processing_time_seconds_bucket[5m])) by (le))",
                  "interval": "",
                  "legendFormat": "median",
                  "refId": "B"
                }
              ],
              "title": "Order Processing Time",
              "type": "timeseries"
            }
          ],
          "refresh": "10s",
          "schemaVersion": 27,
          "style": "dark",
          "time": {
            "from": "now-6h",
            "to": "now"
          },
          "title": "Order Service Dashboard"
        }
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### 용량 계획 및 성능 분석")
        st.markdown("""
        **Kubernetes 클러스터의 용량 계획**을 위한 방법과 도구를 소개합니다.
    
        **Vertical Pod Autoscaler (VPA) Recommendations**:
        ```yaml
        apiVersion: autoscaling.k8s.io/v1
        kind: VerticalPodAutoscaler
        metadata:
          name: my-app-recommender
        spec:
          targetRef:
            apiVersion: "apps/v1"
            kind: Deployment
            name: my-app
          updatePolicy:
            updateMode: "Off"  # 추천만 제공하고 자동 적용은 하지 않음
        ```
    
        **성능 분석을 위한 PromQL 쿼리**:
        ```
        # 노드 CPU 사용률
        100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
    
        # 노드 메모리 사용률
        (1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100
    
        # 네임스페이스별 CPU 요청 대비 사용률
        sum(rate(container_cpu_usage_seconds_total{namespace="app"}[5m])) / sum(kube_pod_container_resource_requests{namespace="app", resource="cpu"})
    
        # 클러스터 내 사용 가능한 할당 가능 CPU 비율
        sum(kube_node_status_allocatable{resource="cpu"}) - sum(kube_pod_container_resource_requests{resource="cpu"})
        ```
    
        **리소스 사용량 예측 및 계획**:
        ```python
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
        from prophet import Prophet
        from prometheus_api_client import PrometheusConnect
    
        # Prometheus에 연결
        prom = PrometheusConnect(url="http://prometheus-server.monitoring.svc:9090", disable_ssl=True)
    
        # CPU 사용량 쿼리
        cpu_query = 'sum(rate(container_cpu_usage_seconds_total{namespace="app"}[5m]))'
        cpu_data = prom.custom_query(cpu_query)
    
        # 데이터 변환 및 Prophet 모델 준비
        df = pd.DataFrame({
            'ds': pd.to_datetime([item[0] for item in cpu_data[0]['values']], unit='s'),
            'y': [float(item[1]) for item in cpu_data[0]['values']]
        })
    
        # Prophet 모델 학습
        model = Prophet(changepoint_prior_scale=0.05, yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=True)
        model.fit(df)
    
        # 향후 30일 예측
        future = model.make_future_dataframe(periods=30*24, freq='H')
        forecast = model.predict(future)
    
        # 시각화
        fig1 = model.plot(forecast)
        plt.title('CPU Usage Forecast')
        plt.ylabel('CPU Cores')
        plt.savefig('cpu_forecast.png')
        
        # 용량 계획 권장 사항
        peak_forecast = forecast['yhat_upper'].max()
        current_limit = 10  # 현재 할당된 CPU 코어
        
        print(f"예상 피크 CPU 사용량: {peak_forecast:.2f} 코어")
        print(f"현재 제한: {current_limit} 코어")
        print(f"권장 버퍼: {peak_forecast * 1.2:.2f} 코어 (20% 버퍼 포함)")
        
        if peak_forecast * 1.2 > current_limit:
            print(f"경고: 현재 리소스 제한이 예상 사용량보다 낮습니다. {math.ceil(peak_forecast * 1.2)} 코어로 업그레이드 고려하세요.")
        else:
            print(f"현재 리소스 제한은 예상 사용량에 충분합니다.")
        ```
        """)
        
        # 다음 학습 추천 섹션 추가
        st.markdown("""
        <div class="next-learning">
            <h4>관련 학습 리소스</h4>
            <ul>
                <li>분산 추적과 서비스 메시를 통합하는 방법은 <a href="/?page=advanced#networking">네트워킹 고급</a> 모듈을 참고하세요.</li>
                <li>관찰성 솔루션과 함께 멀티클러스터 관리를 위해 <a href="/?page=advanced#multi_cluster">멀티클러스터 관리</a> 모듈을 확인하세요.</li>
                <li>AI/ML 워크로드 모니터링은 <a href="/?page=advanced#ai_ml_workloads">AI/ML 워크로드</a> 모듈을 살펴보세요.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # AI/ML 워크로드 탭 (신규 추가)
    with tabs[7]:
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        st.markdown("### Kubeflow 배포 및 설정")
        st.markdown("""
        **Kubeflow**는 Kubernetes에서 머신러닝 워크플로우를 배포, 관리, 확장하기 위한 플랫폼입니다.
        
        **Kubeflow 설치 (AWS Distribution for Kubeflow)**:
        ```bash
        # AWS Distribution for Kubeflow 설치
        git clone https://github.com/awslabs/kubeflow-manifests.git
        cd kubeflow-manifests
        
        # AWS 환경 준비
        export CLUSTER_NAME=my-eks-cluster
        export CLUSTER_REGION=us-west-2
        
        # Kubeflow 설치
        make deploy-kubeflow INSTALLATION_OPTION=kustomize \
          DEPLOYMENT_OPTION=vanilla \
          AWS_REGION=\$CLUSTER_REGION
        
        # 설치 확인
        kubectl get pods -n kubeflow
        ```
        
        **Kubeflow 주요 구성요소**:
        - **Pipelines**: 재사용 가능한 ML 워크플로우 생성 및 배포
        - **Notebook 서버**: 대화형 개발 환경
        - **KFServing**: ML 모델 서빙
        - **Katib**: 하이퍼파라미터 튜닝
        - **Training Operator**: 분산 훈련 작업 관리
        
        **사용자 정의 프로필 생성**:
        ```yaml
        apiVersion: kubeflow.org/v1
        kind: Profile
        metadata:
          name: data-science-team
        spec:
          owner:
            kind: User
            name: user@example.com
          resourceQuotaSpec:
            hard:
              cpu: 20
              memory: 100Gi
              nvidia.com/gpu: 4
              persistentvolumeclaims: 10
              requests.storage: 500Gi
        ```
        
        **Kubeflow 파이프라인 정의 예시(Python)**:
        ```python
        import kfp
        from kfp import dsl
        from kfp.components import func_to_container_op
    
        # 데이터 전처리 컴포넌트
        @func_to_container_op
        def preprocess_data(data_path: str) -> str:
            import pandas as pd
            
            # 데이터 로드 및 전처리
            df = pd.read_csv(data_path)
            # ... 전처리 로직 ...
            
            output_path = '/tmp/processed_data.csv'
            df.to_csv(output_path, index=False)
            return output_path
    
        # 모델 훈련 컴포넌트
        @func_to_container_op
        def train_model(data_path: str, hyperparams: dict) -> str:
            import pandas as pd
            import sklearn
            from joblib import dump
            
            df = pd.read_csv(data_path)
            X = df.drop('target', axis=1)
            y = df['target']
            
            # 모델 훈련
            model = sklearn.ensemble.RandomForestClassifier(**hyperparams)
            model.fit(X, y)
            
            # 모델 저장
            model_path = '/tmp/model.joblib'
            dump(model, model_path)
            return model_path
    
        # 모델 평가 컴포넌트
        @func_to_container_op
        def evaluate_model(model_path: str, test_data_path: str) -> float:
            import pandas as pd
            from joblib import load
            from sklearn.metrics import accuracy_score
            
            # 테스트 데이터 로드
            df = pd.read_csv(test_data_path)
            X_test = df.drop('target', axis=1)
            y_test = df['target']
            
            # 모델 로드 및 평가
            model = load(model_path)
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            print(f"Model accuracy: {accuracy}")
            return accuracy
    
        # 전체 파이프라인 정의
        @dsl.pipeline(
            name='ML Training Pipeline',
            description='A simple ML training pipeline'
        )
        def ml_pipeline(data_path: str = 's3://my-bucket/data.csv',
                       test_data_path: str = 's3://my-bucket/test_data.csv',
                       n_estimators: int = 100,
                       max_depth: int = 10):
            
            # 데이터 전처리
            preprocess_task = preprocess_data(data_path)
            
            # 모델 훈련
            hyperparams = {'n_estimators': n_estimators, 'max_depth': max_depth}
            train_task = train_model(preprocess_task.output, hyperparams)
            
            # 모델 평가
            evaluate_task = evaluate_model(train_task.output, test_data_path)
            
        # 파이프라인 컴파일 및 실행
        kfp.compiler.Compiler().compile(ml_pipeline, 'ml_pipeline.yaml')
        
        client = kfp.Client()
        client.create_run_from_pipeline_func(
            ml_pipeline,
            arguments={
                'data_path': 's3://my-bucket/data.csv',
                'test_data_path': 's3://my-bucket/test_data.csv',
                'n_estimators': 150,
                'max_depth': 15
            }
        )
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### GPU 노드 관리와 최적화")
        st.markdown("""
        **EKS에서 GPU 노드 그룹 생성**:
        ```bash
        eksctl create nodegroup \\
          --cluster my-eks-cluster \\
          --name gpu-nodes \\
          --node-type p3.2xlarge \\
          --nodes 2 \\
          --nodes-min 1 \\
          --nodes-max 5 \\
          --asg-access \\
          --install-nvidia-plugin=true
        ```
        
        **NVIDIA 장치 플러그인 확인**:
        ```bash
        kubectl get daemonset -n kube-system nvidia-device-plugin-daemonset
        ```
        
        **GPU 요청 및 제한이 있는 Pod 예시**:
        ```yaml
        apiVersion: v1
        kind: Pod
        metadata:
          name: gpu-pod
        spec:
          containers:
          - name: cuda-container
            image: nvidia/cuda:11.6.2-base-ubuntu20.04
            command: ["nvidia-smi"]
            resources:
              limits:
                nvidia.com/gpu: 1  # GPU 요청
          nodeSelector:
            accelerator: nvidia-tesla  # GPU 노드에 배치
        ```
        
        **GPU 공유 및 분할(NVIDIA MPS) 설정**:
        ```yaml
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: gpu-mps-config
          namespace: gpu-workloads
        data:
          entrypoint.sh: |
            #!/bin/bash
            set -e
            
            # NVIDIA MPS 서버 시작
            nvidia-smi -c EXCLUSIVE_PROCESS
            nvidia-cuda-mps-control -d
            
            # Pod가 종료될 때 정리 작업
            trap "echo quit | nvidia-cuda-mps-control" EXIT
            
            # 기본 명령 실행
            exec "\$@"
        ---
        apiVersion: v1
        kind: Pod
        metadata:
          name: mps-gpu-pod
        spec:
          hostIPC: true  # MPS에 필요함
          containers:
          - name: mps-container
            image: nvidia/cuda:11.6.2-base-ubuntu20.04
            command: ["/bin/entrypoint.sh", "python", "train.py"]
            resources:
              limits:
                nvidia.com/gpu: 1
            volumeMounts:
            - name: entrypoint
              mountPath: /bin/entrypoint.sh
              subPath: entrypoint.sh
          volumes:
          - name: entrypoint
            configMap:
              name: gpu-mps-config
              defaultMode: 0755
          nodeSelector:
            accelerator: nvidia-tesla
        ```
        
        **자동 스케일링을 위한 DCGM 모니터링 설정**:
        ```bash
        # NVIDIA DCGM 익스포터 설치
        helm repo add gpu-helm-charts https://nvidia.github.io/dcgm-exporter/helm-charts
        helm repo update
        
        helm install dcgm-exporter gpu-helm-charts/dcgm-exporter -n gpu-monitoring --create-namespace
        ```
        
        **GPU 메트릭 기반 HPA 설정**:
        ```yaml
        apiVersion: autoscaling/v2
        kind: HorizontalPodAutoscaler
        metadata:
          name: ml-training-hpa
          namespace: gpu-workloads
        spec:
          scaleTargetRef:
            apiVersion: apps/v1
            kind: Deployment
            name: ml-training
          minReplicas: 1
          maxReplicas: 10
          metrics:
          - type: Pods
            pods:
              metric:
                name: DCGM_FI_DEV_GPU_UTIL
              target:
                type: AverageValue
                averageValue: 80
          behavior:
            scaleDown:
              stabilizationWindowSeconds: 300
        ```
        
        **GPU 노드 라벨링을 통한 워크로드 격리**:
        ```bash
        # GPU 유형별 라벨 추가
        kubectl label nodes ip-192-168-123-456.ec2.internal gpu-type=t4
        kubectl label nodes ip-192-168-123-457.ec2.internal gpu-type=v100
        
        # 메모리 크기별 라벨 추가
        kubectl label nodes ip-192-168-123-456.ec2.internal gpu-memory=16Gi
        kubectl label nodes ip-192-168-123-457.ec2.internal gpu-memory=32Gi
        ```
        
        **우선순위 기반 GPU 스케줄링**:
        ```yaml
        apiVersion: scheduling.k8s.io/v1
        kind: PriorityClass
        metadata:
          name: high-priority-gpu
        value: 1000000
        globalDefault: false
        description: "High priority GPU workloads"
        ---
        apiVersion: v1
        kind: Pod
        metadata:
          name: high-priority-training
        spec:
          priorityClassName: high-priority-gpu
          containers:
          - name: training
            image: my-ml-image:latest
            resources:
              limits:
                nvidia.com/gpu: 2
          nodeSelector:
            gpu-type: v100
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### 분산 학습 구성")
        st.markdown("""
        **Kubernetes에서의 분산 학습 설정**:
        
        **PyTorch 분산 훈련 작업**:
        ```yaml
        apiVersion: kubeflow.org/v1
        kind: PyTorchJob
        metadata:
          name: pytorch-dist
          namespace: kubeflow
        spec:
          pytorchReplicaSpecs:
            Master:
              replicas: 1
              restartPolicy: OnFailure
              template:
                spec:
                  containers:
                  - name: pytorch
                    image: my-pytorch-image:latest
                    command:
                      - "python"
                      - "-m"
                      - "torch.distributed.launch"
                      - "--nproc_per_node=1"
                      - "--nnodes=3"
                      - "--node_rank=0"
                      - "--master_addr=\$(MASTER_ADDR)"
                      - "--master_port=23456"
                      - "/workspace/train.py"
                    env:
                    - name: MASTER_ADDR
                      value: pytorch-dist-master-0.pytorch-dist-master
                    resources:
                      limits:
                        nvidia.com/gpu: 1
                    volumeMounts:
                    - name: dataset
                      mountPath: /data
                    - name: model-store
                      mountPath: /models
                  volumes:
                  - name: dataset
                    persistentVolumeClaim:
                      claimName: dataset-pvc
                  - name: model-store
                    persistentVolumeClaim:
                      claimName: model-store-pvc
            Worker:
              replicas: 2
              restartPolicy: OnFailure
              template:
                spec:
                  containers:
                  - name: pytorch
                    image: my-pytorch-image:latest
                    command:
                      - "python"
                      - "-m"
                      - "torch.distributed.launch"
                      - "--nproc_per_node=1"
                      - "--nnodes=3"
                      - "--node_rank=\$(RANK)"
                      - "--master_addr=\$(MASTER_ADDR)"
                      - "--master_port=23456"
                      - "/workspace/train.py"
                    env:
                    - name: MASTER_ADDR
                      value: pytorch-dist-master-0.pytorch-dist-master
                    - name: RANK
                      valueFrom:
                        fieldRef:
                          fieldPath: metadata.annotations['worker-id']
                    resources:
                      limits:
                        nvidia.com/gpu: 1
                    volumeMounts:
                    - name: dataset
                      mountPath: /data
                    - name: model-store
                      mountPath: /models
                  volumes:
                  - name: dataset
                    persistentVolumeClaim:
                      claimName: dataset-pvc
                  - name: model-store
                    persistentVolumeClaim:
                      claimName: model-store-pvc
        ```
        
        **TensorFlow 분산 훈련 작업**:
        ```yaml
        apiVersion: kubeflow.org/v1
        kind: TFJob
        metadata:
          name: tf-dist-training
          namespace: kubeflow
        spec:
          tfReplicaSpecs:
            Chief:
              replicas: 1
              template:
                spec:
                  containers:
                  - name: tensorflow
                    image: my-tensorflow-image:latest
                    command:
                    - python
                    - /opt/train.py
                    - --model_dir=/models
                    - --train_steps=20000
                    resources:
                      limits:
                        nvidia.com/gpu: 1
                    volumeMounts:
                    - name: dataset
                      mountPath: /data
                    - name: model-store
                      mountPath: /models
                  volumes:
                  - name: dataset
                    persistentVolumeClaim:
                      claimName: dataset-pvc
                  - name: model-store
                    persistentVolumeClaim:
                      claimName: model-store-pvc
            Worker:
              replicas: 3
              template:
                spec:
                  containers:
                  - name: tensorflow
                    image: my-tensorflow-image:latest
                    command:
                    - python
                    - /opt/train.py
                    - --model_dir=/models
                    - --train_steps=20000
                    resources:
                      limits:
                        nvidia.com/gpu: 1
                    volumeMounts:
                    - name: dataset
                      mountPath: /data
                    - name: model-store
                      mountPath: /models
                  volumes:
                  - name: dataset
                    persistentVolumeClaim:
                      claimName: dataset-pvc
                  - name: model-store
                    persistentVolumeClaim:
                      claimName: model-store-pvc
            PS:
              replicas: 2
              template:
                spec:
                  containers:
                  - name: tensorflow
                    image: my-tensorflow-image:latest
                    command:
                    - python
                    - /opt/train.py
                    - --model_dir=/models
                    - --train_steps=20000
                    resources:
                      requests:
                        memory: "4Gi"
                        cpu: "2"
                      limits:
                        memory: "8Gi"
                        cpu: "4"
                    volumeMounts:
                    - name: model-store
                      mountPath: /models
                  volumes:
                  - name: model-store
                    persistentVolumeClaim:
                      claimName: model-store-pvc
        ```
        
        **AWS EFS를 사용한 공유 스토리지 설정**:
        ```yaml
        apiVersion: storage.k8s.io/v1
        kind: StorageClass
        metadata:
          name: efs-sc
        provisioner: efs.csi.aws.com
        parameters:
          provisioningMode: efs-ap
          fileSystemId: fs-0123456789abcdef0
          directoryPerms: "700"
          
        ---
        apiVersion: v1
        kind: PersistentVolumeClaim
        metadata:
          name: model-store-pvc
          namespace: kubeflow
        spec:
          accessModes:
            - ReadWriteMany
          storageClassName: efs-sc
          resources:
            requests:
              storage: 50Gi
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### ML 파이프라인 자동화")
        st.markdown("""
        **MLflow와 EKS 통합**:
        ```bash
        # MLflow 설치
        helm repo add larribas https://larribas.me/helm-charts
        helm install mlflow larribas/mlflow --set backendStore.postgres.enabled=true --namespace mlflow --create-namespace
        ```
        
        **MLflow 트래킹 서버 설정**:
        ```yaml
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: mlflow-config
          namespace: mlflow
        data:
          tracking_server: http://mlflow-service.mlflow:5000
          
        ---
        apiVersion: v1
        kind: Pod
        metadata:
          name: ml-training
        spec:
          containers:
          - name: training
            image: my-ml-image:latest
            command: ["python", "train.py"]
            env:
            - name: MLFLOW_TRACKING_URI
              valueFrom:
                configMapKeyRef:
                  name: mlflow-config
                  key: tracking_server
            - name: MLFLOW_EXPERIMENT_NAME
              value: "production-experiment"
            # ... 추가 구성 ...
        ```
        
        **지속적 통합 및 모델 배포**:
        ```yaml
        # GitLab CI/CD 설정 (.gitlab-ci.yml)
        stages:
          - train
          - validate
          - register
          - deploy
        
        train_model:
          stage: train
          image: python:3.9
          script:
            - pip install -r requirements.txt
            - python train.py
          artifacts:
            paths:
              - models/
        
        validate_model:
          stage: validate
          image: python:3.9
          script:
            - pip install -r requirements.txt
            - python validate.py --model-dir models/
          dependencies:
            - train_model
        
        register_model:
          stage: register
          image: python:3.9
          script:
            - pip install -r requirements.txt
            - python register_model.py
              --model-dir models/
              --model-name "my-model"
              --model-version "0.1"
          dependencies:
            - validate_model
          rules:
            - if: \$CI_COMMIT_BRANCH == "main"
        
        deploy_model:
          stage: deploy
          image: 
            name: bitnami/kubectl:latest
            entrypoint: [""]
          script:
            - kubectl apply -f k8s/deployment.yaml
          dependencies:
            - register_model
          rules:
            - if: \$CI_COMMIT_BRANCH == "main"
        ```
        
        **KFServing/KServe를 사용한 모델 서빙**:
        ```yaml
        apiVersion: "serving.kserve.io/v1beta1"
        kind: "InferenceService"
        metadata:
          name: "my-model-predictor"
          namespace: kserve
        spec:
          predictor:
            model:
              modelFormat:
                name: sklearn
              storageUri: "s3://my-bucket/models/my-model/"
              resources:
                limits:
                  memory: 1Gi
                  cpu: "1"
        ```
        
        **모델 A/B 테스트 설정**:
        ```yaml
        apiVersion: serving.kserve.io/v1beta1
        kind: InferenceService
        metadata:
          name: model-ab-test
          namespace: kserve
        spec:
          predictor:
            canaryTrafficPercent: 20
            containers:
            - name: model-a
              image: myregistry/model-a:v1
              resources:
                requests:
                  cpu: 100m
                limits:
                  memory: 1Gi
            canary:
            - name: model-b
              image: myregistry/model-b:v1
              resources:
                requests:
                  cpu: 100m
                limits:
                  memory: 1Gi
        ```
        """)
        
        # 다음 학습 추천 섹션 추가
        st.markdown("""
        <div class="next-learning">
            <h4>관련 학습 리소스</h4>
            <ul>
                <li>ML 워크로드 비용 최적화는 <a href="/?page=advanced#cost_optimization">비용 최적화 전략</a> 모듈을 확인하세요.</li>
                <li>ML 파이프라인 보안 강화는 <a href="/?page=advanced#security">보안 강화</a> 모듈을 참고하세요.</li>
                <li>ML 워크로드의 관찰성 향상은 <a href="/?page=advanced#observability">고급 관찰성</a> 모듈을 살펴보세요.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 비용 최적화 전략 탭 (신규 추가)
    with tabs[8]:
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        st.markdown("### EKS 비용 구성 요소 이해")
        st.markdown("""
        **EKS 클러스터 비용 구성**:
        
        1. **EKS 컨트롤 플레인 비용**:
          - 시간당 \$0.10 (월 약 \$73)
          - 리전당 클러스터 수에 따라 청구됨
          - HA를 위한 다중 AZ 배포는 추가 비용 없음
        
        2. **노드 비용**:
          - EC2 인스턴스 비용 (온디맨드, 예약 인스턴스, 스팟)
          - EBS 볼륨 비용
        
        3. **Fargate 비용**:
          - vCPU 및 메모리 리소스 사용량에 따라 청구
          - 초 단위 요금, 최소 1분 청구
        
        4. **네트워킹 비용**:
          - VPC 내 데이터 전송 (무료)
          - 리전 간 데이터 전송
          - 인터넷 아웃바운드 데이터 전송
        
        5. **스토리지 비용**:
          - EBS 볼륨 (gp2, gp3, io1, io2 등)
          - EFS 파일 시스템
          - S3 버킷
          
        6. **추가 서비스 비용**:
          - AWS Load Balancer
          - CloudWatch 로그 및 메트릭
          - Route 53 호스팅
        
        **비용 모니터링 도구**:
        - AWS Cost Explorer
        - AWS Trusted Advisor
        - AWS Cost and Usage Reports
        - Kubecost (Kubernetes 특화 비용 모니터링)
        
        **비용 할당을 위한 태그 전략**:
        ```bash
        # EC2 인스턴스에 태그 추가
        aws ec2 create-tags \\
          --resources i-1234567890abcdef0 \\
          --tags Key=Environment,Value=Production Key=Team,Value=DataScience Key=Project,Value=ML-Analysis
        
        # EKS 클러스터에 태그 추가
        aws eks tag-resource \\
          --resource-arn arn:aws:eks:region:account-id:cluster/my-cluster \\
          --tags Environment=Production,CostCenter=123456
        ```
        
        **Kubernetes 네임스페이스 및 워크로드 라벨링**:
        ```yaml
        apiVersion: v1
        kind: Namespace
        metadata:
          name: team-a
          labels:
            environment: production
            team: team-a
            cost-center: 12345
            
        ---
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: backend-service
          namespace: team-a
          labels:
            app: backend-service
            environment: production
            team: team-a
            cost-center: 12345
            project: web-platform
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### 스팟 인스턴스 활용 전략")
        st.markdown("""
        **스팟 인스턴스 노드 그룹 생성**:
        ```bash
        eksctl create nodegroup \\
          --cluster my-cluster \\
          --name spot-ng \\
          --node-type m5.large \\
          --nodes 3 \\
          --nodes-min 1 \\
          --nodes-max 10 \\
          --spot
        ```
        
        **다중 인스턴스 유형을 사용한 스팟 노드 그룹 생성**:
        ```bash
        eksctl create nodegroup \\
          --cluster my-cluster \\
          --name mixed-spot-ng \\
          --instance-types m5.large,m5d.large,m5a.large,m4.large \\
          --nodes 3 \\
          --nodes-min 1 \\
          --nodes-max 10 \\
          --spot
        ```
        
        **중단 내성이 있는 애플리케이션 설계**:
        ```yaml
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: spot-tolerant-app
          labels:
            app: spot-tolerant-app
        spec:
          replicas: 3
          selector:
            matchLabels:
              app: spot-tolerant-app
          template:
            metadata:
              labels:
                app: spot-tolerant-app
            spec:
              terminationGracePeriodSeconds: 60  # 중단 시 정상 종료 시간
              topologySpreadConstraints:  # 가용성 향상을 위한 Pod 분산
              - maxSkew: 1
                topologyKey: topology.kubernetes.io/zone
                whenUnsatisfiable: ScheduleAnyway
                labelSelector:
                  matchLabels:
                    app: spot-tolerant-app
              affinity:
                podAntiAffinity:  # 같은 노드에 배포 방지
                  preferredDuringSchedulingIgnoredDuringExecution:
                  - weight: 100
                    podAffinityTerm:
                      labelSelector:
                        matchExpressions:
                        - key: app
                          operator: In
                          values:
                          - spot-tolerant-app
                      topologyKey: kubernetes.io/hostname
              containers:
              - name: spot-app
                image: my-app:latest
                lifecycle:
                  preStop:
                    exec:
                      command: ["/bin/sh", "-c", "./graceful-shutdown.sh"]  # 정상 종료 스크립트
                readinessProbe:
                  httpGet:
                    path: /health
                    port: 8080
                  initialDelaySeconds: 5
                  periodSeconds: 10
        ```
        
        **인스턴스 중단 처리를 위한 Kubernetes 이벤트 핸들러**:
        ```yaml
        apiVersion: rbac.authorization.k8s.io/v1
        kind: ClusterRole
        metadata:
          name: node-drainer
        rules:
        - apiGroups: [""]
          resources: ["nodes"]
          verbs: ["get", "list", "patch", "update"]
        - apiGroups: [""]
          resources: ["pods"]
          verbs: ["get", "list"]
        - apiGroups: ["apps"]
          resources: ["daemonsets"]
          verbs: ["get"]
        ---
        apiVersion: v1
        kind: ServiceAccount
        metadata:
          name: node-drainer
          namespace: kube-system
        ---
        apiVersion: rbac.authorization.k8s.io/v1
        kind: ClusterRoleBinding
        metadata:
          name: node-drainer
        roleRef:
          apiGroup: rbac.authorization.k8s.io
          kind: ClusterRole
          name: node-drainer
        subjects:
        - kind: ServiceAccount
          name: node-drainer
          namespace: kube-system
        ---
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: spot-interrupt-handler
          namespace: kube-system
        spec:
          replicas: 1
          selector:
            matchLabels:
              app: spot-interrupt-handler
          template:
            metadata:
              labels:
                app: spot-interrupt-handler
            spec:
              serviceAccountName: node-drainer
              containers:
              - name: handler
                image: amazon/aws-node-termination-handler:v1.13.3
                env:
                - name: NODE_TERMINATION_GRACE_PERIOD
                  value: "120"
                - name: ENABLE_SPOT_INTERRUPTION_DRAINING
                  value: "true"
                - name: ENABLE_SCHEDULED_EVENT_DRAINING
                  value: "true"
                - name: METADATA_TRIES
                  value: "3"
        ```
        
        **하이브리드 노드 그룹 전략**:
        ```bash
        # 온디맨드 노드 그룹 (중요 워크로드용)
        eksctl create nodegroup \\
          --cluster my-cluster \\
          --name critical-workloads \\
          --node-type m5.xlarge \\
          --nodes 3 \\
          --node-labels "workload-type=critical"
        
        # 스팟 노드 그룹 (일반 워크로드용)
        eksctl create nodegroup \\
          --cluster my-cluster \\
          --name general-workloads \\
          --instance-types m5.large,m5d.large,m5a.large \\
          --nodes 3 \\
          --nodes-min 1 \\
          --nodes-max 20 \\
          --node-labels "workload-type=general" \\
          --spot
        ```
        
        **중요 워크로드 노드 선택기 설정**:
        ```yaml
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: critical-service
        spec:
          replicas: 3
          selector:
            matchLabels:
              app: critical-service
          template:
            metadata:
              labels:
                app: critical-service
            spec:
              nodeSelector:
                workload-type: critical  # 온디맨드 노드에만 배포
              containers:
              - name: critical-service
                image: critical-service:latest
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### 리소스 요청 최적화")
        st.markdown("""
        **Vertical Pod Autoscaler (VPA)**를 사용한 리소스 요청 최적화:
        ```yaml
        apiVersion: autoscaling.k8s.io/v1
        kind: VerticalPodAutoscaler
        metadata:
          name: my-app-vpa
        spec:
          targetRef:
            apiVersion: "apps/v1"
            kind: Deployment
            name: my-app
          updatePolicy:
            updateMode: "Auto"  # "Off"로 설정하면 추천만 제공
          resourcePolicy:
            containerPolicies:
            - containerName: '*'
              minAllowed:
                cpu: 10m
                memory: 50Mi
              maxAllowed:
                cpu: 1
                memory: 500Mi
              controlledResources: ["cpu", "memory"]
        ```
        
        **Goldilocks**를 통한 VPA 추천 시각화:
        ```bash
        # Goldilocks 설치
        helm repo add fairwinds-stable https://charts.fairwinds.com/stable
        helm install goldilocks fairwinds-stable/goldilocks --namespace goldilocks --create-namespace
        
        # 네임스페이스 활성화
        kubectl label namespace default goldilocks.fairwinds.com/enabled=true
        ```
        
        **리소스 요청 및 제한 설정 가이드라인**:
        ```yaml
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: optimized-app
        spec:
          replicas: 3
          selector:
            matchLabels:
              app: optimized-app
          template:
            metadata:
              labels:
                app: optimized-app
            spec:
              containers:
              - name: app
                image: my-app:latest
                resources:
                  requests:
                    cpu: 200m       # 0.2 CPU 코어
                    memory: 256Mi   # 256 MB 메모리
                  limits:
                    cpu: 500m       # 0.5 CPU 코어
                    memory: 512Mi   # 512 MB 메모리
        ```
        
        **LimitRange를 사용한 네임스페이스 수준의 기본값 설정**:
        ```yaml
        apiVersion: v1
        kind: LimitRange
        metadata:
          name: default-limits
          namespace: my-namespace
        spec:
          limits:
          - default:
              cpu: 500m
              memory: 512Mi
            defaultRequest:
              cpu: 100m
              memory: 128Mi
            max:
              cpu: 2
              memory: 2Gi
            min:
              cpu: 50m
              memory: 64Mi
            type: Container
        ```
        
        **ResourceQuota로 네임스페이스 사용량 제한**:
        ```yaml
        apiVersion: v1
        kind: ResourceQuota
        metadata:
          name: team-quota
          namespace: team-a
        spec:
          hard:
            requests.cpu: "10"
            requests.memory: 20Gi
            limits.cpu: "20"
            limits.memory: 40Gi
            pods: "50"
            services: "10"
            services.loadbalancers: "1"
            persistentvolumeclaims: "20"
            requests.storage: "100Gi"
        ```
        
        **Kubecost를 사용한 비용 모니터링 및 최적화**:
        ```bash
        # Kubecost 설치
        helm repo add kubecost https://kubecost.github.io/cost-analyzer/
        helm repo update
        
        helm install kubecost kubecost/cost-analyzer \\
          --namespace kubecost \\
          --create-namespace \\
          --set kubecostToken="<Your Kubecost token>" \\
          --set prometheus.server.persistentVolume.size=100Gi
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### 워크로드 스케줄링 최적화")
        st.markdown("""
        **노드 사용률 최적화를 위한 bin-packing**:
        ```yaml
        # kube-scheduler 구성 예시
        apiVersion: kubescheduler.config.k8s.io/v1beta3
        kind: KubeSchedulerConfiguration
        profiles:
        - schedulerName: default-scheduler
          plugins:
            score:
              disabled:
              - name: NodeResourcesLeastAllocated  # 기본 스케줄러 비활성화
              enabled:
              - name: NodeResourcesMostAllocated   # bin packing 활성화
          pluginConfig:
          - name: NodeResourcesMostAllocated
            args:
              scoringStrategy:
                resources:
                - name: cpu
                  weight: 1
                - name: memory
                  weight: 1
        ```
        
        **Pod 토폴로지 분산 제약**:
        ```yaml
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: web-server
        spec:
          replicas: 9
          selector:
            matchLabels:
              app: web-server
          template:
            metadata:
              labels:
                app: web-server
            spec:
              topologySpreadConstraints:
              - maxSkew: 1
                topologyKey: topology.kubernetes.io/zone
                whenUnsatisfiable: DoNotSchedule
                labelSelector:
                  matchLabels:
                    app: web-server
              - maxSkew: 1
                topologyKey: kubernetes.io/hostname
                whenUnsatisfiable: ScheduleAnyway
                labelSelector:
                  matchLabels:
                    app: web-server
              containers:
              - name: nginx
                image: nginx:latest
        ```
        
        **노드 어피니티를 통한 워크로드 배치 최적화**:
        ```yaml
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: cost-optimized-app
        spec:
          replicas: 3
          selector:
            matchLabels:
              app: cost-optimized-app
          template:
            metadata:
              labels:
                app: cost-optimized-app
            spec:
              affinity:
                nodeAffinity:
                  requiredDuringSchedulingIgnoredDuringExecution:
                    nodeSelectorTerms:
                    - matchExpressions:
                      - key: node.kubernetes.io/instance-type
                        operator: In
                        values:
                        - m5.large
                        - m5a.large
                        - m4.large
                  preferredDuringSchedulingIgnoredDuringExecution:
                  - weight: 100
                    preference:
                      matchExpressions:
                      - key: eks.amazonaws.com/capacityType
                        operator: In
                        values:
                        - SPOT
                podAntiAffinity:
                  preferredDuringSchedulingIgnoredDuringExecution:
                  - weight: 100
                    podAffinityTerm:
                      labelSelector:
                        matchExpressions:
                        - key: app
                          operator: In
                          values:
                          - cost-optimized-app
                      topologyKey: kubernetes.io/hostname
              containers:
              - name: app
                image: my-app:latest
        ```
        
        **Descheduler를 통한 클러스터 밸런싱**:
        ```bash
        # Descheduler 설치
        helm repo add descheduler https://kubernetes-sigs.github.io/descheduler/
        helm repo update
        
        helm install descheduler descheduler/descheduler \\
          --namespace kube-system \\
          --set schedule="*/30 * * * *" \\
          --set strategies.removePodsViolatingNodeTaints=true \\
          --set strategies.removePodsViolatingNodeAffinity=true \\
          --set strategies.removePodsViolatingInterPodAntiAffinity=true \\
          --set strategies.lownodeutilization.enabled=true \\
          --set strategies.lownodeutilization.params.nodeResourceUtilizationThresholds.thresholds.cpu=50 \\
          --set strategies.lownodeutilization.params.nodeResourceUtilizationThresholds.thresholds.memory=50 \\
          --set strategies.lownodeutilization.params.nodeResourceUtilizationThresholds.thresholds.pods=50 \\
          --set strategies.lownodeutilization.params.nodeResourceUtilizationThresholds.targetThresholds.cpu=70 \\
          --set strategies.lownodeutilization.params.nodeResourceUtilizationThresholds.targetThresholds.memory=70 \\
          --set strategies.lownodeutilization.params.nodeResourceUtilizationThresholds.targetThresholds.pods=70
        ```
        
        **Karpenter를 통한 적시 프로비저닝**:
        ```yaml
        apiVersion: karpenter.sh/v1alpha5
        kind: Provisioner
        metadata:
          name: cost-optimized
        spec:
          # 효율적인 노드 유형 사용
          requirements:
            - key: karpenter.sh/capacity-type
              operator: In
              values: ["spot", "on-demand"]
            - key: node.kubernetes.io/instance-type
              operator: In
              values: ["m5.large", "m5a.large", "m5n.large", "m4.large", "t3.large"]
            - key: kubernetes.io/arch
              operator: In
              values: ["amd64"]
            - key: topology.kubernetes.io/zone
              operator: In
              values: ["us-west-2a", "us-west-2b", "us-west-2c"]
          # 사용률 기반 스케일 다운
          consolidation:
            enabled: true
          # 최대 노드 갯수 제한
          limits:
            resources:
              cpu: "100"
              memory: 400Gi
          # 노드 수명 제한
          ttlSecondsAfterEmpty: 30
          ttlSecondsUntilExpired: 2592000  # 30일
        ```
        """)
        
        # 다음 학습 추천 섹션 추가
        st.markdown("""
        <div class="next-learning">
            <h4>관련 학습 리소스</h4>
            <ul>
                <li>서버리스와 Fargate 비용 최적화는 <a href="/?page=advanced#serverless_advanced">서버리스 EKS 심화</a> 모듈을 참고하세요.</li>
                <li>비용 모니터링을 위한 관찰성 기법은 <a href="/?page=advanced#observability">고급 관찰성</a> 모듈을 확인하세요.</li>
                <li>멀티클러스터 환경에서의 비용 최적화는 <a href="/?page=advanced#multi_cluster">멀티클러스터 관리</a> 모듈을 살펴보세요.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 고급 실습 프로젝트 탭
    with tabs[9]:
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        st.markdown("### 다중 영역 HA 아키텍처")
        st.markdown("""
        다중 가용 영역에 걸쳐 고가용성 애플리케이션을 설계하고 배포하는 실습 프로젝트입니다.
    
        **프로젝트 개요**:
        - 여러 AZ에 분산된 3-티어 애플리케이션 구축
        - 무중단 배포 구현
        - 자동 장애 조치 설정
        
        **핵심 구성 요소**:
        1. 다중 AZ에 분산된 EKS 노드
        2. 영역 인식 Pod 배포
        3. 고가용성 데이터 계층
        4. 충돌 및 복구 테스트
        
        **구현 방법**:
        ```bash
        # 1. 다중 AZ EKS 클러스터 생성
        eksctl create cluster \\
          --name ha-cluster \\
          --version 1.23 \\
          --region us-west-2 \\
          --zones us-west-2a,us-west-2b,us-west-2c \\
          --nodegroup-name ha-nodes \\
          --nodes-per-az 2 \\
          --node-type m5.large
        ```
        
        ```yaml
        # 2. 영역 인식 배포 구성
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: ha-frontend
        spec:
          replicas: 6  # 가용 영역당 2개씩
          selector:
            matchLabels:
              app: ha-frontend
          template:
            metadata:
              labels:
                app: ha-frontend
            spec:
              topologySpreadConstraints:
              - maxSkew: 1
                topologyKey: topology.kubernetes.io/zone
                whenUnsatisfiable: DoNotSchedule
                labelSelector:
                  matchLabels:
                    app: ha-frontend
              containers:
              - name: frontend
                image: my-frontend:1.0
                resources:
                  limits:
                    memory: "256Mi"
                    cpu: "500m"
                readinessProbe:
                  httpGet:
                    path: /health
                    port: 80
                livenessProbe:
                  httpGet:
                    path: /health
                    port: 80
                startupProbe:
                  httpGet:
                    path: /health
                    port: 80
                  failureThreshold: 30
                  periodSeconds: 10
        ```
        
        ```yaml
        # 3. 연결성 테스트를 위한 서비스 및 인그레스
        apiVersion: v1
        kind: Service
        metadata:
          name: ha-frontend-service
        spec:
          selector:
            app: ha-frontend
          ports:
          - port: 80
            targetPort: 80
          type: ClusterIP
        ---
        apiVersion: networking.k8s.io/v1
        kind: Ingress
        metadata:
          name: ha-frontend-ingress
          annotations:
            kubernetes.io/ingress.class: alb
            alb.ingress.kubernetes.io/scheme: internet-facing
            alb.ingress.kubernetes.io/target-type: ip
            alb.ingress.kubernetes.io/healthcheck-path: /health
        spec:
          rules:
          - http:
              paths:
              - path: /
                pathType: Prefix
                backend:
                  service:
                    name: ha-frontend-service
                    port:
                      number: 80
        ```
        
        ```yaml
        # 4. 고가용성 데이터 계층 (StatefulSet + PV)
        apiVersion: apps/v1
        kind: StatefulSet
        metadata:
          name: ha-database
        spec:
          serviceName: "ha-database"
          replicas: 3
          selector:
            matchLabels:
              app: ha-database
          template:
            metadata:
              labels:
                app: ha-database
            spec:
              topologySpreadConstraints:
              - maxSkew: 1
                topologyKey: topology.kubernetes.io/zone
                whenUnsatisfiable: DoNotSchedule
                labelSelector:
                  matchLabels:
                    app: ha-database
              containers:
              - name: db
                image: postgres:14
                env:
                - name: POSTGRES_PASSWORD
                  valueFrom:
                    secretKeyRef:
                      name: db-secret
                      key: password
                ports:
                - containerPort: 5432
                  name: db
                volumeMounts:
                - name: db-data
                  mountPath: /var/lib/postgresql/data
                readinessProbe:
                  exec:
                    command: ["pg_isready", "-U", "postgres"]
                  initialDelaySeconds: 10
                  periodSeconds: 5
          volumeClaimTemplates:
          - metadata:
              name: db-data
            spec:
              accessModes: [ "ReadWriteOnce" ]
              storageClassName: "gp2"
              resources:
                requests:
                  storage: 10Gi
        ```
        
        ```bash
        # 5. 장애 주입 및 복구 테스트
        # AZ 실패 시뮬레이션
        ZONE=us-west-2a
        NODE_LIST=\$(kubectl get nodes -l topology.kubernetes.io/zone=\$ZONE -o jsonpath='{.items[*].metadata.name}')
        
        # 해당 영역의 노드 cordon 및 drain
        for NODE in \$NODE_LIST; do
          echo "Simulating zone failure for node \$NODE..."
          kubectl cordon \$NODE
          kubectl drain \$NODE --ignore-daemonsets --delete-emptydir-data
        done
        
        # 애플리케이션 가용성 확인
        watch kubectl get pods -o wide
        
        # 서비스 가용성 테스트
        curl -v http://\$(kubectl get ingress ha-frontend-ingress -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')/health
        
        # 복구 시뮬레이션 (노드 uncordon)
        for NODE in \$NODE_LIST; do
          echo "Recovering node \$NODE..."
          kubectl uncordon \$NODE
        done
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### GitOps 기반 멀티클러스터")
        st.markdown("""
        GitOps 방식을 사용하여 여러 EKS 클러스터를 관리하는 고급 실습 프로젝트입니다.
        
        **프로젝트 개요**:
        - 3개의 환경(개발, 스테이징, 프로덕션)을 위한 별도 클러스터 구성
        - ArgoCD를 사용하여 모든 클러스터에 일관된 구성 적용
        - 환경별 구성 차이를 관리하기 위한 Kustomize 사용
        - 코드 변경 시 점진적 배포 자동화
        
        **구현 단계**:
        ```bash
        # 1. 멀티 클러스터 생성
        eksctl create cluster --name eks-dev --region us-west-2
        eksctl create cluster --name eks-staging --region us-west-2
        eksctl create cluster --name eks-prod --region us-west-2 --nodes 3 --nodes-min 3 --nodes-max 6
        ```
        
        ```bash
        # 2. 각 클러스터의 kubeconfig 설정
        aws eks update-kubeconfig --name eks-dev --alias eks-dev
        aws eks update-kubeconfig --name eks-staging --alias eks-staging
        aws eks update-kubeconfig --name eks-prod --alias eks-prod
        ```
        
        ```bash
        # 3. ArgoCD 설치 (중앙 관리 클러스터)
        kubectl config use-context eks-dev
        kubectl create namespace argocd
        kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
        ```
        
        **GitOps 레포지토리 구조**:
        ```
        gitops-repo/
        ├── base/                       # 기본 매니페스트
        │   ├── deployment.yaml
        │   ├── service.yaml
        │   ├── configmap.yaml
        │   └── kustomization.yaml
        │
        ├── overlays/                   # 환경별 오버레이
        │   ├── dev/
        │   │   ├── kustomization.yaml  # 개발 환경 설정
        │   │   └── env-config.yaml
        │   │
        │   ├── staging/
        │   │   ├── kustomization.yaml  # 스테이징 환경 설정
        │   │   └── env-config.yaml
        │   │
        │   └── prod/
        │       ├── kustomization.yaml  # 프로덕션 환경 설정
        │       └── env-config.yaml
        │
        ├── clusters/                   # 클러스터 구성
        │   ├── dev-cluster.yaml
        │   ├── staging-cluster.yaml
        │   └── prod-cluster.yaml
        │
        └── infra/                      # 인프라 구성요소
            ├── monitoring/
            ├── ingress-controller/
            └── cert-manager/
        ```
        
        **ArgoCD 애플리케이션 설정**:
        ```yaml
        # 클러스터 추가
        apiVersion: v1
        kind: Secret
        metadata:
          name: eks-staging-cluster
          namespace: argocd
          labels:
            argocd.argoproj.io/secret-type: cluster
        type: Opaque
        stringData:
          name: eks-staging
          server: https://STAGING_CLUSTER_ENDPOINT
          config: |
            {
              "bearerToken": "STAGING_SERVICE_ACCOUNT_TOKEN",
              "tlsClientConfig": {
                "caData": "STAGING_CLUSTER_CA_DATA"
              }
            }
        ---
        # AppProject 정의
        apiVersion: argoproj.io/v1alpha1
        kind: AppProject
        metadata:
          name: microservices
          namespace: argocd
        spec:
          description: Microservices Applications
          sourceRepos:
          - 'https://github.com/myorg/gitops-repo.git'
          destinations:
          - namespace: '*'
            server: https://kubernetes.default.svc  # dev cluster
          - namespace: '*'
            server: https://STAGING_CLUSTER_ENDPOINT  # staging cluster
          - namespace: '*'
            server: https://PROD_CLUSTER_ENDPOINT  # prod cluster
          clusterResourceWhitelist:
          - group: '*'
            kind: '*'
        ---
        # ApplicationSet 사용한 멀티클러스터 배포
        apiVersion: argoproj.io/v1alpha1
        kind: ApplicationSet
        metadata:
          name: microservice-appset
          namespace: argocd
        spec:
          generators:
          - matrix:
              generators:
              - list:
                  elements:
                  - cluster: eks-dev
                    url: https://kubernetes.default.svc
                    env: dev
                  - cluster: eks-staging
                    url: https://STAGING_CLUSTER_ENDPOINT
                    env: staging
                  - cluster: eks-prod
                    url: https://PROD_CLUSTER_ENDPOINT
                    env: prod
              - list:
                  elements:
                  - name: api
                    namespace: backend
                  - name: frontend
                    namespace: frontend
                  - name: auth
                    namespace: auth
          template:
            metadata:
              name: '{{env}}-{{name}}'
            spec:
              project: microservices
              source:
                repoURL: https://github.com/myorg/gitops-repo.git
                targetRevision: main
                path: 'overlays/{{env}}/{{name}}'
              destination:
                server: '{{url}}'
                namespace: '{{namespace}}'
              syncPolicy:
                automated:
                  prune: true
                  selfHeal: true
                syncOptions:
                - CreateNamespace=true
        ```
        
        **점진적 배포 파이프라인(GitHub Actions + ArgoCD)**:
        ```yaml
        # .github/workflows/progressive-deploy.yaml
        name: Progressive Deployment
        
        on:
          push:
            branches:
              - main
            paths:
              - 'src/**'
              
        jobs:
          build:
            runs-on: ubuntu-latest
            steps:
            - uses: actions/checkout@v3
            
            - name: Build and push Docker image
              uses: docker/build-push-action@v4
              with:
                context: .
                push: true
                tags: \${{ secrets.DOCKER_REGISTRY }}/app:\${{ github.sha }}
        
          update-dev:
            needs: build
            runs-on: ubuntu-latest
            steps:
            - uses: actions/checkout@v3
            
            - name: Update dev manifest
              run: |
                cd gitops-repo/overlays/dev
                kustomize edit set image app=\${{ secrets.DOCKER_REGISTRY }}/app:\${{ github.sha }}
                git config user.name "GitHub Actions"
                git config user.email "actions@github.com"
                git add .
                git commit -m "Update dev image to \${{ github.sha }}"
                git push
        
          # 스테이징 → 프로덕션으로 점진적 배포
          promote-to-staging:
            needs: update-dev
            runs-on: ubuntu-latest
            environment: 'staging'  # 승인 환경으로 설정
            steps:
            - uses: actions/checkout@v3
            
            - name: Update staging manifest
              run: |
                cd gitops-repo/overlays/staging
                kustomize edit set image app=\${{ secrets.DOCKER_REGISTRY }}/app:\${{ github.sha }}
                git config user.name "GitHub Actions"
                git config user.email "actions@github.com"
                git add .
                git commit -m "Update staging image to \${{ github.sha }}"
                git push
        
          promote-to-production:
            needs: promote-to-staging
            runs-on: ubuntu-latest
            environment: 'production'  # 승인 환경으로 설정
            steps:
            - uses: actions/checkout@v3
            
            - name: Update production manifest
              run: |
                cd gitops-repo/overlays/prod
                kustomize edit set image app=\${{ secrets.DOCKER_REGISTRY }}/app:\${{ github.sha }}
                git config user.name "GitHub Actions"
                git config user.email "actions@github.com"
                git add .
                git commit -m "Update production image to \${{ github.sha }}"
                git push
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### 서비스 메시 구현")
        st.markdown("""
        Istio 서비스 메시를 사용하여 마이크로서비스 아키텍처를 구현하는 실습 프로젝트입니다.
        
        **프로젝트 개요**:
        - 6개 마이크로서비스로 구성된 이커머스 애플리케이션
        - Istio를 사용한 고급 트래픽 관리
        - 서비스 간 인증 및 통신 보안
        - 분산 추적 및 관찰성 구현
        
        **구현 단계**:
        
        ```bash
        # 1. EKS 클러스터 준비
        eksctl create cluster \\
          --name service-mesh-cluster \\
          --region us-west-2 \\
          --nodes 3 \\
          --node-type m5.xlarge
        ```
        
        ```bash
        # 2. Istio 설치
        curl -L https://istio.io/downloadIstio | sh -
        cd istio-*
        export PATH=\$PWD/bin:\$PATH
        
        # Istio 설치 (데모 프로필)
        istioctl install --set profile=demo -y
        
        # 기본 네임스페이스에 자동 사이드카 주입 활성화
        kubectl label namespace default istio-injection=enabled
        ```
        
        ```bash
        # 3. 애드온 설치 (관찰성)
        kubectl apply -f samples/addons/prometheus.yaml
        kubectl apply -f samples/addons/grafana.yaml
        kubectl apply -f samples/addons/jaeger.yaml
        kubectl apply -f samples/addons/kiali.yaml
        ```
        
        **마이크로서비스 아키텍처 다이어그램**:
        ```
        [ Frontend ] → [ Gateway API ] → [ Auth Service ]
              ↓                ↓              ↑ 
        [ Catalog ] ← [ Cart Service ] → [ Payment Service ]
              ↓
        [ Product DB ]
        ```
        
        **마이크로서비스 배포**:
        ```yaml
        # 각 마이크로서비스 배포 예시 (frontend)
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: frontend
          labels:
            app: frontend
            version: v1
        spec:
          replicas: 2
          selector:
            matchLabels:
              app: frontend
              version: v1
          template:
            metadata:
              labels:
                app: frontend
                version: v1
            spec:
              containers:
              - name: frontend
                image: ecommerce/frontend:v1
                ports:
                - containerPort: 8080
                env:
                - name: API_GATEWAY_URL
                  value: http://gateway:8080
        ---
        apiVersion: v1
        kind: Service
        metadata:
          name: frontend
        spec:
          selector:
            app: frontend
          ports:
          - port: 8080
            name: http
        ```
        
        **Istio 게이트웨이 및 가상 서비스 구성**:
        ```yaml
        # Istio 인그레스 게이트웨이
        apiVersion: networking.istio.io/v1alpha3
        kind: Gateway
        metadata:
          name: ecommerce-gateway
        spec:
          selector:
            istio: ingressgateway
          servers:
          - port:
              number: 80
              name: http
              protocol: HTTP
            hosts:
            - "*"
        ---
        # 프론트엔드 라우팅
        apiVersion: networking.istio.io/v1alpha3
        kind: VirtualService
        metadata:
          name: frontend
        spec:
          hosts:
          - "*"
          gateways:
          - ecommerce-gateway
          http:
          - match:
            - uri:
                prefix: /
            route:
            - destination:
                host: frontend
                port:
                  number: 8080
        ```
        
        **서비스 간 통신에 대한 보안 정책**:
        ```yaml
        # 상호 TLS 정책
        apiVersion: security.istio.io/v1beta1
        kind: PeerAuthentication
        metadata:
          name: default
          namespace: default
        spec:
          mtls:
            mode: STRICT
        ---
        # 서비스 간 인증 정책
        apiVersion: security.istio.io/v1beta1
        kind: AuthorizationPolicy
        metadata:
          name: gateway-policy
          namespace: default
        spec:
          selector:
            matchLabels:
              app: gateway
          rules:
          - from:
            - source:
                principals: ["cluster.local/ns/default/sa/frontend-sa"]
            to:
            - operation:
                methods: ["GET", "POST"]
        ```
        
        **A/B 테스팅과 점진적 롤아웃**:
        ```yaml
        # 두 버전의 카탈로그 서비스 배포
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: catalog-v2
          labels:
            app: catalog
            version: v2
        spec:
          replicas: 1
          selector:
            matchLabels:
              app: catalog
              version: v2
          template:
            metadata:
              labels:
                app: catalog
                version: v2
            spec:
              containers:
              - name: catalog
                image: ecommerce/catalog:v2
                ports:
                - containerPort: 8080
        ---
        # A/B 테스트를 위한 가상 서비스 구성
        apiVersion: networking.istio.io/v1alpha3
        kind: VirtualService
        metadata:
          name: catalog
        spec:
          hosts:
          - catalog
          http:
          - match:
            - headers:
                end-user:
                  exact: beta-tester
            route:
            - destination:
                host: catalog
                subset: v2
          - route:
            - destination:
                host: catalog
                subset: v1
                weight: 90
            - destination:
                host: catalog
                subset: v2
                weight: 10
        ---
        # 서브셋 정의
        apiVersion: networking.istio.io/v1alpha3
        kind: DestinationRule
        metadata:
          name: catalog
        spec:
          host: catalog
          subsets:
          - name: v1
            labels:
              version: v1
          - name: v2
            labels:
              version: v2
        ```
        
        **회복성 패턴 구현**:
        ```yaml
        # 서킷 브레이커 설정
        apiVersion: networking.istio.io/v1alpha3
        kind: DestinationRule
        metadata:
          name: payments
        spec:
          host: payments
          trafficPolicy:
            connectionPool:
              tcp:
                maxConnections: 100
              http:
                http1MaxPendingRequests: 10
                maxRequestsPerConnection: 10
            outlierDetection:
              consecutive5xxErrors: 5
              interval: 30s
              baseEjectionTime: 30s
              maxEjectionPercent: 100
        ---
        # 타임아웃 및 재시도 정책
        apiVersion: networking.istio.io/v1alpha3
        kind: VirtualService
        metadata:
          name: cart-timeout
        spec:
          hosts:
          - cart
          http:
          - route:
            - destination:
                host: cart
            timeout: 3s
            retries:
              attempts: 3
              perTryTimeout: 1s
              retryOn: gateway-error,connect-failure,refused-stream
        ```
        
        **관찰성 대시보드 접근**:
        ```bash
        # Kiali 대시보드
        istioctl dashboard kiali
        
        # Grafana 대시보드
        istioctl dashboard grafana
        
        # Jaeger UI
        istioctl dashboard jaeger
        
        # 테스트 트래픽 생성
        for i in {1..100}; do
          curl -s -o /dev/null http://\$(kubectl get svc istio-ingressgateway -n istio-system -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
          sleep 0.5
        done
        ```
        """)
        
        # 다음 학습 추천 섹션 추가
        st.markdown("""
        <div class="next-learning">
            <h4>다음 단계</h4>
            <p>축하합니다! 고급 과정의 주요 프로젝트들을 완료하셨습니다. 이제 다음 단계로 진행할 수 있습니다:</p>
            <ul>
                <li>학습한 기술을 실제 환경에 적용해보세요.</li>
                <li>특정 주제에 대해 더 깊이 있는 전문성을 개발하세요.</li>
                <li>Kubernetes 커뮤니티에 기여하고 최신 동향을 계속 탐색하세요.</li>
                <li>자체 커스텀 컨트롤러나 오퍼레이터를 개발해 보세요.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 복습 섹션
    st.markdown("<h2 class='section-title'>개념 정리 및 복습</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="review-section">
        <h3 class="review-title">고급 과정 요약</h3>
        <div class="review-content">
            <p>EKS와 Kubernetes 고급 과정에서 다룬 주요 개념들을 정리합니다.</p>
            
            <h4>1. 확장성과 커스터마이징</h4>
            <ul>
                <li><strong>CRD</strong>: Kubernetes API를 확장하여 사용자 정의 리소스 생성</li>
                <li><strong>Operator</strong>: 특정 애플리케이션의 운영 지식을 자동화하는 패턴</li>
                <li><strong>커스텀 컨트롤러</strong>: 사용자 정의 리소스의 라이프사이클 관리</li>
                <li><strong>고급 스케줄링</strong>: 어피니티, 안티-어피니티, taint, toleration 활용</li>
            </ul>
            
            <h4>2. 고급 배포 전략</h4>
            <ul>
                <li><strong>GitOps</strong>: Git을 단일 진실 원천으로 사용하는 배포 방법론</li>
                <li><strong>ArgoCD/FluxCD</strong>: GitOps 구현을 위한 도구</li>
                <li><strong>블루/그린 배포</strong>: 두 환경을 준비하고 트래픽을 한 번에 전환</li>
                <li><strong>카나리 배포</strong>: 새 버전을 점진적으로 출시하여 위험 최소화</li>
                <li><strong>프로그레시브 딜리버리</strong>: 특성 플래그, A/B 테스트를 통한 점진적 기능 릴리스</li>
            </ul>
            
            <h4>3. 네트워킹과 서비스 메시</h4>
            <ul>
                <li><strong>Calico CNI</strong>: 고급 네트워킹 정책 및 BGP 설정</li>
                <li><strong>고급 네트워크 정책</strong>: 마이크로서비스 간 세분화된 통신 제어</li>
                <li><strong>Istio</strong>: 고급 트래픽 관리, 보안, 관찰성 기능</li>
                <li><strong>멀티클러스터 네트워킹</strong>: 클러스터 간 연결 및 서비스 디스커버리</li>
            </ul>
            
            <h4>4. 보안 강화</h4>
            <ul>
                <li><strong>Pod Security Standards</strong>: Privileged, Baseline, Restricted 수준 보안</li>
                <li><strong>이미지 스캐닝</strong>: 취약점 탐지 및 공급망 보안</li>
                <li><strong>런타임 보안</strong>: Falco, SecurityContext, AppArmor, Seccomp</li>
                <li><strong>Secret 관리</strong>: HashiCorp Vault와 같은 고급 Secret 관리 도구 통합</li>
            </ul>
            
            <h4>5. 멀티클러스터 관리</h4>
            <ul>
                <li><strong>멀티클러스터 아키텍처 설계</strong>: 지역, 환경, 워크로드 기반 분리</li>
                <li><strong>클러스터간 연결</strong>: VPC 피어링, Transit Gateway, 서비스 메시</li>
                <li><strong>중앙 집중식 관리</strong>: Rancher, ArgoCD, Crossplane 활용</li>
                <li><strong>워크로드 페더레이션</strong>: KubeFed, Velero를 통한 워크로드 이동</li>
            </ul>
            
            <h4>6. 재해 복구 및 백업</h4>
            <ul>
                <li><strong>EKS 백업</strong>: Velero를 사용한 클러스터 상태 및 볼륨 백업</li>
                <li><strong>다중 리전 DR</strong>: Cold, Warm, Hot Standby 전략</li>
                <li><strong>고가용성 아키텍처</strong>: 다중 AZ 배포, 영역 인식 스케줄링</li>
                <li><strong>백업 자동화</strong>: 정기적인 백업, 검증, DR 훈련</li>
            </ul>
            
            <h4>7. 고급 관찰성</h4>
            <ul>
                <li><strong>분산 트레이싱</strong>: Jaeger를 통한 마이크로서비스 요청 흐름 분석</li>
                <li><strong>EFK 스택</strong>: 로그 수집, 저장, 분석 파이프라인 구축</li>
                <li><strong>사용자 정의 메트릭</strong>: 애플리케이션별 맞춤 메트릭 수집 및 알림</li>
                <li><strong>용량 계획</strong>: 리소스 사용량 분석 및 예측 모델링</li>
            </ul>
            
            <h4>8. AI/ML 워크로드 관리</h4>
            <ul>
                <li><strong>Kubeflow</strong>: 머신러닝 워크플로우 오케스트레이션</li>
                <li><strong>GPU 노드 관리</strong>: 노드 라벨링, 스케줄링, 리소스 공유</li>
                <li><strong>분산 학습</strong>: PyTorch, TensorFlow 분산 훈련 작업 구성</li>
                <li><strong>ML 파이프라인</strong>: 훈련, 검증, 모델 서빙 자동화</li>
            </ul>
            
            <h4>9. 비용 최적화</h4>
            <ul>
                <li><strong>스팟 인스턴스</strong>: 비용 효율적인 스팟 인스턴스 활용 전략</li>
                <li><strong>리소스 요청 최적화</strong>: VPA, Goldilocks를 통한 리소스 튜닝</li>
                <li><strong>워크로드 스케줄링</strong>: bin-packing, Descheduler, Karpenter 활용</li>
                <li><strong>비용 모니터링</strong>: 태깅, 네임스페이스별 비용 할당, Kubecost</li>
            </ul>
            
            <h4>고급 EKS 관리를 위한 핵심 명령어</h4>
            <div class="code-block">
            # CRD 생성
            kubectl apply -f my-crd.yaml
            
            # 클러스터 간 컨텍스트 전환
            kubectl config use-context my-cluster
            
            # 사용자 정의 메트릭 활성화
            kubectl apply -f custom-metrics-apiserver/
            
            # Pod 보안 표준 적용
            kubectl label namespace my-namespace pod-security.kubernetes.io/enforce=restricted
            
            # Velero로 클러스터 백업
            velero backup create my-backup --include-namespaces app1,app2
            
            # 멀티클러스터 애플리케이션 배포 (ArgoCD)
            argocd app create my-app --repo https://github.com/org/repo.git --path manifests --dest-server https://cluster1 --dest-namespace app
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 마무리 및 학습 완료 메시지
    st.markdown("""
    <div class="next-learning" style="margin-top: 40px;">
        <h4>EKS 학습 여정 완료</h4>
        <p>축하합니다! Amazon EKS에 대한 종합적인 학습 여정을 완료하셨습니다. 기본부터 고급 주제까지 다양한 개념과 기술을 배웠습니다.</p>
        <p>계속해서 실습하고, 최신 기술 동향을 탐색하세요. AWS와 Kubernetes 업데이트를 지속적으로 확인하는 것도 중요합니다.</p>
        <ul>
            <li><a href="/?page=beginner">기본 과정 복습하기 →</a> (기초 개념 다시 살펴보기)</li>
            <li><a href="/?page=intermediate">중급 과정 복습하기 →</a> (심화 개념 다시 살펴보기)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)