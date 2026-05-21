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
if "needs_new_question" not in st.session_state: st.session_state.needs_new_question = True
if "input_buffer" not in st.session_state: st.session_state.input_buffer = ""

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
    else: # 곱셈 나눗셈 생략(기존로직 동일)
        n1, n2 = random.randint(2, 9), random.randint(2, 9)

    st.session_state.num1, st.session_state.num2 = n1, n2
    st.session_state.needs_new_question = False
    st.session_state.input_buffer = ""

# 사이드바 (필요할 때만 꺼내씀)
game_mode = st.sidebar.selectbox("연산 선택", ["1. 덧셈, 뺄셈", "2. 덧셈, 뺄셈, 곱셈, 나눗셈"])
level = st.sidebar.selectbox("난이도 선택", ["1단계 (초급)", "2단계 (중급)", "3단계 (고급)"])

if st.session_state.needs_new_question:
    generate_question(game_mode, level)

# 1. 헤더 & 점수
st.markdown("<h1>🎨 말랑말랑 수학</h1>", unsafe_allow_html=True)
st.markdown(f"<div class='score-box'><h2>✨ 점수: {st.session_state.score}점 ✨</h2></div>", unsafe_allow_html=True)

char_url = CHARACTER_URLS[st.session_state.char_key]
n1, n2, op = st.session_state.num1, st.session_state.num2, st.session_state.operator

# 2. 문제 수식
st.markdown(f"<div class='quiz-text'>{n1} {op} {n2} = ?</div>", unsafe_allow_html=True)
st.markdown("---")

# 3. 그림 힌트 (최대한 압축)
def draw_images(count):
    if count <= 0: return
    html = "<div style='text-align: center;'>"
    for _ in range(count // 5):
        html += "<div class='five-group'>" + f'<img src="{char_url}" class="char-img">'*5 + "</div>"
    if count % 5 > 0:
        html += "<div class='five-group'>" + f'<img src="{char_url}" class="char-img">'*(count%5) + "</div>"
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

if level == "1단계 (초급)":
    st.markdown("<div class='hint-title'>💡 힌트 창</div>", unsafe_allow_html=True)
    draw_images(n1)
    if op == "+":
        st.markdown("<div style='text-align:center; font-size:0.7rem;'>➕</div>", unsafe_allow_html=True)
        draw_images(n2)
    st.markdown("---")

# 4. 정답 디스플레이
disp = st.session_state.input_buffer if st.session_state.input_buffer else "?"
st.markdown(f"<div class='ans-display'>{disp}</div>", unsafe_allow_html=True)

# 5. [와이드 가로형 키패드 - 2줄 배치]
# 첫 번째 줄: 1 2 3 4 5 6
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1: 
    if st.button("1"): st.session_state.input_buffer += "1"; st.rerun()
with c2: 
    if st.button("2"): st.session_state.input_buffer += "2"; st.rerun()
with c3: 
    if st.button("3"): st.session_state.input_buffer += "3"; st.rerun()
with c4: 
    if st.button("4"): st.session_state.input_buffer += "4"; st.rerun()
with c5: 
    if st.button("5"): st.session_state.input_buffer += "5"; st.rerun()
with c6: 
    if st.button("6"): st.session_state.input_buffer += "6"; st.rerun()

# 두 번째 줄: 7 8 9 0 C 확인
c7, c8, c9, c10, c11, c12 = st.columns(6)
with c7: 
    if st.button("7"): st.session_state.input_buffer += "7"; st.rerun()
with c8: 
    if st.button("8"): st.session_state.input_buffer += "8"; st.rerun()
with c9: 
    if st.button("9"): st.session_state.input_buffer += "9"; st.rerun()
with c10: 
    if st.button("0"): 
        if st.session_state.input_buffer: st.session_state.input_buffer += "0"; st.rerun()

with c11: # 지우기 버튼
    st.markdown("<div class='clear-btn'>", unsafe_allow_html=True)
    if st.button("C"): st.session_state.input_buffer = ""; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with c12: # 확인 버튼
    st.markdown("<div class='ok-btn'>", unsafe_allow_html=True)
    ok_btn = st.button("OK")
    st.markdown("</div>", unsafe_allow_html=True)

# 정답 처리
if ok_btn:
    if st.session_state.input_buffer:
        ans = int(st.session_state.input_buffer)
        correct = (n1 + n2) if op == "+" else (n1 - n2)
        if ans == correct:
            st.session_state.score += 10
            st.balloons()
            st.success("정답!")
            st.session_state.needs_new_question = True
            time.sleep(0.5); st.rerun()
        else:
            st.error("다시!"); st.session_state.input_buffer = ""
            time.sleep(0.5); st.rerun()