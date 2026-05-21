import streamlit as st
import random
import time

# 페이지 기본 설정
st.set_page_config(page_title="말랑말랑 레벨업 수학", page_icon="🎨", layout="centered")

# --- [디자인 & 키패드 스타일 최적화 CSS] ---
st.markdown("""
<style>
    /* 전체 배경 그라데이션 */
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
    
    /* 화면 여백 최소화하여 한 화면에 무조건 맞춤 */
    .block-container {
        padding: 0.8rem !important;
    }
    hr { margin: 0.4rem 0 !important; }
    h1 { color: #554488; font-size: 1.6rem !important; text-align: center; margin-bottom: 0.1rem !important; }
    
    /* 점수판 슬림화 */
    .score-box { 
        background-color: white; padding: 5px 10px; border-radius: 12px; 
        border: 2px solid #FFC0CB; text-align: center; margin-bottom: 0.3rem !important; 
    }
    .score-box h4 { font-size: 0.8rem !important; margin: 0 !important; }
    .score-box h2 { font-size: 1.1rem !important; margin: 2px 0 !important; color: #CC4488; }

    /* 대형 문제 수식 디자인 */
    .quiz-text {
        color: #6644AA; font-size: 2.5rem !important; font-weight: bold;
        text-align: center; margin: 0.2rem 0 !important;
    }

    /* 5개 단위 주머니 디자인 */
    .five-group {
        display: inline-flex; background-color: rgba(255, 255, 255, 0.6);
        padding: 3px 5px; border-radius: 10px; margin: 2px 4px; border: 1px dashed #FFB6C1;
    }
    .char-img { width: 28px !important; height: 28px !important; margin: 1px; transition: transform 0.2s; }
    .char-img:active { transform: scale(1.3); }
    .hint-title { font-size: 0.9rem !important; font-weight: bold; color: #4466AA; margin-bottom: 0.1rem !important; }

    /* [중요] 정답 디스플레이 박스 (장난감 모니터 느낌) */
    .ans-display {
        background-color: #E0F2FE; border: 3px solid #7DD3FC; border-radius: 15px;
        padding: 8px; text-align: center; font-size: 1.8rem !important;
        font-weight: bold; color: #0369A1; min-height: 50px; margin-bottom: 0.4rem;
    }
</style>
""", unsafe_allow_html=True)

# 캐릭터 아이콘 세팅
CHARACTER_URLS = {
    "bunny": "https://cdn-icons-png.flaticon.com/512/3261/3261168.png", 
    "bear": "https://cdn-icons-png.flaticon.com/512/1000/1000966.png",  
    "apple": "https://cdn-icons-png.flaticon.com/512/2909/2909787.png", 
    "berry": "https://cdn-icons-png.flaticon.com/512/2316/2316886.png", 
    "cat": "https://cdn-icons-png.flaticon.com/512/616/616430.png"     
}
CHAR_KEYS = list(CHARACTER_URLS.keys())

# 기억장치 관리 변수들
if "score" not in st.session_state: st.session_state.score = 0
if "needs_new_question" not in st.session_state: st.session_state.needs_new_question = True
if "input_buffer" not in st.session_state: st.session_state.input_buffer = "" # 현재 입력중인 글자 보관함

def generate_question(game_mode, level):
    st.session_state.char_key = random.choice(CHAR_KEYS)
    
    if game_mode == "1. 덧셈, 뺄셈": op = random.choice(["+", "-"])
    else: op = random.choice(["+", "-", "×", "÷"])
    st.session_state.operator = op
    
    if op in ["+", "-"]:
        if level == "1단계 (초급)":
            if op == "+": n1, n2 = random.randint(1, 10), random.randint(1, 10)
            else: n1 = random.randint(2, 20); n2 = random.randint(1, n1)
        elif level == "2단계 (중급)":
            if op == "+": n1, n2 = random.randint(1, 50), random.randint(1, 50)
            else: n1 = random.randint(1, 100); n2 = random.randint(1, n1)
        else: n1, n2 = random.randint(10, 500), random.randint(10, 500)
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
    st.session_state.input_buffer = "" # 입력창 완전 비우기

# 왼쪽 설정 사이드바
st.sidebar.markdown("<h2 style='color: #6644AA;'>⚙️ 게임 설정</h2>", unsafe_allow_html=True)
game_mode = st.sidebar.selectbox("연산 종류 선택", ["1. 덧셈, 뺄셈", "2. 덧셈, 뺄셈, 곱셈, 나눗셈"])
level = st.sidebar.selectbox("난이도 선택", ["1단계 (초급)", "2단계 (중급)", "3단계 (고급)"])

if st.sidebar.button("🎨 새로운 게임 시작하기") or st.session_state.needs_new_question:
    generate_question(game_mode, level)

# 상단 인터페이스
st.markdown("<h1>🎨 말랑말랑 수학</h1>", unsafe_allow_html=True)
st.markdown(f"<div class='score-box'><h4>{game_mode} / {level}</h4><h2>✨ 내 점수: {st.session_state.score}점 ✨</h2></div>", unsafe_allow_html=True)

char_url = CHARACTER_URLS[st.session_state.char_key]
n1, n2, op = st.session_state.num1, st.session_state.num2, st.session_state.operator

if op == "+": correct = n1 + n2
elif op == "-": correct = n1 - n2
elif op == "×": correct = n1 * n2
elif op == "÷": correct = n1 // n2

# 수식 노출
st.markdown(f"<div class='quiz-text'> {n1} {op} {n2} = ? </div>", unsafe_allow_html=True)
st.markdown("---")

# 5개 묶음 배치 힌트 시스템
def draw_five_grouped_images(total_count):
    if total_count <= 0:
        st.markdown("<p style='color:gray; text-align:center; margin:0;'>0개</p>", unsafe_allow_html=True)
        return
    full_groups = total_count // 5
    remainder = total_count % 5
    html_result = "<div style='text-align: center; margin: 0; padding: 0;'>"
    for _ in range(full_groups):
        html_result += "<div class='five-group'>"
        for _ in range(5): html_result += f'<img src="{char_url}" class="char-img">'
        html_result += "</div>"
    if remainder > 0:
        html_result += "<div class='five-group'>"
        for _ in range(remainder): html_result += f'<img src="{char_url}" class="char-img">'
        html_result += "</div>"
    html_result += "</div>"
    st.markdown(html_result, unsafe_allow_html=True)

if level == "1단계 (초급)":
    if op == "+":
        st.markdown("<div class='hint-title'>💡 힌트 (그림을 터치해봐요!)</div>", unsafe_allow_html=True)
        draw_five_grouped_images(n1)
        st.markdown("<div style='text-align:center; font-size:1rem; margin:1px 0;'>➕</div>", unsafe_allow_html=True)
        draw_five_grouped_images(n2)
    elif op == "-":
        st.markdown(f"<div class='hint-title'>💡 전체 {n1}개 중 {n2}개를 손가락으로 지워보세요!</div>", unsafe_allow_html=True)
        draw_five_grouped_images(n1)
    elif op == "×":
        st.markdown(f"<div class='hint-title'>💡 {n1}개씩 {n2} 묶음</div>", unsafe_allow_html=True)
        for _ in range(n2): draw_five_grouped_images(n1)
    elif op == "÷":
        st.markdown(f"<div class='hint-title'>💡 {n1}개를 {n2}명이 똑같이 나눠요.</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:center;'><img src='{char_url}' style='width:35px;'></div>", unsafe_allow_html=True)
    st.markdown("---")
else:
    st.markdown("<p style='text-align: center; color: #88AABB; margin:0; font-size:0.85rem;'>중급/고급은 머릿속으로 계산해요! 💪</p>", unsafe_allow_html=True)
    st.markdown("---")

# --- [이번 업그레이드의 핵심: 전용 숫자 키패드 UI 및 로직] ---

# 1. 내가 입력한 숫자가 실시간으로 보여지는 장난감 화면창 (비어있으면 물음표 표시)
disp_text = st.session_state.input_buffer if st.session_state.input_buffer != "" else "?"
st.markdown(f"<div class='ans-display'>{disp_text}</div>", unsafe_allow_html=True)

# 2. 알록달록한 키패드 버튼 전용 테마 CSS 설정
st.markdown("""
<style>
    /* 숫자 버튼 디자인 (노란색 파스텔톤 동글이 버튼) */
    div[data-testid="column"] button {
        background-color: #FEF08A !important;
        color: #854D0E !important;
        border: 2px solid #FDE047 !important;
        border-radius: 12px !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
        padding: 5px !important;
        width: 100% !important;
    }
    /* 지우기(C) 버튼 디자인 */
    div.clear-btn button {
        background-color: #FED7AA !important;
        color: #9A3412 !important;
        border: 2px solid #FDBA74 !important;
    }
    /* 정답제출(OK) 버튼 디자인 */
    div.ok-btn button {
        background-color: #86EFAC !important;
        color: #166534 !important;
        border: 2px solid #4ADE80 !important;
        font-size: 1.3rem !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. 키패드 배열 만들기 (가로로 가치있게 컴팩트 배치)
row1_col1, row1_col2, row1_col3 = st.columns(3)
row2_col1, row2_col2, row2_col3 = st.columns(3)
row3_col1, row3_col2, row3_col3 = st.columns(3)
row4_col1, row4_col2, row4_col3 = st.columns(3)

# 버튼 클릭 감지 및 문자열 보관함(버퍼) 연산
with row1_col1:
    if st.button("1"): st.session_state.input_buffer += "1"; st.rerun()
with row1_col2:
    if st.button("2"): st.session_state.input_buffer += "2"; st.rerun()
with row1_col3:
    if st.button("3"): st.session_state.input_buffer += "3"; st.rerun()

with row2_col1:
    if st.button("4"): st.session_state.input_buffer += "4"; st.rerun()
with row2_col2:
    if st.button("5"): st.session_state.input_buffer += "5"; st.rerun()
with row2_col3:
    if st.button("6"): st.session_state.input_buffer += "6"; st.rerun()

with row3_col1:
    if st.button("7"): st.session_state.input_buffer += "7"; st.rerun()
with row3_col2:
    if st.button("8"): st.session_state.input_buffer += "8"; st.rerun()
with row3_col3:
    if st.button("9"): st.session_state.input_buffer += "9"; st.rerun()

with row4_col1:
    st.markdown("<div class='clear-btn'>", unsafe_allow_html=True)
    if st.button("C"): # 전체 지우기
        st.session_state.input_buffer = ""
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
with row4_col2:
    if st.button("0"):
        # 첫 글자가 0이 되는 것을 방지
        if st.session_state.input_buffer != "":
            st.session_state.input_buffer += "0"
            st.rerun()
            
with row4_col3:
    st.markdown("<div class='ok-btn'>", unsafe_allow_html=True)
    submit_pressed = st.button("확인")
    st.markdown("</div>", unsafe_allow_html=True)

# 4. 정답 판정 메커니즘
if submit_pressed:
    if st.session_state.input_buffer != "":
        user_ans = int(st.session_state.input_buffer)
        if user_ans == correct:
            st.session_state.score += 10
            st.balloons()
            st.success(f"🎉 정답! [{n1} {op} {n2} = {correct}] 참 잘했어요!")
            st.session_state.needs_new_question = True
            time.sleep(0.8)
            st.rerun()
        else:
            st.error("😮 조금만 더 생각해볼까요? 그림을 다시 세어보세요!")
            st.session_state.input_buffer = "" # 틀리면 초기화
            time.sleep(0.8)
            st.rerun()
    else:
        st.warning("⚠️ 숫자를 먼저 입력창에 적어주세요!")