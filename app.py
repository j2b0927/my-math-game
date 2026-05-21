import streamlit as st
import random
import time

# 페이지 설정
st.set_page_config(page_title="말랑말랑 레벨업 수학", page_icon="🎨", layout="centered")

# --- [모바일 고정형 & 와이드 키패드 CSS] ---
st.markdown("""
<style>
    /* 스크롤 절대 방지 및 높이 고정 */
    html, body, [data-testid="stAppViewContainer"] {
        max-height: 100vh !important;
        overflow: hidden !important;
        height: 100vh !important;
    }
    
    .stApp {
        background: linear-gradient(-45deg, #FAF8F1, #FFE0F0, #E6E6FA, #FFE0F0);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .block-container {
        padding: 0.5rem 0.8rem !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: flex-start !important;
        height: 100vh !important;
    }
    
    [data-testid="stVerticalBlock"] { gap: 0.1rem !important; }
    hr { margin: 0.2rem 0 !important; opacity: 0.3; }
    
    h1 { color: #554488; font-size: 1.2rem !important; text-align: center; margin: 0 !important; }
    
    /* 점수판 슬림화 */
    .score-box { 
        background-color: white; padding: 4px 8px; border-radius: 10px; 
        border: 1.5px solid #FFC0CB; text-align: center; margin: 0.2rem auto !important;
        width: 85%;
    }
    .score-box h2 { font-size: 0.9rem !important; margin: 0 !important; color: #CC4488; font-weight: bold; }

    /* 문제 수식 압축 */
    .quiz-text {
        color: #6644AA; font-size: 2.3rem !important; font-weight: bold;
        text-align: center; margin: 0.1rem 0 !important;
    }

    /* 캐릭터 및 5개 주머니 크기 최적화 */
    .five-group {
        display: inline-flex; background-color: rgba(255, 255, 255, 0.6);
        padding: 2px 4px; border-radius: 8px; margin: 1px 2px; border: 1px dashed #FFB6C1;
    }
    .char-img { width: 22px !important; height: 22px !important; margin: 1px; }
    .hint-title { font-size: 0.75rem !important; font-weight: bold; color: #4466AA; margin: 0 !important; text-align: center; }

    /* 정답 모니터 창 */
    .ans-display {
        background-color: #F0F9FF; border: 2px solid #7DD3FC; border-radius: 10px;
        padding: 4px; text-align: center; font-size: 1.5rem !important;
        font-weight: bold; color: #0369A1; min-height: 40px; margin: 0.3rem auto !important;
        width: 80%;
    }

    /* --- [와이드 키패드 버튼 디자인] --- */
    div[data-testid="column"] button {
        background-color: #FEF08A !important; /* 파스텔 노랑 */
        color: #854D0E !important;
        border: 1.5px solid #FDE047 !important;
        border-radius: 8px !important;
        font-size: 1rem !important;
        font-weight: bold !important;
        height: 45px !important; /* 가로로 길어지므로 높이는 약간 확보 */
        padding: 0 !important;
        width: 100% !important;
    }
    /* 지우기(C) 버튼: 빨강 계열 */
    div.clear-btn button { background-color: #FECACA !important; color: #991B1B !important; border-color: #FCA5A5 !important; }
    /* 확인(OK) 버튼: 초록 계열 */
    div.ok-btn button { background-color: #BBF7D0 !important; color: #166534 !important; border-color: #86EFAC !important; }
    
    /* 버튼 내부 텍스트 위치 조정 */
    button p { margin: 0 !important; line-height: 45px !important; }
</style>
""", unsafe_allow_html=True)

# 캐릭터 설정
CHARACTER_URLS = {
    "bunny": "https://cdn-icons-png.flaticon.com/512/3261/3261168.png", 
    "bear": "https://cdn-icons-png.flaticon.com/512/1000/1000966.png",  
    "apple": "https://cdn-icons-png.flaticon.com/512/2909/2909787.png", 
    "berry": "https://cdn-icons-png.flaticon.com/512/2316/2316886.png", 
    "cat": "https://cdn-icons-png.flaticon.com/512/616/616430.png"     
}
CHAR_KEYS = list(CHARACTER_URLS.keys())

# 상태 관리
if "score" not in st.session_state: st.session_state.score = 0
if "needs_new_question