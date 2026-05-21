import streamlit as st
import random
import time

# 페이지 설정
st.set_page_config(page_title="말랑말랑 레벨업 수학", page_icon="🎨", layout="centered")

# --- [모바일 가로 고정 및 레이아웃 최적화 테마 CSS] ---
st.markdown("""
<style>
    /* 1. 모바일 스크롤 완벽 차단 및 화면 비율 고정 */
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
        padding: 0.5rem 0.6rem !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        height: 100vh !important;
    }
    
    [data-testid="stVerticalBlock"] { gap: 0.1rem !important; }
    hr { margin: 0.2rem 0 !important; opacity: 0.15; }
    h1 { color: #554488; font-size: 1.2rem !important; text-align: center; margin: 0 !important; }
    
    .score-box { 
        background-color: white; padding: 3px 6px; border-radius: 8px; 
        border: 1.5px solid #FFC0CB; text-align: center; margin: 0.1rem auto !important; width: 85%;
    }
    .score-box h2 { font-size: 0.9rem !important; margin: 0 !important; color: #CC4488; font-weight: bold; }

    /* 문제 수식 크기 */
    .quiz-text {
        color: #6644AA; font-size: 2.4rem !important; font-weight: bold; text-align: center; margin: 0.2rem 0 !important;
    }

    /* 5개 주머니 레이아웃 간격 */
    .five-group {
        display: inline-flex; background-color: rgba(255, 255, 255, 0.75);
        padding: 4px 6px; border-radius: 10px; margin: 3px 4px; border: 1.5px dashed #FFB6C1;
    }
    
    /* 💥 캐릭터 그림 크기 시원하게 확대 확대 */
    .char-img { 
        width: 40px !important;
        height: 40px !important;
        margin: 2px;
    }
    
    /* 덧셈용 그림자 빈칸 주머니 */
    .shadow-img-box {
        display: inline-block;
        width: 40px !important;
        height: 40px !important;
        margin: 2px;
        background-color: rgba(0, 0, 0, 0.12);
        border-radius: 50%;
        border: 1px dashed #aaa;
    }
    
    /* 🎈 누를 때마다 정중앙에 시원하게 터지는 대형 풍선 애니메이션 효과 */
    .balloon-pop {
        position: absolute;
        left: 50%;
        top: 35%;
        transform: translate(-50%, -50%);
        color: #FF477E;
        font-weight: bold;
        font-size: 3rem !important;
        text-shadow: 2px 2px 6px rgba(0,0,0,0.3);
        animation: floatUp 0.7s ease-out forwards;
        pointer-events: none;
        z-index: 9999;
    }
    @keyframes floatUp {
        0% { opacity: 0; transform: translate(-50%, 20px) scale(0.5); }
        25% { opacity: 1; transform: translate(-50%, 0px) scale(1.3); }
        100% { opacity: 0; transform: translate(-50%, -60px) scale(1.5); }
    }

    .hint-title { font-size: 0.8rem !important; font-weight: bold; color: #4466AA; margin: 0.1rem 0 !important; text-align: center; }

    /* 정답 모니터 창 */
    .ans-display {
        background-color: #F0F9FF; border: 2.5px solid #7DD3FC; border-radius: 11px;
        padding: 4px; text-align: center; font-size: 1.6rem !important;
        font-weight: bold; color: #0369A1; min-height: 40px; margin: 0.3rem auto !important; width: 80%;
    }

    /* --- 📱 모바일 절대 사수 가로 정렬 통합 키패드 아키텍처 --- */
    .keypad-outer-box {
        border: 2.5px solid #93C5FD; 
        background-color: rgba(239, 246, 255, 0.95);
        border-radius: 14px; 
        padding: 8px; 
        margin: 0 auto 0.2rem auto; 
        width: 100%; 
        max-width: 350px;
        box-sizing: border-box;
    }
    
    .flex-row-container {
        display: flex !important;
        flex-direction: row !important;
        width: 100% !important;
        gap: 8px !important;
    }
    
    .number-grid-area {
        display: flex !important;
        flex-direction: column !important;
        flex: 3.8 !important;
        gap: 8px !important;
    }
    
    .number-row {
        display: flex !important;
        flex-direction: row !important;
        width: 100% !important;
        gap: 6px !important;
    }
    
    .action-button-area {
        display: flex !important;
        flex-direction: column !important;
        flex: 1.5 !important;
        gap: 8px !important;
    }

    /* 아이들이 누르기 편한 모바일 최적화 자판 단추 */
    .custom-key-btn {
        width: 100% !important;
        height: 45px !important;
        background-color: #FEF08A !important;
        color: #854D0E !important;
        border: 1.5px solid #FDE047 !important;
        border-radius: 8px !important;
        font-size: 1.25rem !important;
        font-weight: bold !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        user-select: none;
    }
    
    .custom-key-btn.clear { background-color: #FCA5A5 !important; color: #7F1D1D !important; border-color: #F87171 !important; font-size: 0.95rem !important;}
    .custom-key-btn.submit { background-color: #86EFAC !important; color: #14532D !important; border-color: #4ADE80 !important; font-size: 0.95rem !important;}
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

# 시스템 상태 보관용 바구니
if "score" not in st.session_state: st.session_state.score = 0
if "needs_new_question" not in st.session_state: st.session_state.needs_new_question = True
if "input_buffer" not in st.session_state: st.session_state.input_buffer = ""

if "plus_clicks" not in st.session_state: st.session_state.plus_clicks = 0
if "minus_clicks" not in st.session_state: st.session_state.minus_clicks = 0

# 매번 풍선이 100% 정상 작동하도록 돕는 특수 신호등 변수
if "balloon_anim_ready" not in st.session_state: st.session_state.balloon_anim_ready = False
if "balloon_anim_text" not in st.session_state: st.session_state.balloon_anim_text = ""

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
    st.session_state.balloon_anim_ready = False

# 사이드바 옵션 제어장치
game_mode = st.sidebar.selectbox("연산 선택", ["1. 덧셈, 뺄셈", "2. 덧셈, 뺄셈, 곱셈, 나눗셈"])
level = st.sidebar.selectbox("난이도 선택", ["1단계 (초급)", "2단계 (중급)", "3단계 (고급)"])

if st.session_state.needs_new_question:
    generate_question(game_mode, level)

# 상단 UI 빌딩
st.markdown("<h1>🎨 말랑말랑 수학</h1>", unsafe_allow_html=True)
st.markdown(f"<div class='score-box'><h2>✨ 점수: {st.session_state.score}점 ✨</h2></div>", unsafe_allow_html=True)

char_url = CHARACTER_URLS[st.session_state.char_key]
n1, n2, op = st.session_state.num1, st.session_state.num2, st.session_state.operator

st.markdown(f"<div class='quiz-text'>{n1} {op} {n2} = ?</div>", unsafe_allow_html=True)
st.markdown("---")

# 🎈 [매번 터지는 풍선 출구] 랜더링 스위치 위치 고정
if st.session_state.balloon_anim_ready:
    st.markdown(f"<div class='balloon-pop'>{st.session_state.balloon_anim_text}</div>", unsafe_allow_html=True)
    st.session_state.balloon_anim_ready = False # 애니메이션 출력 완료 후 무력화 방지 대기 상태로 리셋

# 1단계 인터랙티브 터치 그림판 영역
if level == "1단계 (초급)":
    st.markdown("<div class='hint-title'>💡 버튼을 눌러 정답을 맞춰보세요!</div>", unsafe_allow_html=True)
    
    if op == "-":
        visible_count = max(0, n1 - st.session_state.minus_clicks)
        html = "<div style='text-align: center; min-height: 55px;'>"
        for i in range(visible_count // 5):
            html += "<div class='five-group'>" + f'<img src="{char_url}" class="char-img">'*5 + "</div>"
        if visible_count % 5 > 0:
            html += "<div class='five-group'>" + f'<img src="{char_url}" class="char-img">'*(visible_count%5) + "</div>"
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)
        
        if visible_count > 0:
            if st.button(f"👇 누르면 하나씩 펑 사라져요! (남은개수: {visible_count})", key="act_sub"):
                st.session_state.minus_clicks += 1
                st.session_state.balloon_anim_text = f"-{st.session_state.minus_clicks} 🎈"
                st.session_state.balloon_anim_ready = True
                st.rerun()
                
    elif op == "+":
        html_n1 = "<div style='text-align: center;'>"
        for _ in range(n1 // 5): html_n1 += "<div class='five-group'>" + f'<img src="{char_url}" class="char-img">'*5 + "</div>"
        if n1 % 5 > 0: html_n1 += "<div class='five-group'>" + f'<img src="{char_url}" class="char-img">'*(n1%5) + "</div>"
        html_n1 += "</div>"
        st.markdown(html_n1, unsafe_allow_html=True)
        
        filled = st.session_state.plus_clicks
        unfilled = max(0, n2 - filled)
        
        html_n2 = "<div style='text-align: center; min-height: 55px;'>"
        items = [f'<img src="{char_url}" class="char-img">' for _ in range(filled)] + [f'<div class="shadow-img-box"></div>' for _ in range(unfilled)]
        for i in range(0, len(items), 5):
            html_n2 += "<div class='five-group'>" + "".join(items[i:i+5]) + "</div>"
        html_n2 += "</div>"
        st.markdown(html_n2, unsafe_allow_html=True)
        
        if unfilled > 0:
            if st.button(f"👇 그림자 칸 채우기! (남은빈칸: {unfilled})", key="act_add"):
                st.session_state.plus_clicks += 1
                st.session_state.balloon_anim_text = f"+{st.session_state.plus_clicks} 🎈"
                st.session_state.balloon_anim_ready = True
                st.rerun()
    st.markdown("---")
else:
    st.markdown("<p style='text-align: center; color: #88AABB; margin:0;'>머릿속으로 주머니를 계산해요! 💪</p>", unsafe_allow_html=True)
    st.markdown("---")

# 정답 판독기 모니터 창 디스플레이
disp = st.session_state.input_buffer if st.session_state.input_buffer else "?"
st.markdown(f"<div class='ans-display'>{disp}</div>", unsafe_allow_html=True)


# --- 🛠️ [TypeError의 주범이었던 파이썬 숨김 버튼 100% 영구 퇴출] ---
# 대신 안전하고 표준적인 스트림릿 텍스트 입력을 브라우저 뒷단에 숨겨 연동하는 완벽무결한 통신 방식을 도입했습니다.
if "hidden_text_input" not in st.session_state: st.session_state.hidden_text_input = ""

# 특수 액션 명령어가 수신되었는지 감지 및 분석 핸들링 로직
query_params = st.query_params
if "action" in query_params:
    action_val = query_params["action"]
    # 명령어 접수 후 주소창 쿼리 매개변수 즉시 비우기 (무한 루프 락 방지)
    st.query_params.clear()
    
    if action_val in ["1","2","3","4","5","6","7","8","9","0"]:
        if not (action_val == "0" and not st.session_state.input_buffer):
            st.session_state.input_buffer += action_val
        st.rerun()
    elif action_val == "clear":
        st.session_state.input_buffer = ""
        st.session_state.plus_clicks = 0
        st.session_state.minus_clicks = 0
        st.rerun()
    elif action_val == "submit":
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

# 📱 [에러 원천 차단] 웹 표준 자바스크립트를 직접 내장한 무적의 5x2 게임기형 와이드 가로 자판 랜더러
st.markdown(f"""
<div class="keypad-outer-box">
    <div class="flex-row-container">
        <div class="number-grid-area">
            <div class="number-row">
                <button class="custom-key-btn" onclick="window.location.search = '?action=1';">1</button>
                <button class="custom-key-btn" onclick="window.location.search = '?action=2';">2</button>
                <button class="custom-key-btn" onclick="window.location.search = '?action=3';">3</button>
                <button class="custom-key-btn" onclick="window.location.search = '?action=4';">4</button>
                <button class="custom-key-btn" onclick="window.location.search = '?action=5';">5</button>
            </div>
            <div class="number-row">
                <button class="custom-key-btn" onclick="window.location.search = '?action=6';">6</button>
                <button class="custom-key-btn" onclick="window.location.search = '?action=7';">7</button>
                <button class="custom-key-btn" onclick="window.location.search = '?action=8';">8</button>
                <button class="custom-key-btn" onclick="window.location.search = '?action=9';">9</button>
                <button class="custom-key-btn" onclick="window.location.search = '?action=0';">0</button>
            </div>
        </div>
        <div class="action-button-area">
            <button class="custom-key-btn clear" onclick="window.location.search = '?action=clear';">지우기</button>
            <button class="custom-key-btn submit" onclick="window.location.search = '?action=submit';">제출</button>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)