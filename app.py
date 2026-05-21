import streamlit as st
import random
import time

# 페이지 기본 설정 (스마트폰 최적화)
st.set_page_config(page_title="말랑말랑 레벨업 수학", page_icon="🎨", layout="centered")

# --- [디자인 & 애니메이션 치트키] 파스텔톤, 움직이는 배경, 캐릭터 튕김 효과 ---
st.markdown("""
<style>
    /* 전체 배경: 은은하게 움직이는 파스텔 그라데이션 */
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
    
    /* [모바일 반응형] 휴대폰 화면 크기에 맞춰 글씨 크기 자동 조절 */
    html {
        font-size: calc(14px + 0.5vw);
    }
    
    h1 { color: #554488; font-family: 'sans-serif'; text-align: center; }
    h2 { color: #CC4488; text-align: center; }
    
    /* 점수판 디자인 */
    .score-box { 
        background-color: white; 
        padding: 15px; 
        border-radius: 20px; 
        border: 2px solid #FFC0CB; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); 
        text-align: center; 
        margin-bottom: 20px; 
    }

    /* 5개 단위로 묶어줄 주머니(그룹) 스타일 */
    .five-group {
        display: inline-flex;
        background-color: rgba(255, 255, 255, 0.6); /* 연한 흰색 바탕으로 5개 묶음 강조 */
        padding: 8px;
        border-radius: 15px;
        margin: 5px 10px; /* 5개 묶음끼리 약간 띄우기 */
        border: 1px dashed #FFB6C1;
    }

    /* [움직임 치트키] 손으로 누르거나 마우스를 대면 찡긋 웃고 통 튕기는 캐릭터 */
    .char-img {
        width: 40px;
        height: 40px;
        margin: 3px;
        transition: transform 0.2s ease-in-out;
        cursor: pointer;
    }
    .char-img:active, .char-img:hover {
        animation: bounceWink 0.4s ease;
        transform: scale(1.3); /* 누르면 조금 더 크게 튕김 */
    }
    @keyframes bounceWink {
        0% { transform: scale(1) rotate(0deg); }
        30% { transform: scale(1.3) rotate(-8deg); }
        70% { transform: scale(1.2) rotate(8deg); }
        100% { transform: scale(1) rotate(0deg); }
    }
</style>
""", unsafe_allow_html=True)

# --- [캐릭터 치트키] 말랑말랑한 고화질 아이콘 URL ---
CHARACTER_URLS = {
    "bunny": "https://cdn-icons-png.flaticon.com/512/3261/3261168.png", # 말랑토끼
    "bear": "https://cdn-icons-png.flaticon.com/512/1000/1000966.png",  # 말랑곰
    "apple": "https://cdn-icons-png.flaticon.com/512/2909/2909787.png", # 말랑사과
    "berry": "https://cdn-icons-png.flaticon.com/512/2316/2316886.png", # 말랑딸기
    "cat": "https://cdn-icons-png.flaticon.com/512/616/616430.png"     # 말랑고양이
}
CHAR_KEYS = list(CHARACTER_URLS.keys())

# 세션 상태 초기화
if "score" not in st.session_state: st.session_state.score = 0
if "needs_new_question" not in st.session_state: st.session_state.needs_new_question = True

def generate_question(game_mode, level):
    st.session_state.char_key = random.choice(CHAR_KEYS)
    
    if game_mode == "1. 덧셈, 뺄셈": op = random.choice(["+", "-"])
    else: op = random.choice(["+", "-", "×", "÷"])
    st.session_state.operator = op
    
    if op in ["+", "-"]:
        if level == "1단계 (초급)":
            if op == "+":
                n1 = random.randint(1, 10)
                n2 = random.randint(1, 10)
            else:
                n1 = random.randint(2, 20)
                n2 = random.randint(1, n1)
        elif level == "2단계 (중급)":
            if op == "+": n1, n2 = random.randint(1, 50), random.randint(1, 50)
            else: n1 = random.randint(1, 100); n2 = random.randint(1, n1)
        else:
            n1, n2 = random.randint(10, 500), random.randint(10, 500)
                
    elif op == "×":
        if level == "1단계 (초급)": n1, n2 = random.randint(1, 9), random.randint(1, 5)
        elif level == "2단계 (중급)": n1, n2 = random.randint(2, 19), random.randint(1, 10)
        else: n1, n2 = random.randint(10, 50), random.randint(2, 20)
            
    elif op == "÷":
        if level == "1단계 (초급)": n2 = random.randint(1, 5); ans = random.randint(1, 5); n1 = n2 * ans
        elif level == "2단계 (중급)": n2 = random.randint(2, 9); ans = random.randint(2, 10); n1 = n2 * ans
        else: n2 = random.randint(5, 20); ans = random.randint(5, 30); n1 = n2 * ans

    st.session_state.num1 = n1
    st.session_state.num2 = n2
    st.session_state.needs_new_question = False

# 사이드바 설정창
st.sidebar.markdown("<h2 style='color: #6644AA;'>⚙️ 게임 설정</h2>", unsafe_allow_html=True)
game_mode = st.sidebar.selectbox("연산 종류 선택", ["1. 덧셈, 뺄셈", "2. 덧셈, 뺄셈, 곱셈, 나눗셈"])
level = st.sidebar.selectbox("난이도 선택", ["1단계 (초급)", "2단계 (중급)", "3단계 (고급)"])

if st.sidebar.button("🎨 새로운 게임 시작하기") or st.session_state.needs_new_question:
    generate_question(game_mode, level)

# 메인 제목 및 점수판
st.markdown("<h1>🎨 말랑말랑 레벨업 수학</h1>", unsafe_allow_html=True)
st.markdown(f"""
<div class='score-box'>
    <h4 style='color: #EE6688; margin: 0;'>현재 설정: {game_mode} / {level}</h4>
    <h2 style='color: #CC4488; margin: 5px 0;'>✨ 내 점수: {st.session_state.score}점 ✨</h2>
</div>
""", unsafe_allow_html=True)

char_url = CHARACTER_URLS[st.session_state.char_key]
n1, n2, op = st.session_state.num1, st.session_state.num2, st.session_state.operator

if op == "+": correct = n1 + n2
elif op == "-": correct = n1 - n2
elif op == "×": correct = n1 * n2
elif op == "÷": correct = n1 // n2

# 문제 대형 표시
st.markdown("<h1 style='color: #6644AA; font-size: 3.8rem; text-align: center;'> %d %s %d = ? </h1>" % (n1, op, n2), unsafe_allow_html=True)
st.markdown("---")

# [핵심] 5개 단위로 정렬하여 화면에 그리는 함수 구현
def draw_five_grouped_images(total_count):
    if total_count <= 0:
        st.markdown("<p style='color:gray;'>0개</p>", unsafe_allow_html=True)
        return
        
    full_groups = total_count // 5
    remainder = total_count % 5
    
    html_result = "<div style='text-align: center;'>"
    
    # 5개짜리 묶음 주머니 만들기
    for _ in range(full_groups):
        html_result += "<div class='five-group'>"
        for _ in range(5):
            html_result += f'<img src="{char_url}" class="char-img" title="눌러봐요!">'
        html_result += "</div>"
        
    # 남은 자투리 주머니 만들기
    if remainder > 0:
        html_result += "<div class='five-group'>"
        for _ in range(remainder):
            html_result += f'<img src="{char_url}" class="char-img" title="눌러봐요!">'
        html_result += "</div>"
        
    html_result += "</div>"
    st.markdown(html_result, unsafe_allow_html=True)

# 1단계 초급에서만 5개 단위 정렬 및 터치 반응형 힌트 노출
if level == "1단계 (초급)":
    st.markdown("### 💡 말랑말랑 힌트 창 (그림을 터치하면 튕겨요!)")
    
    if op == "+":
        st.markdown(f"**앞의 숫자 ({n1}) 만큼:**")
        draw_five_grouped_images(n1)
        st.markdown(f"**뒤의 숫자 ({n2}) 만큼:**")
        draw_five_grouped_images(n2)
        
    elif op == "-":
        st.markdown(f"**전체 {n1}개 중에서 {n2}개를 손가락으로 가리고 세어보세요!**")
        draw_five_grouped_images(n1)
        
    elif op == "×":
        st.markdown(f"**{n1}개씩 {n2} 묶음이에요!**")
        for i in range(n2):
            st.markdown(f"📍 {i+1}번째 묶음 ({n1}개)")
            draw_five_grouped_images(n1)
            
    elif op == "÷":
        st.markdown(f"**전체 {n1}개를 {n2}명이 똑같이 나누어 가질 거예요.**")
        st.markdown(f"<div style='text-align:center;'><img src='{char_url}' style='width:70px; animation: bounceWink 1s infinite;'></div>", unsafe_allow_html=True)
    st.markdown("---")
else:
    st.markdown("<p style='text-align: center; color: #88AABB; font-size: 1.1rem;'>중급/고급 단계는 그림 힌트 없이 머릿속으로 계산해봐요! 💪</p>", unsafe_allow_html=True)
    st.markdown("---")

# 정답 입력칸
with st.form(key="game_form", clear_on_submit=True):
    st.markdown("### ✍️ 정답 적기")
    user_ans = st.number_input("", min_value=0, max_value=2000, step=1, value=0, label_visibility="collapsed")
    
    st.markdown("""
    <style>
        div.stButton > button:first-child {
            background-color: #55AADD; color: white; border-radius: 20px; border: none; font-weight: bold; width: 100%; padding: 10px;
        }
    </style>
    """, unsafe_allow_html=True)
    submit_btn = st.form_submit_button(label="정답 확인! 👍")

if submit_btn:
    if user_ans == correct:
        st.session_state.score += 10
        st.balloons()
        st.success(f"🎉 딩동댕! 정답이에요! [{n1} {op} {n2} = {correct}] 참 잘했어요! (+10점)")
        st.session_state.needs_new_question = True
        time.sleep(1)
        st.rerun()
    else:
        st.error("😮 조금만 더 생각해볼까요? 그림을 다시 차근차근 세어보세요!")