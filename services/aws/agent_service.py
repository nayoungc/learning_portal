import boto3
import json
import os
import streamlit as st
from datetime import datetime
from config import Config


class AgentService:
    """AWS Bedrock Agent 서비스"""
    
    @staticmethod
    def initialize():
        """Agent 클라이언트 초기화"""
        try:
            # Bedrock Agent 클라이언트 초기화
            return boto3.client('bedrock-agent-runtime', region_name=Config.AWS_REGION)
        except Exception as e:
            st.error(f"Agent 클라이언트 초기화 오류: {str(e)}")
            return None
    
    @staticmethod
    def invoke_agent(prompt, session_id=None, agent_id=None, agent_alias_id=None):
        """Agent 호출"""
        try:
            # Agent ID와 Alias ID가 없으면 설정에서 가져오기
            agent_id = agent_id or Config.BEDROCK_AGENT_ID
            agent_alias_id = agent_alias_id or Config.BEDROCK_AGENT_ALIAS_ID
            
            # 세션 ID가 없으면 생성
            if not session_id:
                session_id = f"session-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            if not agent_id or not agent_alias_id:
                return "Agent ID 또는 Agent Alias ID가 설정되지 않았습니다."
            
            # 시뮬레이션 모드 체크
            if os.environ.get("SIMULATION_MODE", "false").lower() == "true":
                return AgentService._simulate_agent_response(prompt)
            
            # 클라이언트 초기화
            client = AgentService.initialize()
            
            # Agent 호출
            response = client.invoke_agent(
                agentId=agent_id,
                agentAliasId=agent_alias_id,
                sessionId=session_id,
                inputText=prompt
            )
            
            # 응답 처리
            result = ""
            completion = response.get("completion", None)
            
            if completion:
                chunks = completion.get("chunks", [])
                for chunk in chunks:
                    if "bytes" in chunk:
                        result += chunk["bytes"].decode('utf-8')
            
            return result
            
        except Exception as e:
            # 오류 발생 시 디버그 정보 기록
            if 'debug_info' not in st.session_state:
                st.session_state.debug_info = []
                
            st.session_state.debug_info.append({
                "timestamp": datetime.now().isoformat(),
                "info": f"Agent API 오류: {str(e)}"
            })
            
            # 오류 처리
            if os.environ.get("SIMULATION_MODE", "false").lower() == "true":
                return AgentService._simulate_agent_response(prompt, is_error=True)
            
            # 실제 오류 반환
            return f"죄송합니다. Agent 응답 생성 중 오류가 발생했습니다: {str(e)}"
    
    @staticmethod
    def _simulate_agent_response(prompt, is_error=False):
        """Agent 응답 시뮬레이션"""
        if is_error:
            return """
            ⚠  현재 Agent 연결이 불안정합니다. 시뮬레이션 응답을 제공합니다.
            
            실제 서비스 환경에서는 AWS Bedrock Agent를 통해 정확한 응답이 제공됩니다.
            """
        
        # 키워드에 따른 시뮬레이션 응답
        eks_keywords = ["eks", "elastic kubernetes service"]
        yaml_keywords = ["yaml", "템플릿", "template"]
        kubectl_keywords = ["kubectl", "명령어", "command"]
        
        if any(keyword in prompt.lower() for keyword in eks_keywords):
            return """
            Amazon EKS 클러스터를 생성하는 기본 단계입니다:

            1. **사전 요구 사항 설정**
               - AWS CLI 설치 및 구성
               - kubectl 설치
               - eksctl 설치

            2. **eksctl을 사용한 클러스터 생성**
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

            3. **클러스터 접근 확인**
            ```bash
            aws eks update-kubeconfig --name my-cluster --region us-east-1
            kubectl get nodes
            ```

            이 명령은 EKS 클러스터와 노드 그룹을 생성하고, 노드 수를 1에서 5 사이로 자동 조정하도록 설정합니다.
            """
        elif any(keyword in prompt.lower() for keyword in yaml_keywords):
            return """
            간단한 Nginx 애플리케이션을 위한 EKS Deployment 및 Service YAML 템플릿입니다:

            ```yaml
            # deployment.yaml
            apiVersion: apps/v1
            kind: Deployment
            metadata:
              name: nginx
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
                    image: nginx:1.21
                    ports:
                    - containerPort: 80
                    resources:
                      limits:
                        cpu: 500m
                        memory: 512Mi
                      requests:
                        cpu: 250m
                        memory: 256Mi
            ```

            ```yaml
            # service.yaml
            apiVersion: v1
            kind: Service
            metadata:
              name: nginx
              namespace: default
            spec:
              selector:
                app: nginx
              ports:
              - port: 80
                targetPort: 80
              type: LoadBalancer
            ```

            이 템플릿을 저장하고 다음 명령으로 적용할 수 있습니다:
            ```bash
            kubectl apply -f deployment.yaml
            kubectl apply -f service.yaml
            ```
            """
        elif any(keyword in prompt.lower() for keyword in kubectl_keywords):
            return """
            자주 사용하는 kubectl 명령어 모음입니다:

            **기본 명령어**:
            ```bash
            # 모든 리소스 확인
            kubectl get all --all-namespaces

            # 특정 네임스페이스의 파드 확인
            kubectl get pods -n kube-system

            # 파드 상세 정보 확인
            kubectl describe pod <pod-name>

            # 파드 로그 확인
            kubectl logs <pod-name>
            ```

            **리소스 생성 및 관리**:
            ```bash
            # YAML 파일로부터 리소스 생성
            kubectl apply -f <file.yaml>

            # 실행 중인 파드에 접속
            kubectl exec -it <pod-name> -- /bin/bash

            # 서비스 노출 (포트포워딩)
            kubectl port-forward svc/<service-name> 8080:80
            ```

            **트러블슈팅**:
            ```bash
            # 이벤트 확인
            kubectl get events --sort-by='.lastTimestamp'

            # 리소스 사용량 확인
            kubectl top nodes
            kubectl top pods -n <namespace>
            ```
            """
        else:
            return """
            안녕하세요! AWS EKS와 Kubernetes에 관한 질문에 도움을 드릴 수 있습니다.
            
            도움이 필요한 내용을 구체적으로 물어보시면 더 정확한 정보를 제공해 드리겠습니다.
            
            예를 들어 다음과 같은 주제에 대해 질문할 수 있습니다:
            
            - EKS 클러스터 생성 및 관리
            - Kubernetes 리소스 (Pod, Service, Deployment 등) 사용법
            - YAML 템플릿 작성 방법
            - 네트워킹 및 보안 설정
            - 트러블슈팅 가이드
            
            어떤 도움이 필요하신가요?
            
            (이것은 시뮬레이션된 응답입니다. 실제 서비스에서는 더 정확한 정보를 제공합니다.)
            """
