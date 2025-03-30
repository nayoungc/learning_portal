import streamlit as st
from utils.localization import t
from services.analytics.usage_tracker import UsageTracker


def render_cheatsheets():
    """치트시트 페이지"""
    # 사용 추적
    UsageTracker.track_page_view("cheatsheets")
    
    st.title(t("cheatsheets"))
    
    st.markdown("""
    <div style="background-color: #f0f7ff; padding: 12px; border-radius: 8px; 
         border-left: 4px solid #326CE5; margin-bottom: 20px;">
        <p style="margin: 0; font-size: 0.95rem;">
            자주 사용하는 명령어와 패턴을 빠르게 찾아볼 수 있는 치트시트입니다.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 카테고리 탭
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "kubectl", "eksctl", "AWS CLI", "Docker CLI", "Helm"
    ])
    
    with tab1:
        st.subheader("kubectl 명령어 모음")
        
        with st.expander("기본 조회 명령어", expanded=True):
            st.code("""# 모든 파드 조회
kubectl get pods --all-namespaces

# 특정 네임스페이스의 모든 리소스 조회
kubectl get all -n <namespace>

# 파드 상세 정보
kubectl describe pod <pod-name> -n <namespace>

# 파드 로그 확인
kubectl logs <pod-name> -n <namespace>""")
            if st.button("복사", key="copy_kubectl"):
                st.toast("클립보드에 복사되었습니다!", icon="✓")
    
    with tab2:
        st.subheader("eksctl 명령어 모음")
        
        with st.expander("클러스터 관리", expanded=True):
            st.code("""# 클러스터 생성
eksctl create cluster --name=<cluster-name> --region=<region> --nodes=3

# 클러스터 삭제
eksctl delete cluster --name=<cluster-name> --region=<region>""")
            if st.button("복사", key="copy_eksctl"):
                st.toast("클립보드에 복사되었습니다!", icon="✓")
    
    with tab3:
        st.subheader("AWS CLI 명령어 모음")
        
        with st.expander("EKS 관련 명령어", expanded=True):
            st.code("""# EKS 클러스터 목록 확인
aws eks list-clusters --region <region>

# EKS 클러스터 설명
aws eks describe-cluster --name <cluster-name> --region <region>

# kubeconfig 업데이트
aws eks update-kubeconfig --name <cluster-name> --region <region>""")
            if st.button("복사", key="copy_aws"):
                st.toast("클립보드에 복사되었습니다!", icon="✓")
                
    with tab4:
        st.subheader("Docker CLI 명령어 모음")
        
        with st.expander("기본 명령어", expanded=True):
            st.code("""# 이미지 빌드
docker build -t <image-name>:<tag> .

# 컨테이너 실행
docker run -d -p 8080:80 <image-name>:<tag>

# 컨테이너 목록 확인 
docker ps""")
            if st.button("복사", key="copy_docker"):
                st.toast("클립보드에 복사되었습니다!", icon="✓")
                
    with tab5:
        st.subheader("Helm CLI 명령어 모음")
        
        with st.expander("기본 명령어", expanded=True):
            st.code("""# 차트 설치
helm install <release-name> <chart>

# 릴리스 목록 확인
helm list

# 차트 업그레이드
helm upgrade <release-name> <chart>

# 릴리스 삭제
helm uninstall <release-name>""")
            if st.button("복사", key="copy_helm"):
                st.toast("클립보드에 복사되었습니다!", icon="✓")
