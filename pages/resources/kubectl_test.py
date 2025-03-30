import streamlit as st
from utils.localization import t
from services.analytics.usage_tracker import UsageTracker


def render_kubectl_test():
    """kubectl 명령어 테스트 페이지"""
    # 사용 추적
    UsageTracker.track_page_view("kubectl_test")
    
    st.title(t("kubectl_test"))
    
    st.markdown("""
    <div style="background-color: #f0f7ff; padding: 12px; border-radius: 8px; 
         border-left: 4px solid #326CE5; margin-bottom: 20px;">
        <p style="margin: 0; font-size: 0.95rem;">
            kubectl 명령어를 직접 실행하고 결과를 확인해보세요. 현재 클러스터에 연결된 상태에서 실행됩니다.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # kubectl 명령어 입력
    kubectl_cmd = st.text_input(
        "kubectl 명령어를 입력하세요", 
        value="kubectl version --client", 
        placeholder="예: kubectl get pods -n kube-system"
    )
    
    # 왼쪽에는 명령어 실행, 오른쪽에는 도움말
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # 실행 버튼
        if st.button("명령어 실행"):
            # 명령어 실행 시뮬레이션
            if "version" in kubectl_cmd:
                output = """CLIENT VERSION: v1.27.3\nKUBERNETES VERSION: v1.27"""
            elif "get pods" in kubectl_cmd:
                output = """NAME                  READY   STATUS    RESTARTS   AGE
nginx-abc123          1/1     Running   0          3d
backend-xyz456        1/1     Running   0          2d"""
            else:
                output = f"시뮬레이션 모드: {kubectl_cmd} 실행 (실제 실행되지 않음)"
                
            st.text_area("명령어 결과", value=output, height=200)
            st.success("명령어가 시뮬레이션 모드로 실행되었습니다.")
    
    with col2:
        st.markdown("### 자주 사용하는 명령어")
        
        with st.expander("기본 명령어", expanded=True):
            st.code("""
# 파드 목록 보기
kubectl get pods

# 특정 네임스페이스의 파드 보기
kubectl get pods -n kube-system

# 모든 네임스페이스의 파드 보기
kubectl get pods --all-namespaces
""")
        
        with st.expander("EKS 특화 명령어"):
            st.code("""
# EKS 클러스터 접근 설정
aws eks update-kubeconfig --name <cluster> --region <region>

# EKS 관리형 애드온 확인
kubectl get pods -n kube-system
""")
