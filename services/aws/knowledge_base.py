import boto3
import json
import os
import streamlit as st
from config import Config


class KnowledgeBaseService:
    """AWS Bedrock Knowledge Base 서비스"""
    
    @staticmethod
    def initialize():
        """Knowledge Base 클라이언트 초기화"""
        try:
            # Bedrock Agent 클라이언트 초기화
            return boto3.client('bedrock-agent-runtime', region_name=Config.AWS_REGION)
        except Exception as e:
            st.error(f"Knowledge Base 클라이언트 초기화 오류: {str(e)}")
            return None
    
    @staticmethod
    def query_knowledge_base(query, kb_id=None, max_results=5):
        """Knowledge Base에 쿼리 보내기"""
        try:
            # 지정된 KB ID가 없으면 설정에서 가져오기
            kb_id = kb_id or Config.BEDROCK_KB_ID
            
            if not kb_id:
                return {
                    "error": "Knowledge Base ID가 설정되지 않았습니다.",
                    "results": []
                }
            
            # 시뮬레이션 모드 체크
            if os.environ.get("SIMULATION_MODE", "false").lower() == "true":
                return KnowledgeBaseService._simulate_kb_response(query)
            
            # 클라이언트 초기화
            client = KnowledgeBaseService.initialize()
            
            # Knowledge Base 쿼리
            response = client.retrieve(
                knowledgeBaseId=kb_id,
                retrievalQuery={
                    'text': query
                },
                retrievalConfiguration={
                    'vectorSearchConfiguration': {
                        'numberOfResults': max_results
                    }
                }
            )
            
            # 결과 처리
            results = []
            for result in response.get('retrievalResults', []):
                for document in result.get('content', {}).get('text', {}).get('documents', []):
                    results.append({
                        "content": document.get('text'),
                        "location": document.get('location', ''),
                        "score": result.get('score', 0)
                    })
            
            return {
                "success": True,
                "results": results
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "results": []
            }
    
    @staticmethod
    def _simulate_kb_response(query):
        """Knowledge Base 응답 시뮬레이션"""
        # EKS/K8s 관련 키워드 체크
        eks_keywords = ["eks", "elastic kubernetes service"]
        k8s_keywords = ["kubernetes", "쿠버네티스", "pod", "deployment"]
        aws_keywords = ["aws", "amazon", "iam", "ec2", "vpc"]
        
        if any(keyword in query.lower() for keyword in eks_keywords):
            # EKS 관련 시뮬레이션 응답
            return {
                "success": True,
                "results": [
                    {
                        "content": "Amazon EKS(Elastic Kubernetes Service)는 AWS에서 자체 Kubernetes 컨트롤 플레인을 설치, 운영 및 유지 관리할 필요 없이 AWS에서 Kubernetes를 쉽게 실행할 수 있게 해주는 관리형 서비스입니다.",
                        "location": "eks_overview.md",
                        "score": 0.95
                    },
                    {
                        "content": "EKS 클러스터는 eksctl 명령줄 도구를 사용하여 쉽게 생성할 수 있습니다. 기본 명령어는 'eksctl create cluster'입니다.",
                        "location": "eks_cluster_creation.md",
                        "score": 0.87
                    },
                    {
                        "content": "Amazon EKS는 IAM을 사용하여 Kubernetes 클러스터에 인증을 제공합니다. 이를 통해 AWS IAM 자격 증명을 사용하여 Kubernetes 클러스터에 대한 액세스를 제어할 수 있습니다.",
                        "location": "eks_iam_integration.md",
                        "score": 0.82
                    }
                ]
            }
        elif any(keyword in query.lower() for keyword in k8s_keywords):
            # Kubernetes 관련 시뮬레이션 응답
            return {
                "success": True,
                "results": [
                    {
                        "content": "Kubernetes는 컨테이너화된 애플리케이션의 자동 배포, 스케일링 및 관리를 위한 오픈소스 시스템입니다.",
                        "location": "kubernetes_intro.md",
                        "score": 0.92
                    },
                    {
                        "content": "Pod는 쿠버네티스에서 생성하고 관리할 수 있는 배포 가능한 가장 작은 컴퓨팅 단위입니다. 하나 이상의 컨테이너 그룹으로 구성됩니다.",
                        "location": "kubernetes_pods.md",
                        "score": 0.89
                    },
                    {
                        "content": "Deployment는 Pod와 ReplicaSet에 대한 선언적 업데이트를 제공합니다. Deployment에서 원하는 상태를 설명하면 Deployment 컨트롤러가 제어된 속도로 현재 상태에서 원하는 상태로 변경합니다.",
                        "location": "kubernetes_deployments.md",
                        "score": 0.85
                    }
                ]
            }
        elif any(keyword in query.lower() for keyword in aws_keywords):
            # AWS 관련 시뮬레이션 응답
            return {
                "success": True,
                "results": [
                    {
                        "content": "AWS IAM(Identity and Access Management)은 AWS 리소스에 대한 액세스를 안전하게 제어할 수 있는 웹 서비스입니다.",
                        "location": "aws_iam.md",
                        "score": 0.91
                    },
                    {
                        "content": "Amazon VPC를 사용하면 논리적으로 격리된 AWS 클라우드의 가상 네트워크에서 AWS 리소스를 시작할 수 있습니다.",
                        "location": "aws_vpc.md",
                        "score": 0.88
                    }
                ]
            }
        else:
            # 일반 시뮬레이션 응답
            return {
                "success": True,
                "results": [
                    {
                        "content": "시뮬레이션 지식 베이스 응답입니다. 실제 서비스에서는 질의에 맞는 정보를 반환합니다.",
                        "location": "simulation.md",
                        "score": 0.80
                    }
                ]
            }
