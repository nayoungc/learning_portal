import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
from streamlit.components.v1 import html
import graphviz
from utils.session_manager import SessionManager
from utils.localization import t

# 확장/축소 기능이 있는 markmap 렌더링 함수
def render_markmap_with_expand(markdown_content):
    """확장/축소 기능이 있는 markmap 렌더링 함수"""
    # 특수문자 처리
    markdown_content = markdown_content.replace('`', '\\`').replace("'", "\\'").replace('"', '\\"')
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <script src="https://cdn.jsdelivr.net/npm/d3@6"></script>
        <script src="https://cdn.jsdelivr.net/npm/markmap-view@0.2.7"></script>
        <style>
            body {{
                margin: 0;
                padding: 0;
                font-family: 'Noto Sans KR', 'Malgun Gothic', -apple-system, sans-serif;
            }}
            
            .markmap-container {{
                width: 100%;
                height: 500px;
                position: relative;
                background-color: white;
            }}
            
            .markmap {{
                width: 100%;
                height: 500px;
            }}
            
            /* 확대/축소 컨트롤 */
            .zoom-controls {{
                position: absolute;
                right: 20px;
                top: 20px;
                background-color: white;
                border-radius: 4px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
                z-index: 100;
                display: flex;
                flex-direction: column;
            }}
            
            .zoom-btn {{
                width: 36px;
                height: 36px;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                font-size: 18px;
                border: none;
                background: none;
                color: #555;
                transition: all 0.2s;
            }}
            
            .zoom-btn:hover {{
                background-color: #e0f5f1;
                color: #2a9d8f;
            }}
            
            .zoom-divider {{
                height: 1px;
                background-color: #eee;
                width: 80%;
                margin: 0 auto;
            }}
            
            /* 마크맵 노드 스타일 */
            .markmap-foreign {{
                font-size: 12px !important;
                line-height: 1.2;
            }}
        </style>
    </head>
    <body>
        <div class="markmap-container">
            <div class="zoom-controls">
                <button class="zoom-btn" onclick="zoomIn()">+</button>
                <div class="zoom-divider"></div>
                <button class="zoom-btn" onclick="zoomOut()">-</button>
                <div class="zoom-divider"></div>
                <button class="zoom-btn" onclick="resetZoom()">↺</button>
            </div>
            <div class="markmap"></div>
        </div>
        
        <script>
        (async () => {{
            const {{ Markmap }} = window.markmap;
            const container = document.querySelector('.markmap');
            
            // 마크다운 콘텐츠
            const content = `{markdown_content}`;
            
            // 마인드맵 생성
            const mm = Markmap.create(container, {{
                initialExpandLevel: 2,  // 초기에 펼칠 레벨
                maxWidth: 300,         // 노드 최대 너비
                color: ['#1e7d71', '#2a9d8f', '#40b3a2', '#52b69a', '#76c893']
            }}, content);
            
            // 확대/축소 기능
            window.mm = mm;
            window.zoomIn = function() {{
                mm.rescale(1.2);
            }};
            window.zoomOut = function() {{
                mm.rescale(0.8);
            }};
            window.resetZoom = function() {{
                mm.fit();
            }};
            
            // CSS 스타일을 직접 적용 (마크맵 로드 후)
            setTimeout(() => {{
                // 루트 노드
                const rootNodes = document.querySelectorAll('g.markmap-node-root > circle');
                rootNodes.forEach(node => {{
                    node.style.fill = '#1e7d71';
                    node.style.stroke = '#fff';
                }});
                
                // 모든 노드
                const allNodes = document.querySelectorAll('g.markmap-node > circle');
                allNodes.forEach(node => {{
                    if (!node.style.fill) node.style.fill = '#2a9d8f';
                    node.style.stroke = '#fff';
                }});
                
                // 브랜치 노드
                const branchNodes = document.querySelectorAll('g.markmap-node-branch > circle');
                branchNodes.forEach(node => {{
                    node.style.fill = '#40b3a2';
                }});
                
                // 리프 노드
                const leafNodes = document.querySelectorAll('g.markmap-node-leaf > circle');
                leafNodes.forEach(node => {{
                    node.style.fill = '#52b69a';
                }});
                
                // 연결선
                const links = document.querySelectorAll('.markmap-link');
                links.forEach(link => {{
                    link.style.stroke = '#76c893';
                }});
                
                // 텍스트 크기 조정
                const rootTexts = document.querySelectorAll('g.markmap-node-root > foreignObject');
                rootTexts.forEach(text => {{
                    text.style.fontSize = '16px';
                    text.style.fontWeight = 'bold';
                }});
                
                const branchTexts = document.querySelectorAll('g.markmap-node-branch > foreignObject');
                branchTexts.forEach(text => {{
                    text.style.fontSize = '14px';
                }});
                
                const leafTexts = document.querySelectorAll('g.markmap-node-leaf > foreignObject');
                leafTexts.forEach(text => {{
                    text.style.fontSize = '12px';
                }});
            }}, 100);
        }})();
        </script>
    </body>
    </html>
    """
    html(html_content, height=520, scrolling=True)

def render_mindmap():
    """마인드맵 페이지 렌더링 - agraph, markmap, flowchart 3가지 시각화 제공"""
    # 스타일 정의
    st.markdown("""
    <style>
    /* 색상 변수 */
    :root {
        --green-color: #2a9d8f;      /* 메인 녹색 */
        --green-light: #e0f5f1;      /* 연한 녹색 */
        --green-dark: #1e7d71;       /* 진한 녹색 */
        --green-extra-light: #f0faf8; /* 매우 연한 녹색 (배경용) */
        --green-accent: #52b69a;     /* 강조용 녹색 */
        --green-soft: #76c893;       /* 부드러운 녹색 */
        --blue-color: #4361ee;       /* 기존 파란색 - 일관성 유지용 */
        --yellow-color: #ffb703;     /* 기존 노란색 - 일관성 유지용 */
        --red-color: #e63946;        /* 기존 빨간색 - 일관성 유지용 */
        --gray-light: #f8f9fa;       /* 연한 회색 */
        --divider-color: #e0e0e0;    /* 구분선 색상 */
    }
    
    /* 페이지 제목 */
    .mindmap-title {
        font-size: 2rem !important;
        color: #000000 !important;  /* 검정색으로 변경 */
        margin-bottom: 20px !important;
        padding-bottom: 10px;
        border-bottom: 2px solid var(--green-color);
    }
    
    /* 학습 경로 네비게이션 */
    .learning-path-nav {
        display: flex;
        background-color: var(--gray-light);
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
        cursor: pointer;
    }
    
    .nav-item:not(:last-child):after {
        content: "→";
        position: absolute;
        right: -5px;
        top: 50%;
        transform: translateY(-50%);
        color: #999;
    }
    
    .nav-link {
        color: #333333;  /* 동일한 색상 (검은색) */
        text-decoration: none;
        font-weight: normal;
    }
    
    .nav-link:hover {
        color: var(--green-color);
        text-decoration: underline;
    }
    
    .tools-nav {
        color: var(--green-color);
        font-weight: bold;
    }
    
    /* 섹션 헤더 - 검은색으로 변경 */
    .section-header {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        margin-top: 30px !important;
        margin-bottom: 20px !important;
        color: #000000 !important;  /* 검은색으로 변경 */
        padding-bottom: 8px !important;
        border-bottom: 2px solid var(--green-color) !important;
    }
    
    /* 마인드맵 소개 카드 */
    .mindmap-intro {
        background-color: var(--green-light);
        border-left: 4px solid var(--green-color);
        padding: 15px;
        border-radius: 6px;
        margin-bottom: 25px;
        font-size: 0.95rem;
    }
    
    /* 마인드맵 카테고리 박스 */
    .category-box {
        background-color: white;
        border-radius: 10px;
        border-top: 5px solid var(--green-color);
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        padding: 20px;
        margin-bottom: 20px;
    }
    
    .category-title {
        font-size: 1.3rem !important;
        font-weight: 600;
        color: #000000 !important;  /* 검은색으로 변경 */
        margin-bottom: 15px !important;
        padding-bottom: 8px;
        border-bottom: 1px solid var(--divider-color);
        display: flex;
        align-items: center;
    }
    
    .category-title .icon {
        background-color: var(--green-light);
        color: var(--green-color);
        width: 35px;
        height: 35px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        margin-right: 12px;
        font-weight: bold;
        font-size: 1.2rem;
    }
    
    /* 시각화 컨테이너 - 통합 스타일 */
    .visualization-container {
        border: 1px solid var(--green-light);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        background-color: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        min-height: 500px;
        overflow: hidden;
        position: relative;
    }
    
    /* markmap 스타일 커스터마이징 */
    .markmap-container {
        height: 500px;
        overflow: hidden;
    }
    
    /* flowchart 스타일 */
    .flowchart-container {
        height: 500px;
        overflow: hidden;
    }
    
    /* 탭 스타일링 - 탭 제목을 더 두드러지게 표시 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 10px 16px;
        border-radius: 4px 4px 0 0;
        background-color: transparent !important;
        color: #000000 !important;  /* 검은색으로 변경 */
        border: none !important;
        font-size: 1rem !important;
    }
    
    /* 탭 호버 효과 */
    .stTabs [data-baseweb="tab"]:hover {
        color: var(--green-color) !important;
        border-bottom: 2px solid var(--green-color) !important;
    }
    
    /* 선택된 탭 스타일 - 굵게 표시 */
    .stTabs [aria-selected="true"] {
        color: var(--green-color) !important;
        border-bottom: 2px solid var(--green-color) !important;
        font-weight: 600 !important;
    }
    
    /* 2차 탭 스타일링 */
    .stTabs [data-baseweb="tab-panel"] .stTabs [data-baseweb="tab"] {
        background-color: #f9f9f9 !important;
        font-size: 0.9rem !important;
    }
    
    /* 관련 리소스 섹션 */
    .related-resources {
        margin-top: 40px;
        background-color: var(--green-light);
        border-radius: 8px;
        padding: 20px;
        border-left: 4px solid var(--green-color);
    }
    
    .related-resources h4 {
        color: #000000 !important;  /* 검은색으로 변경 */
        margin-top: 0;
        margin-bottom: 15px;
        font-size: 1.2rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 학습 경로 네비게이션 JavaScript
    st.markdown("""
    <script>
    function navigateTo(pageId) {
        // 네비게이션 이벤트 발생
        window.dispatchEvent(new CustomEvent('nav-event', { 
            detail: pageId 
        }));
    }
    </script>
    """, unsafe_allow_html=True)
    
    # 페이지 제목
    st.markdown("<h1 class='mindmap-title'>쿠버네티스 & EKS 마인드맵</h1>", unsafe_allow_html=True)
    
    # 학습 경로 네비게이션
    st.markdown("""
    <div class="learning-path-nav">
        <div class="nav-item" onclick="navigateTo('beginner')">
            <span class="nav-link">기본 과정</span>
        </div>
        <div class="nav-item" onclick="navigateTo('intermediate')">
            <span class="nav-link">중급 과정</span>
        </div>
        <div class="nav-item" onclick="navigateTo('advanced')">
            <span class="nav-link">고급 과정</span>
        </div>
        <div class="nav-item current">
            <span class="tools-nav">학습 도구</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 마인드맵 소개
    st.markdown("""
    <div class="mindmap-intro">
        <p>이 마인드맵은 쿠버네티스와 EKS의 주요 개념, 리소스, 도구 간의 관계를 시각적으로 보여줍니다. 개념을 체계적으로 이해하고 복습하는 데 도움이 됩니다.</p>
        <p>세 가지 다른 시각화 방식을 선택하여 개념 간의 관계를 다양한 관점에서 탐색할 수 있습니다.</p>
        <p><strong>마인드맵</strong> 탭에서는 노드를 클릭하여 하위 항목을 확장하거나 축소할 수 있으며, 확대/축소 버튼을 사용할 수 있습니다.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 전체 마인드맵 섹션
    st.markdown("<h2 class='section-header'>쿠버네티스 & EKS 전체 개요</h2>", unsafe_allow_html=True)
    
    # 시각화 방식 선택 탭 (라디오 버튼 대신 탭으로 변경)
    overview_tabs = st.tabs(["네트워크 그래프", "마인드맵", "플로우 차트"])
    
    # 네트워크 그래프 탭 (agraph)
    with overview_tabs[0]:
        with st.container():
            # 메인 마인드맵 노드 정의 (agraph)
            nodes = [
                # 핵심 노드
                Node(id="k8s", label="쿠버네티스", size=30, color="#2a9d8f", shape="dot"),
                Node(id="eks", label="Amazon EKS", size=30, color="#2a9d8f", shape="dot"),
                
                # 1단계 개념
                Node(id="core", label="핵심 컴포넌트", size=25, color="#40b3a2", shape="dot"),
                Node(id="workload", label="워크로드", size=25, color="#40b3a2"),
                Node(id="network", label="네트워킹", size=25, color="#40b3a2"),
                Node(id="storage", label="스토리지", size=25, color="#40b3a2"),
                Node(id="security", label="보안", size=25, color="#40b3a2"),
                Node(id="aws", label="AWS 통합", size=25, color="#40b3a2"),
                
                # 2단계 개념 - Core Components
                Node(id="control", label="컨트롤 플레인", size=20, color="#52b69a"),
                Node(id="worker", label="워커 노드", size=20, color="#52b69a"),
                
                # 2단계 개념 - Workloads
                Node(id="pod", label="파드", size=20, color="#52b69a"),
                Node(id="deploy", label="디플로이먼트", size=20, color="#52b69a"),
                Node(id="stateful", label="스테이트풀셋", size=20, color="#52b69a"),
                Node(id="daemon", label="데몬셋", size=20, color="#52b69a"),
                
                # 2단계 개념 - Networking
                Node(id="service", label="서비스", size=20, color="#52b69a"),
                Node(id="ingress", label="인그레스", size=20, color="#52b69a"),
                Node(id="policy", label="네트워크 정책", size=20, color="#52b69a"),
                
                # 2단계 개념 - Storage
                Node(id="pv", label="퍼시스턴트볼륨", size=20, color="#52b69a"),
                Node(id="sc", label="스토리지클래스", size=20, color="#52b69a"),
                
                # 2단계 개념 - Security
                Node(id="rbac", label="RBAC", size=20, color="#52b69a"),
                Node(id="secret", label="시크릿", size=20, color="#52b69a"),
                
                # 2단계 개념 - AWS Integration
                Node(id="iam", label="IAM", size=20, color="#52b69a"),
                Node(id="elb", label="ELB", size=20, color="#52b69a"),
                Node(id="ebs", label="EBS", size=20, color="#52b69a"),
                Node(id="fargate", label="파게이트", size=20, color="#52b69a"),
            ]
            
            # 마인드맵 엣지(연결선) 정의
            edges = [
                # 핵심 개념 간 연결
                Edge(source="k8s", target="core", type="CURVE_SMOOTH"),
                Edge(source="k8s", target="workload", type="CURVE_SMOOTH"),
                Edge(source="k8s", target="network", type="CURVE_SMOOTH"),
                Edge(source="k8s", target="storage", type="CURVE_SMOOTH"),
                Edge(source="k8s", target="security", type="CURVE_SMOOTH"),
                
                Edge(source="eks", target="k8s", type="CURVE_SMOOTH"),
                Edge(source="eks", target="aws", type="CURVE_SMOOTH"),
                
                # Core Components
                Edge(source="core", target="control", type="CURVE_SMOOTH"),
                Edge(source="core", target="worker", type="CURVE_SMOOTH"),
                
                # Workloads
                Edge(source="workload", target="pod", type="CURVE_SMOOTH"),
                Edge(source="workload", target="deploy", type="CURVE_SMOOTH"),
                Edge(source="workload", target="stateful", type="CURVE_SMOOTH"),
                Edge(source="workload", target="daemon", type="CURVE_SMOOTH"),
                
                # Networking
                Edge(source="network", target="service", type="CURVE_SMOOTH"),
                Edge(source="network", target="ingress", type="CURVE_SMOOTH"),
                Edge(source="network", target="policy", type="CURVE_SMOOTH"),
                
                # Storage
                Edge(source="storage", target="pv", type="CURVE_SMOOTH"),
                Edge(source="storage", target="sc", type="CURVE_SMOOTH"),
                
                # Security
                Edge(source="security", target="rbac", type="CURVE_SMOOTH"),
                Edge(source="security", target="secret", type="CURVE_SMOOTH"),
                
                # AWS Integration
                Edge(source="aws", target="iam", type="CURVE_SMOOTH"),
                Edge(source="aws", target="elb", type="CURVE_SMOOTH"),
                Edge(source="aws", target="ebs", type="CURVE_SMOOTH"),
                Edge(source="aws", target="fargate", type="CURVE_SMOOTH"),
                
                # 추가 연결 관계
                Edge(source="deploy", target="pod", type="CURVE_SMOOTH"),
                Edge(source="service", target="pod", type="CURVE_SMOOTH"),
                Edge(source="elb", target="service", type="CURVE_SMOOTH"),
                Edge(source="ebs", target="pv", type="CURVE_SMOOTH"),
            ]
            
            # 마인드맵 구성
            config = Config(
                width=700,
                height=500,
                directed=True,
                physics=True,
                hierarchical=False,
                nodeHighlightBehavior=True,
                highlightColor="#e0f5f1",
                collapsible=True,
                node={"labelProperty": "label"},
                link={"labelProperty": "label", "renderLabel": True},
                node_color="#2a9d8f",
                node_size=20,
                node_font_size=12,
                edge_color="#76c893",
            )
            
            # 마인드맵 렌더링
            agraph(nodes=nodes, edges=edges, config=config)
    
    # 마인드맵 탭 (markmap)
    with overview_tabs[1]:
        with st.container():
            # 한국어 markmap 데이터 정의
            markmap_data = """
            # 쿠버네티스
            
            ## 핵심 컴포넌트
            - 컨트롤 플레인
              - kube-apiserver
              - etcd
              - kube-scheduler
              - kube-controller-manager
              - 클라우드 컨트롤러 매니저
            - 워커 노드
              - kubelet
              - kube-proxy
              - 컨테이너 런타임
            - CoreDNS
            - CNI (컨테이너 네트워크 인터페이스)
            
            ## 워크로드
            - 파드
            - 디플로이먼트
              - 레플리카셋
              - 롤아웃
              - 롤백
            - 스테이트풀셋
              - 헤드리스 서비스
              - 영구 식별자
            - 데몬셋
            - 잡
            - 크론잡
            
            ## 네트워킹
            - 서비스
              - 클러스터IP
              - 노드포트
              - 로드밸런서
              - 외부이름
            - 인그레스
              - 인그레스 컨트롤러
              - 경로 기반 라우팅
            - 네트워크 정책
              - 인그레스 규칙
              - 이그레스 규칙
              - 레이블 선택기
            
            ## 스토리지
            - 퍼시스턴트볼륨
            - 퍼시스턴트볼륨클레임
            - 스토리지클래스
            - 볼륨 유형
              - emptyDir
              - hostPath
              - configMap/Secret
            
            ## 보안
            - RBAC
              - 롤
              - 클러스터롤
              - 롤바인딩
            - 시크릿
              - Opaque
              - TLS
              - Docker Registry
            - 서비스어카운트
            
            # Amazon EKS
            
            ## AWS 통합
            - IAM
              - IRSA (서비스 계정용 IAM 역할)
              - IAM 인증기
            - ELB
              - ALB 인그레스 컨트롤러
              - NLB
            - EBS
              - EBS CSI 드라이버
            - 파게이트
            - VPC CNI
            - ECR
            """
            
            # 확장/축소 기능이 있는 마인드맵 렌더링
            render_markmap_with_expand(markmap_data)
    
    # 플로우 차트 탭 (graphviz)
    with overview_tabs[2]:
        with st.container():
            # graphviz를 사용한 플로우차트
            flow = graphviz.Digraph()
            flow.attr('node', shape='box', style='filled', color='#2a9d8f', 
                     fillcolor='#e0f5f1', fontname='Arial', fontsize='14')
            flow.attr('edge', color='#76c893')
            flow.attr(rankdir='TB', bgcolor='white')
            
            # 주요 노드 추가
            flow.node('k8s', '쿠버네티스', fillcolor='#2a9d8f', fontcolor='white')
            flow.node('eks', 'Amazon EKS', fillcolor='#2a9d8f', fontcolor='white')
            
            # 1차 레벨 노드
            flow.node('core', '핵심 컴포넌트', fillcolor='#40b3a2', fontcolor='white')
            flow.node('workload', '워크로드', fillcolor='#40b3a2', fontcolor='white')
            flow.node('network', '네트워킹', fillcolor='#40b3a2', fontcolor='white')
            flow.node('storage', '스토리지', fillcolor='#40b3a2', fontcolor='white')
            flow.node('security', '보안', fillcolor='#40b3a2', fontcolor='white')
            flow.node('aws', 'AWS 통합', fillcolor='#40b3a2', fontcolor='white')
            
            # 2차 레벨 노드들
            # 핵심 컴포넌트
            flow.node('control', '컨트롤 플레인', fillcolor='#52b69a', fontcolor='white')
            flow.node('worker', '워커 노드', fillcolor='#52b69a', fontcolor='white')
            
            # 워크로드 
            flow.node('pod', '파드', fillcolor='#52b69a', fontcolor='white')
            flow.node('deploy', '디플로이먼트', fillcolor='#52b69a', fontcolor='white')
            
            # 네트워킹
            flow.node('service', '서비스', fillcolor='#52b69a', fontcolor='white')
            flow.node('ingress', '인그레스', fillcolor='#52b69a', fontcolor='white')
            
            # 연결 관계 설정
            # 메인 연결
            flow.edge('eks', 'k8s')
            flow.edge('eks', 'aws')
            
            # 쿠버네티스에서 주요 카테고리로
            flow.edge('k8s', 'core')
            flow.edge('k8s', 'workload')
            flow.edge('k8s', 'network')
            flow.edge('k8s', 'storage')
            flow.edge('k8s', 'security')
            
            # 핵심 컴포넌트 연결
            flow.edge('core', 'control')
            flow.edge('core', 'worker')
            
            # 워크로드 연결
            flow.edge('workload', 'pod')
            flow.edge('workload', 'deploy')
            flow.edge('deploy', 'pod', label='관리')
            
            # 네트워킹 연결
            flow.edge('network', 'service')
            flow.edge('network', 'ingress')
            flow.edge('service', 'pod', label='노출')
            flow.edge('ingress', 'service', label='라우팅')
            
            # AWS 통합
            flow.edge('aws', 'iam', label='인증')
            flow.edge('aws', 'elb', label='로드밸런싱')
            
            # graphviz 렌더링
            st.graphviz_chart(flow, use_container_width=True)
            
    # 카테고리별 마인드맵 탭
    st.markdown("<h2 class='section-header'>카테고리별 개념 탐색</h2>", unsafe_allow_html=True)
    
    # 1차 탭: 카테고리 선택
    category_tabs = st.tabs(["핵심 컴포넌트", "워크로드", "네트워킹", "스토리지", "보안", "AWS 통합"])
    
    # 핵심 컴포넌트 탭
    with category_tabs[0]:
        st.markdown("<div class='category-box'>", unsafe_allow_html=True)
        st.markdown("<h3 class='category-title'><span class='icon'>C</span>핵심 컴포넌트</h3>", unsafe_allow_html=True)
        
        # 2차 탭: 시각화 방식 선택
        core_viz_tabs = st.tabs(["네트워크 그래프", "마인드맵", "플로우 차트"])
        
        # 네트워크 그래프 (agraph)
        with core_viz_tabs[0]:
            with st.container():
                # Core Components 마인드맵 (agraph)
                core_nodes = [
                    # 메인 노드
                    Node(id="core_main", label="핵심 컴포넌트", size=30, color="#2a9d8f"),
                    
                    # 컨트롤 플레인
                    Node(id="control_plane", label="컨트롤 플레인", size=25, color="#40b3a2"),
                    Node(id="api_server", label="kube-apiserver", size=20, color="#52b69a"),
                    Node(id="etcd", label="etcd", size=20, color="#52b69a"),
                    Node(id="scheduler", label="kube-scheduler", size=20, color="#52b69a"),
                    Node(id="controller", label="kube-controller-manager", size=20, color="#52b69a"),
                    Node(id="ccm", label="cloud-controller-manager", size=20, color="#52b69a"),
                    
                    # 워커 노드
                    Node(id="worker_node", label="워커 노드", size=25, color="#40b3a2"),
                    Node(id="kubelet", label="kubelet", size=20, color="#52b69a"),
                    Node(id="kube_proxy", label="kube-proxy", size=20, color="#52b69a"),
                    Node(id="container", label="컨테이너 런타임", size=20, color="#52b69a"),
                    
                    # 추가 컴포넌트
                    Node(id="dns", label="CoreDNS", size=20, color="#52b69a"),
                    Node(id="cni", label="CNI", size=20, color="#52b69a"),
                ]
                
                core_edges = [
                    # 컨트롤 플레인 연결
                    Edge(source="core_main", target="control_plane"),
                    Edge(source="control_plane", target="api_server"),
                    Edge(source="control_plane", target="etcd"),
                    Edge(source="control_plane", target="scheduler"),
                    Edge(source="control_plane", target="controller"),
                    Edge(source="control_plane", target="ccm"),
                    
                    # 워커 노드 연결
                    Edge(source="core_main", target="worker_node"),
                    Edge(source="worker_node", target="kubelet"),
                    Edge(source="worker_node", target="kube_proxy"),
                    Edge(source="worker_node", target="container"),
                    
                    # 추가 컴포넌트 연결
                    Edge(source="core_main", target="dns"),
                    Edge(source="core_main", target="cni"),
                    
                    # 구성 요소 간 연결
                    Edge(source="api_server", target="etcd"),
                    Edge(source="kubelet", target="api_server"),
                    Edge(source="kubelet", target="container"),
                ]
                
                core_config = Config(
                    width=700,
                    height=500,
                    directed=True,
                    physics=True,
                    hierarchical=True,
                    nodeHighlightBehavior=True,
                    highlightColor="#e0f5f1",
                    collapsible=True,
                    node={"labelProperty": "label"},
                    link={"labelProperty": "label", "renderLabel": False},
                    node_color="#2a9d8f",
                    node_size=20,
                    node_font_size=12,
                    edge_color="#76c893"
                )
                
                agraph(nodes=core_nodes, edges=core_edges, config=core_config)
        
        # 마인드맵 (markmap)
        with core_viz_tabs[1]:
            with st.container():
                # 핵심 컴포넌트 마인드맵 (markmap)
                core_markmap = """
                # 핵심 컴포넌트
                
                ## 컨트롤 플레인
                - kube-apiserver
                  - REST API 엔드포인트
                  - 인증 및 인가
                  - 클러스터 관리 기능
                - etcd
                  - 분산 키-값 저장소
                  - 모든 클러스터 상태 저장
                  - 고가용성 설계
                - kube-scheduler
                  - Pod 배치 결정
                  - 리소스 요구사항 분석
                  - 노드 선택 알고리즘
                - kube-controller-manager
                  - 각종 컨트롤러 관리
                  - Node 컨트롤러
                  - Deployment 컨트롤러
                  - Service 컨트롤러
                - cloud-controller-manager
                  - 클라우드 리소스 관리
                  - Load Balancer 컨트롤러
                  - Node 라이프사이클 관리
                
                ## 워커 노드
                - kubelet
                  - Pod 및 컨테이너 관리
                  - API 서버와 통신
                  - 노드 상태 보고
                  - Pod 스케줄링 실행
                - kube-proxy
                  - 네트워크 규칙 설정
                  - 서비스 IP 라우팅
                  - iptables/IPVS 규칙 관리
                - 컨테이너 런타임
                  - containerd
                  - CRI-O
                  - Docker (레거시)
                
                ## 추가 컴포넌트
                - CoreDNS
                  - 클러스터 내 DNS 서비스
                  - 서비스 디스커버리
                - CNI (컨테이너 네트워크 인터페이스)
                  - Calico
                  - Flannel
                  - Cilium
                  - AWS VPC CNI
                """
                
                render_markmap_with_expand(core_markmap)
        
        # 플로우 차트 (graphviz)
        with core_viz_tabs[2]:
            with st.container():
                # graphviz를 사용한 플로우차트 (핵심 컴포넌트)
                core_flow = graphviz.Digraph()
                core_flow.attr('node', shape='box', style='filled', color='#2a9d8f', 
                             fillcolor='#e0f5f1', fontname='Arial', fontsize='14')
                core_flow.attr('edge', color='#76c893')
                core_flow.attr(rankdir='TB', bgcolor='white')
                
                # 주요 노드 추가
                core_flow.node('core', '핵심 컴포넌트', fillcolor='#2a9d8f', fontcolor='white')
                
                # 컨트롤 플레인 서브그래프
                with core_flow.subgraph(name='cluster_control') as control:
                    control.attr(style='filled', color='#e0f5f1')
                    control.node('control_plane', '컨트롤 플레인', fillcolor='#40b3a2', fontcolor='white')
                    control.node('api', 'kube-apiserver', fillcolor='#52b69a', fontcolor='white')
                    control.node('etcd', 'etcd', fillcolor='#52b69a', fontcolor='white')
                    control.node('scheduler', 'kube-scheduler', fillcolor='#52b69a', fontcolor='white')
                    control.node('controller', 'kube-controller-manager', fillcolor='#52b69a', fontcolor='white')
                
                # 워커 노드 서브그래프
                with core_flow.subgraph(name='cluster_worker') as worker:
                    worker.attr(style='filled', color='#e0f5f1')
                    worker.node('worker', '워커 노드', fillcolor='#40b3a2', fontcolor='white')
                    worker.node('kubelet', 'kubelet', fillcolor='#52b69a', fontcolor='white')
                    worker.node('proxy', 'kube-proxy', fillcolor='#52b69a', fontcolor='white')
                    worker.node('runtime', '컨테이너 런타임', fillcolor='#52b69a', fontcolor='white')
                
                # 추가 컴포넌트
                core_flow.node('dns', 'CoreDNS', fillcolor='#52b69a', fontcolor='white')
                core_flow.node('cni', 'CNI', fillcolor='#52b69a', fontcolor='white')
                
                # 연결
                core_flow.edge('core', 'control_plane')
                core_flow.edge('core', 'worker')
                core_flow.edge('core', 'dns')
                core_flow.edge('core', 'cni')
                
                core_flow.edge('control_plane', 'api')
                core_flow.edge('control_plane', 'etcd')
                core_flow.edge('control_plane', 'scheduler')
                core_flow.edge('control_plane', 'controller')
                
                core_flow.edge('worker', 'kubelet')
                core_flow.edge('worker', 'proxy')
                core_flow.edge('worker', 'runtime')
                
                core_flow.edge('api', 'etcd', label='저장')
                core_flow.edge('kubelet', 'api', label='통신')
                core_flow.edge('kubelet', 'runtime', label='관리')
                
                # graphviz 렌더링
                st.graphviz_chart(core_flow, use_container_width=True)
        
        # 핵심 컴포넌트 설명
        st.markdown("""
        <div style="margin-top: 20px; padding: 15px; background-color: var(--green-light); border-radius: 8px;">
            <h4 style="color: #000000; margin-top: 0;">주요 구성 요소 설명</h4>
            <ul>
                <li><strong>kube-apiserver</strong>: 모든 쿠버네티스 컴포넌트의 통신을 중재하는 중앙 API 서버</li>
                <li><strong>etcd</strong>: 클러스터의 모든 상태 정보를 저장하는 분산형 키-값 저장소</li>
                <li><strong>kube-scheduler</strong>: 새로운 파드를 워커 노드에 할당하는 스케줄러</li>
                <li><strong>kube-controller-manager</strong>: 다양한 컨트롤러를 실행하여 클러스터 상태 관리</li>
                <li><strong>kubelet</strong>: 각 노드에서 컨테이너 실행을 담당하는 에이전트</li>
                <li><strong>kube-proxy</strong>: 네트워크 프록시 및 로드 밸런싱 기능 제공</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 워크로드 탭
    with category_tabs[1]:
        st.markdown("<div class='category-box'>", unsafe_allow_html=True)
        st.markdown("<h3 class='category-title'><span class='icon'>W</span>워크로드</h3>", unsafe_allow_html=True)
        
        # 2차 탭: 시각화 방식 선택
        workload_viz_tabs = st.tabs(["네트워크 그래프", "마인드맵", "플로우 차트"])
        
        # 네트워크 그래프 (agraph)
        with workload_viz_tabs[0]:
            with st.container():
                # 워크로드 네트워크 그래프
                workload_nodes = [
                    Node(id="workload_main", label="워크로드", size=30, color="#2a9d8f"),
                    
                    # 주요 워크로드 유형
                    Node(id="pod_main", label="파드", size=25, color="#40b3a2"),
                    Node(id="deploy_main", label="디플로이먼트", size=25, color="#40b3a2"),
                    Node(id="stateful_main", label="스테이트풀셋", size=25, color="#40b3a2"),
                    Node(id="daemon_main", label="데몬셋", size=25, color="#40b3a2"),
                    Node(id="job_main", label="잡", size=25, color="#40b3a2"),
                    Node(id="cronjob_main", label="크론잡", size=25, color="#40b3a2"),
                    
                    # 추가 상세 노드
                    Node(id="container_pod", label="컨테이너", size=20, color="#52b69a"),
                    Node(id="volume_pod", label="볼륨", size=20, color="#52b69a"),
                    Node(id="replicaset", label="레플리카셋", size=20, color="#52b69a"),
                    Node(id="rollout", label="롤아웃", size=20, color="#52b69a"),
                    Node(id="pvc_stateful", label="PVC", size=20, color="#52b69a"),
                    Node(id="headless", label="헤드리스 서비스", size=20, color="#52b69a"),
                ]
                
                workload_edges = [
                    Edge(source="workload_main", target="pod_main"),
                    Edge(source="workload_main", target="deploy_main"),
                    Edge(source="workload_main", target="stateful_main"),
                    Edge(source="workload_main", target="daemon_main"),
                    Edge(source="workload_main", target="job_main"),
                    Edge(source="workload_main", target="cronjob_main"),
                    
                    Edge(source="pod_main", target="container_pod"),
                    Edge(source="pod_main", target="volume_pod"),
                    Edge(source="deploy_main", target="replicaset"),
                    Edge(source="deploy_main", target="rollout"),
                    Edge(source="replicaset", target="pod_main"),
                    Edge(source="stateful_main", target="pod_main"),
                    Edge(source="stateful_main", target="pvc_stateful"),
                    Edge(source="stateful_main", target="headless"),
                    Edge(source="daemon_main", target="pod_main"),
                    Edge(source="job_main", target="pod_main"),
                    Edge(source="cronjob_main", target="job_main"),
                ]
                
                workload_config = Config(
                    width=700,
                    height=500,
                    directed=True,
                    physics=True,
                    hierarchical=False,
                    nodeHighlightBehavior=True,
                    highlightColor="#e0f5f1",
                    collapsible=True,
                    node={"labelProperty": "label"},
                    link={"labelProperty": "label", "renderLabel": False},
                    node_color="#2a9d8f",
                    node_size=20,
                    node_font_size=12,
                    edge_color="#76c893"
                )
                
                agraph(nodes=workload_nodes, edges=workload_edges, config=workload_config)
        
        # 마인드맵 (markmap)
        with workload_viz_tabs[1]:
            with st.container():
                # 워크로드 마인드맵
                workload_markmap = """
                # 워크로드
                
                ## 파드 (Pod)
                - 가장 작은 배포 단위
                - 하나 이상의 컨테이너로 구성
                - 동일 노드에서 실행
                - 공유 컨텍스트
                  - 네트워크 네임스페이스
                  - IPC 네임스페이스
                  - 볼륨
                
                ## 디플로이먼트 (Deployment)
                - 상태가 없는(Stateless) 애플리케이션 관리
                - 레플리카셋 자동 생성
                - 배포 전략
                  - 롤링 업데이트 (기본값)
                  - 재생성 (Recreate)
                - 롤백 기능
                - 수평 스케일링
                
                ## 스테이트풀셋 (StatefulSet)
                - 상태가 있는(Stateful) 애플리케이션 관리
                - 안정적인 네트워크 아이덴티티
                  - 예측 가능한 파드 이름
                  - 영구 식별자
                - 순서 보장
                  - 순차적 배포
                  - 순차적 스케일링
                - 영구 스토리지 연결
                
                ## 데몬셋 (DaemonSet)
                - 모든(또는 특정) 노드에 파드 배포
                - 용도
                  - 로그 수집기
                  - 모니터링 에이전트
                  - 스토리지 데몬
                  - 네트워크 플러그인
                
                ## 잡 (Job)
                - 일회성 작업 실행
                - 완료 보장
                - 실패 시 재시도
                - 병렬 실행 지원
                
                ## 크론잡 (CronJob)
                - 일정에 따라 잡 실행
                - Cron 표현식 사용
                  - `* * * * *` (분, 시, 일, 월, 요일)
                - 타임아웃 및 동시성 설정
                """
                
                render_markmap_with_expand(workload_markmap)
        
        # 플로우 차트 (graphviz)
        with workload_viz_tabs[2]:
            with st.container():
                # 워크로드 플로우 차트
                workload_flow = graphviz.Digraph()
                workload_flow.attr('node', shape='box', style='filled', color='#2a9d8f', 
                                  fillcolor='#e0f5f1', fontname='Arial', fontsize='14')
                workload_flow.attr('edge', color='#76c893')
                workload_flow.attr(rankdir='TB', bgcolor='white')
                
                # 메인 노드
                workload_flow.node('workload', '워크로드', fillcolor='#2a9d8f', fontcolor='white')
                
                # 워크로드 타입
                workload_flow.node('pod', '파드', fillcolor='#40b3a2', fontcolor='white')
                workload_flow.node('deploy', '디플로이먼트', fillcolor='#40b3a2', fontcolor='white')
                workload_flow.node('stateful', '스테이트풀셋', fillcolor='#40b3a2', fontcolor='white')
                workload_flow.node('daemonset', '데몬셋', fillcolor='#40b3a2', fontcolor='white')
                workload_flow.node('job', '잡', fillcolor='#40b3a2', fontcolor='white')
                workload_flow.node('cronjob', '크론잡', fillcolor='#40b3a2', fontcolor='white')
                
                # 관련 리소스
                workload_flow.node('container', '컨테이너', fillcolor='#52b69a', fontcolor='white')
                workload_flow.node('rs', '레플리카셋', fillcolor='#52b69a', fontcolor='white')
                workload_flow.node('pvc', 'PVC', fillcolor='#52b69a', fontcolor='white')
                
                # 연결 관계
                workload_flow.edge('workload', 'pod')
                workload_flow.edge('workload', 'deploy')
                workload_flow.edge('workload', 'stateful')
                workload_flow.edge('workload', 'daemonset')
                workload_flow.edge('workload', 'job')
                workload_flow.edge('workload', 'cronjob')
                
                workload_flow.edge('pod', 'container')
                workload_flow.edge('deploy', 'rs')
                workload_flow.edge('rs', 'pod')
                workload_flow.edge('stateful', 'pod')
                workload_flow.edge('stateful', 'pvc', label='영구 저장소')
                workload_flow.edge('daemonset', 'pod')
                workload_flow.edge('job', 'pod')
                workload_flow.edge('cronjob', 'job', label='스케줄')
                
                # 렌더링
                st.graphviz_chart(workload_flow, use_container_width=True)
        
        # 워크로드 설명
        st.markdown("""
        <div style="margin-top: 20px; padding: 15px; background-color: var(--green-light); border-radius: 8px;">
            <h4 style="color: #000000; margin-top: 0;">워크로드 리소스 특징</h4>
            <ul>
                <li><strong>Pod</strong>: Kubernetes에서 배포할 수 있는 가장 작은 단위로, 하나 이상의 컨테이너를 포함</li>
                <li><strong>Deployment</strong>: 상태가 없는(Stateless) 애플리케이션을 위한 선언적 업데이트</li>
                <li><strong>StatefulSet</strong>: 상태 유지가 필요한(Stateful) 애플리케이션을 위한 워크로드 리소스</li>
                <li><strong>DaemonSet</strong>: 클러스터의 모든 노드에 특정 Pod가 실행되도록 보장</li>
                <li><strong>Job</strong>: 실행 완료될 때까지 Pod를 실행</li>
                <li><strong>CronJob</strong>: 시간 기반 스케줄에 따라 Job을 생성</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 네트워킹 탭
    with category_tabs[2]:
        st.markdown("<div class='category-box'>", unsafe_allow_html=True)
        st.markdown("<h3 class='category-title'><span class='icon'>N</span>네트워킹</h3>", unsafe_allow_html=True)
        
        network_viz_tabs = st.tabs(["네트워크 그래프", "마인드맵", "플로우 차트"])
        
        # 네트워크 그래프 (agraph)
        with network_viz_tabs[0]:
            with st.container():
                # 네트워킹 네트워크 그래프
                network_nodes = [
                    Node(id="network_main", label="네트워킹", size=30, color="#2a9d8f"),
                    
                    # 주요 서비스 유형
                    Node(id="service_main", label="서비스", size=25, color="#40b3a2"),
                    Node(id="ingress_main", label="인그레스", size=25, color="#40b3a2"),
                    Node(id="network_policy", label="네트워크 정책", size=25, color="#40b3a2"),
                    Node(id="dns_main", label="DNS", size=25, color="#40b3a2"),
                    
                    # 서비스 타입
                    Node(id="clusterip", label="ClusterIP", size=20, color="#52b69a"),
                    Node(id="nodeport", label="NodePort", size=20, color="#52b69a"),
                    Node(id="loadbalancer", label="LoadBalancer", size=20, color="#52b69a"),
                    Node(id="externalname", label="ExternalName", size=20, color="#52b69a"),
                    
                    # 인그레스 관련
                    Node(id="ingress_controller", label="인그레스 컨트롤러", size=20, color="#52b69a"),
                    Node(id="tls", label="TLS 종료", size=20, color="#52b69a"),
                    
                    # 기타 네트워킹 구성 요소
                    Node(id="pod_net", label="파드 네트워킹", size=20, color="#52b69a"),
                    Node(id="cni_main", label="CNI", size=20, color="#52b69a"),
                ]
                
                network_edges = [
                    Edge(source="network_main", target="service_main"),
                    Edge(source="network_main", target="ingress_main"),
                    Edge(source="network_main", target="network_policy"),
                    Edge(source="network_main", target="dns_main"),
                    Edge(source="network_main", target="pod_net"),
                    Edge(source="network_main", target="cni_main"),
                    
                    Edge(source="service_main", target="clusterip"),
                    Edge(source="service_main", target="nodeport"),
                    Edge(source="service_main", target="loadbalancer"),
                    Edge(source="service_main", target="externalname"),
                    
                    Edge(source="ingress_main", target="ingress_controller"),
                    Edge(source="ingress_main", target="tls"),
                    Edge(source="ingress_main", target="service_main"),
                ]
                
                network_config = Config(
                    width=700,
                    height=500,
                    directed=True,
                    physics=True,
                    hierarchical=False,
                    nodeHighlightBehavior=True,
                    highlightColor="#e0f5f1",
                    collapsible=True,
                    node={"labelProperty": "label"},
                    link={"labelProperty": "label", "renderLabel": False},
                    node_color="#2a9d8f",
                    node_size=20,
                    node_font_size=12,
                    edge_color="#76c893"
                )
                
                agraph(nodes=network_nodes, edges=network_edges, config=network_config)
        
        # 마인드맵 (markmap)
        with network_viz_tabs[1]:
            with st.container():
                # 네트워킹 마인드맵
                network_markmap = """
                # 쿠버네티스 네트워킹
                
                ## 서비스
                - ClusterIP (기본)
                  - 클러스터 내부 통신용
                  - 안정적인 IP 주소
                - NodePort
                  - 외부에서 접근 가능
                  - 노드 포트 범위: 30000-32767
                - LoadBalancer
                  - 클라우드 로드 밸런서 프로비저닝
                  - 외부 트래픽 분산
                - ExternalName
                  - DNS CNAME 레코드 매핑
                - Headless Service
                  - ClusterIP 없음
                  - 모든 Pod IP 반환
                
                ## 인그레스
                - 외부 HTTP(S) 트래픽 라우팅
                - URL 기반 라우팅
                - SSL/TLS 종단
                - 컨트롤러 종류
                  - Nginx Ingress Controller
                  - AWS ALB Controller
                  - Contour
                  - Traefik
                
                ## 네트워크 정책
                - Pod 간 통신 제한
                - 네트워크 세분화
                - 방향성
                  - Ingress 규칙 (들어오는 트래픽)
                  - Egress 규칙 (나가는 트래픽)
                
                ## CNI (Container Network Interface)
                - 네트워크 플러그인 인터페이스
                - 구현체
                  - AWS VPC CNI
                  - Calico
                  - Cilium
                  - Flannel
                
                ## DNS
                - CoreDNS
                  - 클러스터 내부 DNS 서비스
                  - 서비스 디스커버리
                - 네임스페이스 기반 DNS
                  - service.namespace.svc.cluster.local
                
                ## Service Mesh
                - Istio
                - Linkerd
                - AWS App Mesh
                """
                
                render_markmap_with_expand(network_markmap)
        
        # 플로우 차트 (graphviz)
        with network_viz_tabs[2]:
            with st.container():
                # 네트워킹 플로우 차트
                network_flow = graphviz.Digraph()
                network_flow.attr('node', shape='box', style='filled', color='#2a9d8f', 
                                 fillcolor='#e0f5f1', fontname='Arial', fontsize='14')
                network_flow.attr('edge', color='#76c893')
                network_flow.attr(rankdir='LR', bgcolor='white')
                
                # 메인 노드
                network_flow.node('network', '네트워킹', fillcolor='#2a9d8f', fontcolor='white')
                
                # 주요 네트워킹 컴포넌트
                network_flow.node('service', '서비스', fillcolor='#40b3a2', fontcolor='white')
                network_flow.node('ingress', '인그레스', fillcolor='#40b3a2', fontcolor='white')
                network_flow.node('netpol', '네트워크 정책', fillcolor='#40b3a2', fontcolor='white')
                network_flow.node('dns', 'DNS (CoreDNS)', fillcolor='#40b3a2', fontcolor='white')
                
                # 서비스 유형
                network_flow.node('clusterip', 'ClusterIP', fillcolor='#52b69a', fontcolor='white')
                network_flow.node('nodeport', 'NodePort', fillcolor='#52b69a', fontcolor='white')
                network_flow.node('lb', 'LoadBalancer', fillcolor='#52b69a', fontcolor='white')
                
                # 외부 요소
                network_flow.node('external', '외부 사용자', shape='ellipse')
                network_flow.node('pod', '파드', fillcolor='#52b69a', fontcolor='white')
                
                # 연결 관계
                network_flow.edge('network', 'service')
                network_flow.edge('network', 'ingress')
                network_flow.edge('network', 'netpol')
                network_flow.edge('network', 'dns')
                
                network_flow.edge('service', 'clusterip')
                network_flow.edge('service', 'nodeport')
                network_flow.edge('service', 'lb')
                
                network_flow.edge('external', 'ingress', label='HTTP(S)')
                network_flow.edge('ingress', 'service', label='라우팅')
                network_flow.edge('service', 'pod', label='트래픽 전달')
                network_flow.edge('dns', 'service', label='이름 해석')
                network_flow.edge('netpol', 'pod', label='통신 제어')
                
                # 렌더링
                st.graphviz_chart(network_flow, use_container_width=True)
                
        # 네트워킹 설명
        st.markdown("""
        <div style="margin-top: 20px; padding: 15px; background-color: var(--green-light); border-radius: 8px;">
            <h4 style="color: #000000; margin-top: 0;">쿠버네티스 네트워킹 주요 개념</h4>
            <ul>
                <li><strong>Service</strong>: 파드 집합에 대한 안정적인 엔드포인트와 로드 밸런싱 제공</li>
                <li><strong>Ingress</strong>: HTTP/HTTPS 트래픽을 클러스터 내부 서비스로 라우팅</li>
                <li><strong>NetworkPolicy</strong>: 파드 간 네트워크 통신에 대한 액세스 제어 규칙 정의</li>
                <li><strong>CoreDNS</strong>: 쿠버네티스 클러스터 내에서 DNS 기반 서비스 디스커버리 제공</li>
                <li><strong>CNI</strong>: 컨테이너 간 네트워크 통신을 위한 플러그인 인터페이스 표준</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 스토리지 탭
    with category_tabs[3]:
        st.markdown("<div class='category-box'>", unsafe_allow_html=True)
        st.markdown("<h3 class='category-title'><span class='icon'>S</span>스토리지</h3>", unsafe_allow_html=True)
        
        storage_viz_tabs = st.tabs(["네트워크 그래프", "마인드맵", "플로우 차트"])
        
        # 네트워크 그래프 (agraph)
        with storage_viz_tabs[0]:
            with st.container():
                # 스토리지 네트워크 그래프
                storage_nodes = [
                    Node(id="storage_main", label="스토리지", size=30, color="#2a9d8f"),
                    
                    # 주요 스토리지 리소스
                    Node(id="pv_main", label="퍼시스턴트볼륨", size=25, color="#40b3a2"),
                    Node(id="pvc_main", label="퍼시스턴트볼륨클레임", size=25, color="#40b3a2"),
                    Node(id="sc_main", label="스토리지클래스", size=25, color="#40b3a2"),
                    Node(id="volume_main", label="볼륨", size=25, color="#40b3a2"),
                    Node(id="csi_main", label="CSI", size=25, color="#40b3a2"),
                    
                    # 볼륨 타입
                    Node(id="emptydir", label="emptyDir", size=20, color="#52b69a"),
                    Node(id="hostpath", label="hostPath", size=20, color="#52b69a"),
                    Node(id="configmap", label="ConfigMap", size=20, color="#52b69a"),
                    Node(id="secret_vol", label="Secret", size=20, color="#52b69a"),
                    
                    # 클라우드 스토리지
                    Node(id="awsebs", label="awsElasticBlockStore", size=20, color="#52b69a"),
                    Node(id="azuredisk", label="azureDisk", size=20, color="#52b69a"),
                    Node(id="gcepd", label="gcePersistentDisk", size=20, color="#52b69a"),
                ]
                
                storage_edges = [
                    Edge(source="storage_main", target="pv_main"),
                    Edge(source="storage_main", target="pvc_main"),
                    Edge(source="storage_main", target="sc_main"),
                    Edge(source="storage_main", target="volume_main"),
                    Edge(source="storage_main", target="csi_main"),
                    
                    Edge(source="pvc_main", target="pv_main"),
                    Edge(source="sc_main", target="pv_main"),
                    
                    Edge(source="volume_main", target="emptydir"),
                    Edge(source="volume_main", target="hostpath"),
                    Edge(source="volume_main", target="configmap"),
                    Edge(source="volume_main", target="secret_vol"),
                    Edge(source="volume_main", target="awsebs"),
                    Edge(source="volume_main", target="azuredisk"),
                    Edge(source="volume_main", target="gcepd"),
                    
                    Edge(source="csi_main", target="pv_main"),
                ]
                
                storage_config = Config(
                    width=700,
                    height=500,
                    directed=True,
                    physics=True,
                    hierarchical=False,
                    nodeHighlightBehavior=True,
                    highlightColor="#e0f5f1",
                    collapsible=True,
                    node={"labelProperty": "label"},
                    link={"labelProperty": "label", "renderLabel": False},
                    node_color="#2a9d8f",
                    node_size=20,
                    node_font_size=12,
                    edge_color="#76c893"
                )
                
                agraph(nodes=storage_nodes, edges=storage_edges, config=storage_config)
        
        # 마인드맵 (markmap)
        with storage_viz_tabs[1]:
            with st.container():
                # 스토리지 마인드맵
                storage_markmap = """
                # 쿠버네티스 스토리지
                
                ## 볼륨 종류
                - emptyDir
                  - 임시 스토리지
                  - Pod 생명주기와 연결
                - hostPath
                  - 노드의 파일시스템 마운트
                  - 개발 및 테스트용
                - configMap/Secret
                  - 구성 데이터 저장
                  - 환경변수/파일로 마운트
                - 클라우드 볼륨
                  - awsElasticBlockStore
                  - azureDisk
                  - gcePersistentDisk
                
                ## 퍼시스턴트볼륨 (PV)
                - 클러스터 수준 리소스
                - 관리자가 프로비저닝
                - 수명주기
                  - 프로비저닝
                  - 바인딩
                  - 사용
                  - 반환
                - 접근 모드
                  - ReadWriteOnce (RWO)
                  - ReadOnlyMany (ROX)
                  - ReadWriteMany (RWX)
                
                ## 퍼시스턴트볼륨클레임 (PVC)
                - 사용자의 스토리지 요청
                - PV와 바인딩
                - 네임스페이스 범위
                
                ## 스토리지클래스
                - 동적 볼륨 프로비저닝
                - 스토리지 프로파일 정의
                - 프로비저너 유형
                  - AWS EBS
                  - Azure Disk
                  - NFS
                  - Ceph RBD
                - 파라미터
                  - 유형
                  - 성능 등급
                  - 영역/리전
                
                ## CSI (Container Storage Interface)
                - 스토리지 드라이버 표준
                - 플러그인
                  - EBS CSI Driver
                  - EFS CSI Driver
                  - Azure Disk CSI Driver
                """
                
                render_markmap_with_expand(storage_markmap)
        
        # 플로우 차트 (graphviz)
        with storage_viz_tabs[2]:
            with st.container():
                # 스토리지 플로우 차트
                storage_flow = graphviz.Digraph()
                storage_flow.attr('node', shape='box', style='filled', color='#2a9d8f', 
                                 fillcolor='#e0f5f1', fontname='Arial', fontsize='14')
                storage_flow.attr('edge', color='#76c893')
                storage_flow.attr(rankdir='LR', bgcolor='white')
                
                # 메인 노드
                storage_flow.node('storage', '스토리지', fillcolor='#2a9d8f', fontcolor='white')
                
                # 주요 스토리지 컴포넌트
                storage_flow.node('pv', '퍼시스턴트볼륨 (PV)', fillcolor='#40b3a2', fontcolor='white')
                storage_flow.node('pvc', '퍼시스턴트볼륨클레임 (PVC)', fillcolor='#40b3a2', fontcolor='white')
                storage_flow.node('sc', '스토리지클래스', fillcolor='#40b3a2', fontcolor='white')
                
                # 볼륨 타입
                storage_flow.node('vol_types', '볼륨 타입', fillcolor='#52b69a', fontcolor='white')
                
                # 관련 요소
                storage_flow.node('pod', '파드', fillcolor='#52b69a', fontcolor='white')
                storage_flow.node('cloud', '클라우드 스토리지', shape='ellipse')
                
                # 연결 관계
                storage_flow.edge('storage', 'pv')
                storage_flow.edge('storage', 'pvc')
                storage_flow.edge('storage', 'sc')
                storage_flow.edge('storage', 'vol_types')
                
                storage_flow.edge('pvc', 'pv', label='바인딩')
                storage_flow.edge('sc', 'pv', label='동적 프로비저닝')
                storage_flow.edge('pvc', 'pod', label='볼륨 요청')
                storage_flow.edge('pv', 'cloud', label='백엔드 스토리지')
                storage_flow.edge('vol_types', 'pod', label='직접 마운트')
                
                # 렌더링
                st.graphviz_chart(storage_flow, use_container_width=True)
                
        # 스토리지 설명
        st.markdown("""
        <div style="margin-top: 20px; padding: 15px; background-color: var(--green-light); border-radius: 8px;">
            <h4 style="color: #000000; margin-top: 0;">쿠버네티스 스토리지 개념</h4>
            <ul>
                <li><strong>볼륨</strong>: 파드 내 컨테이너에 마운트하여 데이터를 저장하기 위한 디렉토리</li>
                <li><strong>퍼시스턴트볼륨(PV)</strong>: 관리자가 프로비저닝하거나 동적으로 생성된 스토리지 단위</li>
                <li><strong>퍼시스턴트볼륨클레임(PVC)</strong>: 사용자의 스토리지 요청을 나타내는 리소스</li>
                <li><strong>스토리지클래스</strong>: 스토리지 프로비저너와 파라미터를 정의하는 리소스</li>
                <li><strong>CSI</strong>: 쿠버네티스에서 외부 스토리지 시스템을 통합하기 위한 표준 인터페이스</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 보안 탭
    with category_tabs[4]:
        st.markdown("<div class='category-box'>", unsafe_allow_html=True)
        st.markdown("<h3 class='category-title'><span class='icon'>S</span>보안</h3>", unsafe_allow_html=True)
        
        security_viz_tabs = st.tabs(["네트워크 그래프", "마인드맵", "플로우 차트"])
        
        # 네트워크 그래프 (agraph)
        with security_viz_tabs[0]:
            with st.container():
                # 보안 네트워크 그래프
                security_nodes = [
                    Node(id="security_main", label="보안", size=30, color="#2a9d8f"),
                    
                    # 주요 보안 리소스
                    Node(id="rbac_main", label="RBAC", size=25, color="#40b3a2"),
                    Node(id="secret_main", label="시크릿", size=25, color="#40b3a2"),
                    Node(id="sa_main", label="서비스어카운트", size=25, color="#40b3a2"),
                    Node(id="psp_main", label="파드시큐리티폴리시", size=25, color="#40b3a2"),
                    Node(id="netpol_main", label="네트워크 정책", size=25, color="#40b3a2"),
                    
                    # RBAC 구성 요소
                    Node(id="role_main", label="롤", size=20, color="#52b69a"),
                    Node(id="clusterrole_main", label="클러스터롤", size=20, color="#52b69a"),
                    Node(id="rolebinding_main", label="롤바인딩", size=20, color="#52b69a"),
                    Node(id="clusterrolebinding_main", label="클러스터롤바인딩", size=20, color="#52b69a"),
                    
                    # 시크릿 타입
                    Node(id="opaque_secret", label="Opaque", size=20, color="#52b69a"),
                    Node(id="tls_secret", label="TLS", size=20, color="#52b69a"),
                    Node(id="docker_secret", label="Docker Registry", size=20, color="#52b69a"),
                ]
                
                security_edges = [
                    Edge(source="security_main", target="rbac_main"),
                    Edge(source="security_main", target="secret_main"),
                    Edge(source="security_main", target="sa_main"),
                    Edge(source="security_main", target="psp_main"),
                    Edge(source="security_main", target="netpol_main"),
                    
                    Edge(source="rbac_main", target="role_main"),
                    Edge(source="rbac_main", target="clusterrole_main"),
                    Edge(source="rbac_main", target="rolebinding_main"),
                    Edge(source="rbac_main", target="clusterrolebinding_main"),
                    
                    Edge(source="secret_main", target="opaque_secret"),
                    Edge(source="secret_main", target="tls_secret"),
                    Edge(source="secret_main", target="docker_secret"),
                    
                    Edge(source="sa_main", target="rbac_main"),
                ]
                
                security_config = Config(
                    width=700,
                    height=500,
                    directed=True,
                    physics=True,
                    hierarchical=False,
                    nodeHighlightBehavior=True,
                    highlightColor="#e0f5f1",
                    collapsible=True,
                    node={"labelProperty": "label"},
                    link={"labelProperty": "label", "renderLabel": False},
                    node_color="#2a9d8f",
                    node_size=20,
                    node_font_size=12,
                    edge_color="#76c893"
                )
                
                agraph(nodes=security_nodes, edges=security_edges, config=security_config)
        
        # 마인드맵 (markmap)
        with security_viz_tabs[1]:
            with st.container():
                # 보안 마인드맵
                security_markmap = """
                # 쿠버네티스 보안
                
                ## RBAC (역할 기반 접근 제어)
                - 롤 (Role)
                  - 네임스페이스 범위
                  - API 자원 접근 권한 정의
                  - 특정 네임스페이스 내 권한
                - 클러스터롤 (ClusterRole)
                  - 클러스터 범위
                  - 모든 네임스페이스에 적용
                  - 클러스터 범위 자원 적용 가능
                - 롤바인딩 (RoleBinding)
                  - 사용자와 롤 연결
                  - 네임스페이스 범위
                - 클러스터롤바인딩 (ClusterRoleBinding)
                  - 사용자와 클러스터롤 연결
                  - 클러스터 전체 적용
                
                ## 시크릿 (Secret)
                - 민감한 정보 저장
                - 유형
                  - Opaque (기본 타입)
                  - kubernetes.io/tls (TLS 인증서)
                  - kubernetes.io/dockerconfigjson (Docker 레지스트리)
                  - kubernetes.io/service-account-token
                - 접근 방법
                  - 환경 변수로 마운트
                  - 볼륨으로 마운트
                
                ## 서비스어카운트 (ServiceAccount)
                - Pod 인증용 계정
                - 기본 서비스어카운트 자동 할당
                - Pod 권한 제어 
                - RBAC와 연동
                
                ## 인증 (Authentication)
                - X.509 인증서
                - 서비스어카운트 토큰
                - OpenID Connect
                - Webhook Token
                - 인증 프록시
                
                ## 인가 (Authorization)
                - RBAC (기본)
                - ABAC (속성 기반)
                - Node 인가
                - Webhook
                
                ## 네트워크 보안
                - 네트워크 정책 (NetworkPolicy)
                - Pod 간 통신 제어
                - 네임스페이스 격리
                """
                
                render_markmap_with_expand(security_markmap)
        
        # 플로우 차트 (graphviz)
        with security_viz_tabs[2]:
            with st.container():
                # 보안 플로우 차트
                security_flow = graphviz.Digraph()
                security_flow.attr('node', shape='box', style='filled', color='#2a9d8f', 
                                  fillcolor='#e0f5f1', fontname='Arial', fontsize='14')
                security_flow.attr('edge', color='#76c893')
                security_flow.attr(rankdir='TB', bgcolor='white')
                
                # 메인 노드
                security_flow.node('security', '보안', fillcolor='#2a9d8f', fontcolor='white')
                
                # 인증/인가
                security_flow.node('auth', '인증/인가', fillcolor='#40b3a2', fontcolor='white')
                security_flow.node('rbac', 'RBAC', fillcolor='#40b3a2', fontcolor='white')
                security_flow.node('sa', '서비스어카운트', fillcolor='#40b3a2', fontcolor='white')
                
                # 리소스
                security_flow.node('secret', '시크릿', fillcolor='#40b3a2', fontcolor='white')
                security_flow.node('netpol', '네트워크 정책', fillcolor='#40b3a2', fontcolor='white')
                
                # 객체 및 리소스
                security_flow.node('pod', '파드', fillcolor='#52b69a', fontcolor='white')
                security_flow.node('user', '사용자', shape='ellipse')
                security_flow.node('role', '롤/클러스터롤', fillcolor='#52b69a', fontcolor='white')
                
                # 연결 관계
                security_flow.edge('security', 'auth')
                security_flow.edge('security', 'rbac')
                security_flow.edge('security', 'sa')
                security_flow.edge('security', 'secret')
                security_flow.edge('security', 'netpol')
                
                security_flow.edge('auth', 'user', label='인증')
                security_flow.edge('rbac', 'role', label='정의')
                security_flow.edge('role', 'user', label='권한 부여')
                security_flow.edge('sa', 'pod', label='identity')
                security_flow.edge('secret', 'pod', label='민감 정보')
                security_flow.edge('netpol', 'pod', label='네트워크 제어')
                
                # 렌더링
                st.graphviz_chart(security_flow, use_container_width=True)
                
        # 보안 설명
        st.markdown("""
        <div style="margin-top: 20px; padding: 15px; background-color: var(--green-light); border-radius: 8px;">
            <h4 style="color: #000000; margin-top: 0;">쿠버네티스 보안 개념</h4>
            <ul>
                <li><strong>RBAC</strong>: 사용자나 그룹이 쿠버네티스 API 리소스에 어떤 작업을 수행할 수 있는지 제어하는 역할 기반 접근 제어</li>
                <li><strong>ServiceAccount</strong>: 쿠버네티스 내부에서 실행되는 Pod가 API 서버에 인증하기 위한 계정</li>
                <li><strong>Secret</strong>: 비밀번호, API 키 등 민감한 정보를 저장하기 위한 리소스</li>
                <li><strong>NetworkPolicy</strong>: Pod 간 통신을 제어하는 방화벽 규칙</li>
                <li><strong>인증 & 인가</strong>: 사용자 인증(Authentication)과 권한 확인(Authorization)을 통한 API 접근 제어</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

    # AWS 통합 탭
    with category_tabs[5]:
        st.markdown("<div class='category-box'>", unsafe_allow_html=True)
        st.markdown("<h3 class='category-title'><span class='icon'>A</span>AWS 통합</h3>", unsafe_allow_html=True)
        
        aws_viz_tabs = st.tabs(["네트워크 그래프", "마인드맵", "플로우 차트"])
        
        # 네트워크 그래프 (agraph)
        with aws_viz_tabs[0]:
            with st.container():
                # AWS 통합 네트워크 그래프
                aws_nodes = [
                    Node(id="aws_main", label="AWS 통합", size=30, color="#2a9d8f"),
                    
                    # 주요 AWS 통합 영역
                    Node(id="iam_main", label="IAM", size=25, color="#40b3a2"),
                    Node(id="elb_main", label="ELB", size=25, color="#40b3a2"),
                    Node(id="ebs_main", label="EBS", size=25, color="#40b3a2"),
                    Node(id="ecr_main", label="ECR", size=25, color="#40b3a2"),
                    Node(id="vpc_main", label="VPC", size=25, color="#40b3a2"),
                    Node(id="fargate_main", label="Fargate", size=25, color="#40b3a2"),
                    
                    # IAM 관련
                    Node(id="irsa_main", label="IRSA", size=20, color="#52b69a"),
                    Node(id="iam_auth", label="IAM 인증", size=20, color="#52b69a"),
                    
                    # ELB 관련
                    Node(id="alb_main", label="ALB 인그레스", size=20, color="#52b69a"),
                    Node(id="nlb_main", label="NLB", size=20, color="#52b69a"),
                    
                    # EBS 관련
                    Node(id="ebs_csi", label="EBS CSI 드라이버", size=20, color="#52b69a"),
                    
                    # 쿠버네티스 통합 포인트
                    Node(id="service_main", label="서비스", size=20, color="#52b69a"),
                    Node(id="ingress_main", label="인그레스", size=20, color="#52b69a"),
                    Node(id="pv_main", label="퍼시스턴트볼륨", size=20, color="#52b69a"),
                    Node(id="pod_main", label="파드", size=20, color="#52b69a"),
                ]
                
                aws_edges = [
                    Edge(source="aws_main", target="iam_main"),
                    Edge(source="aws_main", target="elb_main"),
                    Edge(source="aws_main", target="ebs_main"),
                    Edge(source="aws_main", target="ecr_main"),
                    Edge(source="aws_main", target="vpc_main"),
                    Edge(source="aws_main", target="fargate_main"),
                    
                    Edge(source="iam_main", target="irsa_main"),
                    Edge(source="iam_main", target="iam_auth"),
                    
                    Edge(source="elb_main", target="alb_main"),
                    Edge(source="elb_main", target="nlb_main"),
                    
                    Edge(source="ebs_main", target="ebs_csi"),
                    
                    Edge(source="alb_main", target="ingress_main"),
                    Edge(source="nlb_main", target="service_main"),
                    Edge(source="ebs_csi", target="pv_main"),
                    Edge(source="irsa_main", target="pod_main"),
                    Edge(source="fargate_main", target="pod_main"),
                ]
                
                aws_config = Config(
                    width=700,
                    height=500,
                    directed=True,
                    physics=True,
                    hierarchical=False,
                    nodeHighlightBehavior=True,
                    highlightColor="#e0f5f1",
                    collapsible=True,
                    node={"labelProperty": "label"},
                    link={"labelProperty": "label", "renderLabel": False},
                    node_color="#2a9d8f",
                    node_size=20,
                    node_font_size=12,
                    edge_color="#76c893"
                )
                
                agraph(nodes=aws_nodes, edges=aws_edges, config=aws_config)
        
        # 마인드맵 (markmap)
        with aws_viz_tabs[1]:
            with st.container():
                # AWS 통합 마인드맵
                aws_markmap = """
                # Amazon EKS 통합
                
                ## IAM
                - IRSA (IAM Roles for Service Accounts)
                  - Pod 수준 권한 부여
                  - AWS 서비스 접근 권한
                  - 웹 아이덴티티 페더레이션
                - IAM 인증기
                  - kubectl 인증
                  - 콘솔 접근
                - 클러스터 롤 연동
                  - 관리자 권한
                  - 읽기 전용 권한
                - EKS 서비스 역할
                
                ## 로드 밸런서 통합
                - ALB (Application Load Balancer)
                  - ALB 인그레스 컨트롤러
                  - 경로 기반 라우팅
                  - TLS 종료
                  - WebSocket 지원
                - NLB (Network Load Balancer)
                  - 서비스 타입 LoadBalancer
                  - 고성능, 저지연
                  - 정적 IP 주소
                
                ## 스토리지 통합
                - EBS (Elastic Block Store)
                  - EBS CSI 드라이버
                  - 동적 프로비저닝
                  - 스냅샷
                - EFS (Elastic File System)
                  - EFS CSI 드라이버
                  - ReadWriteMany 지원
                - S3 (Simple Storage Service)
                  - 백업
                  - 로그
                  - 정적 컨텐츠
                
                ## 컨테이너 이미지
                - ECR (Elastic Container Registry)
                  - 프라이빗 이미지 저장소
                  - 취약성 스캔
                  - IRSA 인증
                  - 이미지 버전 관리
                
                ## 네트워킹
                - VPC CNI
                  - Pod IP = VPC IP
                  - 보안그룹 통합
                - AWS PrivateLink
                - VPC 엔드포인트
                - Transit Gateway 연동
                
                ## 서버리스 통합
                - AWS Fargate
                  - 노드 관리 불필요
                  - Pod 단위 과금
                  - 보안 격리
                """
                
                render_markmap_with_expand(aws_markmap)
        
        # 플로우 차트 (graphviz)
        with aws_viz_tabs[2]:
            with st.container():
                # AWS 통합 플로우 차트
                aws_flow = graphviz.Digraph()
                aws_flow.attr('node', shape='box', style='filled', color='#2a9d8f', 
                             fillcolor='#e0f5f1', fontname='Arial', fontsize='14')
                aws_flow.attr('edge', color='#76c893')
                aws_flow.attr(rankdir='LR', bgcolor='white')
                
                # 메인 노드
                aws_flow.node('eks', 'Amazon EKS', fillcolor='#2a9d8f', fontcolor='white')
                
                # AWS 서비스
                aws_flow.node('iam', 'IAM', fillcolor='#40b3a2', fontcolor='white')
                aws_flow.node('lb', 'ELB', fillcolor='#40b3a2', fontcolor='white')
                aws_flow.node('storage', 'Storage', fillcolor='#40b3a2', fontcolor='white')
                aws_flow.node('fargate', 'Fargate', fillcolor='#40b3a2', fontcolor='white')
                
                # K8s 리소스
                aws_flow.node('pod', '파드', fillcolor='#52b69a', fontcolor='white')
                aws_flow.node('sa', '서비스어카운트', fillcolor='#52b69a', fontcolor='white')
                aws_flow.node('ingress', '인그레스', fillcolor='#52b69a', fontcolor='white')
                aws_flow.node('service', '서비스', fillcolor='#52b69a', fontcolor='white')
                aws_flow.node('pv', 'PV', fillcolor='#52b69a', fontcolor='white')
                
                # 연결 관계
                aws_flow.edge('eks', 'iam')
                aws_flow.edge('eks', 'lb')
                aws_flow.edge('eks', 'storage')
                aws_flow.edge('eks', 'fargate')
                
                aws_flow.edge('iam', 'sa', label='IRSA')
                aws_flow.edge('sa', 'pod')
                aws_flow.edge('lb', 'ingress', label='ALB Controller')
                aws_flow.edge('lb', 'service', label='NLB/CLB')
                aws_flow.edge('storage', 'pv', label='EBS/EFS')
                aws_flow.edge('fargate', 'pod', label='서버리스 실행')
                
                # 렌더링
                st.graphviz_chart(aws_flow, use_container_width=True)
                
        # AWS 통합 설명
        st.markdown("""
        <div style="margin-top: 20px; padding: 15px; background-color: var(--green-light); border-radius: 8px;">
            <h4 style="color: #000000; margin-top: 0;">Amazon EKS와 AWS 서비스 통합</h4>
            <ul>
                <li><strong>IAM</strong>: 쿠버네티스 인증 및 권한 부여 시스템과 AWS IAM 통합, Pod 수준 권한 부여를 위한 IRSA</li>
                <li><strong>ELB</strong>: 쿠버네티스 서비스의 외부 트래픽을 처리하기 위한 Application Load Balancer와 Network Load Balancer</li>
                <li><strong>EBS/EFS</strong>: CSI 드라이버를 통한 쿠버네티스 스토리지 시스템과 AWS 블록 및 파일 스토리지 통합</li>
                <li><strong>Fargate</strong>: 서버리스 컨테이너 실행 환경 제공, 노드 관리 불필요</li>
                <li><strong>VPC CNI</strong>: 쿠버네티스 Pod에 VPC IP 할당, AWS VPC 네트워킹 및 보안 기능 활용</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 관련 리소스 섹션
    st.markdown("""
        <div class="learning-path-nav">
            <div class="nav-item">
                <a href="/?page=beginner" class="nav-link">기본 과정</a>
            </div>
            <div class="nav-item">
                <a href="/?page=intermediate" class="nav-link">중급 과정</a>
            </div>
            <div class="nav-item">
                <a href="/?page=advanced" class="nav-link">고급 과정</a>
            </div>
            <div class="nav-item current">
                <span class="tools-nav">학습 도구</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    # st.markdown("""
    # <div class="related-resources">
    #     <h4>관련 학습 자료</h4>
    #     <ul>
    #         <li><a href="#" onclick="navigateTo('beginner')">기본 과정</a>에서 쿠버네티스와 EKS의 기초 개념을 학습하세요.</li>
    #         <li><a href="#" onclick="navigateTo('resources')">자료실</a>에서 다양한 YAML 템플릿과 치트시트를 확인하세요.</li>
    #         <li><a href="https://kubernetes.io/docs/home/" target="_blank">쿠버네티스 공식 문서</a>에서 더 자세한 정보를 찾아보세요.</li>
    #         <li><a href="https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html" target="_blank">Amazon EKS 공식 문서</a>에서 EKS에 대해 자세히 알아보세요.</li>
    #     </ul>
    # </div>
    # """, unsafe_allow_html=True)

    st.markdown("""
        <div class="related-resources">
            <h4>관련 학습 자료</h4>
            <ul>
                <li><a href="/?page=beginner">기본 과정</a>에서 쿠버네티스와 EKS의 기초 개념을 학습하세요.</li>
                <li><a href="/?page=resources">자료실</a>에서 다양한 YAML 템플릿과 치트시트를 확인하세요.</li>
                <li><a href="https://kubernetes.io/docs/home/" target="_blank">쿠버네티스 공식 문서</a>에서 더 자세한 정보를 찾아보세요.</li>
                <li><a href="https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html" target="_blank">Amazon EKS 공식 문서</a>에서 EKS에 대해 자세히 알아보세요.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)