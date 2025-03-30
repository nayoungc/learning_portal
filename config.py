import os
from enum import Enum


class Config:
    """애플리케이션 전체 설정을 관리하는 클래스"""

    # 앱 기본 설정
    APP_TITLE = "AWS EKS & Kubernetes Learning Portal"
    APP_ICON = "🚀 "
    APP_DESCRIPTION = "AWS EKS와 Kubernetes 학습 및 실습을 위한 포털"

    # 지원 언어
    class Language(Enum):
        EN = "English"
        KO = "한국어"

    # AWS 설정
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    
    # Bedrock 설정
    BEDROCK_MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"
    BEDROCK_KB_ID = os.getenv("KB_ID", "")
    BEDROCK_AGENT_ID = os.getenv("AGENT_ID", "")
    BEDROCK_AGENT_ALIAS_ID = os.getenv("AGENT_ALIAS_ID", "")
    BEDROCK_FLOW_ID = os.getenv("FLOW_ID", "")
    BEDROCK_GUARDRAIL_ID = os.getenv("GUARDRAIL_ID", "")

    # DynamoDB 설정
    DYNAMODB_CHAT_TABLE = "eks-kubernetes-learning-chatlog"
    DYNAMODB_ANALYTICS_TABLE = "eks-kubernetes-learning-analytics"

    # 학습 경로 설정
    class LearningPath(Enum):
        BEGINNER = "beginner"
        INTERMEDIATE = "intermediate"
        ADVANCED = "advanced"

    # 시각화 설정
    MINDMAP_LEVELS = 3  # 마인드맵에 표시할 단계 수
    
    # 마인드맵 유형
    class MindMapType(Enum):
        KUBERNETES = "kubernetes_concepts"
        EKS = "eks_architecture"
        DEVOPS = "devops_tools"

    # UI 설정
    DEFAULT_CHAT_WIDTH = 0.35  # 채팅 패널 기본 너비 (비율)
    DEFAULT_CHAT_VISIBLE = True  # 채팅 패널 기본 표시 여부
    DEBUG_MODE = True  # 디버깅 정보 표시

    # 색상 테마
    COLOR_BEGINNER = "#4285F4"     # 파란색
    COLOR_INTERMEDIATE = "#FBBC04"  # 노란색
    COLOR_ADVANCED = "#EA4335"     # 빨간색
    COLOR_KUBERNETES = "#326CE5"   # 쿠버네티스 로고 색
    COLOR_AWS = "#FF9900"          # AWS 주요 색상

    # 앱 경로
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(ROOT_DIR, "data")
    CONTENT_DIR = os.path.join(DATA_DIR, "content")
    YAML_TEMPLATES_DIR = os.path.join(DATA_DIR, "yaml_templates")
    KUBECTL_EXAMPLES_DIR = os.path.join(DATA_DIR, "kubectl_examples")
    EKS_SPECIFIC_DIR = os.path.join(DATA_DIR, "eks_specific")
    GITOPS_DIR = os.path.join(DATA_DIR, "gitops")
    MINDMAP_DATA_DIR = os.path.join(DATA_DIR, "mindmap_data")
    I18N_DIR = os.path.join(DATA_DIR, "i18n")
    IMAGES_DIR = os.path.join(DATA_DIR, "images")
