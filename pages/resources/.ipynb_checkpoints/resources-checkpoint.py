import streamlit as st
import yaml
import json
import re
import base64
from yaml.parser import ParserError
from utils.localization import t
from services.analytics.usage_tracker import UsageTracker
from io import BytesIO  # 이 부분이 누락됨
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

def render_resources():
    """Kubernetes & EKS 마인드맵 - 템플릿 생성, 치트시트, 레퍼런스 자료"""
    
    # 사용 추적
    UsageTracker.track_page_view("resource_hub")
    
    # 스타일 정의
    st.markdown("""
    <style>
    /* 색상 변수 */
    :root {
        --main-color: #FF1493;
        --main-light: #ffe6f2;
        --main-very-light: #fff0f8;
        --main-dark: #cc0066;
        --gray-100: #f8f9fa;
        --gray-200: #e9ecef;
        --gray-300: #dee2e6;
        --gray-600: #6c757d;
        --gray-800: #343a40;
        --success-color: #28a745;
        --warning-color: #ffc107;
        --danger-color: #dc3545;
    }
    
    /* 페이지 제목 */
    .mindmap-title {
        font-size: 2rem !important;
        color: var(--main-color);
        margin-bottom: 20px !important;
        padding-bottom: 10px;
        border-bottom: 2px solid var(--main-color);
    }
    
    /* 마인드맵 소개 스타일 */
    .mindmap-intro {
        background-color: var(--main-very-light);
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 30px;
        border-left: 4px solid var(--main-color);
    }
    
    .mindmap-intro p {
        color: var(--gray-800);
        margin-bottom: 10px;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    /* 탭 스타일 커스터마이즈 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        margin-bottom: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 4px 4px 0 0;
        padding: 10px 20px;
        font-weight: 500;
        font-size: 0.9rem;
    }
    
    .stTabs [aria-selected="true"] {
        color: var(--main-color) !important;
        border-bottom: 2px solid var(--main-color) !important;
    }
    
    /* 버튼 스타일 핫핑크로 변경 */
    .stButton>button {
        background-color: #FF1493 !important;
        color: white !important;
        border: none !important;
    }
    
    .stButton>button:hover {
        background-color: #cc0066 !important;
        color: white !important;
    }

    /* 코드 스타일링 */
    .stCode {
        font-size: 0.9rem !important;
        line-height: 1.5 !important;
    }
    
    /* 템플릿 정보 스타일 (배경색을 흰색으로) */
    .template-info {
        background-color: white;
        padding: 15px;
        border-radius: 6px;
        margin-bottom: 20px;
        border-left: 4px solid var(--main-color);
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .template-info h4 {
        color: var(--main-color);
        margin-top: 0;
        margin-bottom: 10px;
        font-size: 1.1rem;
    }
    
    .template-info p {
        margin: 0;
        color: var(--gray-600);
        font-size: 0.9rem;
    }
    
    /* 치트시트 & 자료실 스타일 (수정) */
    .section-title {
        color: var(--main-color);
        font-size: 1.2rem;
        font-weight: 600;
        margin: 1rem 0 0.5rem 0;
        padding-bottom: 5px;
        border-bottom: 1px solid var(--main-light);
    }
    
    .cheatsheet-card {
        background-color: white;
        border: 1px solid var(--gray-300);
        border-radius: 8px;
        overflow: hidden;
        margin-bottom: 15px;
        transition: all 0.3s ease;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .cheatsheet-card:hover {
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transform: translateY(-1px);
    }
    
    .cheatsheet-header {
        padding: 12px 15px;
        border-bottom: 1px solid var(--gray-300);
    }
    
    .cheatsheet-title {
        color: var(--main-color);
        font-size: 1rem;
        font-weight: 600;
        margin: 0;
    }
    
    .cheatsheet-subtitle {
        font-size: 0.8rem;
        color: var(--gray-600);
        margin-top: 3px;
    }
    
    .cheatsheet-body {
        padding: 12px 15px;
    }
    
    .cheatsheet-preview {
        border: 1px solid var(--gray-300);
        border-radius: 4px;
        padding: 10px;
        background-color: var(--gray-100);
        font-family: monospace;
        font-size: 0.8rem;
        margin-bottom: 12px;
        max-height: 150px;
        overflow-y: auto;
        white-space: pre;
    }
    
    .cheatsheet-actions {
        display: flex;
        justify-content: flex-end;
        gap: 8px;
    }
    
    /* 리소스 카드 스타일 (수정) */
    .hub-card {
        background-color: white;
        border-radius: 8px;
        border: 1px solid var(--gray-300);
        overflow: hidden;
        transition: all 0.2s;
        height: 100%;
        display: flex;
        flex-direction: column;
        margin-bottom: 15px;
    }
    
    .hub-card:hover {
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transform: translateY(-1px);
    }
    
    .hub-card-header {
        padding: 12px 15px;
        border-bottom: 1px solid var(--gray-300);
    }
    
    .hub-card-icon {
        font-size: 20px;
        margin-bottom: 8px;
        color: var(--main-color);
    }
    
    .hub-card-title {
        color: var(--main-color);
        font-size: 1rem;
        font-weight: 600;
        margin: 0;
    }
    
    .hub-card-body {
        padding: 12px 15px;
        flex: 1;
        font-size: 0.9rem;
    }
    
    .hub-card-description {
        color: var(--gray-600);
        margin-bottom: 12px;
        font-size: 0.85rem;
    }
    
    /* 전체적인 폰트 사이즈 감소 */
    .st-ae, .st-af, .st-ag, .st-ah, .st-ai, .st-aj {
        font-size: 0.9rem !important;
    }
    
    h1, h2, h3 {
        font-size: 1.6rem !important;
    }
    
    h4, h5, h6 {
        font-size: 1.1rem !important;
    }
    
    .stMarkdown p {
        font-size: 0.9rem !important;
    }
    
    .stSelectbox label, .stMultiSelect label {
        font-size: 0.85rem !important;
    }
    
    /* CLI 명령어 스타일 */
    .command-section {
        margin-bottom: 20px;
    }
    
    .command-title {
        color: var(--main-color);
        font-size: 1rem;
        font-weight: 600;
        margin: 0.5rem 0;
    }
    
    .command-description {
        font-size: 0.85rem;
        margin-bottom: 8px;
        color: var(--gray-600);
    }
    
    .command-block {
        background-color: var(--gray-100);
        border-radius: 4px;
        padding: 10px 12px;
        font-family: monospace;
        font-size: 0.85rem;
        margin-bottom: 10px;
        white-space: pre;
        overflow-x: auto;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 세션 상태 초기화
    if 'yaml_template' not in st.session_state:
        st.session_state.yaml_template = ""
    if 'dockerfile_template' not in st.session_state:
        st.session_state.dockerfile_template = ""
    if 'edit_mode' not in st.session_state:
        st.session_state.edit_mode = False  # 기본적으로 편집 모드 비활성화
    if 'validation_result' not in st.session_state:
        st.session_state.validation_result = None
    if 'simulation_result' not in st.session_state:
        st.session_state.simulation_result = None
    if 'current_file_type' not in st.session_state:  # 이 부분이 누락됐을 수 있음
        st.session_state.current_file_type = "kubernetes"
    if 'customize_fields' not in st.session_state:
        st.session_state.customize_fields = {}
    if 'best_practices' not in st.session_state:
        st.session_state.best_practices = None
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "templates"
    if 'selected_commands' not in st.session_state:
        st.session_state.selected_commands = []
    
    # 페이지 제목
    st.markdown("<h1 class='mindmap-title'>Kubernetes & EKS 리소스</h1>", unsafe_allow_html=True)
    
    # 리소스 소개
    st.markdown("""
    <div class="mindmap-intro">
        <p>이 리소스는 Kubernetes와 EKS의 템플릿, 명령어 등을 체계적으로 이해하고 복습하는 데 도움이 됩니다.</p>
        <p>명령어 연습을 할 수 있습니다. </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 탭 UI 구현
    tab1, tab2, tab3, tab4 = st.tabs(["📝 템플릿 도구", "📋 치트시트", "🖥️ CLI 안내서", "📚 학습 자료"])
    
    # 템플릿 도구 탭 콘텐츠
    with tab1:
        render_templates_tab()
        
    # 치트시트 탭 콘텐츠
    with tab2:
        render_cheatsheets_tab()
        
    # CLI 안내서 탭 콘텐츠
    with tab3:
        render_cli_guide_tab()
        
    # 학습 자료 탭 콘텐츠
    with tab4:
        render_resources_tab()

def render_templates_tab():
    """템플릿 도구 탭 렌더링"""
    
    # 템플릿 데이터 정의
    template_categories = {
        "kubernetes": [
            {
                "category": "워크로드 리소스",
                "templates": [
                    {
                        "name": "Pod",
                        "description": "가장 기본적인 배포 단위로, 하나 이상의 컨테이너를 포함합니다.",
                        "template": """apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
  labels:
    app: nginx
spec:
  containers:
  - name: nginx
    image: nginx:1.14.2
    ports:
    - containerPort: 80
    resources:
      requests:
        memory: "64Mi"
        cpu: "100m"
      limits:
        memory: "128Mi"
        cpu: "200m"
"""
                    },
                    {
                        "name": "Deployment",
                        "description": "Pod의 복제본을 생성하고 관리하며 업데이트 전략을 설정할 수 있습니다.",
                        "template": """apiVersion: apps/v1
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
        image: nginx:1.14.2
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
"""
                    },
                    {
                        "name": "StatefulSet",
                        "description": "상태를 유지해야 하는 애플리케이션을 위한 워크로드 리소스입니다.",
                        "template": """apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
spec:
  selector:
    matchLabels:
      app: nginx
  serviceName: "nginx"
  replicas: 3
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
          name: web
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
"""
                    }
                ]
            },
            {
                "category": "서비스 & 네트워킹",
                "templates": [
                    {
                        "name": "Service",
                        "description": "Pod 집합에 대한 단일 접근 지점을 제공하는 추상화 계층입니다.",
                        "template": """apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: MyApp
  ports:
  - port: 80
    targetPort: 9376
  type: ClusterIP
"""
                    },
                    {
                        "name": "Ingress",
                        "description": "클러스터 외부에서 내부 서비스로의 HTTP/HTTPS 라우팅을 관리합니다.",
                        "template": """apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: example-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: my-service
            port:
              number: 80
"""
                    }
                ]
            },
            {
                "category": "확장 & 사용자 정의",
                "templates": [
                    {
                        "name": "CustomResourceDefinition",
                        "description": "Kubernetes API를 확장하여 사용자 정의 리소스 유형을 정의합니다.",
                        "template": """apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: crontabs.stable.example.com
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
                cronSpec:
                  type: string
                image:
                  type: string
                replicas:
                  type: integer
  scope: Namespaced
  names:
    plural: crontabs
    singular: crontab
    kind: CronTab
    shortNames:
    - ct
"""
                    }
                ]
            }
        ],
        "dockerfile": [
            {
                "category": "웹 애플리케이션",
                "templates": [
                    {
                        "name": "Node.js 애플리케이션",
                        "description": "Express.js를 사용한 기본 Node.js 웹 애플리케이션 Dockerfile입니다.",
                        "template": """# Node.js 16 Alpine 기반 이미지 사용
FROM node:16-alpine

# 작업 디렉토리 설정
WORKDIR /app

# 패키지 파일 복사 및 설치
COPY package*.json ./
RUN npm install

# 애플리케이션 소스코드 복사 
COPY . .

# 포트 설정
EXPOSE 3000

# 애플리케이션 실행 명령
CMD ["npm", "start"]
"""
                    },
                    {
                        "name": "Python 애플리케이션",
                        "description": "Flask를 사용한 기본 Python 웹 애플리케이션 Dockerfile입니다.",
                        "template": """# Python 3.10 Alpine 기반 이미지 사용
FROM python:3.10-alpine

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 소스코드 복사
COPY . .

# 포트 설정
EXPOSE 5000

# 환경변수 설정
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# 애플리케이션 실행 명령
CMD ["flask", "run", "--host=0.0.0.0"]
"""
                    }
                ]
            },
            {
                "category": "멀티스테이지 빌드",
                "templates": [
                    {
                        "name": "Go 애플리케이션",
                        "description": "Go 애플리케이션을 위한 멀티스테이지 빌드 Dockerfile입니다.",
                        "template": """# 빌드 스테이지
FROM golang:1.18-alpine AS builder

# 작업 디렉토리 설정
WORKDIR /app

# 소스코드 복사 및 의존성 다운로드
COPY go.* ./
RUN go mod download

# 소스코드 복사 및 빌드
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main .

# 실행 스테이지
FROM alpine:3.16

# 필요한 CA 인증서 설치
RUN apk --no-cache add ca-certificates

# 바이너리 복사
COPY --from=builder /app/main /app/main

# 포트 설정
EXPOSE 8080

# 애플리케이션 실행
CMD ["/app/main"]
"""
                    }
                ]
            }
        ]
    }
    
    # 분류 및 템플릿 선택 영역 - 한 행에 모두 배치
    selection_cols = st.columns([2, 2, 2, 1])
    
    # 파일 유형 선택
    with selection_cols[0]:
        file_type = st.selectbox(
            "파일 유형",
            ["Kubernetes YAML", "Dockerfile"],
            index=0 if st.session_state.current_file_type == "kubernetes" else 1,
            label_visibility="collapsed"
        )
        
        current_file_type = "kubernetes" if file_type == "Kubernetes YAML" else "dockerfile"
        if st.session_state.current_file_type != current_file_type:
            st.session_state.current_file_type = current_file_type
            st.session_state.yaml_template = ""
            st.session_state.dockerfile_template = ""
            st.session_state.validation_result = None
            st.session_state.simulation_result = None
            st.session_state.best_practices = None
    
    # 선택한 파일 유형에 맞는 카테고리 목록
    current_templates = template_categories.get(st.session_state.current_file_type, [])
    categories = [item["category"] for item in current_templates]
    
    # 카테고리 선택
    with selection_cols[1]:
        if categories:
            selected_category = st.selectbox(
                "카테고리", 
                categories,
                label_visibility="collapsed"
            )
            selected_category_templates = next(
                (item for item in current_templates if item["category"] == selected_category),
                {"templates": []}
            )["templates"]
        else:
            selected_category = ""
            selected_category_templates = []
    
    # 템플릿 선택
    with selection_cols[2]:
        if selected_category_templates:
            template_names = [item["name"] for item in selected_category_templates]
            selected_template_name = st.selectbox(
                "템플릿 선택", 
                template_names,
                label_visibility="collapsed"
            )
            
            selected_template = next(
                (item for item in selected_category_templates if item["name"] == selected_template_name),
                None
            )
        else:
            selected_template = None
            selected_template_name = ""
    
    # 템플릿 로드 버튼
    with selection_cols[3]:
        st.markdown("<div style='padding-top: 5px;'></div>", unsafe_allow_html=True)  # 버튼 위치 조정
        if selected_template and st.button("선택", type="primary", use_container_width=True):
            if st.session_state.current_file_type == "kubernetes":
                st.session_state.yaml_template = selected_template["template"]
            else:
                st.session_state.dockerfile_template = selected_template["template"]
            
            # 검증 결과 초기화
            st.session_state.validation_result = None
            st.session_state.simulation_result = None
            st.session_state.best_practices = None
    
    # 선택된 템플릿 정보 표시 (흰색 배경)
    if selected_template:
        st.markdown(f"""
        <div class="template-info">
            <h4>{selected_template_name}</h4>
            <p>{selected_template["description"]}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 메인 에디터 및 결과 컨테이너
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # 메인 컨테이너 레이아웃
    main_cols = st.columns([3, 2])
    
    # 왼쪽 패널 - 코드 에디터
    with main_cols[0]:
        # 파일명 표시 및 편집 모드 토글 - columns 중첩 제거
        if st.session_state.current_file_type == "kubernetes":
            try:
                yaml_dict = yaml.safe_load(st.session_state.yaml_template) if st.session_state.yaml_template else {}
                kind = yaml_dict.get("kind", "resource").lower() if yaml_dict else "resource"
                name = yaml_dict.get("metadata", {}).get("name", "unnamed") if yaml_dict else "unnamed"
                file_name = f"{name}-{kind}.yaml"
            except:
                file_name = "kubernetes-template.yaml"
        else:
            file_name = "Dockerfile"
        
        # 파일이름과 편집 모드 토글을 한 줄에 표시 (HTML로 처리)
        st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <div class='filename-badge'>{file_name}</div>
                <div>편집</div>
            </div>
            """, unsafe_allow_html=True)
        
        edit_mode = st.checkbox("편집 활성화", value=st.session_state.edit_mode, label_visibility="collapsed")
        if edit_mode != st.session_state.edit_mode:
            st.session_state.edit_mode = edit_mode
        
        # 코드 에디터 (편집 모드에 따라 다르게 표시)
        current_template = ""
        if st.session_state.current_file_type == "kubernetes":
            current_template = st.session_state.yaml_template
            
            if st.session_state.edit_mode:
                st.session_state.yaml_template = st.text_area(
                    "YAML 편집",
                    value=current_template,
                    height=400,
                    key="yaml_editor",
                    help="Kubernetes YAML 템플릿을 편집하세요."
                )
            else:
                st.code(current_template, language="yaml", line_numbers=True)
        else:
            current_template = st.session_state.dockerfile_template
            
            if st.session_state.edit_mode:
                st.session_state.dockerfile_template = st.text_area(
                    "Dockerfile 편집",
                    value=current_template,
                    height=400,
                    key="dockerfile_editor",
                    help="Dockerfile 템플릿을 편집하세요."
                )
            else:
                st.code(current_template, language="dockerfile", line_numbers=True)
        
        # 템플릿 커스터마이저 구현
        if st.session_state.current_file_type == "kubernetes" and st.session_state.yaml_template:
            try:
                yaml_dict = yaml.safe_load(st.session_state.yaml_template)
                
                # 기본 필드 추출 (Deployment 등)
                if yaml_dict and "kind" in yaml_dict:
                    kind = yaml_dict["kind"]
                    name = yaml_dict.get("metadata", {}).get("name", "")
                    
                    with st.expander("템플릿 커스터마이즈"):
                        custom_name = st.text_input("이름", value=name, key="custom_name")
                        if custom_name != name and custom_name:
                            # YAML에서 이름 변경
                            yaml_dict["metadata"]["name"] = custom_name
                            st.session_state.yaml_template = yaml.dump(yaml_dict, default_flow_style=False)
                        
                        # 레플리카 수 (Deployment, StatefulSet 등)
                        if kind in ["Deployment", "StatefulSet", "ReplicaSet"]:
                            current_replicas = yaml_dict.get("spec", {}).get("replicas", 1)
                            new_replicas = st.number_input("레플리카 수", min_value=1, value=current_replicas, key="custom_replicas")
                            if new_replicas != current_replicas:
                                # YAML에서 레플리카 수 변경
                                yaml_dict["spec"]["replicas"] = new_replicas
                                st.session_state.yaml_template = yaml.dump(yaml_dict, default_flow_style=False)
                        
                        # 컨테이너 이미지 (Pod, Deployment 등)
                        if "containers" in yaml_dict.get("spec", {}).get("template", {}).get("spec", {}) or \
                           "containers" in yaml_dict.get("spec", {}):
                            containers = yaml_dict.get("spec", {}).get("template", {}).get("spec", {}).get("containers", [])
                            if not containers:
                                containers = yaml_dict.get("spec", {}).get("containers", [])
                            
                            if containers:
                                current_image = containers[0].get("image", "")
                                new_image = st.text_input("컨테이너 이미지", value=current_image, key="custom_image")
                                if new_image != current_image and new_image:
                                    # YAML에서 이미지 변경
                                    if "template" in yaml_dict.get("spec", {}):
                                        yaml_dict["spec"]["template"]["spec"]["containers"][0]["image"] = new_image
                                    else:
                                        yaml_dict["spec"]["containers"][0]["image"] = new_image
                                    st.session_state.yaml_template = yaml.dump(yaml_dict, default_flow_style=False)
            except:
                pass
                
        elif st.session_state.current_file_type == "dockerfile" and st.session_state.dockerfile_template:
            # Dockerfile 커스터마이저
            with st.expander("Dockerfile 커스터마이즈"):
                # 베이스 이미지 추출 및 변경
                base_image_match = re.search(r'^FROM\s+([^\s]+)', st.session_state.dockerfile_template, re.MULTILINE)
                if base_image_match:
                    current_base = base_image_match.group(1)
                    new_base = st.text_input("베이스 이미지", value=current_base, key="custom_base")
                    if new_base != current_base and new_base:
                        # Dockerfile에서 베이스 이미지 변경
                        new_dockerfile = re.sub(
                            r'^FROM\s+([^\s]+)',
                            f'FROM {new_base}',
                            st.session_state.dockerfile_template,
                            count=1,
                            flags=re.MULTILINE
                        )
                        st.session_state.dockerfile_template = new_dockerfile
                
                # EXPOSE 포트 추출 및 변경
                expose_match = re.search(r'^EXPOSE\s+(\d+)', st.session_state.dockerfile_template, re.MULTILINE)
                if expose_match:
                    current_port = expose_match.group(1)
                    new_port = st.text_input("노출 포트", value=current_port, key="custom_port")
                    if new_port != current_port and new_port:
                        # Dockerfile에서 포트 변경
                        new_dockerfile = re.sub(
                            r'^EXPOSE\s+\d+',
                            f'EXPOSE {new_port}',
                            st.session_state.dockerfile_template,
                            count=1,
                            flags=re.MULTILINE
                        )
                        st.session_state.dockerfile_template = new_dockerfile
        
        # 액션 버튼 그룹 - 중첩된 columns를 제거하고 HTML로 표현
        st.markdown("""
        <div style="display: flex; gap: 10px; margin-top: 15px;">
            <div style="flex: 1;">버튼을 눌러 작업을 수행하세요</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 버튼을 세로로 배치하여 columns 중첩 방지
        if st.button("✓ 유효성 검증", type="primary", use_container_width=True):
            # 유효성 검증 로직
            if st.session_state.current_file_type == "kubernetes":
                template = st.session_state.yaml_template
                try:
                    if not template.strip():
                        st.session_state.validation_result = {
                            "status": "error",
                            "message": "YAML이 비어 있습니다."
                        }
                    else:
                        yaml_dict = yaml.safe_load(template)
                        
                        # 필수 필드 검증
                        if not yaml_dict:
                            st.session_state.validation_result = {
                                "status": "error", 
                                "message": "유효한 YAML이지만 내용이 비어 있습니다."
                            }
                        elif 'apiVersion' not in yaml_dict:
                            st.session_state.validation_result = {
                                "status": "error", 
                                "message": "필수 필드 'apiVersion'이 누락되었습니다."
                            }
                        elif 'kind' not in yaml_dict:
                            st.session_state.validation_result = {
                                "status": "error", 
                                "message": "필수 필드 'kind'가 누락되었습니다."
                            }
                        elif 'metadata' not in yaml_dict:
                            st.session_state.validation_result = {
                                "status": "error", 
                                "message": "필수 필드 'metadata'가 누락되었습니다."
                            }
                        else:
                            st.session_state.validation_result = {
                                "status": "success", 
                                "message": "YAML이 유효합니다.",
                                "parsed": yaml_dict
                            }
                            
                            # 베스트 프랙티스 검사
                            best_practices = []
                            
                            # 1. 리소스 제한 설정 확인
                            kind = yaml_dict.get("kind", "")
                            containers = yaml_dict.get('spec', {}).get('template', {}).get('spec', {}).get('containers', []) if kind in ['Deployment', 'StatefulSet', 'DaemonSet'] else []
                            if containers:
                                missing_resources = []
                                for i, container in enumerate(containers):
                                    if 'resources' not in container:
                                        missing_resources.append(f"컨테이너 #{i+1} ({container.get('name', '이름 없음')})")
                                
                                if missing_resources:
                                    best_practices.append({
                                        "title": "리소스 제한이 설정되지 않음",
                                        "severity": "high",
                                        "status": "error",
                                        "message": f"다음 컨테이너에 리소스 제한(requests/limits)이 설정되지 않았습니다: {', '.join(missing_resources)}"
                                    })
                                else:
                                    best_practices.append({
                                        "title": "리소스 제한 설정 완료",
                                        "severity": "low",
                                        "status": "success",
                                        "message": "모든 컨테이너에 리소스 제한이 올바르게 설정되었습니다."
                                    })
                            
                            # 베스트 프랙티스 결과 저장
                            st.session_state.best_practices = best_practices
                            
                except ParserError as e:
                    st.session_state.validation_result = {
                        "status": "error", 
                        "message": f"YAML 구문 오류:\n{str(e)}"
                    }
                except Exception as e:
                    st.session_state.validation_result = {
                        "status": "error", 
                        "message": f"오류 발생:\n{str(e)}"
                    }
            else:  # Dockerfile 검증
                dockerfile = st.session_state.dockerfile_template
                try:
                    if not dockerfile.strip():
                        st.session_state.validation_result = {
                            "status": "error",
                            "message": "Dockerfile이 비어 있습니다."
                        }
                    else:
                        # 간단한 Dockerfile 구문 검사
                        errors = []
                        
                        # FROM 명령이 있는지 확인
                        if not re.search(r'^FROM\s+\S+', dockerfile, re.MULTILINE):
                            errors.append("FROM 명령이 없거나 잘못되었습니다.")
                        
                        if errors:
                            st.session_state.validation_result = {
                                "status": "error",
                                "message": "Dockerfile 오류:\n" + "\n".join(errors)
                            }
                        else:
                            st.session_state.validation_result = {
                                "status": "success",
                                "message": "Dockerfile이 유효합니다."
                            }
                            
                            # 베스트 프랙티스 검사 수행
                            best_practices = []
                            
                            # 1. 멀티스테이지 빌드 확인
                            if dockerfile.count('FROM') > 1:
                                best_practices.append({
                                    "title": "멀티스테이지 빌드 사용",
                                    "severity": "low",
                                    "status": "success",
                                    "message": "멀티스테이지 빌드를 사용하여 이미지 크기가 최적화되었습니다."
                                })
                            else:
                                best_practices.append({
                                    "title": "멀티스테이지 빌드 미사용",
                                    "severity": "medium",
                                    "status": "warning",
                                    "message": "이미지 크기 최적화를 위해 멀티스테이지 빌드 사용을 고려하세요."
                                })
                            
                            # 베스트 프랙티스 결과 저장
                            st.session_state.best_practices = best_practices
                            
                except Exception as e:
                    st.session_state.validation_result = {
                        "status": "error",
                        "message": f"Dockerfile 분석 중 오류 발생:\n{str(e)}"
                    }
        
        # 두 번째 버튼
        if st.button("▶ 시뮬레이션", key="simulate_btn", use_container_width=True):
            # 시뮬레이션 로직
            if st.session_state.current_file_type == "kubernetes":
                try:
                    if not st.session_state.yaml_template.strip():
                        st.session_state.simulation_result = {
                            "status": "error",
                            "message": "시뮬레이션할 YAML이 비어 있습니다."
                        }
                    else:
                        # YAML이 유효한지 먼저 확인
                        yaml_dict = yaml.safe_load(st.session_state.yaml_template)
                        
                        # 간단한 시뮬레이션
                        if 'kind' in yaml_dict:
                            kind = yaml_dict['kind']
                            name = yaml_dict.get('metadata', {}).get('name', '미정의')
                            
                            # 종류별 특화된 시뮬레이션 결과
                            if kind == 'Deployment':
                                replicas = yaml_dict.get('spec', {}).get('replicas', 1)
                                
                                simulation_details = {
                                    "리소스 종류": kind,
                                    "이름": name,
                                    "레플리카 수": replicas,
                                    "시뮬레이션": f"{name} 디플로이먼트가 {replicas}개의 레플리카로 생성됩니다."
                                }
                            
                            else:
                                # 기타 리소스 유형에 대한 일반적인 시뮬레이션
                                simulation_details = {
                                    "리소스 종류": kind,
                                    "이름": name,
                                    "시뮬레이션": f"{name} {kind}가 지정된 구성으로 생성됩니다."
                                }
                                
                            st.session_state.simulation_result = {
                                "status": "success",
                                "message": "시뮬레이션이 완료되었습니다.",
                                "details": simulation_details
                            }
                        else:
                            st.session_state.simulation_result = {
                                "status": "error",
                                "message": "리소스 'kind'가 정의되지 않았습니다."
                            }
                except Exception as e:
                    st.session_state.simulation_result = {
                        "status": "error",
                        "message": f"시뮬레이션 오류:\n{str(e)}"
                    }
            else:
                # Dockerfile 시뮬레이션
                try:
                    if not st.session_state.dockerfile_template.strip():
                        st.session_state.simulation_result = {
                            "status": "error",
                            "message": "시뮬레이션할 Dockerfile이 비어 있습니다."
                        }
                    else:
                        # 간단한 Dockerfile 시뮬레이션
                        base_image = ""
                        base_image_match = re.search(r'^FROM\s+([^\s]+)', st.session_state.dockerfile_template, re.MULTILINE)
                        if base_image_match:
                            base_image = base_image_match.group(1)
                        
                        expose_port = ""
                        expose_match = re.search(r'^EXPOSE\s+(\d+)', st.session_state.dockerfile_template, re.MULTILINE)
                        if expose_match:
                            expose_port = expose_match.group(1)
                        
                        simulation_details = {
                            "베이스 이미지": base_image,
                            "노출 포트": expose_port or "없음",
                            "시뮬레이션": f"이미지가 {base_image}를 기반으로 빌드됩니다." + 
                                      (f" 포트 {expose_port}가 노출됩니다." if expose_port else "")
                        }
                        
                        st.session_state.simulation_result = {
                            "status": "success",
                            "message": "시뮬레이션이 완료되었습니다.",
                            "details": simulation_details
                        }
                except Exception as e:
                    st.session_state.simulation_result = {
                        "status": "error",
                        "message": f"시뮬레이션 오류:\n{str(e)}"
                    }
        
        # 세 번째 버튼
        if st.button("↺ 초기화", key="reset_btn", use_container_width=True):
            if st.session_state.current_file_type == "kubernetes":
                st.session_state.yaml_template = ""
            else:
                st.session_state.dockerfile_template = ""
            
            st.session_state.validation_result = None
            st.session_state.simulation_result = None
            st.session_state.best_practices = None
            st.rerun()
    
    # 오른쪽 패널 - 결과 표시
    with main_cols[1]:
        # 탭 선택 (결과, CLI 명령어, 시각화)
        tab1, tab2, tab3 = st.tabs(["검증 결과", "CLI 명령어", "리소스 시각화"])
    
        # 결과 탭
        with tab1:
            # 검증 결과 표시
            if st.session_state.validation_result:
                if st.session_state.validation_result["status"] == "success":
                    st.markdown(f"""
                    <div class="validation-result validation-success">
                        ✅ {st.session_state.validation_result["message"]}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="validation-result validation-error">
                        ❌ {st.session_state.validation_result["message"]}
                    </div>
                    """, unsafe_allow_html=True)
            
            # 베스트 프랙티스 표시
            if st.session_state.best_practices:
                st.markdown("<h4>베스트 프랙티스 검사 결과</h4>", unsafe_allow_html=True)
                
                for practice in st.session_state.best_practices:
                    title = practice.get("title", "")
                    severity = practice.get("severity", "low")
                    status = practice.get("status", "")
                    message = practice.get("message", "")
                    
                    icon = "✓" if status == "success" else ("⚠" if status == "warning" else "✗")
                    icon_class = "success" if status == "success" else ("warning" if status == "warning" else "error")
                    
                    st.markdown(f"""
                    <div class="best-practice">
                        <div class="practice-header">
                            <div class="practice-title">
                                <span class="practice-icon {icon_class}">{icon}</span>
                                {title}
                            </div>
                            <div class="severity-tag severity-{severity}">
                                {severity.title()}
                            </div>
                        </div>
                        <div class="practice-content">
                            {message}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # 시뮬레이션 결과 표시
            if st.session_state.simulation_result and st.session_state.simulation_result["status"] == "success":
                st.markdown("<h4>시뮬레이션 결과</h4>", unsafe_allow_html=True)
                
                details = st.session_state.simulation_result["details"]
                # 결과 내용 렌더링
                st.markdown(f"""
                <div class="simulation-result">
                    <div class="result-title">
                        <span class="result-icon">▶</span>
                        {details.get('리소스 종류', '미정의')} 시뮬레이션
                    </div>
                    <p><strong>이름:</strong> {details.get('이름', '미정의')}</p>
                    <p><strong>결과:</strong> {details.get('시뮬레이션', '정보 없음')}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # CLI 명령어 탭
        with tab2:
            st.markdown("<h4>관련 CLI 명령어</h4>", unsafe_allow_html=True)
            
            # 탭으로 CLI 종류 선택
            cli_tabs = st.tabs(["kubectl", "docker", "eksctl", "aws"])
            
            # kubectl 명령어
            with cli_tabs[0]:
                if st.session_state.current_file_type == "kubernetes" and st.session_state.yaml_template:
                    try:
                        yaml_dict = yaml.safe_load(st.session_state.yaml_template)
                        if yaml_dict:
                            kind = yaml_dict.get('kind', '')
                            name = yaml_dict.get('metadata', {}).get('name', '')
                            
                            # 주요 명령어 표시
                            st.code(f"# 리소스 생성 또는 업데이트\nkubectl apply -f {name}-{kind.lower()}.yaml", language="bash")
                            st.code(f"# 리소스 상태 확인\nkubectl get {kind.lower()} {name}", language="bash")
                            st.code(f"# 리소스 상세 정보 확인\nkubectl describe {kind.lower()} {name}", language="bash")
                    except:
                        st.info("YAML을 먼저 로드하거나 작성하세요.")
                else:
                    st.info("Kubernetes YAML 템플릿을 로드하면 관련 kubectl 명령어가 표시됩니다.")
            
            # docker 명령어
            with cli_tabs[1]:
                if st.session_state.current_file_type == "dockerfile" and st.session_state.dockerfile_template:
                    st.code("# Docker 이미지 빌드\ndocker build -t myapp:1.0 .", language="bash")
                    st.code("# 컨테이너 실행\ndocker run -d -p 8080:80 --name myapp myapp:1.0", language="bash")
                    st.code("# 실행 중인 컨테이너 확인\ndocker ps", language="bash")
                else:
                    st.info("Dockerfile 템플릿을 로드하면 관련 docker 명령어가 표시됩니다.")
            
            # eksctl 명령어
            with cli_tabs[2]:
                if st.session_state.current_file_type == "kubernetes":
                    st.code("# EKS 클러스터 생성\neksctl create cluster --name my-cluster --region us-west-2 --nodes 3", language="bash")
                    st.code("# 노드그룹 추가\neksctl create nodegroup --cluster=my-cluster --name=ng-1 --node-type=t3.medium --nodes=3 --nodes-min=1 --nodes-max=4", language="bash")
                
            # AWS CLI 명령어
            with cli_tabs[3]:
                if st.session_state.current_file_type == "kubernetes":
                    st.code("# EKS 클러스터 정보 확인\naws eks describe-cluster --name my-cluster --region us-west-2", language="bash")
                    st.code("# kubeconfig 업데이트\naws eks update-kubeconfig --name my-cluster --region us-west-2", language="bash")


        render_resource_visualization(tab3)
        # # 리소스 시각화 탭
        # with tab3:
        #     if st.session_state.current_file_type == "kubernetes" and st.session_state.yaml_template:
        #         try:
        #             yaml_dict = yaml.safe_load(st.session_state.yaml_template)
        #             if yaml_dict and "kind" in yaml_dict:
        #                 kind = yaml_dict.get("kind", "")
        #                 name = yaml_dict.get("metadata", {}).get("name", "")
                        
        #                 st.markdown("<h4>리소스 시각화</h4>", unsafe_allow_html=True)
                        
        #                 # 리소스 유형별 시각화 (간소화된 버전)
        #                 if kind in ["Deployment", "StatefulSet", "ReplicaSet"]:
        #                     replicas = yaml_dict.get("spec", {}).get("replicas", 1)
                            
        #                     st.markdown(f"""
        #                     <div class="resource-box">
        #                         <div class="resource-header">
        #                             <div class="resource-icon">{kind[0]}</div>
        #                             <div class="resource-title">{kind}: {name}</div>
        #                         </div>
        #                         <div>레플리카: {replicas}개</div>
        #                     </div>
                            
        #                     <div class="resource-arrow">↓</div>
                            
        #                     <div class="resource-box">
        #                         <div class="resource-header">
        #                             <div class="resource-icon" style="background-color:#4361ee;">P</div>
        #                             <div class="resource-title">Pods</div>
        #                         </div>
        #                         <div>총 {replicas}개 Pod 관리</div>
        #                     </div>
        #                     """, unsafe_allow_html=True)
        #                 elif kind == "Service":
        #                     service_type = yaml_dict.get("spec", {}).get("type", "ClusterIP")
        #                     selectors = yaml_dict.get("spec", {}).get("selector", {})
        #                     selectors_str = ", ".join([f"{k}={v}" for k, v in selectors.items()]) if selectors else "없음"
                            
        #                     st.markdown(f"""
        #                     <div class="resource-box">
        #                         <div class="resource-header">
        #                             <div class="resource-icon">S</div>
        #                             <div class="resource-title">Service: {name}</div>
        #                         </div>
        #                         <div>타입: {service_type}</div>
        #                         <div>셀렉터: {selectors_str}</div>
        #                     </div>
        #                     """, unsafe_allow_html=True)
        #         except:
        #             st.info("유효한 YAML을 먼저 로드하거나 작성하세요.")
        #     elif st.session_state.current_file_type == "dockerfile" and st.session_state.dockerfile_template:
        #         st.markdown("<h4>Dockerfile 구조 시각화</h4>", unsafe_allow_html=True)
                
        #         # Dockerfile 명령어 추출 및 시각화
        #         lines = st.session_state.dockerfile_template.split('\n')
        #         layer_cmds = [line.strip() for line in lines if line.strip() and not line.strip().startswith('#')]
                
        #         if layer_cmds:
        #             st.markdown("<p>Docker 레이어 구조:</p>", unsafe_allow_html=True)
                    
        #             for i, cmd in enumerate(layer_cmds):
        #                 cmd_parts = cmd.split(' ', 1)
        #                 instruction = cmd_parts[0] if cmd_parts else ""
                        
        #                 # FROM, RUN 등의 주요 명령어만 표시
        #                 if instruction in ["FROM", "RUN", "COPY", "ADD"]:
        #                     st.markdown(f"""
        #                     <div class="docker-layer">
        #                         <div class="layer-content">{cmd}</div>
        #                         <div class="layer-size">Layer {i+1}</div>
        #                     </div>
        #                     """, unsafe_allow_html=True)
        #         else:
        #             st.info("Dockerfile을 먼저 로드하거나 작성하세요.")
    
    st.markdown('</div>', unsafe_allow_html=True)  # main-container 끝

def render_cheatsheets_tab():
    """치트시트 탭 렌더링"""
    
    # 제목을 작게 표시
    st.markdown("<h3 style='font-size: 1.2rem;'>쿠버네티스 & Docker 치트시트</h3>", unsafe_allow_html=True)
    
    # 카테고리 선택 탭
    category_tabs = st.tabs(["Kubernetes", "Docker", "AWS/EKS", "커스텀 치트시트"])
    
    # Kubernetes 치트시트
    with category_tabs[0]:
        # kubectl 명령어 치트시트 (수정된 디자인)
        st.markdown("<div class='section-title'>kubectl 명령어 치트시트</div>", unsafe_allow_html=True)
        
        kubectl_preview = """# 기본 명령어
kubectl get pods                        # 모든 파드 조회
kubectl get pods -n <namespace>         # 특정 네임스페이스의 파드 조회
kubectl get pods -o wide               # 파드 상세 정보 조회
kubectl get all                        # 모든 리소스 조회

# 리소스 상세 정보 확인
kubectl describe pod <pod-name>        # 파드 상세 정보
kubectl describe deployment <name>     # 디플로이먼트 상세 정보
kubectl logs <pod-name>                # 파드 로그 확인
kubectl logs -f <pod-name>             # 파드 로그 스트리밍

# 리소스 생성 및 관리
kubectl apply -f <file.yaml>           # 리소스 생성/업데이트
kubectl delete -f <file.yaml>          # 리소스 삭제
kubectl scale deployment <name> --replicas=3  # 디플로이먼트 스케일링

# 디버깅 및 테스트
kubectl exec -it <pod-name> -- /bin/bash  # 파드 셸 접속
kubectl port-forward <pod-name> 8080:80   # 포트 포워딩
kubectl cp <pod-name>:/path/to/file ./local/path  # 파일 복사
"""
        
        st.code(kubectl_preview, language="bash")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.button("👁️ 미리보기", key="preview_kubectl", use_container_width=True)
        with col2:
            # kubectl 치트시트 생성
            kubectl_pdf = generate_dummy_pdf_content(title="Kubectl 명령어 치트시트", content_type="kubectl")
            
            # docker 치트시트 생성 
            #docker_pdf = generate_dummy_pdf_content(title="Docker 치트시트", content_type="docker")
            
            st.download_button(
                "📥 PDF 다운로드",
                data=generate_dummy_pdf_content(),
                file_name="kubectl_cheatsheet.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        
        # Kubernetes YAML 구성 가이드 (수정된 디자인)
        st.markdown("<div class='section-title'>Kubernetes YAML 구성 가이드</div>", unsafe_allow_html=True)
        
        yaml_preview = """# Deployment 기본 구조
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-name
  labels:
    app: app-name
spec:
  replicas: 3
  selector:
    matchLabels:
      app: app-name
  template:
    metadata:
      labels:
        app: app-name
    spec:
      containers:
      - name: container-name
        image: container-image:tag
        resources:
          limits:
            cpu: "1"
            memory: "512Mi"
          requests:
            cpu: "500m"
            memory: "256Mi"
        ports:
        - containerPort: 80

# Service 구조
apiVersion: v1
kind: Service
metadata:
  name: service-name
spec:
  selector:
    app: app-name
  ports:
  - port: 80
    targetPort: 8080
  type: ClusterIP  # ClusterIP, NodePort, LoadBalancer
"""
        
        st.code(yaml_preview, language="yaml")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.button("👁️ 미리보기", key="preview_yaml", use_container_width=True)
        with col2:
            st.download_button(
                "📥 PDF 다운로드",
                data=generate_dummy_pdf_content(),
                file_name="kubernetes_yaml_guide.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    
    # Docker 치트시트
    with category_tabs[1]:
        # Docker 기본 명령어 (수정된 디자인)
        st.markdown("<div class='section-title'>Docker 기본 명령어</div>", unsafe_allow_html=True)
        
        docker_preview = """# 이미지 관리
docker pull <이미지명>[:<태그>]     # 이미지 다운로드
docker images                      # 이미지 목록 조회
docker rmi <이미지ID|이미지명>      # 이미지 삭제
docker image prune                 # 미사용 이미지 제거

# 컨테이너 관리
docker run -d -p 8080:80 --name my-nginx nginx  # 컨테이너 실행
docker ps                          # 실행 중인 컨테이너 목록
docker ps -a                       # 모든 컨테이너 목록
docker stop <컨테이너ID|이름>       # 컨테이너 정지
docker start <컨테이너ID|이름>      # 컨테이너 시작
docker rm <컨테이너ID|이름>         # 컨테이너 삭제
docker logs <컨테이너ID|이름>       # 컨테이너 로그 확인
docker exec -it <컨테이너ID|이름> bash  # 컨테이너 내부 접속

# 네트워크 & 볼륨
docker network ls                  # 네트워크 목록
docker volume ls                   # 볼륨 목록
docker volume create <볼륨명>      # 볼륨 생성
"""
        
        st.code(docker_preview, language="bash")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.button("👁️ 미리보기", key="preview_docker", use_container_width=True)
        with col2:
            st.download_button(
                "📥 PDF 다운로드",
                data=generate_dummy_pdf_content(),
                file_name="docker_commands.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        
        # Dockerfile 모범 사례 (수정된 디자인)
        st.markdown("<div class='section-title'>Dockerfile 모범 사례</div>", unsafe_allow_html=True)
        
        dockerfile_preview = """# 멀티스테이지 빌드 패턴
FROM node:14 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

# 모범 사례
# 1. 적절한 베이스 이미지 선택 (가능하면 공식 이미지의 alpine 태그 사용)
FROM python:3.9-alpine

# 2. 라벨로 메타데이터 추가
LABEL maintainer="name@example.com"
LABEL version="1.0"

# 3. 불필요한 패키지 설치 피하기
RUN apk add --no-cache curl

# 4. 여러 RUN 명령어를 하나로 체이닝하여 레이어 줄이기
RUN apk add --no-cache gcc musl-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /var/cache/apk/*
"""
        
        st.code(dockerfile_preview, language="dockerfile")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.button("👁️ 미리보기", key="preview_dockerfile", use_container_width=True)
        with col2:
            st.download_button(
                "📥 PDF 다운로드",
                data=generate_dummy_pdf_content(),
                file_name="dockerfile_best_practices.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    
    # AWS/EKS 치트시트
    with category_tabs[2]:
        # AWS CLI 치트시트 (수정된 디자인)
        st.markdown("<div class='section-title'>AWS CLI EKS 명령어</div>", unsafe_allow_html=True)
        
        aws_preview = """# EKS 클러스터 관리
aws eks list-clusters                # EKS 클러스터 목록 조회
aws eks describe-cluster --name my-cluster  # 클러스터 상세 정보 조회
aws eks update-kubeconfig --name my-cluster --region us-west-2  # kubeconfig 설정

# 노드그룹 관리
aws eks list-nodegroups --cluster-name my-cluster  # 노드그룹 목록
aws eks describe-nodegroup --cluster-name my-cluster --nodegroup-name ng-1  # 노드그룹 정보

# Fargate 프로필 관리
aws eks list-fargate-profiles --cluster-name my-cluster  # Fargate 프로필 목록
aws eks create-fargate-profile \
  --fargate-profile-name profile-1 \
  --cluster-name my-cluster \
  --pod-execution-role-arn arn:aws:iam::111122223333:role/AmazonEKSFargatePodExecutionRole \
  --selectors namespace=default,labels={app=nginx}  # Fargate 프로필 생성

# 애드온 관리
aws eks list-addons --cluster-name my-cluster  # 애드온 목록
aws eks describe-addon --cluster-name my-cluster --addon-name vpc-cni  # 애드온 정보
"""
        
        st.code(aws_preview, language="bash")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.button("👁️ 미리보기", key="preview_aws", use_container_width=True)
        with col2:
            st.download_button(
                "📥 PDF 다운로드",
                data=generate_dummy_pdf_content(),
                file_name="aws_eks_commands.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        
        # eksctl 명령어 (수정된 디자인)
        st.markdown("<div class='section-title'>eksctl 명령어</div>", unsafe_allow_html=True)
        
        eksctl_preview = """# 클러스터 관리
eksctl create cluster --name my-cluster --region us-west-2 --nodes 3  # 클러스터 생성
eksctl get cluster  # 클러스터 목록
eksctl delete cluster --name my-cluster  # 클러스터 삭제

# 노드그룹 관리
eksctl create nodegroup \
  --cluster my-cluster \
  --name ng-1 \
  --node-type t3.medium \
  --nodes 3 \
  --nodes-min 1 \
  --nodes-max 5  # 노드그룹 생성

eksctl get nodegroup --cluster my-cluster  # 노드그룹 목록
eksctl scale nodegroup --cluster my-cluster --name ng-1 --nodes 5  # 노드그룹 스케일링
eksctl delete nodegroup --cluster my-cluster --name ng-1  # 노드그룹 삭제

# IAM 관리
eksctl create iamserviceaccount \
  --name aws-load-balancer-controller \
  --namespace kube-system \
  --cluster my-cluster \
  --attach-policy-arn arn:aws:iam::111122223333:policy/AWSLoadBalancerControllerIAMPolicy \
  --approve  # 서비스 계정 생성
"""
        
        st.code(eksctl_preview, language="bash")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.button("👁️ 미리보기", key="preview_eksctl", use_container_width=True)
        with col2:
            st.download_button(
                "📥 PDF 다운로드",
                data=generate_dummy_pdf_content(),
                file_name="eksctl_commands.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    
    # 커스텀 치트시트 빌더
    with category_tabs[3]:
        st.markdown("<div class='section-title'>나만의 커스텀 치트시트 만들기</div>", unsafe_allow_html=True)
        st.markdown("자주 사용하는 명령어를 선택하여 맞춤형 치트시트 PDF를 생성하세요.", unsafe_allow_html=True)
        
        # 명령어 카테고리 선택
        cmd_category = st.selectbox(
            "명령어 카테고리",
            ["Kubernetes", "Docker", "AWS CLI", "eksctl"]
        )
        
        # 명령어 목록 (카테고리에 따라 다른 명령어 표시)
        kubernetes_commands = [
            {"cmd": "kubectl get pods", "desc": "모든 파드 조회"},
            {"cmd": "kubectl get services", "desc": "모든 서비스 조회"},
            {"cmd": "kubectl logs <pod-name>", "desc": "파드 로그 확인"},
            {"cmd": "kubectl describe pod <pod-name>", "desc": "파드 상세 정보 확인"},
            {"cmd": "kubectl apply -f <file.yaml>", "desc": "리소스 생성 또는 업데이트"},
            {"cmd": "kubectl delete -f <file.yaml>", "desc": "리소스 삭제"},
            {"cmd": "kubectl exec -it <pod-name> -- /bin/bash", "desc": "파드 셸 접속"},
            {"cmd": "kubectl port-forward <pod-name> 8080:80", "desc": "포트 포워딩"}
        ]
        
        docker_commands = [
            {"cmd": "docker ps", "desc": "실행 중인 컨테이너 조회"},
            {"cmd": "docker images", "desc": "이미지 목록 조회"},
            {"cmd": "docker build -t <name>:<tag> .", "desc": "이미지 빌드"},
            {"cmd": "docker run -d -p <host-port>:<container-port> <image>", "desc": "컨테이너 실행"},
            {"cmd": "docker logs <container>", "desc": "컨테이너 로그 확인"},
            {"cmd": "docker exec -it <container> bash", "desc": "컨테이너 셸 접속"},
            {"cmd": "docker-compose up -d", "desc": "컨테이너 그룹 시작"},
            {"cmd": "docker system prune", "desc": "미사용 리소스 정리"}
        ]
        
        aws_commands = [
            {"cmd": "aws eks list-clusters", "desc": "EKS 클러스터 목록 조회"},
            {"cmd": "aws eks describe-cluster --name <cluster-name>", "desc": "클러스터 상세 정보 조회"},
            {"cmd": "aws eks update-kubeconfig --name <cluster-name>", "desc": "kubeconfig 업데이트"},
            {"cmd": "aws ec2 describe-instances", "desc": "EC2 인스턴스 목록 조회"},
            {"cmd": "aws ecr get-login-password | docker login --username AWS --password-stdin <repo-url>", "desc": "ECR 로그인"},
            {"cmd": "aws s3 ls", "desc": "S3 버킷 목록 조회"},
            {"cmd": "aws iam list-roles", "desc": "IAM 역할 목록 조회"},
            {"cmd": "aws cloudformation deploy --template-file <file> --stack-name <name>", "desc": "CloudFormation 스택 배포"}
        ]
        
        eksctl_commands = [
            {"cmd": "eksctl create cluster --name <cluster-name>", "desc": "클러스터 생성"},
            {"cmd": "eksctl get clusters", "desc": "클러스터 목록 조회"},
            {"cmd": "eksctl create nodegroup --cluster <cluster-name>", "desc": "노드그룹 생성"},
            {"cmd": "eksctl get nodegroup --cluster <cluster-name>", "desc": "노드그룹 조회"},
            {"cmd": "eksctl scale nodegroup --cluster <cluster-name> --name <ng-name> --nodes <count>", "desc": "노드그룹 스케일링"},
            {"cmd": "eksctl delete cluster --name <cluster-name>", "desc": "클러스터 삭제"},
            {"cmd": "eksctl create iamserviceaccount --name <name> --namespace <ns> --cluster <cluster>", "desc": "IAM 서비스 계정 생성"},
            {"cmd": "eksctl utils describe-addon-versions --cluster <cluster-name>", "desc": "사용 가능한 애드온 버전 조회"}
        ]
        
        # 선택한 카테고리에 따른 명령어 목록
        if cmd_category == "Kubernetes":
            commands = kubernetes_commands
        elif cmd_category == "Docker":
            commands = docker_commands
        elif cmd_category == "AWS CLI":
            commands = aws_commands
        else:  # eksctl
            commands = eksctl_commands
        
        # 명령어 선택 인터페이스
        st.markdown("<div class='command-list'>", unsafe_allow_html=True)
        
        # 체크박스로 명령어 선택
        selected_commands = []
        for i, cmd in enumerate(commands):
            if st.checkbox(f"{cmd['cmd']} - {cmd['desc']}", key=f"cmd_{i}"):
                selected_commands.append(cmd)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 파일 이름 설정 및 PDF 생성
        col1, col2 = st.columns([2, 1])
        
        with col1:
            pdf_name = st.text_input("치트시트 파일 이름", value=f"my-{cmd_category.lower()}-cheatsheet")
        
        with col2:
            st.markdown("<div style='padding-top: 25px;'></div>", unsafe_allow_html=True)  # 버튼 위치 조정
            generate_btn = st.button("PDF 생성", type="primary", use_container_width=True)
        
        # PDF 생성 로직
        if generate_btn and selected_commands:
            # 다운로드 버튼
            st.download_button(
                label="📥 치트시트 PDF 다운로드",
                data=generate_dummy_pdf_content(),
                file_name=f"{pdf_name}.pdf",
                mime="application/pdf"
            )
            
            st.success(f"{len(selected_commands)}개 명령어가 포함된 치트시트가 생성되었습니다!")

def render_cli_guide_tab():
    """CLI 안내서 탭 렌더링"""
    
    st.markdown("<h3 style='font-size: 1.2rem;'>CLI 명령어 안내서</h3>", unsafe_allow_html=True)
    st.markdown("Kubernetes, Docker, AWS, EKS 관련 주요 명령어 안내서입니다.", unsafe_allow_html=True)
    
    # CLI 종류 선택
    cli_type = st.selectbox(
        "CLI 도구 선택",
        ["kubectl", "docker", "aws", "eksctl"]
    )
    
    # kubectl 명령어
    if cli_type == "kubectl":
        st.markdown("<div class='section-title'>kubectl - Kubernetes 명령줄 도구</div>", unsafe_allow_html=True)
        
        # 명령어 카테고리 선택
        kubectl_category = st.radio(
            "명령어 카테고리",
            ["기본 명령어", "디버깅", "리소스 관리", "고급 명령어"]
        )
        
        if kubectl_category == "기본 명령어":
            st.markdown("<div class='command-title'>클러스터 & 노드 정보</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>클러스터와 노드 정보를 확인하는 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>kubectl cluster-info                  # 클러스터 정보 표시\nkubectl cluster-info dump           # 클러스터 디버깅 정보 덤프\nkubectl config view                # kubeconfig 설정 보기\nkubectl get nodes                  # 노드 목록 확인\nkubectl describe node <node-name>  # 특정 노드 상세 정보</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-title'>리소스 조회</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>다양한 Kubernetes 리소스를 조회하는 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>kubectl get all                       # 모든 리소스 조회\nkubectl get pods                     # 파드 목록 조회\nkubectl get pods -o wide            # 파드 상세 정보 포함 조회\nkubectl get pods --all-namespaces   # 모든 네임스페이스의 파드 조회\nkubectl get svc                     # 서비스 목록 조회\nkubectl get deployments             # 디플로이먼트 목록 조회\nkubectl get configmaps             # ConfigMap 목록 조회\nkubectl get secrets                # Secret 목록 조회\nkubectl get pv                     # PersistentVolume 목록 조회\nkubectl get pvc                    # PersistentVolumeClaim 목록 조회</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-title'>컨텍스트 관리</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>kubectl 컨텍스트를 관리하는 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>kubectl config get-contexts          # 모든 컨텍스트 조회\nkubectl config current-context      # 현재 컨텍스트 확인\nkubectl config use-context <name>   # 컨텍스트 전환\nkubectl config set-context --current --namespace=<ns>  # 현재 컨텍스트의 기본 네임스페이스 변경</div>", unsafe_allow_html=True)
            
        elif kubectl_category == "디버깅":
            st.markdown("<div class='command-title'>로그 확인</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>컨테이너 로그를 확인하는 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>kubectl logs <pod-name>                  # 파드 로그 확인\nkubectl logs <pod-name> -c <container>  # 특정 컨테이너 로그 확인\nkubectl logs -f <pod-name>             # 로그 스트리밍(실시간)\nkubectl logs --tail=100 <pod-name>     # 마지막 100줄만 확인\nkubectl logs --since=1h <pod-name>     # 최근 1시간 로그만 확인</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-title'>Pod 디버깅 및 상세 정보</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>파드 및 컨테이너 디버깅을 위한 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>kubectl describe pod <pod-name>            # 파드 상세 정보 확인\nkubectl exec -it <pod-name> -- /bin/bash  # 파드 내 셸 접속\nkubectl exec <pod-name> -- <command>     # 파드에서 명령어 실행\nkubectl port-forward <pod-name> 8080:80  # 로컬 포트 8080을 파드 포트 80으로 포워딩</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-title'>이벤트 및 문제 해결</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>클러스터 이벤트와 문제 해결을 위한 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>kubectl get events                       # 모든 이벤트 조회\nkubectl get events --sort-by=.metadata.creationTimestamp  # 생성 시간순 정렬\nkubectl top pods                        # 파드 리소스 사용량 확인\nkubectl top nodes                       # 노드 리소스 사용량 확인\nkubectl explain <resource>              # 리소스 필드 설명 확인\nkubectl cluster-info dump > cluster-dump.txt  # 클러스터 디버깅 정보 파일로 저장</div>", unsafe_allow_html=True)
            
        elif kubectl_category == "리소스 관리":
            st.markdown("<div class='command-title'>리소스 생성 및 변경</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>Kubernetes 리소스를 생성하고 관리하는 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>kubectl create -f <file.yaml>          # 리소스 생성\nkubectl apply -f <file.yaml>           # 리소스 생성 또는 업데이트\nkubectl apply -f <directory>/        # 디렉토리의 모든 매니페스트 적용\nkubectl replace -f <file.yaml>        # 리소스 교체\nkubectl delete -f <file.yaml>        # 리소스 삭제</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-title'>리소스 편집 및 스케일링</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>리소스를 직접 편집하고 스케일링하는 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>kubectl edit <resource> <name>        # 리소스 직접 편집\nkubectl scale deployment <name> --replicas=3  # 디플로이먼트 스케일링\nkubectl autoscale deployment <name> --min=2 --max=5 --cpu-percent=80  # HPA 설정\nkubectl rollout restart deployment <name>  # 디플로이먼트 재시작</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-title'>ConfigMaps & Secrets</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>ConfigMap과 Secret을 관리하는 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>kubectl create configmap <name> --from-file=<file>  # 파일로부터 ConfigMap 생성\nkubectl create configmap <name> --from-literal=key1=value1 --from-literal=key2=value2  # 리터럴 값으로 생성\nkubectl create secret generic <name> --from-file=<file>  # 파일로부터 Secret 생성\nkubectl create secret generic <name> --from-literal=key1=value1  # 리터럴 값으로 Secret 생성\nkubectl create secret tls <name> --cert=<cert-file> --key=<key-file>  # TLS Secret 생성</div>", unsafe_allow_html=True)
            
        elif kubectl_category == "고급 명령어":
            st.markdown("<div class='command-title'>RBAC 관리</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>역할 기반 액세스 제어(RBAC)를 관리하는 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>kubectl create serviceaccount <name>  # 서비스 계정 생성\nkubectl create role <name> --verb=get,list --resource=pods  # Role 생성\nkubectl create rolebinding <name> --role=<role> --serviceaccount=<ns>:<sa>  # RoleBinding 생성\nkubectl create clusterrole <name> --verb=get,list --resource=pods  # ClusterRole 생성\nkubectl create clusterrolebinding <name> --clusterrole=<role> --serviceaccount=<ns>:<sa>  # ClusterRoleBinding 생성</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-title'>출력 형식 & JSONPath</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>다양한 출력 형식과 JSONPath를 사용하는 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>kubectl get pods -o json                  # JSON 형식으로 출력\nkubectl get pods -o yaml                  # YAML 형식으로 출력\nkubectl get pods -o wide                  # 상세 정보 포함 테이블 형식\nkubectl get pods -o jsonpath='{.items[0].metadata.name}'  # 첫 번째 파드 이름 추출\nkubectl get pods -o jsonpath='{.items[*].metadata.name}'  # 모든 파드 이름 추출\nkubectl get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase  # 커스텀 컬럼</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-title'>패치 & 컨테이너 명령</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>리소스를 패치하고 컨테이너 명령을 관리하는 고급 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>kubectl patch deployment <name> -p '{\"spec\":{\"replicas\":3}}'  # JSON 패치로 스케일링\nkubectl patch deployment <name> --type json -p '[{\"op\":\"replace\",\"path\":\"/spec/replicas\",\"value\":3}]'  # JSON 패치(RFC 6902)\nkubectl set image deployment/<name> container-name=new-image:tag  # 컨테이너 이미지 변경\nkubectl set resources deployment/<name> -c container-name --limits=cpu=200m,memory=512Mi  # 리소스 제한 설정</div>", unsafe_allow_html=True)
            
    # docker 명령어
    elif cli_type == "docker":
        st.markdown("<div class='section-title'>Docker 명령줄 도구</div>", unsafe_allow_html=True)
        
        # 명령어 카테고리 선택
        docker_category = st.radio(
            "명령어 카테고리",
            ["이미지 관리", "컨테이너 관리", "Docker Compose", "네트워크 & 볼륨"]
        )
        
        if docker_category == "이미지 관리":
            st.markdown("<div class='command-title'>이미지 가져오기 & 조회</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>Docker 이미지를 검색, 가져오기, 조회하는 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>docker search nginx                # nginx 이미지 검색\ndocker pull nginx:latest          # 최신 nginx 이미지 다운로드\ndocker pull ubuntu:20.04          # 특정 태그 지정 다운로드\ndocker images                   # 모든 이미지 목록 조회\ndocker image ls                 # 이미지 목록(최신 문법)\ndocker image inspect nginx      # nginx 이미지 상세 정보\ndocker image history nginx      # 이미지 레이어 히스토리 확인</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-title'>이미지 빌드 & 관리</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>Dockerfile로부터 이미지를 빌드하고 관리하는 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>docker build -t myapp:1.0 .       # 현재 디렉토리의 Dockerfile로 이미지 빌드\ndocker build -f custom.dockerfile -t myapp:latest .  # 커스텀 Dockerfile 지정\ndocker tag myapp:1.0 username/myapp:1.0  # 이미지 태그 추가\ndocker push username/myapp:1.0    # Docker Hub에 이미지 푸시\ndocker save -o myapp.tar myapp:1.0  # 이미지를 tar 파일로 저장\ndocker load -i myapp.tar         # tar 파일에서 이미지 로드\ndocker rmi myapp:1.0            # 이미지 삭제\ndocker image prune -a           # 미사용 이미지 모두 제거</div>", unsafe_allow_html=True)
            
        elif docker_category == "컨테이너 관리":
            st.markdown("<div class='command-title'>컨테이너 실행 & 관리</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>컨테이너를 실행하고 관리하는 기본 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>docker run -d nginx              # 백그라운드로 nginx 실행\ndocker run -d -p 8080:80 nginx   # 포트 매핑(8080->80)\ndocker run -d --name web nginx   # 컨테이너 이름 지정\ndocker run -e VAR=value nginx   # 환경 변수 설정\ndocker run -v /host:/container nginx  # 볼륨 마운트\ndocker run --rm nginx           # 종료 시 자동 삭제\ndocker ps                      # 실행 중인 컨테이너 목록\ndocker ps -a                   # 모든 컨테이너 목록(정지된 것 포함)</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-title'>컨테이너 조작 & 모니터링</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>실행 중인 컨테이너를 조작하고 모니터링하는 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>docker start <container>         # 컨테이너 시작\ndocker stop <container>          # 컨테이너 정지\ndocker restart <container>      # 컨테이너 재시작\ndocker pause <container>        # 컨테이너 일시 중지\ndocker unpause <container>      # 컨테이너 일시 중지 해제\ndocker exec -it <container> bash  # 컨테이너 내부 셸 접속\ndocker logs <container>         # 컨테이너 로그 확인\ndocker logs -f <container>      # 컨테이너 로그 스트리밍\ndocker stats                    # 모든 컨테이너 자원 사용량\ndocker top <container>          # 컨테이너 내부 프로세스 목록</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-title'>컨테이너 정리 & 제거</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>컨테이너를 정리하고 제거하는 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>docker rm <container>            # 컨테이너 삭제(중지된 상태)\ndocker rm -f <container>         # 컨테이너 강제 삭제(실행 중이라도)\ndocker container prune           # 중지된 컨테이너 모두 제거\ndocker rm \$(docker ps -aq)      # 모든 컨테이너 제거\ndocker system prune             # 미사용 컨테이너, 이미지, 네트워크 제거\ndocker system prune -a          # 모든 미사용 리소스 제거(사용중이지 않은 이미지 포함)</div>", unsafe_allow_html=True)
            
        elif docker_category == "Docker Compose":
            st.markdown("<div class='command-title'>기본 Compose 명령어</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>docker-compose.yml 파일로 멀티 컨테이너 앱을 관리하는 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>docker-compose up               # 서비스 시작(포그라운드)\ndocker-compose up -d            # 서비스 백그라운드로 시작\ndocker-compose down            # 서비스 중지 및 제거\ndocker-compose ps              # 서비스 상태 확인\ndocker-compose logs            # 서비스 로그 확인\ndocker-compose logs -f         # 서비스 로그 스트리밍\ndocker-compose exec <service> <command>  # 서비스 컨테이너에서 명령 실행\ndocker-compose exec web bash   # 웹 서비스 컨테이너 셸 접속</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-title'>서비스 관리 & 스케일링</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>Docker Compose 서비스를 관리하고 스케일링하는 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>docker-compose start           # 중지된 서비스 시작\ndocker-compose stop            # 실행 중인 서비스 중지(제거하지 않음)\ndocker-compose restart         # 서비스 재시작\ndocker-compose build           # 서비스 이미지 빌드\ndocker-compose pull            # 서비스 이미지 가져오기\ndocker-compose up --build     # 빌드 후 서비스 시작\ndocker-compose up -d --scale web=3  # 웹 서비스를 3개 인스턴스로 스케일링</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-title'>Compose 파일 & 환경</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>다양한 Compose 파일과 환경 설정을 관리하는 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>docker-compose -f custom-compose.yml up  # 커스텀 파일 지정\ndocker-compose -f docker-compose.yml -f docker-compose.prod.yml up  # 여러 파일 결합\ndocker-compose --env-file .env.prod up  # 환경 파일 지정\ndocker-compose config           # 실제 compose 설정 확인\ndocker-compose --profile dev up  # 특정 프로필 사용</div>", unsafe_allow_html=True)
            
        elif docker_category == "네트워크 & 볼륨":
            st.markdown("<div class='command-title'>네트워크 관리</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>Docker 네트워크를 생성하고 관리하는 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>docker network ls                # 모든 네트워크 목록\ndocker network create mynet      # 브릿지 네트워크 생성\ndocker network create --driver overlay mynet  # 오버레이 네트워크 생성\ndocker network inspect mynet     # 네트워크 상세 정보\ndocker network connect mynet container1  # 컨테이너를 네트워크에 연결\ndocker network disconnect mynet container1  # 컨테이너 연결 해제\ndocker network prune             # 미사용 네트워크 제거\ndocker run --network=mynet nginx  # 특정 네트워크로 컨테이너 실행</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-title'>볼륨 관리</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>Docker 볼륨을 생성하고 관리하는 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>docker volume ls                # 모든 볼륨 목록\ndocker volume create myvol      # 볼륨 생성\ndocker volume inspect myvol     # 볼륨 상세 정보\ndocker volume rm myvol          # 볼륨 삭제\ndocker volume prune             # 미사용 볼륨 제거\ndocker run -v myvol:/app/data nginx  # 볼륨 마운트로 컨테이너 실행\ndocker run --mount source=myvol,target=/app/data nginx  # mount 플래그 사용\ndocker run -v /host/path:/container/path nginx  # 바인드 마운트</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-title'>시스템 관리</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>Docker 시스템 정보와 리소스를 관리하는 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>docker info                      # Docker 시스템 정보\ndocker system df                 # 디스크 사용량 정보\ndocker system events             # 실시간 Docker 이벤트 확인\ndocker system prune              # 미사용 데이터 정리\ndocker system prune -a --volumes  # 모든 미사용 객체(볼륨 포함) 정리\ndocker stats                     # 컨테이너 자원 사용량 실시간 모니터링</div>", unsafe_allow_html=True)
    
    # aws 명령어
    elif cli_type == "aws":
        st.markdown("<div class='section-title'>AWS CLI 명령어</div>", unsafe_allow_html=True)
        
        # 명령어 카테고리 선택
        aws_category = st.radio(
            "명령어 카테고리",
            ["EKS", "EC2", "IAM", "S3 & ECR"]
        )
        
        if aws_category == "EKS":
            st.markdown("<div class='command-title'>EKS 클러스터 관리</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>EKS 클러스터를 생성하고 관리하는 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>aws eks list-clusters                           # EKS 클러스터 목록 조회\naws eks describe-cluster --name my-cluster       # 클러스터 상세 정보 조회\naws eks create-cluster --name my-cluster \\\n  --role-arn arn:aws:iam::111122223333:role/eks-cluster-role \\\n  --resources-vpc-config subnetIds=subnet-id1,subnet-id2,securityGroupIds=sg-id  # 클러스터 생성\naws eks delete-cluster --name my-cluster        # 클러스터 삭제\naws eks update-kubeconfig --name my-cluster     # kubeconfig 업데이트\naws eks update-cluster-version --name my-cluster --kubernetes-version 1.22  # 클러스터 버전 업데이트</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-title'>EKS 노드그룹 관리</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>EKS 노드그룹을 생성하고 관리하는 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>aws eks list-nodegroups --cluster-name my-cluster  # 노드그룹 목록\naws eks describe-nodegroup --cluster-name my-cluster --nodegroup-name ng-1  # 노드그룹 정보\naws eks create-nodegroup --cluster-name my-cluster \\\n  --nodegroup-name ng-1 \\\n  --node-role arn:aws:iam::111122223333:role/eks-node-role \\\n  --subnets subnet-id1 subnet-id2 \\\n  --instance-types t3.medium \\\n  --scaling-config minSize=2,maxSize=5,desiredSize=3  # 노드그룹 생성\naws eks update-nodegroup-config --cluster-name my-cluster \\\n  --nodegroup-name ng-1 \\\n  --scaling-config minSize=2,maxSize=10,desiredSize=5  # 노드그룹 설정 업데이트\naws eks delete-nodegroup --cluster-name my-cluster --nodegroup-name ng-1  # 노드그룹 삭제</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-title'>EKS Fargate & 애드온</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>EKS Fargate 프로필과 애드온을 관리하는 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>aws eks create-fargate-profile \\\n  --fargate-profile-name fp-default \\\n  --cluster-name my-cluster \\\n  --pod-execution-role-arn arn:aws:iam::111122223333:role/eks-fargate-role \\\n  --selectors namespace=default  # Fargate 프로필 생성\naws eks list-fargate-profiles --cluster-name my-cluster  # Fargate 프로필 목록\naws eks describe-fargate-profile \\\n  --cluster-name my-cluster \\\n  --fargate-profile-name fp-default  # Fargate 프로필 정보\naws eks delete-fargate-profile \\\n  --cluster-name my-cluster \\\n  --fargate-profile-name fp-default  # Fargate 프로필 삭제\naws eks list-addons --cluster-name my-cluster  # 설치된 애드온 목록\naws eks describe-addon \\\n  --cluster-name my-cluster \\\n  --addon-name vpc-cni  # 애드온 정보 조회\naws eks create-addon \\\n  --cluster-name my-cluster \\\n  --addon-name vpc-cni \\\n  --addon-version v1.10.1-eksbuild.1  # 애드온 설치</div>", unsafe_allow_html=True)
            
        elif aws_category == "EC2":
            st.markdown("<div class='command-title'>EC2 인스턴스 관리</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>EC2 인스턴스를 생성하고 관리하는 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>aws ec2 describe-instances                    # 모든 인스턴스 조회\naws ec2 describe-instances --filters Name=instance-type,Values=t2.micro  # 필터링된 인스턴스 조회\naws ec2 run-instances \\\n  --image-id ami-12345678 \\\n  --instance-type t2.micro \\\n  --key-name MyKeyPair \\\n  --security-group-ids sg-12345678  # 인스턴스 생성\naws ec2 start-instances --instance-ids i-1234567890abcdef0  # 인스턴스 시작\naws ec2 stop-instances --instance-ids i-1234567890abcdef0   # 인스턴스 중지\naws ec2 terminate-instances --instance-ids i-1234567890abcdef0  # 인스턴스 종료</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-title'>EC2 보안그룹 & 키페어</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>EC2 보안그룹과 키페어를 관리하는 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>aws ec2 describe-security-groups                   # 모든 보안그룹 조회\naws ec2 create-security-group \\\n  --group-name MySecurityGroup \\\n  --description \"My security group\" \\\n  --vpc-id vpc-12345678  # 보안그룹 생성\naws ec2 authorize-security-group-ingress \\\n  --group-id sg-12345678 \\\n  --protocol tcp \\\n  --port 22 \\\n  --cidr 203.0.113.0/24  # 인바운드 규칙 추가\naws ec2 describe-key-pairs                       # 키페어 목록 조회\naws ec2 create-key-pair --key-name MyKeyPair     # 키페어 생성\naws ec2 delete-key-pair --key-name MyKeyPair     # 키페어 삭제</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-title'>EC2 볼륨 & 스냅샷</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>EC2 볼륨과 스냅샷을 관리하는 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>aws ec2 describe-volumes                       # 모든 볼륨 조회\naws ec2 create-volume \\\n  --size 8 \\\n  --availability-zone us-east-1a \\\n  --volume-type gp2  # 볼륨 생성\naws ec2 attach-volume \\\n  --volume-id vol-12345678 \\\n  --instance-id i-1234567890abcdef0 \\\n  --device /dev/sdf  # 볼륨 연결\naws ec2 create-snapshot \\\n  --volume-id vol-12345678 \\\n  --description \"My snapshot\"  # 스냅샷 생성\naws ec2 describe-snapshots --owner-ids self      # 내 스냅샷 조회\naws ec2 delete-snapshot --snapshot-id snap-12345678  # 스냅샷 삭제</div>", unsafe_allow_html=True)
            
        elif aws_category == "IAM":
            st.markdown("<div class='command-title'>IAM 사용자 & 그룹 관리</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>IAM 사용자와 그룹을 관리하는 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>aws iam list-users                            # 사용자 목록 조회\naws iam create-user --user-name johndoe         # 사용자 생성\naws iam delete-user --user-name johndoe         # 사용자 삭제\naws iam list-groups                           # 그룹 목록 조회\naws iam create-group --group-name Developers   # 그룹 생성\naws iam add-user-to-group \\\n  --user-name johndoe \\\n  --group-name Developers  # 그룹에 사용자 추가\naws iam remove-user-from-group \\\n  --user-name johndoe \\\n  --group-name Developers  # 그룹에서 사용자 제거\naws iam delete-group --group-name Developers   # 그룹 삭제</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-title'>IAM 역할 & 정책 관리</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>IAM 역할과 정책을 관리하는 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>aws iam list-roles                            # 역할 목록 조회\naws iam create-role \\\n  --role-name S3Access \\\n  --assume-role-policy-document file://trust-policy.json  # 역할 생성\naws iam list-policies                          # 정책 목록 조회\naws iam create-policy \\\n  --policy-name MyPolicy \\\n  --policy-document file://policy.json  # 정책 생성\naws iam attach-role-policy \\\n  --role-name S3Access \\\n  --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess  # 정책 연결\naws iam detach-role-policy \\\n  --role-name S3Access \\\n  --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess  # 정책 연결 해제\naws iam delete-role --role-name S3Access        # 역할 삭제</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-title'>IAM 액세스 키 & 자격 증명</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>IAM 액세스 키와 자격 증명을 관리하는 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>aws iam create-access-key --user-name johndoe   # 액세스 키 생성\naws iam list-access-keys --user-name johndoe    # 액세스 키 목록 조회\naws iam update-access-key \\\n  --user-name johndoe \\\n  --access-key-id AKIAIOSFODNN7EXAMPLE \\\n  --status Inactive  # 액세스 키 비활성화\naws iam delete-access-key \\\n  --user-name johndoe \\\n  --access-key-id AKIAIOSFODNN7EXAMPLE  # 액세스 키 삭제\naws iam create-service-specific-credential \\\n  --user-name johndoe \\\n  --service-name codecommit.amazonaws.com  # 서비스별 자격 증명 생성\naws iam reset-service-specific-credential \\\n  --user-name johndoe \\\n  --service-specific-credential-id ACCAEXAMPLE123EXAMPLE  # 서비스별 자격 증명 재설정</div>", unsafe_allow_html=True)
            
        elif aws_category == "S3 & ECR":
            st.markdown("<div class='command-title'>S3 기본 명령어</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>S3 버킷과 객체를 관리하는 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>aws s3 ls                                 # 모든 S3 버킷 목록 조회\naws s3 mb s3://my-bucket                    # 버킷 생성\naws s3 rb s3://my-bucket                    # 비어있는 버킷 삭제\naws s3 rb s3://my-bucket --force            # 버킷 강제 삭제(객체 포함)\naws s3 ls s3://my-bucket                    # 버킷 내 객체 목록 조회\naws s3 cp file.txt s3://my-bucket/          # 파일 업로드\naws s3 cp s3://my-bucket/file.txt ./        # 파일 다운로드\naws s3 rm s3://my-bucket/file.txt           # 객체 삭제\naws s3 sync local-folder s3://my-bucket/    # 로컬 폴더와 S3 동기화\naws s3 sync s3://my-bucket/ local-folder    # S3에서 로컬로 동기화</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-title'>S3 고급 명령어</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>S3 권한, 버전 관리, 웹사이트 설정을 관리하는 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>aws s3api put-bucket-policy \\\n  --bucket my-bucket \\\n  --policy file://policy.json  # 버킷 정책 설정\naws s3api get-bucket-policy --bucket my-bucket  # 버킷 정책 조회\naws s3api put-bucket-versioning \\\n  --bucket my-bucket \\\n  --versioning-configuration Status=Enabled  # 버전 관리 활성화\naws s3api put-bucket-website \\\n  --bucket my-bucket \\\n  --website-configuration file://website.json  # 정적 웹사이트 설정\naws s3api put-public-access-block \\\n  --bucket my-bucket \\\n  --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true  # 공개 액세스 차단</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-title'>ECR 명령어</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>Amazon ECR 레지스트리를 관리하는 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>aws ecr get-login-password | docker login \\\n  --username AWS \\\n  --password-stdin 111122223333.dkr.ecr.us-east-1.amazonaws.com  # ECR 로그인\naws ecr create-repository --repository-name my-repo  # 리포지토리 생성\naws ecr list-repositories                         # 리포지토리 목록 조회\naws ecr describe-repositories --repository-names my-repo  # 리포지토리 상세 정보\naws ecr list-images --repository-name my-repo     # 이미지 목록 조회\n\n# Docker 이미지 태그 지정 및 푸시\ndocker tag myapp:latest 111122223333.dkr.ecr.us-east-1.amazonaws.com/my-repo:latest\ndocker push 111122223333.dkr.ecr.us-east-1.amazonaws.com/my-repo:latest\n\naws ecr delete-repository --repository-name my-repo --force  # 리포지토리 삭제</div>", unsafe_allow_html=True)
    
    # eksctl 명령어
    elif cli_type == "eksctl":
        st.markdown("<div class='section-title'>eksctl - EKS 클러스터 관리 도구</div>", unsafe_allow_html=True)
        
        # 명령어 카테고리 선택
        eksctl_category = st.radio(
            "명령어 카테고리",
            ["클러스터 관리", "노드그룹 관리", "IAM 관리", "애드온 관리"]
        )
        
        if eksctl_category == "클러스터 관리":
            st.markdown("<div class='command-title'>기본 클러스터 생성 & 관리</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>EKS 클러스터를 생성하고 관리하는 기본 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>eksctl create cluster                               # 기본 설정으로 클러스터 생성\neksctl create cluster --name my-cluster            # 이름 지정\neksctl create cluster --region us-west-2           # 리전 지정\neksctl create cluster \\\n  --name my-cluster \\\n  --region us-west-2 \\\n  --version 1.22 \\\n  --nodes 3  # 노드 수와 버전 지정\neksctl get cluster                                 # 모든 클러스터 조회\neksctl get cluster --name my-cluster               # 특정 클러스터 정보 조회\neksctl delete cluster --name my-cluster            # 클러스터 삭제</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-title'>고급 클러스터 설정</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>다양한 옵션을 사용한 클러스터 생성 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>eksctl create cluster \\\n  --name my-cluster \\\n  --region us-west-2 \\\n  --nodegroup-name standard-workers \\\n  --node-type t3.medium \\\n  --nodes 3 \\\n  --nodes-min 1 \\\n  --nodes-max 5 \\\n  --with-oidc \\\n  --ssh-access \\\n  --ssh-public-key my-key \\\n  --managed  # 고급 옵션으로 클러스터 생성\n\n# 프라이빗 클러스터 생성\neksctl create cluster \\\n  --name private-cluster \\\n  --region us-west-2 \\\n  --vpc-private-subnets=subnet-0123abc,subnet-def456 \\\n  --without-nodegroup \\\n  --vpc-nat-mode HighlyAvailable \\\n  --api-public-access=false \\\n  --api-version latest</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-title'>클러스터 업그레이드</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>EKS 클러스터와 컨트롤 플레인을 업그레이드하는 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>eksctl upgrade cluster \\\n  --name my-cluster \\\n  --version 1.22  # 컨트롤 플레인 업그레이드\n\n# 버전 확인\neksctl version\neksctl get cluster --name my-cluster\n\n# kubeconfig 업데이트\neksctl utils write-kubeconfig --cluster=my-cluster\neksctl utils write-kubeconfig --cluster=my-cluster --region=us-west-2 --kubeconfig=~/.kube/my-config</div>", unsafe_allow_html=True)
            
        elif eksctl_category == "노드그룹 관리":
            st.markdown("<div class='command-title'>노드그룹 생성 & 관리</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>노드그룹을 생성하고 관리하는 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>eksctl create nodegroup \\\n  --cluster my-cluster \\\n  --name ng-1 \\\n  --node-type t3.medium \\\n  --nodes 3  # 기본 노드그룹 생성\n\neksctl create nodegroup \\\n  --cluster my-cluster \\\n  --name ng-2 \\\n  --node-type t3.large \\\n  --nodes 2 \\\n  --nodes-min 1 \\\n  --nodes-max 4 \\\n  --ssh-access \\\n  --ssh-public-key my-key \\\n  --managed  # 고급 옵션 노드그룹 생성\n\neksctl get nodegroup --cluster my-cluster  # 노드그룹 목록 조회\neksctl delete nodegroup \\\n  --cluster my-cluster \\\n  --name ng-1  # 노드그룹 삭제</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-title'>노드그룹 스케일링 & 업데이트</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>노드그룹을 스케일링하고 업데이트하는 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'>eksctl scale nodegroup \\\n  --cluster my-cluster \\\n  --name ng-1 \\\n  --nodes 5  # 노드 수 설정\n\neksctl scale nodegroup \\\n  --cluster my-cluster \\\n  --name ng-1 \\\n  --nodes-min 2 \\\n  --nodes-max 8 \\\n  --nodes 5  # 최소, 최대, 현재 노드 수 설정\n\neksctl upgrade nodegroup \\\n  --cluster my-cluster \\\n  --name ng-1 \\\n  --kubernetes-version 1.22  # 노드그룹 업그레이드</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-title'>특수 노드그룹 설정</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>스팟 인스턴스 및 특별한 설정의 노드그룹 생성 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'># 스팟 인스턴스 노드그룹 생성\neksctl create nodegroup \\\n  --cluster my-cluster \\\n  --name spot-ng \\\n  --instance-types t3.medium,t3.large \\\n  --spot \\\n  --nodes 3\n\n# GPU 노드그룹 생성\neksctl create nodegroup \\\n  --cluster my-cluster \\\n  --name gpu-ng \\\n  --node-type p3.2xlarge \\\n  --nodes 2 \\\n  --install-nvidia-plugin\n\n# 테인트가 있는 노드그룹 생성\neksctl create nodegroup \\\n  --cluster my-cluster \\\n  --name tainted-ng \\\n  --node-type t3.medium \\\n  --nodes 3 \\\n  --taints \"dedicated=experimental:NoSchedule\"</div>", unsafe_allow_html=True)
            
        elif eksctl_category == "IAM 관리":
            st.markdown("<div class='command-title'>OIDC 및 IAM 서비스 계정</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>EKS OIDC 공급자 및 서비스 계정을 관리하는 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'># OIDC 공급자 활성화\neksctl utils associate-iam-oidc-provider \\\n  --cluster my-cluster \\\n  --approve\n\n# OIDC 공급자 상태 확인\neksctl utils describe-stacks --cluster my-cluster\n\n# IAM 서비스 계정 생성\neksctl create iamserviceaccount \\\n  --name aws-load-balancer-controller \\\n  --namespace kube-system \\\n  --cluster my-cluster \\\n  --attach-policy-arn arn:aws:iam::111122223333:policy/AWSLoadBalancerControllerIAMPolicy \\\n  --approve\n\n# IAM 서비스 계정 목록 확인\neksctl get iamserviceaccount --cluster my-cluster\n\n# IAM 서비스 계정 삭제\neksctl delete iamserviceaccount \\\n  --name aws-load-balancer-controller \\\n  --namespace kube-system \\\n  --cluster my-cluster</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-title'>클러스터 IAM 역할 관리</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>클러스터 및 노드그룹 IAM 역할을 관리하는 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'># 클러스터 생성 시 IAM 역할 지정\neksctl create cluster \\\n  --name my-cluster \\\n  --service-role arn:aws:iam::111122223333:role/EKSClusterRole\n\n# 노드그룹 생성 시 IAM 역할 지정\neksctl create nodegroup \\\n  --cluster my-cluster \\\n  --name ng-1 \\\n  --node-role arn:aws:iam::111122223333:role/EKSNodeRole\n\n# 기존 클러스터에 IAM 액세스 추가\neksctl create iamidentitymapping \\\n  --cluster my-cluster \\\n  --arn arn:aws:iam::111122223333:role/AdminRole \\\n  --group system:masters \\\n  --username admin\n\n# IAM 매핑 조회\neksctl get iamidentitymapping --cluster my-cluster\n\n# IAM 매핑 삭제\neksctl delete iamidentitymapping \\\n  --cluster my-cluster \\\n  --arn arn:aws:iam::111122223333:role/AdminRole</div>", unsafe_allow_html=True)
            
        elif eksctl_category == "애드온 관리":
            st.markdown("<div class='command-title'>EKS 애드온 관리</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>EKS 애드온을 설치하고 관리하는 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'># 사용 가능한 애드온 버전 조회\neksctl utils describe-addon-versions --cluster my-cluster\n\n# 애드온 생성\neksctl create addon \\\n  --cluster my-cluster \\\n  --name vpc-cni \\\n  --version latest\n\n# 애드온 생성 (서비스 계정 지정)\neksctl create addon \\\n  --cluster my-cluster \\\n  --name aws-load-balancer-controller \\\n  --service-account-role-arn arn:aws:iam::111122223333:role/AWSLoadBalancerControllerIAMRole\n\n# 애드온 목록 조회\neksctl get addon --cluster my-cluster\n\n# 애드온 상세 정보 조회\neksctl describe addon \\\n  --cluster my-cluster \\\n  --name vpc-cni</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-title'>애드온 업데이트 & 삭제</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>EKS 애드온을 업데이트하고 삭제하는 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'># 애드온 업데이트\neksctl update addon \\\n  --cluster my-cluster \\\n  --name vpc-cni \\\n  --version latest\n\n# 애드온 업데이트 (충돌 정책 지정)\neksctl update addon \\\n  --cluster my-cluster \\\n  --name vpc-cni \\\n  --version latest \\\n  --force \\\n  --config-file <(echo '{\"resolveConflicts\":\"OVERWRITE\"}')\n\n# 애드온 삭제\neksctl delete addon \\\n  --cluster my-cluster \\\n  --name vpc-cni\n\n# 임시 자격 증명으로 작업\neksctl utils write-kubeconfig --cluster my-cluster --authenticator-role arn:aws:iam::111122223333:role/EksAdminRole</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-title'>고급 클러스터 유틸리티</div>", unsafe_allow_html=True)
            st.markdown("<div class='command-description'>다양한 EKS 유틸리티 명령어입니다.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='command-block'># 클러스터 스택 상세 정보\neksctl utils describe-stacks --cluster my-cluster\n\n# 클러스터 VPC 정보 확인\neksctl utils describe-vpc --cluster my-cluster\n\n# 클러스터 kubeconfig 업데이트\neksctl utils update-kube-proxy --cluster my-cluster\neksctl utils update-coredns --cluster my-cluster\neksctl utils update-aws-node --cluster my-cluster\n\n# 클러스터 엔드포인트 액세스 설정\neksctl utils update-cluster-endpoints \\\n  --cluster my-cluster \\\n  --private-access=true \\\n  --public-access=false</div>", unsafe_allow_html=True)

def render_resources_tab():
    """학습 자료 탭 렌더링"""
    
    st.markdown("<h3 style='font-size: 1.2rem;'>Kubernetes & EKS 학습 리소스</h3>", unsafe_allow_html=True)
    st.markdown("다양한 학습 자료와 참고 문서로 Kubernetes와 Docker 기술을 마스터하세요.", unsafe_allow_html=True)
    
    # 리소스 카테고리별 탭
    resource_tabs = st.tabs(["공식 문서", "튜토리얼", "설계 패턴", "도구 & 유틸리티"])
    
    # 공식 문서 탭
    with resource_tabs[0]:
        st.markdown("<div class='section-title'>공식 문서 및 레퍼런스</div>", unsafe_allow_html=True)
        
        docs_cols = st.columns(2)
        
        with docs_cols[0]:
            st.markdown("""
            <div class="hub-card">
                <div class="hub-card-header">
                    <div class="hub-card-icon">📘</div>
                    <h3 class="hub-card-title">Kubernetes 공식 문서</h3>
                </div>
                <div class="hub-card-body">
                    <p class="hub-card-description">Kubernetes 공식 문서는 개념, 튜토리얼 및 레퍼런스를 포함합니다.</p>
                    <ul>
                        <li>Kubernetes 기본 개념</li>
                        <li>API 레퍼런스</li>
                        <li>클러스터 관리 가이드</li>
                        <li>워크로드 관리</li>
                    </ul>
                    <a href="https://kubernetes.io/docs/home/" target="_blank">바로가기 →</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with docs_cols[1]:
            st.markdown("""
            <div class="hub-card">
                <div class="hub-card-header">
                    <div class="hub-card-icon">🐳</div>
                    <h3 class="hub-card-title">Docker 공식 문서</h3>
                </div>
                <div class="hub-card-body">
                    <p class="hub-card-description">Docker 설치부터 고급 사용법까지 다루는 공식 문서입니다.</p>
                    <ul>
                        <li>Docker 엔진 가이드</li>
                        <li>Dockerfile 레퍼런스</li>
                        <li>Docker CLI 명령어</li>
                        <li>Docker Compose 가이드</li>
                    </ul>
                    <a href="https://docs.docker.com/" target="_blank">바로가기 →</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # 새로운 행 추가
        docs_cols2 = st.columns(2)
        
        with docs_cols2[0]:
            st.markdown("""
            <div class="hub-card">
                <div class="hub-card-header">
                    <div class="hub-card-icon">☁️</div>
                    <h3 class="hub-card-title">AWS EKS 문서</h3>
                </div>
                <div class="hub-card-body">
                    <p class="hub-card-description">AWS EKS(Elastic Kubernetes Service) 공식 문서입니다.</p>
                    <ul>
                        <li>EKS 시작하기</li>
                        <li>클러스터 관리</li>
                        <li>노드 관리</li>
                        <li>보안 및 네트워킹</li>
                    </ul>
                    <a href="https://docs.aws.amazon.com/eks/" target="_blank">바로가기 →</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with docs_cols2[1]:
            st.markdown("""
            <div class="hub-card">
                <div class="hub-card-header">
                    <div class="hub-card-icon">🔧</div>
                    <h3 class="hub-card-title">kubectl 명령어 레퍼런스</h3>
                </div>
                <div class="hub-card-body">
                    <p class="hub-card-description">kubectl 명령어 공식 레퍼런스 가이드입니다.</p>
                    <ul>
                        <li>kubectl 설치 및 설정</li>
                        <li>상세 명령어 가이드</li>
                        <li>JSONPath 사용법</li>
                        <li>kubectl 플러그인</li>
                    </ul>
                    <a href="https://kubernetes.io/docs/reference/kubectl/" target="_blank">바로가기 →</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # 튜토리얼 탭
    with resource_tabs[1]:
        st.markdown("<div class='section-title'>단계별 튜토리얼</div>", unsafe_allow_html=True)
        
        tutorial_cols = st.columns(2)
        
        with tutorial_cols[0]:
            st.markdown("""
            <div class="hub-card">
                <div class="hub-card-header">
                    <div class="hub-card-icon">🎓</div>
                    <h3 class="hub-card-title">Kubernetes 기초 튜토리얼</h3>
                </div>
                <div class="hub-card-body">
                    <p class="hub-card-description">Kubernetes 입문자를 위한 단계별 가이드입니다.</p>
                    <ol>
                        <li>첫 번째 애플리케이션 배포</li>
                        <li>기본 kubectl 명령어 마스터하기</li>
                        <li>서비스와 네트워킹 이해하기</li>
                        <li>상태 관리 및 영구 스토리지</li>
                    </ol>
                    <a href="https://kubernetes.io/docs/tutorials/kubernetes-basics/" target="_blank">튜토리얼 시작하기 →</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with tutorial_cols[1]:
            st.markdown("""
            <div class="hub-card">
                <div class="hub-card-header">
                    <div class="hub-card-icon">☁️</div>
                    <h3 class="hub-card-title">AWS EKS 워크숍</h3>
                </div>
                <div class="hub-card-body">
                    <p class="hub-card-description">AWS EKS를 처음부터 배우는 실습 워크숍입니다.</p>
                    <ol>
                        <li>EKS 클러스터 생성 및 설정</li>
                        <li>애플리케이션 배포 관리</li>
                        <li>HPA 및 오토스케일링</li>
                        <li>로깅 및 모니터링</li>
                    </ol>
                    <a href="https://www.eksworkshop.com/" target="_blank">워크숍 시작하기 →</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        tutorial_cols2 = st.columns(2)
        
        with tutorial_cols2[0]:
            st.markdown("""
            <div class="hub-card">
                <div class="hub-card-header">
                    <div class="hub-card-icon">🐳</div>
                    <h3 class="hub-card-title">Docker 핸즈온 실습</h3>
                </div>
                <div class="hub-card-body">
                    <p class="hub-card-description">Docker를 실습으로 배우는 가이드입니다.</p>
                    <ol>
                        <li>첫 번째 컨테이너 실행</li>
                        <li>Dockerfile 작성하기</li>
                        <li>Docker Compose로 멀티 컨테이너 앱 배포</li>
                        <li>볼륨 및 네트워킹</li>
                    </ol>
                    <a href="https://docs.docker.com/get-started/" target="_blank">실습 시작하기 →</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with tutorial_cols2[1]:
            st.markdown("""
            <div class="hub-card">
                <div class="hub-card-header">
                    <div class="hub-card-icon">🔐</div>
                    <h3 class="hub-card-title">Kubernetes 보안 튜토리얼</h3>
                </div>
                <div class="hub-card-body">
                    <p class="hub-card-description">Kubernetes 환경 보안에 관한 모범 사례와 튜토리얼입니다.</p>
                    <ol>
                        <li>RBAC 설정하기</li>
                        <li>네트워크 정책 구현</li>
                        <li>시크릿 관리</li>
                        <li>파드 보안 컨텍스트 설정</li>
                    </ol>
                    <a href="https://kubernetes.io/docs/tutorials/clusters/security/" target="_blank">보안 튜토리얼 →</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # 설계 패턴 탭
    with resource_tabs[2]:
        st.markdown("<div class='section-title'>Kubernetes 설계 패턴</div>", unsafe_allow_html=True)
        
        pattern_cols = st.columns(2)
        
        with pattern_cols[0]:
            st.markdown("""
            <div class="hub-card">
                <div class="hub-card-header">
                    <div class="hub-card-icon">🏗️</div>
                    <h3 class="hub-card-title">마이크로서비스 아키텍처</h3>
                </div>
                <div class="hub-card-body">
                    <p class="hub-card-description">Kubernetes에서 마이크로서비스 설계 및 구현 패턴입니다.</p>
                    <ul>
                        <li>서비스 분리 및 통신</li>
                        <li>API 게이트웨이 패턴</li>
                        <li>서비스 메시 구현</li>
                        <li>분산 추적과 모니터링</li>
                    </ul>
                    <a href="https://microservices.io/patterns/microservices.html" target="_blank">자세히 보기 →</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with pattern_cols[1]:
            st.markdown("""
            <div class="hub-card">
                <div class="hub-card-header">
                    <div class="hub-card-icon">🔄</div>
                    <h3 class="hub-card-title">사이드카 패턴</h3>
                </div>
                <div class="hub-card-body">
                    <p class="hub-card-description">메인 애플리케이션 컨테이너와 함께 실행되는 헬퍼 컨테이너 패턴입니다.</p>
                    <ul>
                        <li>로깅 및 모니터링 사이드카</li>
                        <li>프록시 사이드카</li>
                        <li>설정 리로드 사이드카</li>
                        <li>Istio와 서비스 메시</li>
                    </ul>
                    <a href="https://kubernetes.io/blog/2015/06/the-distributed-system-toolkit-patterns/" target="_blank">자세히 보기 →</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        pattern_cols2 = st.columns(2)
        
        with pattern_cols2[0]:
            st.markdown("""
            <div class="hub-card">
                <div class="hub-card-header">
                    <div class="hub-card-icon">🚀</div>
                    <h3 class="hub-card-title">배포 전략</h3>
                </div>
                <div class="hub-card-body">
                    <p class="hub-card-description">Kubernetes에서 다양한 배포 전략 패턴입니다.</p>
                    <ul>
                        <li>롤링 업데이트</li>
                        <li>블루/그린 배포</li>
                        <li>카나리 배포</li>
                        <li>A/B 테스팅</li>
                    </ul>
                    <a href="https://kubernetes.io/docs/concepts/workloads/controllers/deployment/" target="_blank">자세히 보기 →</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with pattern_cols2[1]:
            st.markdown("""
            <div class="hub-card">
                <div class="hub-card-header">
                    <div class="hub-card-icon">⚖️</div>
                    <h3 class="hub-card-title">상태 관리 패턴</h3>
                </div>
                <div class="hub-card-body">
                    <p class="hub-card-description">Kubernetes에서 상태 관리를 위한 패턴입니다.</p>
                    <ul>
                        <li>StatefulSet 사용 패턴</li>
                        <li>외부 스토리지 통합</li>
                        <li>연산자 패턴</li>
                        <li>백업 및 복구 전략</li>
                    </ul>
                    <a href="https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/" target="_blank">자세히 보기 →</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # 도구 & 유틸리티 탭
    with resource_tabs[3]:
        st.markdown("<div class='section-title'>유용한 도구 & 유틸리티</div>", unsafe_allow_html=True)
        
        tools_cols = st.columns(2)
        
        with tools_cols[0]:
            st.markdown("""
            <div class="hub-card">
                <div class="hub-card-header">
                    <div class="hub-card-icon">📊</div>
                    <h3 class="hub-card-title">Prometheus & Grafana</h3>
                </div>
                <div class="hub-card-body">
                    <p class="hub-card-description">Kubernetes 클러스터 모니터링 및 지표 시각화 도구입니다.</p>
                    <ul>
                        <li>실시간 메트릭 수집</li>
                        <li>커스텀 대시보드</li>
                        <li>알림 설정</li>
                        <li>시계열 분석</li>
                    </ul>
                    <a href="https://prometheus.io/" target="_blank">Prometheus 웹사이트 →</a><br>
                    <a href="https://grafana.com/" target="_blank">Grafana 웹사이트 →</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with tools_cols[1]:
            st.markdown("""
            <div class="hub-card">
                <div class="hub-card-header">
                    <div class="hub-card-icon">⛵</div>
                    <h3 class="hub-card-title">Helm</h3>
                </div>
                <div class="hub-card-body">
                    <p class="hub-card-description">Kubernetes 패키지 관리자로, 애플리케이션 배포를 간소화합니다.</p>
                    <ul>
                        <li>차트 기반 템플릿</li>
                        <li>버전 관리</li>
                        <li>릴리스 히스토리</li>
                        <li>커스텀 값 설정</li>
                    </ul>
                    <a href="https://helm.sh/" target="_blank">Helm 웹사이트 →</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        tools_cols2 = st.columns(2)
        
        with tools_cols2[0]:
            st.markdown("""
            <div class="hub-card">
                <div class="hub-card-header">
                    <div class="hub-card-icon">🔍</div>
                    <h3 class="hub-card-title">Lens</h3>
                </div>
                <div class="hub-card-body">
                    <p class="hub-card-description">Kubernetes 대시보드 및 관리 도구입니다.</p>
                    <ul>
                        <li>멀티 클러스터 관리</li>
                        <li>리소스 시각화</li>
                        <li>실시간 로그 뷰어</li>
                        <li>쿠버네티스 내비게이터</li>
                    </ul>
                    <a href="https://k8slens.dev/" target="_blank">Lens 웹사이트 →</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with tools_cols2[1]:
            st.markdown("""
            <div class="hub-card">
                <div class="hub-card-header">
                    <div class="hub-card-icon">🔒</div>
                    <h3 class="hub-card-title">Kube-bench</h3>
                </div>
                <div class="hub-card-body">
                    <p class="hub-card-description">CIS Kubernetes 벤치마크 테스트 자동화 도구입니다.</p>
                    <ul>
                        <li>보안 설정 검사</li>
                        <li>컴플라이언스 점검</li>
                        <li>취약점 평가</li>
                        <li>보안 강화 가이드</li>
                    </ul>
                    <a href="https://github.com/aquasecurity/kube-bench" target="_blank">Kube-bench 깃허브 →</a>
                </div>
            </div>
            """, unsafe_allow_html=True)

# def generate_dummy_pdf_content():
#     """PDF 더미 콘텐츠 생성"""
#     # 실제 구현에서는 reportlab을 사용하여 PDF를 생성합니다.
#     # 여기서는 간단히 더미 데이터를 반환합니다.
#     return b"Dummy PDF content"

def generate_dummy_pdf_content(title="Kubernetes Cheatsheet", content_type="kubectl"):
    """
    ReportLab을 사용하여 PDF 치트시트를 생성합니다.
    (한글 지원을 위한 설정 추가)
    """
    buffer = BytesIO()
    
    # PDF 문서 생성
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=A4,
        rightMargin=72, 
        leftMargin=72,
        topMargin=72, 
        bottomMargin=72
    )
    
    # 스타일 정의
    styles = getSampleStyleSheet()
    
    # 한글 폰트 사용을 위한 설정
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    
    # 내장 폰트 사용 (영어만 지원)
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        textColor=colors.HexColor("#FF1493"),
        spaceAfter=16,
        alignment=1  # 중앙 정렬
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor("#FF1493"),
        spaceAfter=12
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        leading=14
    )
    
    code_style = ParagraphStyle(
        'Code',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=9,
        leftIndent=12,
        rightIndent=12,
        spaceAfter=6,
        backColor=colors.HexColor("#F8F9FA")
    )
    
    # 날짜 정보
    from datetime import datetime
    today_date = datetime.now().strftime("%Y-%m-%d")
    
    # 콘텐츠 구성
    content = []
    
    # 영문 제목으로 변경
    english_title = {
        "kubectl": "Kubernetes kubectl Commands",
        "docker": "Docker Commands",
        "aws": "AWS CLI Commands",
        "eksctl": "eksctl Commands"
    }.get(content_type, title)
    
    # 제목 추가
    content.append(Paragraph(english_title, title_style))
    content.append(Spacer(1, 12))
    
    # 소개 추가
    content.append(Paragraph("Generated: " + today_date, styles["Italic"]))
    content.append(Spacer(1, 20))
    
    # 영문 내용으로 구성
    if content_type == "kubectl":
        content.append(Paragraph("Basic Commands", subtitle_style))
        content.append(Spacer(1, 6))
        
        commands = [
            ("kubectl get pods", "Get all pods"),
            ("kubectl get svc", "Get all services"),
            ("kubectl get all", "Get all resources"),
            ("kubectl describe pod <pod-name>", "Show pod details"),
            ("kubectl logs <pod-name>", "Show pod logs"),
            ("kubectl exec -it <pod-name> -- /bin/bash", "Open shell in pod"),
            ("kubectl apply -f <file.yaml>", "Create or update resource"),
            ("kubectl delete -f <file.yaml>", "Delete resource"),
            ("kubectl scale deployment <name> --replicas=3", "Scale deployment")
        ]
        
        # 테이블 데이터 추가
        data = [["Command", "Description"]]
        for cmd, desc in commands:
            data.append([cmd, desc])
        
        # 테이블 스타일 정의 및 테이블 생성 (이전과 동일)
        # ...
        
    # 나머지 콘텐츠 타입에 대한 설정도 영문으로 변경
    # ...
    
    # PDF 생성
    doc.build(content)
    buffer.seek(0)
    
    return buffer.getvalue()

    # 코드 에디터 (편집 모드에 따라 다르게 표시)
    current_template = ""
    if st.session_state.current_file_type == "kubernetes":
        current_template = st.session_state.yaml_template
        
        if st.session_state.edit_mode:
            try:
                # 최신 Streamlit 버전에서는 code_editor 사용
                st.session_state.yaml_template = st.code_editor(
                    current_template,
                    lang="yaml",
                    height=400,
                    key="yaml_editor"
                )
            except:
                # 구버전에서는 text_area 사용
                st.session_state.yaml_template = st.text_area(
                    "YAML 편집",
                    value=current_template,
                    height=400,
                    key="yaml_editor",
                    help="Kubernetes YAML 템플릿을 편집하세요."
                )
        else:
            st.code(current_template, language="yaml", line_numbers=True)
    else:
        current_template = st.session_state.dockerfile_template
        
        if st.session_state.edit_mode:
            try:
                # 최신 Streamlit 버전에서는 code_editor 사용
                st.session_state.dockerfile_template = st.code_editor(
                    current_template,
                    lang="dockerfile",
                    height=400,
                    key="dockerfile_editor"
                )
            except:
                # 구버전에서는 text_area 사용
                st.session_state.dockerfile_template = st.text_area(
                    "Dockerfile 편집",
                    value=current_template,
                    height=400,
                    key="dockerfile_editor",
                    help="Dockerfile 템플릿을 편집하세요."
                )
        else:
            st.code(current_template, language="dockerfile", line_numbers=True)

# 리소스 시각화 탭 부분 개선
def render_resource_visualization(tab3):
    """리소스 시각화 탭 내용 렌더링"""
    
    with tab3:
        # CSS 스타일 강화
        st.markdown("""
        <style>
        .resource-box {
            background-color: white;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        
        .resource-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 10px;
        }
        
        .resource-icon {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background-color: #FF1493;
            color: white;
            font-weight: bold;
            font-size: 16px;
        }
        
        .resource-title {
            font-weight: 600;
            color: #343a40;
            font-size: 1.1rem;
        }
        
        .resource-details {
            margin-top: 8px;
            padding-left: 48px;
        }
        
        .resource-details p {
            margin: 5px 0;
            color: #495057;
        }
        
        .resource-arrow {
            text-align: center;
            margin: 15px 0;
            color: #6c757d;
            font-size: 20px;
        }
        
        .docker-layer {
            background-color: white;
            border: 1px solid #dee2e6;
            border-radius: 4px;
            margin-bottom: 8px;
            padding: 10px 12px;
            display: flex;
            justify-content: space-between;
            font-family: monospace;
            font-size: 0.9rem;
        }
        
        .layer-content {
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            color: #212529;
        }
        
        .layer-size {
            color: #6c757d;
            font-size: 0.8rem;
            min-width: 70px;
            text-align: right;
        }
        
        /* 리소스별 색상 */
        .pod-color { background-color: #4361ee; }
        .svc-color { background-color: #3a0ca3; }
        .deploy-color { background-color: #7209b7; }
        .rs-color { background-color: #f72585; }
        .ing-color { background-color: #4cc9f0; }
        .cm-color { background-color: #4d908e; }
        .secret-color { background-color: #277da1; }
        </style>
        """, unsafe_allow_html=True)
        
        if st.session_state.current_file_type == "kubernetes" and st.session_state.yaml_template:
            try:
                yaml_dict = yaml.safe_load(st.session_state.yaml_template)
                if not yaml_dict:
                    st.info("YAML이 비어 있습니다. 유효한 리소스 정의를 입력하세요.")
                    return
                
                if "kind" not in yaml_dict:
                    st.warning("리소스 종류(kind)가 정의되지 않았습니다.")
                    return
                
                kind = yaml_dict.get("kind", "")
                name = yaml_dict.get("metadata", {}).get("name", "미정의")
                
                st.markdown("<h4>리소스 시각화</h4>", unsafe_allow_html=True)
                
                # 리소스 유형별 시각화 (확장된 버전)
                if kind == "Pod":
                    containers = yaml_dict.get("spec", {}).get("containers", [])
                    container_count = len(containers)
                    container_names = [c.get("name", f"container-{i+1}") for i, c in enumerate(containers)]
                    
                    st.markdown(f"""
                    <div class="resource-box">
                        <div class="resource-header">
                            <div class="resource-icon pod-color">P</div>
                            <div class="resource-title">Pod: {name}</div>
                        </div>
                        <div class="resource-details">
                            <p><strong>컨테이너 수:</strong> {container_count}</p>
                            <p><strong>컨테이너:</strong> {', '.join(container_names)}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                elif kind == "Service":
                    service_type = yaml_dict.get("spec", {}).get("type", "ClusterIP")
                    ports = yaml_dict.get("spec", {}).get("ports", [])
                    port_info = []
                    for p in ports:
                        port = p.get("port", "")
                        target_port = p.get("targetPort", "")
                        port_info.append(f"{port}→{target_port}")
                    
                    selectors = yaml_dict.get("spec", {}).get("selector", {})
                    selectors_str = ", ".join([f"{k}={v}" for k, v in selectors.items()]) if selectors else "없음"
                    
                    st.markdown(f"""
                    <div class="resource-box">
                        <div class="resource-header">
                            <div class="resource-icon svc-color">S</div>
                            <div class="resource-title">Service: {name}</div>
                        </div>
                        <div class="resource-details">
                            <p><strong>타입:</strong> {service_type}</p>
                            <p><strong>포트:</strong> {', '.join(port_info) if port_info else '정의되지 않음'}</p>
                            <p><strong>셀렉터:</strong> {selectors_str}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 연결된 Pod 표시
                    if selectors:
                        st.markdown('<div class="resource-arrow">↓ 셀렉터 대상</div>', unsafe_allow_html=True)
                        st.markdown(f"""
                        <div class="resource-box">
                            <div class="resource-header">
                                <div class="resource-icon pod-color">P</div>
                                <div class="resource-title">Pods with labels: {selectors_str}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                elif kind in ["Deployment", "StatefulSet", "DaemonSet", "ReplicaSet"]:
                    replicas = yaml_dict.get("spec", {}).get("replicas", 1) if kind != "DaemonSet" else "노드당 1개"
                    selectors = yaml_dict.get("spec", {}).get("selector", {}).get("matchLabels", {})
                    selectors_str = ", ".join([f"{k}={v}" for k, v in selectors.items()]) if selectors else "없음"
                    
                    # 아이콘 결정
                    icon = {
                        "Deployment": "D",
                        "StatefulSet": "S",
                        "DaemonSet": "DS",
                        "ReplicaSet": "RS"
                    }.get(kind, kind[0])
                    
                    color_class = {
                        "Deployment": "deploy-color",
                        "StatefulSet": "deploy-color",
                        "DaemonSet": "deploy-color",
                        "ReplicaSet": "rs-color"
                    }.get(kind, "")
                    
                    st.markdown(f"""
                    <div class="resource-box">
                        <div class="resource-header">
                            <div class="resource-icon {color_class}">{icon}</div>
                            <div class="resource-title">{kind}: {name}</div>
                        </div>
                        <div class="resource-details">
                            <p><strong>레플리카:</strong> {replicas}</p>
                            <p><strong>셀렉터:</strong> {selectors_str}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # ReplicaSet 표시 (Deployment인 경우)
                    if kind == "Deployment":
                        st.markdown('<div class="resource-arrow">↓ 관리</div>', unsafe_allow_html=True)
                        st.markdown(f"""
                        <div class="resource-box">
                            <div class="resource-header">
                                <div class="resource-icon rs-color">RS</div>
                                <div class="resource-title">ReplicaSet: {name}-xxxxx</div>
                            </div>
                            <div class="resource-details">
                                <p><strong>레플리카:</strong> {replicas}</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Pod 표시
                    st.markdown('<div class="resource-arrow">↓ 관리</div>', unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="resource-box">
                        <div class="resource-header">
                            <div class="resource-icon pod-color">P</div>
                            <div class="resource-title">Pods</div>
                        </div>
                        <div class="resource-details">
                            <p><strong>레이블:</strong> {selectors_str}</p>
                            <p><strong>총 Pod 수:</strong> {replicas}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                elif kind == "Ingress":
                    rules = yaml_dict.get("spec", {}).get("rules", [])
                    rule_info = []
                    for rule in rules:
                        host = rule.get("host", "*")
                        paths = rule.get("http", {}).get("paths", [])
                        for path in paths:
                            path_type = path.get("pathType", "Prefix")
                            path_value = path.get("path", "/")
                            service = path.get("backend", {}).get("service", {})
                            service_name = service.get("name", "unknown")
                            port = service.get("port", {}).get("number", "unknown")
                            rule_info.append(f"{host}{path_value} → {service_name}:{port}")
                    
                    st.markdown(f"""
                    <div class="resource-box">
                        <div class="resource-header">
                            <div class="resource-icon ing-color">I</div>
                            <div class="resource-title">Ingress: {name}</div>
                        </div>
                        <div class="resource-details">
                            <p><strong>규칙 수:</strong> {len(rules)}</p>
                            {"".join([f"<p>{info}</p>" for info in rule_info]) if rule_info else "<p>규칙이 없습니다.</p>"}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 서비스 연결 표시
                    if rule_info:
                        st.markdown('<div class="resource-arrow">↓ 라우팅</div>', unsafe_allow_html=True)
                        for rule in rules:
                            paths = rule.get("http", {}).get("paths", [])
                            for path in paths:
                                service = path.get("backend", {}).get("service", {})
                                service_name = service.get("name", "unknown")
                                st.markdown(f"""
                                <div class="resource-box">
                                    <div class="resource-header">
                                        <div class="resource-icon svc-color">S</div>
                                        <div class="resource-title">Service: {service_name}</div>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                
                elif kind == "ConfigMap":
                    data = yaml_dict.get("data", {})
                    data_count = len(data)
                    data_keys = list(data.keys())
                    
                    st.markdown(f"""
                    <div class="resource-box">
                        <div class="resource-header">
                            <div class="resource-icon cm-color">CM</div>
                            <div class="resource-title">ConfigMap: {name}</div>
                        </div>
                        <div class="resource-details">
                            <p><strong>데이터 항목 수:</strong> {data_count}</p>
                            <p><strong>키:</strong> {', '.join(data_keys) if data_keys else '없음'}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                elif kind == "Secret":
                    data = yaml_dict.get("data", {})
                    data_count = len(data)
                    data_keys = list(data.keys())
                    secret_type = yaml_dict.get("type", "Opaque")
                    
                    st.markdown(f"""
                    <div class="resource-box">
                        <div class="resource-header">
                            <div class="resource-icon secret-color">SC</div>
                            <div class="resource-title">Secret: {name}</div>
                        </div>
                        <div class="resource-details">
                            <p><strong>타입:</strong> {secret_type}</p>
                            <p><strong>데이터 항목 수:</strong> {data_count}</p>
                            <p><strong>키:</strong> {', '.join(data_keys) if data_keys else '없음'}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                else:
                    # 기타 리소스 유형에 대한 일반 시각화
                    st.markdown(f"""
                    <div class="resource-box">
                        <div class="resource-header">
                            <div class="resource-icon">{kind[0]}</div>
                            <div class="resource-title">{kind}: {name}</div>
                        </div>
                        <div class="resource-details">
                            <p>이 리소스 유형에 대한 상세 시각화는 아직 지원되지 않습니다.</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            except ParserError as e:
                st.error(f"YAML 파싱 오류: {str(e)}")
            except Exception as e:
                st.error(f"리소스 시각화 중 오류 발생: {str(e)}")
                st.info("유효한 YAML을 먼저 로드하거나 작성하세요.")
        
        elif st.session_state.current_file_type == "dockerfile" and st.session_state.dockerfile_template:
            st.markdown("<h4>Dockerfile 구조 시각화</h4>", unsafe_allow_html=True)
            
            try:
                # Dockerfile 명령어 추출
                lines = st.session_state.dockerfile_template.split('\n')
                layer_cmds = [line.strip() for line in lines if line.strip() and not line.strip().startswith('#')]
                
                if layer_cmds:
                    # 명령어 유형 카운트
                    cmd_types = {}
                    for cmd in layer_cmds:
                        cmd_type = cmd.split(' ')[0] if ' ' in cmd else cmd
                        cmd_types[cmd_type] = cmd_types.get(cmd_type, 0) + 1
                    
                    # 기본 통계 표시
                    st.markdown("<p>Dockerfile 구성 요약:</p>", unsafe_allow_html=True)
                    stats_md = ", ".join([f"{k}: {v}" for k, v in cmd_types.items()])
                    st.markdown(f"<p style='margin-bottom:15px;'>{stats_md}</p>", unsafe_allow_html=True)
                    
                    st.markdown("<p>Docker 레이어 구조:</p>", unsafe_allow_html=True)
                    
                    # 레이어를 유발하는 명령어 목록
                    layer_instructions = ["FROM", "RUN", "COPY", "ADD"]
                    layer_count = 1
                    
                    for i, cmd in enumerate(layer_cmds):
                        cmd_parts = cmd.split(' ', 1)
                        instruction = cmd_parts[0] if cmd_parts else ""
                        
                        # 명령어에 따라 다른 색상 적용
                        color = "#FF1493"  # 기본 핑크
                        if instruction == "FROM":
                            color = "#3a0ca3"  # 보라색
                        elif instruction == "RUN":
                            color = "#4361ee"  # 파란색
                        elif instruction in ["COPY", "ADD"]:
                            color = "#4cc9f0"  # 밝은 파란색
                        
                        # 레이어를 생성하는 명령어인 경우
                        if instruction in layer_instructions:
                            st.markdown(f"""
                            <div class="docker-layer">
                                <div class="layer-content">
                                    <span style="color:{color};font-weight:bold;">{instruction}</span> 
                                    {cmd_parts[1] if len(cmd_parts) > 1 else ""}
                                </div>
                                <div class="layer-size">Layer {layer_count}</div>
                            </div>
                            """, unsafe_allow_html=True)
                            layer_count += 1
                        else:
                            # 레이어를 생성하지 않는 명령어
                            st.markdown(f"""
                            <div class="docker-layer" style="border-style:dashed;background-color:#f8f9fa;">
                                <div class="layer-content">
                                    <span style="color:{color};font-weight:bold;">{instruction}</span> 
                                    {cmd_parts[1] if len(cmd_parts) > 1 else ""}
                                </div>
                                <div class="layer-size">No layer</div>
                            </div>
                            """, unsafe_allow_html=True)
                
                else:
                    st.info("Dockerfile 내용이 비어있거나 주석만 있습니다.")
            
            except Exception as e:
                st.error(f"Dockerfile 시각화 중 오류 발생: {str(e)}")
                st.info("유효한 Dockerfile을 먼저 로드하거나 작성하세요.")
        
        else:
            # 파일 유형이 선택되지 않았거나 내용이 없는 경우
            st.info("시각화할 YAML 또는 Dockerfile을 먼저 로드하거나 작성하세요.")
            
            # 시각화 예시 표시
            with st.expander("리소스 시각화 예시 보기"):
                st.markdown("""
                <div style="text-align:center;padding:15px;">
                    <p>다양한 Kubernetes 리소스 시각화 예시:</p>
                    <img src="https://d33wubrfki0l68.cloudfront.net/2475489eaf20163ec261dce4b77a1f867de9025f/e7c81/images/docs/components-of-kubernetes.svg" style="max-width:100%; margin-top:10px;">
                </div>
                """, unsafe_allow_html=True)