import streamlit as st
from utils.localization import t
from services.analytics.usage_tracker import UsageTracker

def render_intermediate():
    """중급 과정 메인 페이지 - 개선된 디자인 및 이동 경로 추가"""
    
    # 사용 추적
    UsageTracker.track_page_view("intermediate")
    
    # 공통 스타일 정의 - 학습 경로 네비게이션 스타일 추가
    st.markdown("""
    <style>
    /* 색상 변수 */
    :root {
        --yellow-color: #ffb703;
        --yellow-light: #fff8e6;
        --divider-color: #e0e0e0;  /* 회색 구분선 */
        --blue-color: #4361ee;     /* 기본 색상 */
        --red-color: #e63946;      /* 고급 색상 */
        --nav-bg-color: #f8f9fa;
    }

    /* 페이지 제목 - "중급"을 더 크게 */
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
        background-color: var(--yellow-light);
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
        background-color: var(--yellow-light);
        border-radius: 4px;
        font-size: 0.85rem;
    }
    
    .related-module-link a {
        color: var(--yellow-color);
        text-decoration: none;
        font-weight: 600;
    }
    
    .related-module-link a:hover {
        text-decoration: underline;
    }
    
    /* 선수 지식 표시 */
    .prerequisite {
        margin-top: 5px;
        font-size: 0.8rem;
        color: #666;
        font-style: italic;
    }
    
    .prerequisite a {
        color: var(--blue-color);
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
        border-top: 5px solid var(--yellow-color);
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
        background-color: var(--yellow-color);
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
        color: var(--yellow-color);
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
        color: var(--yellow-color);
    }

    /* 인트로 카드 */
    .intro-card {
        background-color: var(--yellow-light);
        border-left: 4px solid var(--yellow-color);
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
        color: var(--yellow-color) !important;
        border-bottom: 2px solid var(--yellow-color) !important;
    }

    /* 선택된 탭 스타일 */
    .stTabs [aria-selected="true"] {
        color: var(--yellow-color) !important;
        border-bottom: 2px solid var(--yellow-color) !important;
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
        background-color: var(--yellow-light);
        border-radius: 6px;
        border-left: 4px solid var(--yellow-color);
    }
    
    .next-learning h4 {
        margin-top: 0 !important;
        color: var(--yellow-color) !important;
    }
    
    .next-learning ul {
        margin-bottom: 0;
    }

    /* 탭 내용 제목 스타일 */
    .tab-content h3 {
        font-size: 1.5rem !important;
        margin-top: 25px !important;
        margin-bottom: 15px !important;
        color: var(--yellow-color) !important;
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
        border-left: 4px solid var(--yellow-color);
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
        color: var(--yellow-color) !important;
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
        <div class="nav-item">
            <a href="/?page=beginner" class="beginner-nav">기본 과정</a>
        </div>
        <div class="nav-item current">
            <span class="intermediate-nav">중급 과정</span>
        </div>
        <div class="nav-item">
            <a href="/?page=advanced" class="advanced-nav">고급 과정</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 인트로 설명
    st.markdown("""
    <div class="intro-card">
        Kubernetes와 EKS의 기본 개념을 이해한 사용자를 위한 심화 학습 내용입니다.
        고급 리소스, 보안 설정, 모니터링 구성, CI/CD 통합, 자동 크기 조정 등을 다룹니다.
    </div>
    """, unsafe_allow_html=True)
    
    # 모듈 정의 - 내용 정리 및 학습 경로 추가
    modules = [
        {
            "id": "k8s_advanced",
            "title": "Kubernetes 심화",
            "icon": "K",
            "description": "고급 Kubernetes 리소스 및 패턴을 학습합니다. StatefulSet, DaemonSet, ConfigMap, Secret 등을 다룹니다.",
            "topics": ["StatefulSet과 DaemonSet", "ConfigMap과 Secret", "PersistentVolume", "기본 네트워킹"],
            "prerequisites": ["kubernetes_intro"],
            "next_modules": {
                "advanced": "k8s_advanced"
            }
        },
        {
            "id": "eks_management",
            "title": "EKS 관리와 운영",
            "icon": "M",
            "description": "EKS 클러스터 인프라 관리, IAM 통합, 로드 밸런서 설정 등을 배웁니다.",
            "topics": ["Terraform/CDK를 이용한 IaC", "IAM과 RBAC 통합", "AWS Load Balancer Controller"],
            "prerequisites": ["eks_basics"],
            "next_modules": {
                "advanced": "networking"
            }
        },
        {
            "id": "scaling_eks",
            "title": "EKS 자동 크기 조정",
            "icon": "S",
            "description": "Amazon EKS에서 수요에 따른 자동 크기 조정 메커니즘 구현 방법을 학습합니다.",
            "topics": ["Horizontal Pod Autoscaler", "Vertical Pod Autoscaler", "Cluster Autoscaler", "Karpenter"],
            "prerequisites": ["eks_basics"],
            "next_modules": {}
        },
        {
            "id": "eks_storage",
            "title": "EKS 스토리지 관리",
            "icon": "V",
            "description": "Amazon EKS에서 EBS, EFS 등 다양한 스토리지 옵션과 영구 볼륨 관리 방법을 학습합니다.",
            "topics": ["Amazon EBS 통합", "Amazon EFS 통합", "Secret 관리", "스토리지 설계 패턴"],
            "prerequisites": ["storage_basics"],
            "next_modules": {
                "advanced": "security"
            }
        },
        {
            "id": "helm_advanced",
            "title": "Helm & 패키지 관리",
            "icon": "H",
            "description": "Helm 차트 사용자 정의, 저장소 관리 등 Kubernetes 패키지 관리 방법을 심화 학습합니다.",
            "topics": ["차트 커스터마이징", "Helm 저장소 관리", "Helm 릴리스 관리", "차트 개발"],
            "prerequisites": ["helm_basics"],
            "next_modules": {}
        },
        {
            "id": "serverless_advanced",
            "title": "서버리스 EKS 심화",
            "icon": "F",
            "description": "EKS Fargate의 고급 구성, 최적화 전략, 프로필 설계 등을 학습합니다.",
            "topics": ["Fargate 프로필 고급 설계", "EKS on Fargate 최적화", "하이브리드 노드 구성", "보안 강화"],
            "prerequisites": ["serverless_intro"],
            "next_modules": {
                "advanced": "security"
            }
        },
        {
            "id": "cicd_basics",
            "title": "CI/CD 및 GitOps",
            "icon": "C",
            "description": "GitHub Actions, AWS CodePipeline 등 CI/CD 파이프라인 구축 방법과 GitOps 기본 개념을 배웁니다.",
            "topics": ["CI/CD 파이프라인 개념", "GitHub Actions 활용", "GitOps 원칙", "AWS CodePipeline 설정"],
            "prerequisites": ["kubernetes_intro"],
            "next_modules": {
                "advanced": "gitops_cicd"
            }
        },
        {
            "id": "monitoring_basics",
            "title": "모니터링 기초",
            "icon": "G",
            "description": "Prometheus, Grafana, CloudWatch를 활용한 모니터링 및 알림 설정 방법을 학습합니다.",
            "topics": ["Prometheus 설치 및 구성", "Grafana 대시보드", "CloudWatch 로그 통합", "알림 설정"],
            "prerequisites": ["kubernetes_intro"],
            "next_modules": {
                "advanced": "observability"
            }
        },
        {
            "id": "service_mesh_intro",
            "title": "서비스 메시 소개",
            "icon": "I",
            "description": "서비스 메시의 기본 개념과 Istio의 기초 활용법을 배웁니다.",
            "topics": ["서비스 메시 개념", "Istio 구성요소", "트래픽 관리 기초", "간단한 메시 구성"],
            "prerequisites": ["kubernetes_intro"],
            "next_modules": {
                "advanced": "networking"
            }
        },
        {
            "id": "intermediate_projects",
            "title": "중급 실습 프로젝트",
            "icon": "P",
            "description": "다양한 중급 수준의 실습 프로젝트를 통해 학습한 내용을 실제로 적용해봅니다.",
            "topics": ["마이크로서비스 배포", "CI/CD 파이프라인 구축", "데이터베이스 연동 애플리케이션"],
            "prerequisites": ["basic_projects"],
            "next_modules": {
                "advanced": "advanced_projects"
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
                    # 선수 지식 표시
                    prereq_html = ""
                    if "prerequisites" in module and module["prerequisites"]:
                        prereq_links = []
                        for prereq in module["prerequisites"]:
                            prereq_title = prereq.replace("_", " ").title()
                            prereq_links.append(f'<a href="/?page=beginner#{prereq}">{prereq_title}</a>')
                        prereq_html = f"""
                        <div class="prerequisite">
                            선수 지식: {", ".join(prereq_links)}
                        </div>
                        """
                        
                    # 관련 모듈 링크 추가
                    next_module_html = ""
                    if "next_modules" in module and "advanced" in module["next_modules"]:
                        next_id = module["next_modules"]["advanced"]
                        next_title = next_id.replace("_", " ").title()
                        next_module_html = f"""
                        <div class="related-module-link">
                            <span>고급 학습: </span>
                            <a href="/?page=advanced#{next_id}">{next_title} →</a>
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
                            {next_module_html}
                        </div>
                        """, unsafe_allow_html=True)
    
    # 탭 인터페이스로 각 모듈의 세부 내용 표시
    st.markdown("<h2 class='section-title'>학습 내용</h2>", unsafe_allow_html=True)
    
    tabs = st.tabs([module["title"] for module in modules])
    
    # Kubernetes 심화 탭
    with tabs[0]:
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        st.markdown("### 고급 Kubernetes 리소스")
        st.markdown("""
        **StatefulSet**: 상태 유지가 필요한 애플리케이션(데이터베이스 등)을 위한 워크로드 API입니다.

        ```yaml
        apiVersion: apps/v1
        kind: StatefulSet
        metadata:
          name: web
        spec:
          serviceName: "nginx"
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
                image: nginx:1.14.2
                ports:
                - containerPort: 80
                volumeMounts:
                - name: www
                  mountPath: /usr/share/nginx/html
          volumeClaimTemplates:
          - metadata:
              name: www
            spec:
              accessModes: [ "ReadWriteOnce" ]
              resources:
                requests:
                  storage: 1Gi
        ```
        
        **DaemonSet**: 모든 노드 또는 특정 노드에 Pod 복제본을 실행합니다. 모니터링, 로그 수집 등에 유용합니다.

        ```yaml
        apiVersion: apps/v1
        kind: DaemonSet
        metadata:
          name: fluentd
        spec:
          selector:
            matchLabels:
              name: fluentd
          template:
            metadata:
              labels:
                name: fluentd
            spec:
              containers:
              - name: fluentd
                image: fluent/fluentd:v1.10
                resources:
                  limits:
                    memory: 200Mi
                  requests:
                    cpu: 100m
                    memory: 100Mi
                volumeMounts:
                - name: varlog
                  mountPath: /var/log
                - name: varlibdockercontainers
                  mountPath: /var/lib/docker/containers
                  readOnly: true
              volumes:
              - name: varlog
                hostPath:
                  path: /var/log
              - name: varlibdockercontainers
                hostPath:
                  path: /var/lib/docker/containers
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### ConfigMap과 Secret")
        st.markdown("""
        **ConfigMap**: 애플리케이션 구성 데이터를 키-값 쌍으로 저장합니다.
        
        ```yaml
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: app-config
        data:
          app.properties: |
            environment=dev
            log_level=info
            cache_size=100
          ui.properties: |
            theme=dark
            language=ko
        ```
        
        ConfigMap을 Pod에 마운트하는 예:
        
        ```yaml
        apiVersion: v1
        kind: Pod
        metadata:
          name: config-pod
        spec:
          containers:
          - name: app
            image: myapp:latest
            volumeMounts:
            - name: config-volume
              mountPath: /etc/config
          volumes:
          - name: config-volume
            configMap:
              name: app-config
        ```
        
        **Secret**: 암호, API 키 등 민감한 정보를 저장합니다.
        
        ```yaml
        apiVersion: v1
        kind: Secret
        metadata:
          name: db-secret
        type: Opaque
        data:
          username: YWRtaW4=  # base64로 인코딩된 'admin'
          password: cGFzc3cwcmQ=  # base64로 인코딩된 'passw0rd'
        ```
        
        Secret을 환경 변수로 사용하는 예:
        
        ```yaml
        apiVersion: v1
        kind: Pod
        metadata:
          name: secret-pod
        spec:
          containers:
          - name: db-client
            image: mysql:client
            env:
            - name: DB_USERNAME
              valueFrom:
                secretKeyRef:
                  name: db-secret
                  key: username
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: db-secret
                  key: password
        ```
        """)
        
        # 다음 학습 추천 섹션 추가
        st.markdown("""
        <div class="next-learning">
            <h4>다음 학습 추천</h4>
            <ul>
                <li>Kubernetes의 심화 개념을 더 깊이 학습하려면 <a href="/?page=advanced#k8s_advanced">고급 Kubernetes</a> 모듈에서 CRD, Operator 패턴 등을 학습하세요.</li>
                <li>상태 유지가 필요한 애플리케이션을 위해 <a href="/?page=intermediate#eks_storage">EKS 스토리지 관리</a> 모듈을 함께 학습하는 것이 좋습니다.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # EKS 관리와 운영 탭
    with tabs[1]:
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        st.markdown("### 인프라 as 코드(IaC)로 EKS 관리")
        st.markdown("""
        **Terraform으로 EKS 클러스터 생성**
        
        ```hcl
        provider "aws" {
          region = "us-west-2"
        }
        
        module "eks" {
          source          = "terraform-aws-modules/eks/aws"
          version         = "17.24.0"
          cluster_name    = "my-eks-cluster"
          cluster_version = "1.27"
          subnets         = ["subnet-abcde012", "subnet-bcde012a"]
        
          vpc_id = "vpc-1234556abcdef"
        
          node_groups = {
            eks_nodes = {
              desired_capacity = 3
              max_capacity     = 5
              min_capacity     = 1
        
              instance_type = "t3.medium"
              key_name      = "my-key"
            }
          }
        }
        ```
        
        **AWS CDK로 EKS 클러스터 생성 (TypeScript)**
        
        ```typescript
        import * as cdk from 'aws-cdk-lib';
        import * as eks from 'aws-cdk-lib/aws-eks';
        import * as ec2 from 'aws-cdk-lib/aws-ec2';
        import { Construct } from 'constructs';
        
        export class EksClusterStack extends cdk.Stack {
          constructor(scope: Construct, id: string, props?: cdk.StackProps) {
            super(scope, id, props);
        
            // VPC 조회
            const vpc = ec2.Vpc.fromLookup(this, 'VPC', {
              vpcId: 'vpc-1234556abcdef'
            });
        
            // EKS 클러스터 생성
            const cluster = new eks.Cluster(this, 'MyCluster', {
              version: eks.KubernetesVersion.V1_27,
              vpc: vpc,
              defaultCapacity: 3,
              defaultCapacityInstance: ec2.InstanceType.of(
                ec2.InstanceClass.T3, 
                ec2.InstanceSize.MEDIUM
              )
            });
          }
        }
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### IAM과 RBAC 통합")
        st.markdown("""
        **EKS의 IAM과 Kubernetes RBAC 통합**
        
        AWS IAM 엔티티를 Kubernetes RBAC 시스템의 사용자 및 그룹에 매핑합니다.
        
        ```bash
        # AWS IAM 사용자/역할을 Kubernetes RBAC에 매핑하는 ConfigMap
        cat > aws-auth-cm.yaml << EOF
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: aws-auth
          namespace: kube-system
        data:
          mapRoles: |
            - rolearn: arn:aws:iam::ACCOUNT_ID:role/EKSNodeRole
              username: system:node:{{EC2PrivateDNSName}}
              groups:
                - system:bootstrappers
                - system:nodes
            - rolearn: arn:aws:iam::ACCOUNT_ID:role/DevTeamRole
              username: dev-team
              groups:
                - developers
          mapUsers: |
            - userarn: arn:aws:iam::ACCOUNT_ID:user/admin
              username: admin
              groups:
                - system:masters
        EOF
        
        kubectl apply -f aws-auth-cm.yaml
        ```
        
        **RBAC 역할 및 역할 바인딩 정의**
        
        ```yaml
        # 개발자 역할 생성
        kind: Role
        apiVersion: rbac.authorization.k8s.io/v1
        metadata:
          namespace: default
          name: developer
        rules:
        - apiGroups: ["", "apps"]
          resources: ["deployments", "pods", "services"]
          verbs: ["get", "list", "watch", "create", "update", "patch"]
          
        ---
        # 역할 바인딩 생성
        kind: RoleBinding
        apiVersion: rbac.authorization.k8s.io/v1
        metadata:
          name: developer-binding
          namespace: default
        subjects:
        - kind: User
          name: dev-team
          apiGroup: rbac.authorization.k8s.io
        roleRef:
          kind: Role
          name: developer
          apiGroup: rbac.authorization.k8s.io
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### AWS Load Balancer Controller")
        st.markdown("""
        **AWS Load Balancer Controller 설치**
        
        ```bash
        # IAM 정책 생성
        curl -o iam-policy.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/main/docs/install/iam_policy.json
        
        aws iam create-policy \\
            --policy-name AWSLoadBalancerControllerIAMPolicy \\
            --policy-document file://iam-policy.json
        
        # eksctl로 서비스 계정 생성
        eksctl create iamserviceaccount \\
          --cluster=my-eks-cluster \\
          --namespace=kube-system \\
          --name=aws-load-balancer-controller \\
          --attach-policy-arn=arn:aws:iam::ACCOUNT_ID:policy/AWSLoadBalancerControllerIAMPolicy \\
          --approve
          
        # Helm으로 AWS Load Balancer Controller 설치
        helm repo add eks https://aws.github.io/eks-charts
        helm repo update
        
        helm install aws-load-balancer-controller eks/aws-load-balancer-controller \\
          -n kube-system \\
          --set clusterName=my-eks-cluster \\
          --set serviceAccount.create=false \\
          --set serviceAccount.name=aws-load-balancer-controller
        ```
        
        **ALB Ingress 예제**
        
        ```yaml
        apiVersion: networking.k8s.io/v1
        kind: Ingress
        metadata:
          name: alb-ingress
          annotations:
            kubernetes.io/ingress.class: alb
            alb.ingress.kubernetes.io/scheme: internet-facing
            alb.ingress.kubernetes.io/target-type: ip
        spec:
          rules:
          - http:
              paths:
              - path: /app1
                pathType: Prefix
                backend:
                  service:
                    name: app1-service
                    port:
                      number: 80
              - path: /app2
                pathType: Prefix
                backend:
                  service:
                    name: app2-service
                    port:
                      number: 80
        ```
        """)
        
        # 다음 학습 추천 섹션 추가
        st.markdown("""
        <div class="next-learning">
            <h4>다음 학습 추천</h4>
            <ul>
                <li>EKS의 심화 네트워킹에 대해 학습하려면 <a href="/?page=advanced#networking">네트워킹 고급</a> 모듈을 확인하세요.</li>
                <li>보안이 강화된 EKS 클러스터를 구현하려면 <a href="/?page=advanced#security">보안 강화</a> 모듈이 도움이 될 것입니다.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # EKS 자동 크기 조정 탭
    with tabs[2]:
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        st.markdown("### Amazon EKS에서 자동 크기 조정의 이해")
        st.markdown("""
        Kubernetes는 다양한 자동 크기 조정 메커니즘을 제공하여 워크로드 요구사항에 맞게 클러스터 리소스를 효율적으로 관리합니다.
        
        **수평 및 수직 크기 조정 개념:**
        - **수평 크기 조정**: 리소스의 수를 조정하는 방식 (스케일 인/아웃)
        - **수직 크기 조정**: 리소스의 크기를 조정하는 방식 (스케일 업/다운)
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### Horizontal Pod Autoscaler (HPA)")
        st.markdown("""
        **HPA**는 CPU 사용률이나 사용자 정의 메트릭에 따라 Pod의 수를 자동으로 조정합니다.
        
        **기본 사용법:**
        ```bash
        # 배포에 대해 HPA 생성 (CPU 사용률 50%를 목표로 함)
        kubectl autoscale deployment myapp --cpu-percent=50 --min=3 --max=10
        ```
        
        **YAML로 정의:**
        ```yaml
        apiVersion: autoscaling/v2
        kind: HorizontalPodAutoscaler
        metadata:
          name: myapp-hpa
        spec:
          scaleTargetRef:
            apiVersion: apps/v1
            kind: Deployment
            name: myapp
          minReplicas: 3
          maxReplicas: 10
          metrics:
          - type: Resource
            resource:
              name: cpu
              target:
                type: Utilization
                averageUtilization: 50
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### Vertical Pod Autoscaler (VPA)")
        st.markdown("""
        **VPA**는 Pod에 할당된 CPU 및 메모리 리소스를 자동으로 조정하여 리소스 활용도를 최적화합니다.
        
        **모드:**
        - **Off**: 권장 리소스 계산만 수행 (변경 사항 미적용)
        - **Initial**: 처음 Pod 생성 시에만 리소스 조정
        - **Auto**: 자동으로 Pod를 재시작하여 리소스 조정
        
        **VPA 예제:**
        ```yaml
        apiVersion: autoscaling.k8s.io/v1
        kind: VerticalPodAutoscaler
        metadata:
          name: myapp-vpa
        spec:
          targetRef:
            apiVersion: "apps/v1"
            kind: Deployment
            name: myapp
          updatePolicy:
            updateMode: "Auto"  # "Off", "Initial", "Auto" 중 선택
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### Cluster Autoscaler (CA)")
        st.markdown("""
        **Cluster Autoscaler**는 Pod가 스케줄링되지 않거나 노드 활용도가 낮을 때 EC2 Auto Scaling 그룹의 크기를 자동으로 조정합니다.
        
        **작동 방식:**
        1. 스케줄링 불가능한 Pod가 발견되면 노드 확장
        2. 노드의 활용도가 지정된 임계값 아래로 내려가면 노드 축소 고려
        
        **배포 예제:**
        ```yaml
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: cluster-autoscaler
        spec:
          replicas: 1
          selector:
            matchLabels:
              app: cluster-autoscaler
          template:
            metadata:
              labels:
                app: cluster-autoscaler
            spec:
              containers:
              - name: cluster-autoscaler
                image: k8s.gcr.io/autoscaling/cluster-autoscaler:v1.21.0
                command:
                - ./cluster-autoscaler
                - --cloud-provider=aws
                - --node-group-auto-discovery=asg:tag=k8s.io/cluster-autoscaler/enabled,k8s.io/cluster-autoscaler/my-cluster
                - --balance-similar-node-groups
                - --skip-nodes-with-system-pods=false
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### Karpenter")
        st.markdown("""
        **Karpenter**는 AWS에서 관리하는 오픈소스 Cluster Autoscaler로, Auto Scaling 그룹에 의존하지 않고 최적의 인스턴스를 프로비저닝합니다.
        
        **특징:**
        - Auto Scaling 그룹을 사용하지 않고 EC2 인스턴스 직접 관리
        - 워크로드 요구사항에 맞춰 최적의 인스턴스 유형 선택
        - 더 빠른 확장 속도 및 효율적인 비용 최적화
        
        **Karpenter Provisioner 예제:**
        ```yaml
        apiVersion: karpenter.sh/v1alpha5
        kind: Provisioner
        metadata:
          name: default
        spec:
          requirements:
            - key: "karpenter.sh/capacity-type"
              operator: In
              values: ["spot", "on-demand"]
            - key: "kubernetes.io/arch"
              operator: In
              values: ["amd64", "arm64"]
          limits:
            resources:
              cpu: 1000
              memory: 1000Gi
          ttlSecondsAfterEmpty: 30
          ttlSecondsUntilExpired: 2592000
        ```
        """)
        
        # 다음 학습 추천 섹션 추가
        st.markdown("""
        <div class="next-learning">
            <h4>다음 학습 추천</h4>
            <ul>
                <li>자동 크기 조정을 실제 워크로드에 적용하는 방법은 <a href="/?page=intermediate#intermediate_projects">중급 실습 프로젝트</a>에서 경험해 보세요.</li>
                <li>비용 효율적인 클러스터 관리를 위해 <a href="/?page=intermediate#serverless_advanced">서버리스 EKS 심화</a> 모듈을 함께 학습하세요.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # EKS 스토리지 관리 탭
    with tabs[3]:
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        st.markdown("### AWS 스토리지 서비스를 사용하는 영구 스토리지")
        st.markdown("""
        **Container Storage Interface(CSI) 드라이버**:
        Kubernetes와 스토리지 제공자 간의 표준 인터페이스입니다. AWS는 다양한 스토리지 서비스를 위한 CSI 드라이버를 제공합니다.
        
        **CSI 드라이버 요구사항**:
        1. IAM 정책: 필요한 권한 정의
        2. IAM 역할: 권한 부여
        3. Service Account: Kubernetes와 AWS 서비스 연결
        4. CSI 드라이버 설치
        """)
        
        st.markdown("### Amazon EBS(Elastic Block Store)")
        st.markdown("""
        - EC2 인스턴스를 위한 블록 수준 스토리지
        - 하나의 EBS 볼륨을 한 번에 하나의 노드에만 연결 가능(ReadWriteOnce)
        - 영구 볼륨으로서 EC2 인스턴스와 독립적인 수명 주기
        
        **Amazon EBS 볼륨 유형**:
        - SSD: gp2, gp3(범용), io1, io2(프로비저닝된 IOPS)
        - HDD: st1, sc1(처리량 최적화, 콜드 스토리지)
        
        **Amazon EBS StorageClass 예제**:
        ```yaml
        apiVersion: storage.k8s.io/v1
        kind: StorageClass
        metadata:
          name: ebs-standard
        provisioner: ebs.csi.aws.com
        volumeBindingMode: WaitForFirstConsumer
        allowVolumeExpansion: true
        reclaimPolicy: Delete
        parameters:
          type: gp3
          encrypted: "true"
        ```
        
        **EBS CSI 드라이버 설치**:
        ```bash
        # IAM 정책 추가
        aws iam create-policy \
            --policy-name AmazonEKS_EBS_CSI_Driver_Policy \
            --policy-document file://ebs-csi-policy.json
            
        # 서비스 계정 생성 및 정책 연결
        eksctl create iamserviceaccount \
            --name ebs-csi-controller-sa \
            --namespace kube-system \
            --cluster my-cluster \
            --attach-policy-arn arn:aws:iam::ACCOUNT_ID:policy/AmazonEKS_EBS_CSI_Driver_Policy \
            --approve \
            --region REGION
            
        # EBS CSI 드라이버 설치
        helm repo add aws-ebs-csi-driver https://kubernetes-sigs.github.io/aws-ebs-csi-driver
        helm repo update
        
        helm upgrade --install aws-ebs-csi-driver \
            --namespace kube-system \
            aws-ebs-csi-driver/aws-ebs-csi-driver
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### Amazon EFS(Elastic File System)")
        st.markdown("""
        - 확장 가능하고 탄력적인 완전 관리형 NFS 파일 시스템
        - 여러 EC2 인스턴스에서 동시에 액세스 가능(ReadWriteMany)
        - 여러 가용 영역에 걸쳐 데이터 중복 제공
        - AWS Fargate에서 실행되는 Pod에서도 사용 가능
        
        **Amazon EFS StorageClass 예제**:
        ```yaml
        kind: StorageClass
        apiVersion: storage.k8s.io/v1
        metadata:
          name: efs-sc
        provisioner: efs.csi.aws.com
        parameters:
          provisioningMode: efs-ap
          fileSystemId: fs-92107410
          directoryPerms: "700"
          basePath: "/dynamic_provisioning"
        ```
        
        **EFS CSI 드라이버 설치**:
        ```bash
        # IAM 정책 생성
        curl -o efs-iam-policy.json https://raw.githubusercontent.com/kubernetes-sigs/aws-efs-csi-driver/master/docs/iam-policy-example.json
        
        aws iam create-policy \
            --policy-name AmazonEKS_EFS_CSI_Driver_Policy \
            --policy-document file://efs-iam-policy.json
            
        # 서비스 계정 생성
        eksctl create iamserviceaccount \
            --name efs-csi-controller-sa \
            --namespace kube-system \
            --cluster my-cluster \
            --attach-policy-arn arn:aws:iam::ACCOUNT_ID:policy/AmazonEKS_EFS_CSI_Driver_Policy \
            --approve \
            --region REGION
            
        # EFS CSI 드라이버 설치
        helm repo add aws-efs-csi-driver https://kubernetes-sigs.github.io/aws-efs-csi-driver
        helm repo update
        
        helm upgrade --install aws-efs-csi-driver \
            --namespace kube-system \
            aws-efs-csi-driver/aws-efs-csi-driver
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### Secret 관리")
        st.markdown("""
        **AWS Secrets Manager and Configuration Provider(ASCP)**:
        - Amazon EKS에서 실행되는 Pod가 AWS Secrets Manager의 Secret에 안전하게 액세스
        - Secret을 Pod 파일 시스템에 볼륨으로 마운트 또는 Kubernetes Secret으로 노출
        - 자동 키 교체 기능 지원
        - IRSA를 통한 IAM 정책으로 Secret 액세스 제한
        
        **Kubernetes Secrets Store CSI 드라이버와 ASCP 사용 예**:
        
        SecretProviderClass 정의:
        ```yaml
        apiVersion: secrets-store.csi.x-k8s.io/v1alpha1
        kind: SecretProviderClass
        metadata:
          name: nginx-deployment-aws-secrets
        spec:
          provider: aws
          parameters:
            objects: |
                - objectName: "MySecret"
                  objectType: "secretsmanager"
                  objectAlias: "supersecret"
        ```
        
        배포에 Secret 마운트:
        ```yaml
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: nginx-deployment
          labels:
            app: nginx
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
              serviceAccountName: nginx-deployment-sa
              volumes:
              - name: secrets-store-inline
                csi:
                  driver: secrets-store.csi.k8s.io
                  readOnly: true
                  volumeAttributes:
                    secretProviderClass: "nginx-deployment-aws-secrets"
              containers:
              - name: nginx-deployment
                image: nginx
                ports:
                - containerPort: 80
                volumeMounts:
                - name: secrets-store-inline
                  mountPath: "/mnt/secrets-store"
                  readOnly: true
        ```
        """)
        
        # 다음 학습 추천 섹션 추가
        st.markdown("""
        <div class="next-learning">
            <h4>다음 학습 추천</h4>
            <ul>
                <li>스토리지 보안을 강화하려면 <a href="/?page=advanced#security">보안 강화</a> 모듈을 확인하세요.</li>
                <li>스테이트풀 애플리케이션을 배포하는 실습을 위해 <a href="/?page=intermediate#intermediate_projects">중급 실습 프로젝트</a>를 진행해보세요.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Helm & 패키지 관리 탭
    with tabs[4]:
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        st.markdown("### Helm 차트 커스터마이징")
        st.markdown("""
        Helm 차트를 자신의 환경이나 요구사항에 맞게 커스터마이징하는 방법입니다.
        
        **values.yaml 오버라이딩**:
        ```bash
        # 명령줄에서 값 직접 설정
        helm install my-release bitnami/wordpress \
          --set wordpressBlogName="My Custom Blog" \
          --set wordpressEmail="user@example.com"
        
        # 커스텀 values 파일 사용
        helm install my-release bitnami/wordpress -f my-values.yaml
        ```
        
        **커스텀 values.yaml 예시**:
        ```yaml
        # my-values.yaml
        wordpressUsername: admin
        wordpressPassword: password123
        wordpressEmail: user@example.com
        wordpressBlogName: My Custom Blog
        
        service:
          type: LoadBalancer
        
        resources:
          requests:
            memory: 256Mi
            cpu: 100m
          limits:
            memory: 512Mi
            cpu: 300m
        ```
        
        **여러 values 파일 계층화**:
        ```bash
        # 여러 values 파일 적용 (오른쪽이 우선순위 높음)
        helm install my-release bitnami/wordpress \
          -f common-values.yaml -f dev-values.yaml -f team-overrides.yaml
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### Helm 차트 개발하기")
        st.markdown("""
        자체 Helm 차트를 개발하는 방법입니다.
        
        **새 차트 생성**:
        ```bash
        # 기본 차트 구조 생성
        helm create my-app
        ```
        
        **생성된 디렉토리 구조**:
        ```
        my-app/
        ├── .helmignore    # 패키징 시 무시할 패턴
        ├── Chart.yaml     # 차트 메타데이터
        ├── values.yaml    # 기본 구성 값
        ├── charts/        # 의존성 차트
        └── templates/     # 템플릿 파일
            ├── NOTES.txt  # 사용 설명
            ├── _helpers.tpl
            ├── deployment.yaml
            ├── service.yaml
            └── ...
        ```
        
        **템플릿에서 사용하는 주요 함수**:
        ```
        {{ .Values.key }}              # values.yaml의 값 참조
        {{ .Release.Name }}            # 릴리스 이름
        {{ .Chart.Name }}              # 차트 이름
        {{ include "mychart.name" . }} # 템플릿 include
        {{ if eq .Values.env "prod" }} # 조건문
        {{ range .Values.servers }}    # 반복문
        ```
        
        **차트 린팅과 테스트**:
        ```bash
        # 차트 문법 검증
        helm lint my-app
        
        # 템플릿 렌더링 테스트
        helm template my-app
        
        # 차트 설치 테스트 (실제로 설치하지 않음)
        helm install --dry-run --debug my-release ./my-app
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### Helm 저장소 관리")
        st.markdown("""
        **저장소 추가 및 관리**:
        ```bash
        # 차트 저장소 추가
        helm repo add bitnami https://charts.bitnami.com/bitnami
        
        # 저장소 목록 확인
        helm repo list
        
        # 저장소 업데이트
        helm repo update
        
        # 저장소 제거
        helm repo remove bitnami
        ```
        
        **차트 검색**:
        ```bash
        # 저장소에서 차트 검색
        helm search repo wordpress
        
        # Artifact Hub에서 차트 검색
        helm search hub prometheus
        ```
        
        **OCI 기반 저장소 활용**:
        ```bash
        # 차트 패키징
        helm package ./my-chart
        
        # OCI 저장소 로그인
        helm registry login -u myuser registry.example.com
        
        # 차트 푸시
        helm push my-chart-0.1.0.tgz oci://registry.example.com/charts
        
        # OCI 저장소에서 설치
        helm install my-release oci://registry.example.com/charts/my-chart --version 0.1.0
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### Helm 릴리스 관리")
        st.markdown("""
        **릴리스 업그레이드**:
        ```bash
        # 새 버전이나 값으로 업그레이드
        helm upgrade my-release bitnami/wordpress --version 10.0.5
        
        # 이전 값 재사용하며 업그레이드
        helm upgrade my-release bitnami/wordpress --reuse-values
        
        # 실패한 릴리스 복구
        helm upgrade --atomic --install my-release bitnami/wordpress
        ```
        
        **롤백 기능**:
        ```bash
        # 릴리스 이력 확인
        helm history my-release
        
        # 특정 버전으로 롤백
        helm rollback my-release 2
        
        # 롤백 시 디버그 정보 확인
        helm rollback my-release 2 --debug
        ```
        
        **릴리스 상태 확인**:
        ```bash
        # 모든 릴리스 나열
        helm list --all-namespaces
        
        # 특정 릴리스 상세 상태
        helm status my-release
        
        # 특정 릴리스의 값 확인
        helm get values my-release
        
        # 매니페스트 확인
        helm get manifest my-release
        ```
        """)
        
        # 다음 학습 추천 섹션 추가
        st.markdown("""
        <div class="next-learning">
            <h4>다음 학습 추천</h4>
            <ul>
                <li>Helm을 CI/CD 파이프라인에 통합하는 방법은 <a href="/?page=intermediate#cicd_basics">CI/CD 및 GitOps</a> 모듈에서 학습하세요.</li>
                <li>복잡한 애플리케이션 배포에 Helm을 활용하려면 <a href="/?page=intermediate#intermediate_projects">중급 실습 프로젝트</a>를 진행해보세요.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 서버리스 EKS 심화 탭 (새로 추가)
    with tabs[5]:
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        st.markdown("### Fargate 프로필 고급 설계")
        st.markdown("""
        **세분화된 Fargate 프로필 설계**
        
        프로필을 기능, 환경, 팀 등으로 세분화하여 리소스 격리 및 비용 최적화를 달성합니다.
        
        ```bash
        # 여러 선택기를 가진 Fargate 프로필
        eksctl create fargateprofile \\
          --cluster my-cluster \\
          --name fp-api-prod \\
          --namespace prod \\
          --labels role=api,tier=backend
        
        # 개발 환경용 별도 프로필
        eksctl create fargateprofile \\
          --cluster my-cluster \\
          --name fp-dev \\
          --namespace dev
        
        # 특정 팀용 프로필
        eksctl create fargateprofile \\
          --cluster my-cluster \\
          --name fp-team-alpha \\
          --namespace team-alpha
        ```
        
        **YAML을 사용한 프로필 정의**:
        ```yaml
        # fargate-profiles.yaml
        apiVersion: eksctl.io/v1alpha5
        kind: ClusterConfig
        metadata:
          name: my-cluster
          region: us-east-1
        
        fargateProfiles:
          - name: fp-default
            selectors:
              - namespace: default
              - namespace: kube-system
                labels:
                  k8s-app: kube-dns
          
          - name: fp-apps
            selectors:
              - namespace: apps
                labels:
                  fargate: "true"
          
          - name: fp-batch
            selectors:
              - namespace: batch-jobs
                labels:
                  type: job
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### EKS on Fargate 최적화 전략")
        st.markdown("""
        **컨테이너 리소스 요청 최적화**
        
        Fargate는 다음 vCPU와 메모리 조합만 지원합니다:
        
        | vCPU | 메모리 범위 |
        |------|-------------|
        | 0.25 | 0.5GB, 1GB |
        | 0.5  | 1GB, 2GB |
        | 1    | 2GB, 3GB, 4GB |
        | 2    | 4GB-8GB (1GB 단위) |
        | 4    | 8GB-16GB (1GB 단위) |
        | 8    | 16GB-32GB (4GB 단위) |
        | 16   | 32GB-64GB (8GB 단위) |
        
        ```yaml
        # 최적화된 리소스 요청 예시
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: optimized-app
        spec:
          replicas: 3
          template:
            spec:
              containers:
              - name: app
                image: my-app:latest
                resources:
                  requests:
                    # Fargate 지원 조합으로 최적화
                    cpu: "0.5"    # vCPU
                    memory: "1Gi" # 메모리
                  limits:
                    cpu: "0.5"
                    memory: "1Gi"
        ```
        
        **초기화 시간 최적화**
        
        Fargate Pod는 첫 시작 시 약간의 지연이 발생할 수 있으므로:
        
        - 주요 서비스를 미리 웜업 (Readiness Probe 활용)
        - 이미지 크기 최적화 (다단계 빌드 사용)
        - 지역적으로 가까운 ECR 리포지토리 활용
        - 가능한 경우 이미지 풀 시간 단축을 위해 기본 이미지 공유
        
        ```yaml
        # 초기화 시간 최적화 예시
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: fast-startup
        spec:
          template:
            spec:
              containers:
              - name: app
                image: my-optimized-app:latest
                readinessProbe:
                  httpGet:
                    path: /ready
                    port: 8080
                  initialDelaySeconds: 5
                  periodSeconds: 5
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### 하이브리드 노드 구성")
        st.markdown("""
        **EC2와 Fargate 혼합 전략**
        
        일부 워크로드는 EC2 노드에서, 다른 워크로드는 Fargate에서 실행하는 하이브리드 접근 방식을 설계합니다.
        
        **적합한 워크로드 분류**:
        - **Fargate에 적합**: 마이크로서비스, 웹 API, 중간 규모 배치 작업
        - **EC2에 적합**: GPU 워크로드, 저지연성 필요 애플리케이션, 사용자 정의 커널 모듈 필요
        
        **노드 선택기와 테인트를 사용한 스케줄링**:
        ```yaml
        # EC2 노드 그룹에만 배포되도록 구성
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: gpu-app
        spec:
          template:
            spec:
              nodeSelector:
                eks.amazonaws.com/nodegroup: gpu-nodes
              containers:
              - name: gpu-app
                image: gpu-app:latest
        
        # Fargate에 배포되도록 구성
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: api-service
          namespace: api
          labels:
            fargate: "true"
        spec:
          template:
            spec:
              containers:
              - name: api
                image: api:latest
        ```
        
        **비용 최적화를 위한 하이브리드 전략**:
        - 지속적으로 실행되는 워크로드는 Reserved Instance를 활용한 EC2
        - 가변적인 워크로드나 단기 작업은 Fargate
        - 중요도가 낮은 작업은 EC2 Spot 인스턴스
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### Fargate 보안 강화")
        st.markdown("""
        **Fargate 보안 강화 전략**
        
        Fargate Pod는 EC2 인스턴스와 달리 격리된 환경에서 실행되지만, 추가 보안 강화가 필요합니다.
        
        **네트워크 정책 적용**:
        ```yaml
        # Fargate Pod에 대한 네트워크 정책
        apiVersion: networking.k8s.io/v1
        kind: NetworkPolicy
        metadata:
          name: api-network-policy
          namespace: api
        spec:
          podSelector:
            matchLabels:
              app: api
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
                  app: database
            ports:
            - protocol: TCP
              port: 5432
        ```
        
        **IAM 역할 세분화**:
        ```bash
        # Fargate 프로필용 세분화된 서비스 계정 및 IAM 연결
        eksctl create iamserviceaccount \\
          --name app-service-account \\
          --namespace app-namespace \\
          --cluster my-cluster \\
          --attach-policy-arn arn:aws:iam::ACCOUNT_ID:policy/AppMinimalPolicy \\
          --approve
        ```
        
        **추가 보안 고려사항**:
        - AppArmor/SecComp 프로필 사용 (Fargate에서 지원 시)
        - 이미지 취약점 스캔 자동화 (ECR 스캔 활성화)
        - AWS Private Registry와 ECR 프라이빗 링크 활용
        - 암호화된 EFS 볼륨 사용
        """)
        
        # 다음 학습 추천 섹션 추가
        st.markdown("""
        <div class="next-learning">
            <h4>다음 학습 추천</h4>
            <ul>
                <li>Fargate에 대한 보안 강화는 <a href="/?page=advanced#security">보안 강화</a> 모듈에서 더 깊이 학습하세요.</li>
                <li>서버리스 워크로드 모니터링 방법은 <a href="/?page=intermediate#monitoring_basics">모니터링 기초</a> 모듈을 참고하세요.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # CI/CD 및 GitOps 탭
    with tabs[6]:
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        st.markdown("### CI/CD 파이프라인 개념")
        st.markdown("""
        CI/CD(지속적 통합/지속적 배포)는 애플리케이션 개발 단계를 자동화하여 애플리케이션을 더 짧은 주기로 고객에게 제공하는 방법입니다.

        **지속적 통합(CI)**은 개발자들이 코드 변경사항을 중앙 레포지토리에 자주 병합하고, 자동화된 빌드 및 테스트를 통해 검증하는 과정입니다.

        **지속적 배포(CD)**는 코드 변경이 테스트를 통과하면 프로덕션 환경까지 자동으로 배포되는 과정입니다.
        
        **릴리스 프로세스 단계:**
        코드 → 빌드 → 테스트 → 프로비저닝 → 배포 → 모니터링
        """)

        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### GitHub Actions 활용")
        st.markdown("""
        **GitHub Actions**는 GitHub 저장소에서 직접 CI/CD 워크플로우를 구성할 수 있는 도구입니다.

        **기본 워크플로우 구조**:
        ```yaml
        name: Build and Deploy

        on:
          push:
            branches: [ main ]

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
                  tags: \\\\${{ secrets.DOCKER_HUB_USERNAME }}/app:latest

          deploy:
            needs: build
            runs-on: ubuntu-latest
            steps:
              - name: Configure AWS credentials
                uses: aws-actions/configure-aws-credentials@v1
                with:
                  aws-access-key-id: \\\\${{ secrets.AWS_ACCESS_KEY_ID }}
                  aws-secret-access-key: \\\\${{ secrets.AWS_SECRET_ACCESS_KEY }}
                  aws-region: us-west-2

              - name: Update Kubernetes deployment
                run: |
                  aws eks update-kubeconfig --name my-eks-cluster --region us-west-2
                  kubectl set image deployment/my-app my-app=\\\\${{ secrets.DOCKER_HUB_USERNAME }}/app:latest
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### GitOps 원칙과 Amazon EKS")
        st.markdown("""
        **GitOps**는 Git을 신뢰할 수 있는 단일 정보 소스로 사용하여 인프라와 애플리케이션을 관리하는 방법입니다.
        
        **GitOps 핵심 원칙:**
        - Git을 단일 정보 소스(Single Source of Truth)로 사용
        - 명령형(Imperative) 대신 선언형(Declarative) 방식 사용
        - 승인된 변경사항이 자동으로 적용됨
        - 시스템 상태 일관성 보장
        
        **GitOps 이점:**
        - 전체 변경 이력 추적 가능 (누가, 무엇을, 언제, 왜)
        - 개발자가 이미 익숙한 Git 워크플로우 활용
        - 인프라 변경에 대한 코드 리뷰 및 승인 프로세스 적용
        - 장애 발생 시 신속한 복구 가능
        
        **Amazon EKS와 Flux CD 통합 예:**
        ```yaml
        apiVersion: source.toolkit.fluxcd.io/v1beta1
        kind: GitRepository
        metadata:
          name: my-app
          namespace: flux-system
        spec:
          interval: 1m
          url: https://github.com/my-org/my-app-manifests
          ref:
            branch: main
        ---
        apiVersion: kustomize.toolkit.fluxcd.io/v1beta1
        kind: Kustomization
        metadata:
          name: my-app
          namespace: flux-system
        spec:
          interval: 5m
          path: "./overlays/production"
          prune: true
          sourceRef:
            kind: GitRepository
            name: my-app
          targetNamespace: production
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### AWS CodePipeline 설정")
        st.markdown("""
        AWS CodePipeline을 사용하여 EKS 클러스터에 CI/CD 파이프라인을 구축하는 방법입니다.
        
        **파이프라인 구성 요소:**
        1. **소스 단계**: AWS CodeCommit 또는 GitHub 저장소
        2. **빌드 단계**: AWS CodeBuild를 사용한 Docker 이미지 빌드
        3. **배포 단계**: Amazon ECR에 이미지 푸시 및 EKS에 배포
        
        **AWS CodeBuild buildspec.yml 예제**:
        ```yaml
        version: 0.2
        phases:
          pre_build:
            commands:
              - echo Logging in to Amazon ECR...
              - aws ecr get-login-password --region \\$AWS_DEFAULT_REGION | docker login --username AWS --password-stdin \\$AWS_ACCOUNT_ID.dkr.ecr.\\$AWS_DEFAULT_REGION.amazonaws.com
              - REPOSITORY_URI=\\$AWS_ACCOUNT_ID.dkr.ecr.\\$AWS_DEFAULT_REGION.amazonaws.com/my-app
              - COMMIT_HASH=\\$(echo \\$CODEBUILD_RESOLVED_SOURCE_VERSION | cut -c 1-7)
              - IMAGE_TAG=\\${COMMIT_HASH:=latest}
          build:
            commands:
              - echo Build started on `date`
              - docker build -t \\$REPOSITORY_URI:\\$IMAGE_TAG .
          post_build:
            commands:
              - docker push \\$REPOSITORY_URI:\\$IMAGE_TAG
              - printf '[{"name":"my-app","imageUri":"%s"}]' \\$REPOSITORY_URI:\\$IMAGE_TAG > imagedefinitions.json
              - aws eks update-kubeconfig --name my-eks-cluster --region \\$AWS_DEFAULT_REGION
              - kubectl set image deployment/my-app my-app=\\$REPOSITORY_URI:\\$IMAGE_TAG
        artifacts:
          files:
            - imagedefinitions.json
        ```
        """)
        
        # 다음 학습 추천 섹션 추가
        st.markdown("""
        <div class="next-learning">
            <h4>다음 학습 추천</h4>
            <ul>
                <li>고급 GitOps 구현에 대해 더 알아보려면 <a href="/?page=advanced#gitops_cicd">GitOps와 고급 CI/CD</a> 모듈을 확인하세요.</li>
                <li>CI/CD 파이프라인을 직접 구현해보려면 <a href="/?page=intermediate#intermediate_projects">중급 실습 프로젝트</a>를 진행해보세요.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 모니터링 기초 탭 (기본에서 이동)
    with tabs[7]:
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        st.markdown("### Prometheus와 Grafana")
        st.markdown("""
        **Prometheus**는 시계열 데이터베이스 및 모니터링 시스템으로, 메트릭을 수집하고 저장합니다.

        **Grafana**는 모니터링 데이터를 위한 시각화 도구로, Prometheus와 같은 다양한 데이터 소스를 연결할 수 있습니다.

        **Helm을 사용한 Prometheus Stack 설치**:
        ```bash
        helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
        helm repo update
        
        helm install prometheus prometheus-community/kube-prometheus-stack \\
          --namespace monitoring \\
          --create-namespace
        ```
        
        **Prometheus Stack 구성 요소**:
        - **Prometheus Server**: 메트릭 수집 및 저장 서버
        - **Alertmanager**: 알림 처리 및 발송
        - **Grafana**: 데이터 시각화 대시보드
        - **kube-state-metrics**: Kubernetes API 객체 메트릭 제공 
        - **node-exporter**: 노드 하드웨어 및 OS 메트릭 수집
        
        **포트포워딩으로 UI 접근**:
        ```bash
        # Prometheus UI
        kubectl port-forward svc/prometheus-kube-prometheus-prometheus -n monitoring 9090:9090
        
        # Grafana UI
        kubectl port-forward svc/prometheus-grafana -n monitoring 3000:80
        ```
        
        **Grafana 로그인 정보**:
        - 사용자: admin
        - 비밀번호: prom-operator (기본값)
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### Prometheus 활용")
        st.markdown("""
        **PromQL(Prometheus Query Language) 기본**:
        
        ```
        # 모든 API 서버 요청 카운터
        apiserver_request_total
        
        # 최근 5분 동안의 HTTP 요청 비율 (초당)
        rate(http_requests_total[5m])
        
        # 노드별 CPU 사용률
        (1 - avg by(instance)(irate(node_cpu_seconds_total{mode="idle"}[5m]))) * 100
        
        # 메모리 사용률
        (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100
        ```
        
        **ServiceMonitor 생성**:
        ```yaml
        apiVersion: monitoring.coreos.com/v1
        kind: ServiceMonitor
        metadata:
          name: my-app-monitor
          namespace: monitoring
          labels:
            release: prometheus  # kube-prometheus-stack Helm 차트와 일치하는 레이블
        spec:
          selector:
            matchLabels:
              app: my-app  # 모니터링할 서비스의 레이블
          endpoints:
          - port: metrics  # 서비스에 정의된 포트 이름
            interval: 15s  # 스크래핑 간격
            path: /metrics  # 메트릭 경로
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### CloudWatch 로그 통합")
        st.markdown("""
        EKS 클러스터의 로그를 Amazon CloudWatch로 보내는 방법입니다.
        
        **Fluent Bit를 이용한 CloudWatch 로그 통합**:
        ```bash
        # IAM 정책 생성
        cat > fluent-bit-policy.json << EOF
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "logs:CreateLogGroup",
                        "logs:CreateLogStream",
                        "logs:PutLogEvents",
                        "logs:DescribeLogStreams"
                    ],
                    "Resource": "*"
                }
            ]
        }
        EOF
        
        aws iam create-policy \\
          --policy-name FluentBitEKSPolicy \\
          --policy-document file://fluent-bit-policy.json
        
        # 서비스 계정 생성
        eksctl create iamserviceaccount \\
          --name fluent-bit \\
          --namespace logging \\
          --cluster my-eks-cluster \\
          --attach-policy-arn arn:aws:iam::ACCOUNT_ID:policy/FluentBitEKSPolicy \\
          --approve \\
          --override-existing-serviceaccounts
        
        # Helm으로 Fluent Bit 설치
        helm repo add fluent https://fluent.github.io/helm-charts
        helm repo update
        
        # fluent-bit-values.yaml 생성
        cat > fluent-bit-values.yaml << EOF
        serviceAccount:
          create: false
          name: fluent-bit
        
        config:
          service: |
            [SERVICE]
                Parsers_File  parsers.conf
                HTTP_Server   On
                HTTP_Listen   0.0.0.0
                HTTP_Port     2020
        
          inputs: |
            [INPUT]
                Name              tail
                Tag               kube.*
                Path              /var/log/containers/*.log
                Parser            docker
                DB                /var/log/flb_kube.db
                Mem_Buf_Limit     5MB
                Skip_Long_Lines   On
                Refresh_Interval  10
        
          filters: |
            [FILTER]
                Name                kubernetes
                Match               kube.*
                Kube_URL            https://kubernetes.default.svc:443
                Kube_CA_File        /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
                Kube_Token_File     /var/run/secrets/kubernetes.io/serviceaccount/token
                Merge_Log           On
                K8S-Logging.Parser  On
        
          outputs: |
            [OUTPUT]
                Name              cloudwatch
                Match             kube.*
                region            us-east-1
                log_group_name    /aws/eks/my-cluster/logs
                log_stream_prefix \${HOST_NAME}.
                auto_create_group true
        EOF
        
        # Fluent Bit 설치
        helm install fluent-bit fluent/fluent-bit \\
          --namespace logging \\
          --create-namespace \\
          -f fluent-bit-values.yaml
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### 알림 설정")
        st.markdown("""
        **Prometheus Alerting Rules 설정**:
        ```yaml
        apiVersion: monitoring.coreos.com/v1
        kind: PrometheusRule
        metadata:
          name: kubernetes-apps
          namespace: monitoring
          labels:
            app: kube-prometheus-stack
            release: prometheus
        spec:
          groups:
          - name: kubernetes-apps
            rules:
            - alert: PodCrashLooping
              expr: rate(kube_pod_container_status_restarts_total[15m]) * 60 * 5 > 5
              for: 1m
              labels:
                severity: warning
              annotations:
                summary: Pod {{ \$labels.namespace }}/{{ \$labels.pod }} is crash looping
                description: Pod {{ \$labels.namespace }}/{{ \$labels.pod }} is restarting {{ printf "%.2f" \$value }} times / 5 minutes.
            
            - alert: PodNotReady
              expr: sum by (namespace, pod) (max by(namespace, pod) (kube_pod_status_phase{phase=~"Pending|Unknown"}) * on(namespace, pod) group_left(owner_kind) topk by(namespace, pod) (1, max by(namespace, pod, owner_kind) (kube_pod_owner{owner_kind!="Job"}))) > 0
              for: 5m
              labels:
                severity: warning
              annotations:
                summary: Pod {{ \$labels.namespace }}/{{ \$labels.pod }} is not ready
                description: Pod {{ \$labels.namespace }}/{{ \$labels.pod }} has been in a non-ready state for longer than 5 minutes.
        ```
        
        **Alertmanager 설정**:
        ```yaml
        # Helm values를 통한 설정
        alertmanager:
          config:
            global:
              resolve_timeout: 5m
              smtp_smarthost: 'smtp.example.com:587'
              smtp_from: 'alertmanager@example.com'
              smtp_auth_username: 'username'
              smtp_auth_password: 'password'
              slack_api_url: 'https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX'
            
            route:
              group_by: ['job', 'alertname', 'namespace']
              group_wait: 30s
              group_interval: 5m
              repeat_interval: 12h
              receiver: 'team-alerts'
              routes:
              - match:
                  severity: critical
                receiver: 'pager-duty'
            
            receivers:
            - name: 'team-alerts'
              slack_configs:
              - channel: '#team-alerts'
                title: '[{{ .Status | toUpper }}{{ if eq .Status "firing" }}:{{ .Alerts.Firing | len }}{{ end }}] {{ .CommonLabels.alertname }}'
                text: >-
                  {{ range .Alerts -}}
                  *Alert:* {{ .Annotations.summary }}
                  *Description:* {{ .Annotations.description }}
                  *Severity:* {{ .Labels.severity }}
                  {{ end }}
            
            - name: 'pager-duty'
              pagerduty_configs:
              - service_key: '<pagerduty-service-key>'
        ```
        """)
        
        # 다음 학습 추천 섹션 추가
        st.markdown("""
        <div class="next-learning">
            <h4>다음 학습 추천</h4>
            <ul>
                <li>분산 시스템에 대한 고급 모니터링 기법을 배우려면 <a href="/?page=advanced#observability">고급 관찰성</a> 모듈을 확인하세요.</li>
                <li>실제 모니터링 시스템 구축은 <a href="/?page=intermediate#intermediate_projects">중급 실습 프로젝트</a>에서 실습할 수 있습니다.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 서비스 메시 소개 탭 (고급에서 이동)
    with tabs[8]:
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        st.markdown("### 서비스 메시 개념")
        st.markdown("""
        **서비스 메시**는 마이크로서비스 간의 통신을 관리하는 인프라 레이어로, 서비스 간 통신을 제어, 관찰, 보호합니다.

        **주요 구성 요소**:
        - **데이터 영역(Data Plane)**: 서비스 트래픽을 처리하는 프록시 (Envoy 등)
        - **컨트롤 영역(Control Plane)**: 프록시를 구성하고 관리 (Istio, Linkerd 등)

        **제공 기능**:
        - **트래픽 관리**: 라우팅, 로드 밸런싱, 장애 조치
        - **보안**: mTLS(상호 TLS), 인증, 권한 부여
        - **관찰성**: 메트릭, 로그, 분산 추적
        
        **서비스 메시 도입 이유**:
        - 복잡한 마이크로서비스 환경에서의 통신 관리 단순화
        - 애플리케이션 코드 변경 없이 보안 강화
        - 서비스 간 통신 가시성 확보
        - 다양한 장애 시나리오에 대한 복원력 향상
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### Istio 서비스 메시 소개")
        st.markdown("""
        **Istio**는 가장 널리 사용되는 오픈소스 서비스 메시 구현체 중 하나입니다.
        
        **Istio 구성 요소**:
        - **Istiod**: 중앙 제어 영역으로 정책과 구성 관리, 인증서 생성 등 담당
        - **Envoy 프록시**: 사이드카로 모든 Pod에 주입되며 모든 네트워크 통신 처리
        - **인그레스/이그레스 게이트웨이**: 클러스터 진입/이탈 트래픽 제어
        
        **Istio 설치**:
        ```bash
        # Istio CLI 설치
        curl -L https://istio.io/downloadIstio | sh -
        cd istio-1.13.2
        export PATH=\\\$PWD/bin:\\\$PATH
        
        # Istio 설치 - 기본 프로필
        istioctl install --set profile=demo -y
        
        # 사이드카 자동 주입 활성화
        kubectl label namespace default istio-injection=enabled
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### 간단한 서비스 메시 구성")
        st.markdown("""
        **Bookinfo 샘플 애플리케이션 배포**:
        ```bash
        # 샘플 애플리케이션 배포
        kubectl apply -f samples/bookinfo/platform/kube/bookinfo.yaml
        
        # 진입점 생성
        kubectl apply -f samples/bookinfo/networking/bookinfo-gateway.yaml
        
        # 게이트웨이 URL 확인
        export INGRESS_HOST=\$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
        export INGRESS_PORT=\$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].port}')
        export GATEWAY_URL=\$INGRESS_HOST:\$INGRESS_PORT
        echo \$GATEWAY_URL
        ```
        
        **기본 트래픽 라우팅 규칙 적용**:
        ```yaml
        # destination-rule.yaml
        apiVersion: networking.istio.io/v1alpha3
        kind: DestinationRule
        metadata:
          name: reviews
        spec:
          host: reviews
          subsets:
          - name: v1
            labels:
              version: v1
          - name: v2
            labels:
              version: v2
          - name: v3
            labels:
              version: v3
        ```
        
        ```bash
        # 적용
        kubectl apply -f destination-rule.yaml
        ```
        
        **특정 버전으로 트래픽 라우팅**:
        ```yaml
        # virtual-service.yaml
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
                subset: v2
        ```
        
        ```bash
        # 적용
        kubectl apply -f virtual-service.yaml
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### 서비스 메시 관찰성")
        st.markdown("""
        Istio는 데이터 영역에서 수집된 원격 분석 데이터를 사용하여 서비스 메시의 동작과 성능을 모니터링합니다.
        
        **Kiali - 서비스 메시 시각화**:
        ```bash
        # Kiali 설치
        kubectl apply -f samples/addons/kiali.yaml
        
        # 접근
        istioctl dashboard kiali
        ```
        
        **Prometheus - 메트릭 수집**:
        ```bash
        # Prometheus 설치
        kubectl apply -f samples/addons/prometheus.yaml
        
        # 접근
        istioctl dashboard prometheus
        ```
        
        **Grafana - 메트릭 시각화**:
        ```bash
        # Grafana 설치
        kubectl apply -f samples/addons/grafana.yaml
        
        # 접근
        istioctl dashboard grafana
        ```
        """)
        
        # 다음 학습 추천 섹션 추가
        st.markdown("""
        <div class="next-learning">
            <h4>다음 학습 추천</h4>
            <ul>
                <li>서비스 메시의 고급 기능을 탐구하려면 <a href="/?page=advanced#networking">네트워킹 고급</a> 모듈을 확인하세요.</li>
                <li>서비스 메시와 함께 모니터링 기능을 활용하는 방법은 <a href="/?page=intermediate#monitoring_basics">모니터링 기초</a> 모듈에서 학습할 수 있습니다.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 중급 실습 프로젝트 탭
    with tabs[9]:
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        st.markdown("### 마이크로서비스 아키텍처 배포")
        st.markdown("""
        마이크로서비스 아키텍처를 EKS에 배포하는 프로젝트 예시입니다.

        **구성 요소**:
        - 프론트엔드 서비스 (React)
        - 백엔드 API 서비스 (Node.js)
        - 데이터 서비스 (MongoDB)
        
        **프로젝트 아키텍처**:
        
        ![마이크로서비스 아키텍처](https://via.placeholder.com/600x300?text=Microservices+Architecture)
        
        **주요 기술 스택**:
        - **컨테이너화**: Docker
        - **오케스트레이션**: Kubernetes/EKS
        - **서비스 검색**: Kubernetes 서비스
        - **구성 관리**: ConfigMaps, Secrets
        - **영구 스토리지**: EBS/EFS
        - **스케일링**: HPA(Horizontal Pod Autoscaler)
        
        **배포 단계**:
        1. 네임스페이스 및 리소스 할당량 설정
        2. MongoDB StatefulSet 배포
        3. 백엔드 API 서비스 배포
        4. 프론트엔드 React 앱 배포
        5. 인그레스 설정 및 SSL/TLS 구성
        6. 자동 스케일링 설정
        7. 모니터링 및 로깅 설정
        
        ```bash
        # 네임스페이스 생성
        kubectl create namespace microservices
        kubectl config set-context --current --namespace=microservices
        
        # 배포 적용
        kubectl apply -f mongodb/
        kubectl apply -f backend/
        kubectl apply -f frontend/
        kubectl apply -f ingress/
        ```
        """)

        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### CI/CD 파이프라인 구축")
        st.markdown("""
        GitOps 방식의 CI/CD 파이프라인을 구축하는 프로젝트입니다.

        **구성 요소**:
        - 소스 코드 저장소 (GitHub)
        - CI 시스템 (GitHub Actions)
        - 컨테이너 레지스트리 (Amazon ECR)
        - GitOps 도구 (FluxCD)
        
        **워크플로우**:
        1. 개발자가 GitHub에 코드 푸시
        2. GitHub Actions가 빌드, 테스트, 이미지 생성
        3. 이미지를 ECR에 푸시
        4. 매니페스트 저장소 업데이트 (이미지 태그 변경)
        5. FluxCD가 변경 감지 및 EKS에 배포
        
        **CI 워크플로우 예시 (GitHub Actions)**:
        ```yaml
        name: Build and Push
        
        on:
          push:
            branches: [ main ]
        
        jobs:
          build:
            runs-on: ubuntu-latest
            steps:
            - uses: actions/checkout@v3
            
            - name: Set up Docker Buildx
              uses: docker/setup-buildx-action@v1
            
            - name: Configure AWS credentials
              uses: aws-actions/configure-aws-credentials@v1
              with:
                aws-access-key-id: \${{ secrets.AWS_ACCESS_KEY_ID }}
                aws-secret-access-key: \${{ secrets.AWS_SECRET_ACCESS_KEY }}
                aws-region: us-west-2
                
            - name: Login to Amazon ECR
              id: login-ecr
              uses: aws-actions/amazon-ecr-login@v1
            
            - name: Build and push
              uses: docker/build-push-action@v2
              with:
                context: .
                push: true
                tags: \${{ steps.login-ecr.outputs.registry }}/my-app:\${{ github.sha }}
                
            - name: Update kustomization
              uses: mikefarah/yq@master
              with:
                cmd: |
                  git config --global user.name 'GitHub Actions'
                  git config --global user.email 'actions@github.com'
                  git clone https://x-access-token:\${{ secrets.GH_TOKEN }}@github.com/my-org/app-manifests.git
                  cd app-manifests
                  yq -i '.images[0].newTag="\${{ github.sha }}"' kustomization.yaml
                  git add kustomization.yaml
                  git commit -m "Update image to \${{ github.sha }}"
                  git push
        ```
        
        **FluxCD 구성**:
        ```yaml
        apiVersion: source.toolkit.fluxcd.io/v1beta1
        kind: GitRepository
        metadata:
          name: app-manifests
          namespace: flux-system
        spec:
          interval: 1m
          url: https://github.com/my-org/app-manifests
          ref:
            branch: main
        ---
        apiVersion: kustomize.toolkit.fluxcd.io/v1beta1
        kind: Kustomization
        metadata:
          name: app-manifests
          namespace: flux-system
        spec:
          interval: 5m
          path: "./overlays/production"
          prune: true
          sourceRef:
            kind: GitRepository
            name: app-manifests
          targetNamespace: production
        ```
        """)
        
        st.markdown("<div class='topic-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### 데이터베이스 연동 애플리케이션")
        st.markdown("""
        AWS 관리형 데이터베이스 서비스와 연동하는 애플리케이션 구축 프로젝트입니다.
        
        **구성 요소**:
        - 웹 애플리케이션 (Spring Boot/NodeJS)
        - Amazon RDS (PostgreSQL)
        - Amazon ElastiCache (Redis)
        - 데이터 백업 및 복구 전략
        
        **구현 내용**:
        1. RDS 인스턴스 프로비저닝 (Terraform)
        2. 서비스 계정 및 IAM 역할 설정 (IRSA)
        3. 애플리케이션 시크릿 관리 (AWS Secrets Manager)
        4. 애플리케이션 배포 (StatefulSet)
        5. 캐시 계층 구축 (ElastiCache)
        6. 읽기 복제본 활용한 읽기/쓰기 분리
        7. 백업 및 장애 복구 테스트
        
        **Spring Boot 애플리케이션 예시**:
        ```yaml
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: spring-db-app
        spec:
          replicas: 3
          selector:
            matchLabels:
              app: spring-db-app
          template:
            metadata:
              labels:
                app: spring-db-app
            spec:
              serviceAccountName: db-app-sa
              containers:
              - name: spring-app
                image: my-registry/spring-db-app:latest
                ports:
                - containerPort: 8080
                env:
                - name: SPRING_PROFILES_ACTIVE
                  value: "production"
                - name: DB_SECRET_NAME
                  value: "prod/spring-app/db"
                - name: AWS_REGION
                  value: "us-west-2"
                resources:
                  limits:
                    memory: "512Mi"
                    cpu: "500m"
                  requests:
                    memory: "256Mi"
                    cpu: "250m"
                readinessProbe:
                  httpGet:
                    path: /actuator/health
                    port: 8080
                livenessProbe:
                  httpGet:
                    path: /actuator/health
                    port: 8080
        ```
        
        **서비스 계정 & 시크릿 접근 설정**:
        ```bash
        # IAM 정책 생성
        aws iam create-policy --policy-name SpringAppSecretsPolicy --policy-document file://secrets-policy.json
        
        # 서비스 계정 생성 & IAM 역할 연결
        eksctl create iamserviceaccount \
          --name db-app-sa \
          --namespace default \
          --cluster my-cluster \
          --attach-policy-arn arn:aws:iam::ACCOUNT_ID:policy/SpringAppSecretsPolicy \
          --approve
        ```
        """)
        
        # 다음 학습 추천 섹션 추가
        st.markdown("""
        <div class="next-learning">
            <h4>다음 학습 추천</h4>
            <ul>
                <li>더 복잡한 실제 프로젝트를 구현하려면 <a href="/?page=advanced#advanced_projects">고급 실습 프로젝트</a> 모듈을 확인하세요.</li>
                <li>프로젝트의 보안을 강화하려면 <a href="/?page=advanced#security">보안 강화</a> 모듈에서 더 많은 기법을 배울 수 있습니다.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 복습 섹션
    st.markdown("<h2 class='section-title'>개념 정리 및 복습</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="review-section">
        <h3 class="review-title">중급 과정 요약</h3>
        <div class="review-content">
            <p>EKS와 Kubernetes 중급 과정에서 다룬 주요 개념들을 정리합니다.</p>
            
            <h4>1. 고급 Kubernetes 리소스</h4>
            <ul>
                <li><strong>StatefulSet</strong>: 상태 유지가 필요한 애플리케이션을 위한 워크로드 API</li>
                <li><strong>DaemonSet</strong>: 모든 노드 또는 특정 노드에 Pod 복제본 실행</li>
                <li><strong>ConfigMap</strong>: 애플리케이션 설정 데이터 저장</li>
                <li><strong>Secret</strong>: 민감한 정보 저장</li>
            </ul>
            
            <h4>2. EKS 관리와 운영</h4>
            <ul>
                <li><strong>인프라 as 코드</strong>: Terraform, AWS CDK를 사용한 EKS 관리</li>
                <li><strong>IAM과 RBAC</strong>: AWS 자격 증명과 Kubernetes 권한 통합</li>
                <li><strong>Load Balancer Controller</strong>: ALB/NLB 자동 프로비저닝</li>
            </ul>
            
            <h4>3. EKS 자동 크기 조정</h4>
            <ul>
                <li><strong>Horizontal Pod Autoscaler</strong>: Pod 복제본 수를 자동으로 조정</li>
                <li><strong>Vertical Pod Autoscaler</strong>: Pod에 할당된 리소스를 자동으로 조정</li>
                <li><strong>Cluster Autoscaler</strong>: Auto Scaling 그룹을 사용하여 노드 수 조정</li>
                <li><strong>Karpenter</strong>: Auto Scaling 그룹 없이 노드 관리 및 최적화</li>
            </ul>
            
            <h4>4. EKS 스토리지 관리</h4>
            <ul>
                <li><strong>Amazon EBS</strong>: 블록 스토리지 옵션(ReadWriteOnce)</li>
                <li><strong>Amazon EFS</strong>: 파일 시스템 스토리지 옵션(ReadWriteMany)</li>
                <li><strong>CSI 드라이버</strong>: 클라우드 스토리지와 Kubernetes 연결</li>
                <li><strong>AWS Secrets Manager</strong>: 안전한 민감 정보 관리</li>
            </ul>
            
            <h4>5. Helm 패키지 관리</h4>
            <ul>
                <li><strong>차트 커스터마이징</strong>: values.yaml 오버라이딩, 템플릿 수정</li>
                <li><strong>차트 개발</strong>: 자체 Helm 차트 작성 방법</li>
                <li><strong>저장소 관리</strong>: 공개/비공개 차트 저장소 활용</li>
                <li><strong>릴리스 관리</strong>: 업그레이드, 롤백, 이력 관리</li>
            </ul>
            
            <h4>6. 서버리스 EKS 심화</h4>
            <ul>
                <li><strong>Fargate 프로필 고급 설계</strong>: 세분화된 프로필 설정</li>
                <li><strong>최적화 전략</strong>: 리소스 요청 및 시작 시간 최적화</li>
                <li><strong>하이브리드 구성</strong>: EC2와 Fargate 혼합 아키텍처</li>
                <li><strong>보안 강화</strong>: Fargate 워크로드 보안 관리</li>
            </ul>
            
            <h4>7. CI/CD 및 GitOps</h4>
            <ul>
                <li><strong>CI/CD 파이프라인</strong>: 코드 통합, 빌드, 테스트, 배포 자동화</li>
                <li><strong>GitHub Actions</strong>: 코드 저장소 내 CI/CD 워크플로우 자동화</li>
                <li><strong>GitOps</strong>: Git을 사용한 인프라 및 애플리케이션 관리</li>
                <li><strong>AWS CodePipeline</strong>: AWS 기반 CI/CD 파이프라인</li>
            </ul>
            
            <h4>8. 모니터링 및 서비스 메시</h4>
            <ul>
                <li><strong>Prometheus</strong>: 메트릭 수집 및 저장</li>
                <li><strong>Grafana</strong>: 시각화 도구</li>
                <li><strong>CloudWatch</strong>: AWS 통합 모니터링 서비스</li>
                <li><strong>서비스 메시</strong>: 마이크로서비스 통신 관리</li>
                <li><strong>Istio</strong>: 트래픽 관리, 보안, 관찰성 제공</li>
            </ul>
            
            <h4>주요 명령어 및 설정</h4>
            <div class="code-block">
            # Horizontal Pod Autoscaler 설정
            kubectl autoscale deployment myapp --cpu-percent=50 --min=3 --max=10
            
            # EBS 영구 볼륨 클레임 생성
            kubectl apply -f pvc.yaml
            
            # Helm 차트 설치 및 값 오버라이드
            helm install my-release bitnami/wordpress --set wordpressBlogName="My Blog"
            
            # Fargate 프로필 생성
            eksctl create fargateprofile --cluster=my-cluster --name=my-profile --namespace=default
            
            # IAM과 RBAC 통합
            eksctl create iamserviceaccount --name=my-sa --namespace=default --cluster=my-cluster
            
            # Prometheus 설치
            helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 기본/고급 과정으로 이동하는 링크 추가
    st.markdown("""
    <div class="next-learning" style="margin-top: 40px;">
        <h4>다음 학습 단계</h4>
        <p>중급 과정을 충분히 이해했다면, 다음 단계로 진행하세요:</p>
        <ul>
            <li><a href="/?page=beginner">기본 과정 복습하기 →</a> (기초 개념 다시 살펴보기)</li>
            <li><a href="/?page=advanced">고급 과정으로 이동하기 →</a> (CRD, 서비스 메시, 고급 보안, 멀티클러스터)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)