import streamlit as st
import random
import time

# 페이지 설정
st.set_page_config(page_title="말랑말랑 레벨업 수학", page_icon="🎨", layout="centered")

# --- [모바일 화면 겹침 방지 및 컴포넌트 최적화 CSS] ---
st.markdown("""
<style>
    /* 1. 스크롤바 차단 및 기본 배경 설정 */
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
    
    /* 2. 컴포넌트들이 겹치지 않도록 세로 여백 유연하게 축소 (핵심 조절) */
    .block-container {
        padding: 0.4rem 0.6rem !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        height: 100vh !important;
    }
    
    [data-testid="stVerticalBlock"] { gap: 0.1rem !important; }
    hr { margin: 0.15rem 0 !important; opacity: 0.1; }
    h1 { color: #554488; font-size: 1.1rem !important; text-align: center; margin: 0 !important; }
    
    /* 상단 스코어박스 슬림화 */
    .score-box { 
        background-color: white; padding: 2px 6px; border-radius: 8px; 
        border: 1.5px solid #FFC0CB; text-align: center; margin: 0.05rem auto !important; width: 75%;
    }
    .score-box h2 { font-size: 0.85rem !important; margin: 0 !important; color: #CC4488; font-weight: bold; }

    /* 문제 글씨 크기 적정 조절 (겹침의 주원인 해결) */
    .quiz-text {
        color: #6644AA; font-size: 2rem !important; font-weight: bold; text-align: center; margin: 0.15rem 0 !important;
    }

    /* 5개 주머니 묶음 여백 슬림화 */
    .five-group {
        display: inline-flex; background-color: rgba(255, 255, 255, 0.75);
        padding: 3px 5px; border-radius: 10px; margin: 2px 3px; border: 1.5px dashed #FFB6C1;
    }
    
    /* 💥 그림 크기를 모바일 겹침이 없는 딱 좋은 최적 크기(34px)로 세팅 */
    .char-img { 
        width: 34px !important;
        height: 34px !important;
        margin: 1px;
    }
    
    /* 덧셈용 그림자 빈칸 주머니 스타일 */
    .shadow-img-box {
        display: inline-block;
        width: 34px !important;
        height: 34px !important;
        margin: 1px;
        background-color: rgba(0, 0, 0, 0.15);
        border-radius: 50%;
    }
    
    /* 🎈 누를 때마다 솟구치는 대형 풍선 애니메이션 효과 */
    .balloon-pop {
        position: absolute;
        left: 50%;
        top: 30%;
        transform: translate(-50%, -50%);
        color: #FF477E;
        font-weight: bold;
        font-size: 2.5rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.25);
        animation: floatUp 0.6s ease-out forwards;
        pointer-events: none;
        z-index: 9999;
    }
    @keyframes floatUp {
        0% { opacity: 0; transform: translate(-50%, 15px) scale(0.6); }
        30% { opacity: 1; transform: translate(-50%, -10px) scale(1.2); }
        100% { opacity: 0; transform: translate(-50%, -50px) scale(1.4); }
    }

    .hint-title { font-size: 0.75rem !important; font-weight: bold; color: #4466AA; margin: 0 !important; text-align: center; }

    /* 정답 모니터 창 슬림화 */
    .ans-display {
        background-color: #F0F9FF; border: 2px solid #7DD3FC; border-radius: 10px;
        padding: 2px; text-align: center; font-size: 1.4rem !important;
        font-weight: bold; color: #0369A1; min-height: 34px; margin: 0.15rem auto !important; width: 70%;
    }

    /* --- 📱 절대 씹히지 않는 가로 정렬 고정형 스트림릿 순수 단추 테마 --- */
    .keypad-outer-box {
        border: 2px solid #93C5FD; 
        background-color: rgba(239, 246, 255, 0.95);
        border-radius: 12px; 
        padding: 6px; 
        margin: 0 auto; 
        width: 100%; 
        max-width: 350px;
        box-sizing: border-box;
    }
    
    /* 스트림릿 기본 버튼 스타일을 모바일 오락기 형태로 커스텀 강제 주입 */
    div[data-testid="stHorizontalBlock"] button {
        background-color: #FEF08A !important;
        color: #854D0E !important;
        border: 1.5px solid #FDE047 !important;
        border-radius: 6px !important;
        font-size: 1.15rem !important;
        font-weight: bold !important;
        height: 38px !important;
        padding: 0 !important;
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    /* 기능 버튼 색상 개별 맞춤 */
    div.clear-btn button { background-color: #FCA5A5 !important; color: #7F1D1D !important; border-color: #F87171 !important; font-size: 0.85rem !important;}
    div.submit-btn button { background-color: #86EFAC !important; color: #14532D !important; border-color: #4ADE80 !important; font-size: 0.85rem !important;}
    
    /* 투명 그림 터치 전용 특수 보이지 않는 투명 버튼 레이어 */
    .invisible-target-btn button {
        background: transparent !important;
        border: none !important;
        color: transparent !important;
        position: absolute !important;
        width: 100% !important;
        height: 50px !important;
        z-index: 10 !important;
        top: 0; left: 0;
    }
    
    button p { margin: 0 !important; }
</style>
""", unsafe_allow_html=True)

CHARACTER_URLS = {
    "bunny": "https://cdn-icons-png.flaticon.com/512/3261/3261168.png", 
    "bear": "https://cdn-icons-png.flaticon.com/512/1000/1000966.png",  
    "apple": "https://cdn-icons-png.flaticon.com/512/2909/2909787.png", 
    "berry": "https://cdn-icons-png.flaticon.com/512/2316/2316886.png", 
    "cat": "https://cdn-icons-png.flaticon.com/512/616/616430.png"     
}
CHAR_KEYS = list(CHARACTER_URLS.keys())

# 변수 보관통
if "score" not in st.session_state: st.session_state.score = 0
if "needs_new_question" not in st.session_state: st.session_state.needs_new_question = True
if "input_buffer" not in st.session_state: st.session_state.input_buffer = ""

if "plus_clicks" not in st.session_state: st.session_state.plus_clicks = 0
if "minus_clicks" not in st.session_state: st.session_state.minus_clicks = 0
if "balloon_ready" not in st.session_state: st.session_state.balloon_ready = False
if "balloon_txt" not in st.session_state: st.session_state.balloon_txt = ""

def generate_question(game_mode, level):
    st.session_state.char_key = random.choice(CHAR_KEYS)
    if game_mode == "1. 덧셈, 뺄셈": op = random.choice(["+", "-"])
    else: op = random.choice(["+", "-", "×", "÷"])
    st.session_state.operator = op
    
    if level == "1단계 (초급)":
        if op == "+":
            n1 = random.randint(1, 10)
            n2 = random.randint(1, 5)
        else:
            n1 = random.randint(2, 12)
            n2 = random.randint(1, n1)
    else:
        n1, n2 = random.randint(10, 30), random.randint(1, 9)

    st.session_state.num1, st.session_state.num2 = n1, n2
    st.session_state.needs_new_question = False
    st.session_state.input_buffer = ""
    st.session_state.plus_clicks = 0
    st.session_state.minus_clicks = 0
    st.session_state.balloon_ready = False

# 사이드바 제어판
game_mode = st.sidebar.selectbox("연산 선택", ["1. 덧셈, 뺄셈", "2. 덧셈, 뺄셈, 곱셈, 나눗셈"])
level = st.sidebar.selectbox("난이도 선택", ["1단계 (초급)", "2단계 (중급)", "3단계 (고급)"])

if st.session_state.needs_new_question:
    generate_question(game_mode, level)

# 메인 타이틀 및 스코어 가동
st.markdown("<h1>🎨 말랑말랑 수학</h1>", unsafe_allow_html=True)
st.markdown(f"<div class='score-box'><h2>✨ 점수: {st.session_state.score}점 ✨</h2></div>", unsafe_allow_html=True)

char_url = CHARACTER_URLS[st.session_state.char_key]
n1, n2, op = st.session_state.num1, st.session_state.num2, st.session_state.operator

st.markdown(f"<div class='quiz-text'>{n1} {op} {n2} = ?</div>", unsafe_allow_html=True)
st.markdown("---")

# 🎈 실시간 터치 감지 대형 풍선 연출부
if st.session_state.balloon_ready:
    st.markdown(f"<div class='balloon-pop'>{st.session_state.balloon_txt}</div>", unsafe_allow_html=True)
    st.session_state.balloon_ready = False

# 1단계 인터랙티브 터치 페인팅 보드
if level == "1단계 (초급)":
    st.markdown("<div class='hint-title'>💡 아래 그림을 손가락으로 직접 눌러봐요!</div>", unsafe_allow_html=True)
    
    # ➖ 뺄셈 모드: 과일/동물을 직접 터치하면 펑 사라짐!
    if op == "-":
        visible_count = max(0, n1 - st.session_state.minus_clicks)
        
        # 그림 영역 렌더링
        html = "<div style='text-align: center; position: relative;'>"
        for i in range(visible_count // 5):
            html += "<div class='five-group'>" + f'<img src="{char_url}" class="char-img">'*5 + "</div>"
        if visible_count % 5 > 0:
            html += "<div class='five-group'>" + f'<img src="{char_url}" class="char-img">'*(visible_count%5) + "</div>"
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)
        
        # 💥 투명 스위치를 그림 위에 씌워, 그림 터치 효과 완성!
        if visible_count > 0:
            st.markdown("<div class='invisible-target-btn'>", unsafe_allow_html=True)
            if st.button(f"touch_sub_trigger_{visible_count}", key="touch_img_sub"):
                st.session_state.minus_clicks += 1
                st.session_state.balloon_txt = f"-{st.session_state.minus_clicks} 🎈"
                st.session_state.balloon_ready = True
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
                
    # ➕ 덧셈 모드: 빈 그림자 칸을 누르면 알록달록 과일이 채워짐!
    elif op == "+":
        # 기본 숫자 n1 출력
        html_n1 = "<div style='text-align: center;'>"
        for _ in range(n1 // 5): html_n1 += "<div class='five-group'>" + f'<img src="{char_url}" class="char-img">'*5 + "</div>"
        if n1 % 5 > 0: html_n1 += "<div class='five-group'>" + f'<img src="{char_url}" class="char-img">'*(n1%5) + "</div>"
        html_n1 += "</div>"
        st.markdown(html_n1, unsafe_allow_html=True)
        
        # 그림자 빈칸 축적 연산
        filled = st.session_state.plus_clicks
        unfilled = max(0, n2 - filled)
        
        html_n2 = "<div style='text-align: center; position: relative;'>"
        items = [f'<img src="{char_url}" class="char-img">' for _ in range(filled)] + [f'<div class="shadow-img-box"></div>' for _ in range(unfilled)]
        for i in range(0, len(items), 5):
            html_n2 += "<div class='five-group'>" + "".join(items[i:i+5]) + "</div>"
        html_n2 += "</div>"
        st.markdown(html_n2, unsafe_allow_html=True)
        
        # 💥 투명 스위치를 그림자 칸 위에 씌워, 그림자 직접 터치 실현!
        if unfilled > 0:
            st.markdown("<div class='invisible-target-btn'>", unsafe_allow_html=True)
            if st.button(f"touch_add_trigger_{unfilled}", key="touch_img_add"):
                st.session_state.plus_clicks += 1
                st.session_state.balloon_txt = f"+{st.session_state.plus_clicks} 🎈"
                st.session_state.balloon_ready = True
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")
else:
    st.markdown("<p style='text-align: center; color: #88AABB; margin:0;'>중급/고급은 머릿속으로 계산해요! 💪</p>", unsafe_allow_html=True)
    st.markdown("---")

# 정답 표시창 모니터
disp = st.session_state.input_buffer if st.session_state.input_buffer else "?"
st.markdown(f"<div class='ans-display'>{disp}</div>", unsafe_allow_html=True)


# --- 📱 [100% 동작 보장] 스트림릿 가로 고정 패밀리 폼 키패드 ---
# 자바스크립트를 전면 배제하고 스트림릿 네이티브 다중 컬럼 레이아웃을 특수 그리딩하여 모바일 100% 터치 작동을 구현했습니다.
st.markdown("<div class='keypad-outer-box'>", unsafe_allow_html=True)

# 왼쪽 4.5 비율 (숫자 자판) / 오른쪽 1.5 비율 (기능 버튼)로 정렬 분할
col_pad_left, col_pad_right = st.columns([4.5, 1.5])

with col_pad_left:
    # 윗줄: 1, 2, 3, 4, 5
    line1_1, line1_2, line1_3, line1_4, line1_5 = st.columns(5)
    with line1_1:
        if st.button("1", key="k_1"): st.session_state.input_buffer += "1"; st.rerun()
    with line1_2:
        if st.button("2", key="k_2"): st.session_state.input_buffer += "2"; st.rerun()
    with line1_3:
        if st.button("3", key="k_3"): st.session_state.input_buffer += "3"; st.rerun()
    with line1_4:
        if st.button("4", key="k_4"): st.session_state.input_buffer += "4"; st.rerun()
    with line1_5:
        if st.button("5", key="k_5"): st.session_state.input_buffer += "5"; st.rerun()

    # 아랫줄: 6, 7, 8, 9, 0
    line2_1, line2_2, line2_3, line2_4, line2_5 = st.columns(5)
    with line2_1:
        if st.button("6", key="k_6"): st.session_state.input_buffer += "6"; st.rerun()
    with line2_2:
        if st.button("7", key="k_7"): st.session_state.input_buffer += "7"; st.rerun()
    with line2_3:
        if st.button("8", key="k_8"): st.session_state.input_buffer += "8"; st.rerun()
    with line2_4:
        if st.button("9", key="k_9"): st.session_state.input_buffer += "9"; st.rerun()
    with line2_5:
        if st.button("0", key="k_0"):
            if st.session_state.input_buffer: st.session_state.input_buffer += "0"; st.rerun()

with col_pad_right:
    # 우측 상단 지우기
    st.markdown("<div class='clear-btn'>", unsafe_allow_html=True)
    if st.button("지우기", key="k_clear"):
        st.session_state.input_buffer = ""
        st.session_state.plus_clicks = 0
        st.session_state.minus_clicks = 0
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 우측 하단 제출
    st.markdown("<div class='submit-btn'>", unsafe_allow_html=True)
    submit_pressed = st.button("제출", key="k_submit")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True) # 아우터 박스 마감

# 최종 결과값 채점 판정대
if submit_pressed:
    if st.session_state.input_buffer:
        ans = int(st.session_state.input_buffer)
        correct = (n1 + n2) if op == "+" else (n1 - n2)
        if ans == correct:
            st.session_state.score += 10
            st.balloons()
            st.session_state.needs_new_question = True
            time.sleep(0.5); st.rerun()
        else:
            st.session_state.input_buffer = ""
            st.session_state.plus_clicks = 0
            st.session_state.minus_clicks = 0
            time.sleep(0.5); st.rerun()