import boto3
import json
import os
import streamlit as st
from datetime import datetime
from config import Config


class BedrockService:
    """AWS Bedrock 서비스를 위한 클래스"""
    
    @staticmethod
    def initialize():
        """Bedrock 클라이언트 초기화"""
        try:
            # AWS 자격 증명 가져오기 (환경 변수 또는 IAM 역할에서)
            return boto3.client('bedrock-runtime', region_name=Config.AWS_REGION)
        except Exception as e:
            st.error(f"Bedrock 클라이언트 초기화 오류: {str(e)}")
            return None
    
    @staticmethod
    def generate_response(prompt, system_instruction=None):
        """Bedrock 모델을 사용하여 응답 생성"""
        try:
            # 시스템 프롬프트 설정 (없으면 기본값 사용)
            if system_instruction is None:
                system_instruction = """
                당신은 AWS EKS와 쿠버네티스 전문가로, 클라우드 네이티브 기술에 대한 정확한 정보를 제공합니다.
                질문에 대해 깊이 있고 정확한 답변을 제공하며, 필요한 경우 YAML 예제나 명령어를 포함합니다.
                컨테이너화, 오케스트레이션, 클라우드 네이티브 아키텍처, 특히 AWS EKS에 관한 질문에 답변할 준비가 되었습니다.
                답변은 구체적이고 실용적이며, 가능한 경우 모범 사례와 실제 사용 사례를 포함해야 합니다.
                """
            
            # Bedrock 클라이언트 초기화
            client = BedrockService.initialize()
            
            # 시뮬레이션 모드 체크 (실제 API 호출 불가 환경을 위함)
            if os.environ.get("SIMULATION_MODE", "false").lower() == "true":
                return BedrockService._simulate_response(prompt)
            
            # 실제 API 요청 형식 구성
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1024,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "system": system_instruction
            }
            
            # 모델 호출
            response = client.invoke_model(
                modelId=Config.BEDROCK_MODEL_ID,
                body=json.dumps(request_body)
            )
            
            # 응답 처리
            response_body = json.loads(response['body'].read())
            return response_body['content'][0]['text']
            
        except Exception as e:
            # 디버그 정보 기록
            if 'debug_info' not in st.session_state:
                st.session_state.debug_info = []
                
            st.session_state.debug_info.append({
                "timestamp": datetime.now().isoformat(),
                "info": f"Bedrock API 오류: {str(e)}"
            })
            
            # 오류 처리
            if os.environ.get("SIMULATION_MODE", "false").lower() == "true":
                return BedrockService._simulate_response(prompt, is_error=True)
            
            # 실제 오류 반환
            return f"죄송합니다. 응답 생성 중 오류가 발생했습니다: {str(e)}"
    
    @staticmethod
    def _simulate_response(prompt, is_error=False):
        """실제 API 호출 없이 응답을 시뮬레이션 (테스트용)"""
        if is_error:
            return """
            ⚠  현재 API 연결이 불안정합니다. 시뮬레이션 응답을 제공합니다.
            
            실제 서비스 환경에서는 AWS Bedrock을 통해 정확한 응답이 제공됩니다.
            """
        
        # EKS/K8s 관련 키워드 체크
        k8s_keywords = ["kubernetes", "쿠버네티스", "pod", "파드", "deployment", "디플로이먼트", 
                       "eks", "서비스", "kubectl", "aws"]
        
        if any(keyword in prompt.lower() for keyword in k8s_keywords):
            return """
            **AWS EKS & Kubernetes 시뮬레이션 응답:**
            
            AWS EKS(Elastic Kubernetes Service)는 AWS에서 제공하는 관리형 쿠버네티스 서비스로, 
            컨테이너화된 애플리케이션의 배포와 관리를 간소화합니다.
            
            주요 특징:
            - **관리형 컨트롤 플레인**: AWS가 컨트롤 플레인을 관리하므로 운영 부담이 감소합니다.
            - **IAM 통합**: AWS IAM과 통합되어 보안 인증과 권한 부여를 간소화합니다.
            - **VPC 통합**: AWS VPC 내에서 클러스터를 배포하여 네트워크 격리와 보안을 강화합니다.
            - **노드 그룹**: 다양한 유형의 EC2 인스턴스 그룹으로 워크로드에 맞게 확장할 수 있습니다.
            
            EKS 클러스터 생성 예시 명령어:
            ```bash
            eksctl create cluster \
              --name my-cluster \
              --region us-east-1 \
              --nodegroup-name standard-workers \
              --node-type t3.medium \
              --nodes 3 \
              --nodes-min 1 \
              --nodes-max 5
            ```
            
            이 응답은 시뮬레이션된 것입니다. 실제 서비스에서는 더 정확하고 맞춤화된 응답을 제공합니다.
            """
        else:
            return """
            안녕하세요! AWS EKS(Elastic Kubernetes Service) 및 Kubernetes에 관한 질문이 있으신가요? 
            
            컨테이너 오케스트레이션, 클러스터 관리, 배포 전략, 마이크로서비스 아키텍처, 
            네트워킹, 스토리지, 보안 등 다양한 주제에 대해 도움을 드릴 수 있습니다.
            
            특정 질문이나 문제가 있으시면 편하게 물어보세요!
            
            이 응답은 시뮬레이션된 것입니다. 실제 서비스에서는 더 정확하고 맞춤화된 응답을 제공합니다.
            """
