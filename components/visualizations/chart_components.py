import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.localization import t
import pandas as pd
import numpy as np


def render_bar_chart(data, x, y, title, color=None, height=400):
    """막대 차트 렌더링 컴포넌트"""
    fig = px.bar(
        data, 
        x=x, 
        y=y, 
        color=color,
        title=title,
        height=height
    )
    
    # 테마에 맞게 차트 스타일 조정
    if st.session_state.theme_mode == "dark":
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(30,30,30,0.3)',
            font_color='#E0E0E0'
        )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


def render_pie_chart(data, values, names, title, height=400):
    """파이 차트 렌더링 컴포넌트"""
    fig = px.pie(
        data,
        values=values,
        names=names,
        title=title,
        height=height
    )
    
    # 테마에 맞게 차트 스타일 조정
    if st.session_state.theme_mode == "dark":
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#E0E0E0'
        )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


def render_line_chart(data, x, y, title, color=None, height=400):
    """선 차트 렌더링 컴포넌트"""
    fig = px.line(
        data,
        x=x,
        y=y,
        color=color,
        title=title,
        height=height,
        markers=True
    )
    
    # 테마에 맞게 차트 스타일 조정
    if st.session_state.theme_mode == "dark":
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(30,30,30,0.3)',
            font_color='#E0E0E0'
        )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


def render_heatmap(data, title, height=400):
    """히트맵 렌더링 컴포넌트"""
    fig = px.imshow(
        data,
        title=title,
        height=height,
        color_continuous_scale="Viridis"
    )
    
    # 테마에 맞게 차트 스타일 조정
    if st.session_state.theme_mode == "dark":
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#E0E0E0'
        )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
