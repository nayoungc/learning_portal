import boto3
import json
import os
import streamlit as st
from datetime import datetime
from config import Config


class UsageTracker:
    """사용자 활동 추적 및 분석 서비스"""
    
    @staticmethod
    def initialize_dynamodb():
        """DynamoDB 클라이언트 초기화"""
        try:
            return boto3.resource('dynamodb', region_name=Config.AWS_REGION)
        except Exception as e:
            if Config.DEBUG_MODE:
                st.error(f"DynamoDB 클라이언트 초기화 오류: {str(e)}")
            return None
    
    @staticmethod
    def track_page_view(page_id, user_id=None):
        """페이지 조회 기록"""
        try:
            # 환경에 따라 저장 방식 선택
            if os.environ.get("LOCAL_DEVELOPMENT", "true").lower() == "true":
                UsageTracker._track_local(event_type="page_view", page_id=page_id)
            else:
                UsageTracker._track_dynamodb(event_type="page_view", page_id=page_id, user_id=user_id)
        except Exception as e:
            if Config.DEBUG_MODE:
                st.error(f"페이지 조회 추적 오류: {str(e)}")
    
    @staticmethod
    def track_search(query, page_id=None, user_id=None):
        """검색 기록"""
        try:
            data = {
                "query": query,
                "page_id": page_id
            }
            
            # 환경에 따라 저장 방식 선택
            if os.environ.get("LOCAL_DEVELOPMENT", "true").lower() == "true":
                UsageTracker._track_local(event_type="search", **data)
            else:
                UsageTracker._track_dynamodb(event_type="search", user_id=user_id, **data)
        except Exception as e:
            if Config.DEBUG_MODE:
                st.error(f"검색 추적 오류: {str(e)}")
    
    @staticmethod
    def track_chat_message(message, role, page_id=None, user_id=None):
        """채팅 메시지 기록"""
        try:
            data = {
                "role": role,
                "message_length": len(message),
                "page_id": page_id
            }
            
            # 환경에 따라 저장 방식 선택
            if os.environ.get("LOCAL_DEVELOPMENT", "true").lower() == "true":
                UsageTracker._track_local(event_type="chat_message", **data)
            else:
                UsageTracker._track_dynamodb(event_type="chat_message", user_id=user_id, **data)
        except Exception as e:
            if Config.DEBUG_MODE:
                st.error(f"채팅 메시지 추적 오류: {str(e)}")
    
    @staticmethod
    def _track_local(event_type, **data):
        """로컬 세션에 활동 기록"""
        if 'analytics' not in st.session_state:
            st.session_state.analytics = []
        
        event_data = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            **data
        }
        
        st.session_state.analytics.append(event_data)
    
    @staticmethod
    def _track_dynamodb(event_type, user_id=None, **data):
        """DynamoDB에 활동 기록"""
        try:
            dynamodb = UsageTracker.initialize_dynamodb()
            if not dynamodb:
                return
            
            # 테이블 가져오기
            table = dynamodb.Table(Config.DYNAMODB_ANALYTICS_TABLE)
            
            # 항목 생성
            timestamp = datetime.now().isoformat()
            item = {
                "id": f"{user_id or 'anonymous'}_{timestamp}",
                "timestamp": timestamp,
                "event_type": event_type,
                **data
            }
            
            # DynamoDB에 저장
            table.put_item(Item=item)
            
        except Exception as e:
            if Config.DEBUG_MODE:
                st.error(f"DynamoDB 추적 오류: {str(e)}")
    
    @staticmethod
    def get_analytics_data(event_type=None, limit=100):
        """분석 데이터 가져오기"""
        try:
            # 로컬 개발 환경에서는 세션 상태에서 가져옴
            if os.environ.get("LOCAL_DEVELOPMENT", "true").lower() == "true":
                if 'analytics' not in st.session_state:
                    return []
                
                data = st.session_state.analytics
                if event_type:
                    data = [item for item in data if item.get('event_type') == event_type]
                
                return sorted(data, key=lambda x: x.get('timestamp', ''), reverse=True)[:limit]
            
            # 프로덕션 환경에서는 DynamoDB에서 가져옴
            else:
                dynamodb = UsageTracker.initialize_dynamodb()
                if not dynamodb:
                    return []
                
                table = dynamodb.Table(Config.DYNAMODB_ANALYTICS_TABLE)
                
                if event_type:
                    # 특정 이벤트 타입 필터링
                    result = table.scan(
                        FilterExpression="event_type = :event_type",
                        ExpressionAttributeValues={":event_type": event_type},
                        Limit=limit
                    )
                else:
                    # 전체 데이터
                    result = table.scan(Limit=limit)
                
                return sorted(result.get('Items', []), key=lambda x: x.get('timestamp', ''), reverse=True)
                
        except Exception as e:
            if Config.DEBUG_MODE:
                st.error(f"분석 데이터 가져오기 오류: {str(e)}")
            return []
