import streamlit as st
import pandas as pd
from utils.localization import t
from components.visualizations.chart_components import render_bar_chart, render_pie_chart, render_line_chart
from datetime import datetime, timedelta
from services.analytics.usage_tracker import UsageTracker
import random


def render_analytics():
    """분석 차트 페이지 렌더링"""
    # 사용 추적
    UsageTracker.track_page_view("analytics")
    
    st.title(t("analytics"))
    
    st.markdown("""
    <div style="background-color: #f0f7ff; padding: 12px; border-radius: 8px; 
         border-left: 4px solid #326CE5; margin-bottom: 20px;">
        <p style="margin: 0; font-size: 0.95rem;">
            이 페이지에서는 학습 콘텐츠 사용 현황과 인기 주제를 시각적으로 분석합니다.
            데이터를 통해 학습 경향을 파악하고 관심 분야를 발견해보세요.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 데모 데이터 생성 함수 (실제로는 서비스에서 데이터를 가져올 것)
    def generate_demo_data():
        # 현재 날짜에서 30일 전 날짜 계산
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        # 날짜 범위 생성
        dates = [start_date + timedelta(days=x) for x in range(31)]
        dates = [d.strftime("%Y-%m-%d") for d in dates]
        
        # 주제 목록
        topics = [
            "EKS 클러스터 생성", 
            "Kubernetes Pod", 
            "Kubernetes Service", 
            "YAML 템플릿",
            "kubectl 명령어",
            "Helm 차트",
            "GitOps",
            "CI/CD 파이프라인",
            "모니터링",
            "네트워크 정책"
        ]
        
        # 데이터 생성
        data = []
        
        # 날짜별 토픽별 질문 수 생성
        for date in dates:
            for topic in topics:
                count = random.randint(5, 50)  # 랜덤 질문 수
                difficulty = random.choice(["초급", "중급", "고급"])
                data.append({
                    "date": date,
                    "topic": topic,
                    "count": count,
                    "difficulty": difficulty,
                    "avg_satisfaction": round(random.uniform(3.0, 5.0), 1)  # 1~5 사이의 만족도
                })
        
        return pd.DataFrame(data)
    
    # 데모 데이터 생성
    df = generate_demo_data()
    
    # 기간 선택
    st.sidebar.subheader("필터 옵션")
    
    time_filter = st.sidebar.selectbox(
        "기간 선택",
        ["지난 7일", "지난 14일", "지난 30일", "전체 기간"],
        index=2
    )
    
    # 기간에 따른 필터링
    if time_filter == "지난 7일":
        df = df[df["date"] >= (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")]
    elif time_filter == "지난 14일":
        df = df[df["date"] >= (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d")]
    elif time_filter == "지난 30일":
        df = df[df["date"] >= (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")]
    
    # 주제별 필터
    topics = list(df["topic"].unique())
    selected_topics = st.sidebar.multiselect("주제 선택", topics, default=topics[:5])
    
    if selected_topics:
        df = df[df["topic"].isin(selected_topics)]
    
    # 탭 생성
    tab1, tab2, tab3 = st.tabs(["주제별 분석", "난이도별 분석", "시간대별 추이"])
    
    with tab1:
        st.subheader("가장 많이 조회된 주제")
        
        # 주제별 조회 수 집계
        topic_counts = df.groupby("topic")["count"].sum().reset_index()
        topic_counts = topic_counts.sort_values("count", ascending=False)
        
        # 막대 차트
        render_bar_chart(
            topic_counts, 
            x="topic", 
            y="count", 
            title="주제별 조회 수",
            color="topic"
        )
        
        # 주제별 평균 만족도
        topic_satisfaction = df.groupby("topic")["avg_satisfaction"].mean().reset_index()
        topic_satisfaction = topic_satisfaction.sort_values("avg_satisfaction", ascending=False)
        
        render_bar_chart(
            topic_satisfaction, 
            x="topic", 
            y="avg_satisfaction", 
            title="주제별 평균 만족도 (5점 만점)",
            color="topic"
        )
    
    with tab2:
        st.subheader("난이도별 조회 분석")
        
        # 난이도별 조회 수
        difficulty_counts = df.groupby("difficulty")["count"].sum().reset_index()
        
        render_pie_chart(
            difficulty_counts,
            values="count",
            names="difficulty",
            title="난이도별 조회 비율"
        )
        
        # 난이도와 주제 교차 분석
        difficulty_topic = df.groupby(["difficulty", "topic"])["count"].sum().reset_index()
        
        render_bar_chart(
            difficulty_topic, 
            x="topic", 
            y="count", 
            title="주제별 난이도 분포",
            color="difficulty"
        )
    
    with tab3:
        st.subheader("시간대별 조회 추이")
        
        # 날짜별 조회 수 집계
        time_counts = df.groupby("date")["count"].sum().reset_index()
        
        render_line_chart(
            time_counts, 
            x="date", 
            y="count",
            title="일별 총 조회 수"
        )
        
        # 주제별 시간 추이
        selected_topic = st.selectbox("주제 선택", topics)
        topic_time_data = df[df["topic"] == selected_topic]
        
        topic_time = topic_time_data.groupby("date")["count"].sum().reset_index()
        
        render_line_chart(
            topic_time, 
            x="date", 
            y="count",
            title=f"{selected_topic} 주제의 일별 조회 수"
        )
    
    # 인사이트 섹션
    st.subheader("주요 인사이트")
    
    # 가장 많이 조회된 주제 top 3 추출
    top_topics = topic_counts.head(3)["topic"].tolist()
    
    st.markdown(f"""
    #### 인기 주제
    
    현재 데이터 분석에 따르면 가장 관심이 많은 주제는 다음과 같습니다:
    
    1. **{top_topics[0]}**: 전체 조회의 약 {random.randint(15, 25)}%를 차지합니다.
    2. **{top_topics[1]}**: 전체 조회의 약 {random.randint(10, 15)}%를 차지합니다.
    3. **{top_topics[2]}**: 전체 조회의 약 {random.randint(8, 12)}%를 차지합니다.
    
    #### 학습 경향
    
    - 초급 내용의 조회가 전체의 약 {random.randint(35, 55)}%를 차지하여 많은 사용자가 기초 학습을 진행 중입니다.
    - 시간이 지남에 따라 중급 및 고급 내용 조회가 점진적으로 증가하는 추세입니다.
    - 주말에는 평일에 비해 약 {random.randint(20, 40)}% 낮은 조회율을 보입니다.
    """)
