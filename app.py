import streamlit as st
import random
import time

# 페이지 설정
st.set_page_config(page_title="말랑말랑 레벨업 수학", page_icon="🎨", layout="centered")

# --- [모바일 가로 강제 고정 및 상하 여백 균등 분배 CSS] ---
st.markdown("""
<style>
    /* 1. 스크롤바 차단 및 기본 비율 고정 */
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
    
    /* 2. 🗂️ 위쪽 뭉침 해결: 상하 여백을 폰 화면에 맞춰 균등 분배 */
    .block-container {
        padding: 1.2rem 0.8rem !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        height: 100vh !important;
        box-sizing: border-box;
    }
    
    /* 수직 배치 컴포넌트 간의 최소 물리적 거리 확보 */
    [data-testid="stVerticalBlock"] { 
        gap: 0.6rem !important; 
    }
    
    hr { margin: 0.4rem 0 !important; opacity: 0.15; }
    h1 { color: #554488; font-size: 1.3rem !important; text-align: center; margin: 0 0 0.2rem 0 !important; }
    
    /* 점수판 여백 확보 */
    .score-box { 
        background-color: white; padding: 4px 8px; border-radius: 10px; 
        border: 1.5px solid #FFC0CB; text-align: center; margin: 0.2rem auto !important; width: 80%;
    }
    .score-box h2 { font-size: 0.95rem !important; margin: 0 !important; color: #CC4488; font-weight: bold; }

    /* 문제 수식 여백 독립 배치 */
    .quiz-text {
        color: #6644AA; font-size: 2.6rem !important; font-weight: bold; text-align: center; margin: 0.5rem 0 !important;
    }

    /* 힌트 주머니 영역 배치 및 터치 타겟 최적화 */
    .hint-container-box {
        text-align: center;
        margin: 0.4rem 0 !important;
        position: relative;
        cursor: pointer;
    }
    
    .five-group {
        display: inline-flex; background-color: rgba(255, 255, 255, 0.8);
        padding: 4px 6px; border-radius: 10px; margin: 3px 4px; border: 1.5px dashed #FFB6C1;
    }
    
    /* 캐릭터 크기 최적화 */
    .char-img { 
        width: 36px !important;
        height: 36px !important;
        margin: 1px;
        pointer-events: none; /* 클릭 이벤트 방해 차단 */
    }
    
    .shadow-img-box {
        display: inline-block;
        width: 36px !important;
        height: 36px !important;
        margin: 1px;
        background-color: rgba(0, 0, 0, 0.14);
        border-radius: 50%;
        pointer-events: none;
    }
    
    /* 🎈 매번 완벽하게 솟구치는 풍선 팝업 자막 */
    .balloon-pop {
        position: absolute;
        left: 50%;
        top: 25%;
        transform: translate(-50%, -50%);
        color: #FF477E;
        font-weight: bold;
        font-size: 2.8rem !important;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.3);
        animation: floatUp 0.65s ease-out forwards;
        pointer-events: none;
        z-index: 9999;
    }
    @keyframes floatUp {
        0% { opacity: 0; transform: translate(-50%, 10px) scale(0.6); }
        25% { opacity: 1; transform: translate(-50%, -15px) scale(1.2); }
        100% { opacity: 0; transform: translate(-50%, -55px) scale(1.4); }
    }

    .hint-title { font-size: 0.85rem !important; font-weight: bold; color: #4466AA; margin: 0 0 0.3rem 0 !important; text-align: center; }

    /* 정답 모니터 창 여백 격리 */
    .ans-display {
        background-color: #F0F9FF; border: 2.5px solid #7DD3FC; border-radius: 12px;
        padding: 4px; text-align: center; font-size: 1.8rem !important;
        font-weight: bold; color: #0369A1; min-height: 42px; margin: 0.6rem auto !important; width: 75%;
    }

    /* --- 📱 [무조건 가로 고정] 혁신형 웹 표준 플렉스 키패드 인터페이스 --- */
    /* 스트림릿 컬럼을 쓰지 않고 HTML로 직접 격자 틀을 짜서 모바일 세로 쪼개짐을 원천 차단합니다. */
    .html-keypad-outer {
        background-color: rgba(239, 246, 255, 0.95);
        border: 2.5px solid #93C5FD;
        border-radius: 16px;
        padding: 10px;
        width: 100%;
        max-width: 360px;
        margin: 0 auto 0.4rem auto;
        box-sizing: border-box;
        display: flex !important;
        flex-direction: row !important;
        gap: 8px !important;
    }
    
    .html-num-zone {
        display: flex !important;
        flex-direction: column !important;
        flex: 4 !important;
        gap: 8px !important;
    }
    
    .html-btn-row {
        display: flex !important;
        flex-direction: row !important;
        width: 100% !important;
        gap: 6px !important;
    }
    
    .html-action-zone {
        display: flex !important;
        flex-direction: column !important;
        flex: 1.3 !important;
        gap: 8px !important;
    }

    /* 누르기 넉넉하고 시원한 버튼 실물 커스텀 기성품 */
    .html-btn {
        flex: 1 !important;
        height: 44px !important;
        background-color: #FEF08A !important;
        color: #854D0E !important;
        border: 1.5px solid #FDE047 !important;
        border-radius: 8px !important;
        font-size: 1.3rem !important;
        font-weight: bold !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer;
        user-select: none;
        -webkit-tap-highlight-color: transparent;
    }
    .html-btn:active { background-color: #FDE047 !important; }
    
    .html-btn.clear { background-color: #FCA5A5 !important; color: #7F1D1D !important; border-color: #F87171 !important; font-size: 0.9rem !important; }
    .html-btn.clear:active { background-color: #F87171 !important; }
    
    .html-btn.submit { background-color: #86EFAC !important; color: #14532D !important; border-color: #4ADE80 !important; font-size: 0.9rem !important; }
    .html-btn.submit:active { background-color: #4ADE80 !important; }
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

# 메모리 버퍼 기지 구축
if "score" not in st.session_state: st.session_state.score = 0
if "needs_new_question" not in st.session_state: st.session_state.needs_new_question = True
if "input_buffer" not in st.session_state: st.session_state.input_buffer = ""

if "plus_clicks" not in st.session_state: st.session_state.plus_clicks = 0
if "minus_clicks" not in st.session_state: st.session_state.minus_clicks = 0

if "balloon_active" not in st.session_state: st.session_state.balloon_active = False
if "balloon_msg" not in st.session_state: st.session_state.balloon_msg = ""

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
    st.session_state.balloon_active = False

# 대시보드 뷰어
game_mode = st.sidebar.selectbox("연산 선택", ["1. 덧셈, 뺄셈", "2. 덧셈, 뺄셈, 곱셈, 나눗셈"])
level = st.sidebar.selectbox("난이도 선택", ["1단계 (초급)", "2단계 (중급)", "3단계 (고급)"])

if st.session_state.needs_new_question:
    generate_question(game_mode, level)

# 헤드 타이틀 스코어 라인 부설
st.markdown("<h1>🎨 말랑말랑 수학</h1>", unsafe_allow_html=True)
st.markdown(f"<div class='score-box'><h2>✨ 점수: {st.session_state.score}점 ✨</h2></div>", unsafe_allow_html=True)

char_url = CHARACTER_URLS[st.session_state.char_key]
n1, n2, op = st.session_state.num1, st.session_state.num2, st.session_state.operator

st.markdown(f"<div class='quiz-text'>{n1} {op} {n2} = ?</div>", unsafe_allow_html=True)
st.markdown("---")

# 🎈 터치할 때마다 예외 없이 100% 발사되는 중앙 풍선 알림장
if st.session_state.balloon_active:
    st.markdown(f"<div class='balloon-pop'>{st.session_state.balloon_msg}</div>", unsafe_allow_html=True)
    st.session_state.balloon_active = False

# 1단계 인터랙티브 그림판 구현부
if level == "1단계 (초급)":
    st.markdown("<div class='hint-title'>💡 아래 그림 무더기를 손가락으로 직접 눌러봐요!</div>", unsafe_allow_html=True)
    
    # ➖ 뺄셈 연산: 그림판 자체를 터치하면 투명 단추가 백엔드로 즉시 신호 전송
    if op == "-":
        visible_count = max(0, n1 - st.session_state.minus_clicks)
        
        # 순수 그림 출력 레이어
        html = "<div class='hint-container-box'>"
        for i in range(visible_count // 5):
            html += "<div class='five-group'>" + f'<img src="{char_url}" class="char-img">'*5 + "</div>"
        if visible_count % 5 > 0:
            html += "<div class='five-group'>" + f'<img src="{char_url}" class="char-img">'*(visible_count%5) + "</div>"
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)
        
        # 영문 텍스트 안내 단추를 없애고, 보이지 않는 투명 전체 면적 터치 트리거로 대체
        if visible_count > 0:
            if st.button("그림 터치용 숨김 스위치 A", key="img_touch_sub_action", label_visibility="collapsed"):
                st.session_state.minus_clicks += 1
                st.session_state.balloon_msg = f"-{st.session_state.minus_clicks} 🎈"
                st.session_state.balloon_active = True
                st.rerun()
                
    # ➕ 덧셈 연산: 빈칸 주머니 터치 빌딩
    elif op == "+":
        filled = st.session_state.plus_clicks
        unfilled = max(0, n2 - filled)
        
        html_add = "<div class='hint-container-box'>"
        # n1 고정 그림단
        for _ in range(n1 // 5): html_add += "<div class='five-group'>" + f'<img src="{char_url}" class="char-img">'*5 + "</div>"
        if n1 % 5 > 0: html_add += "<div class='five-group'>" + f'<img src="{char_url}" class="char-img">'*(n1%5) + "</div>"
        
        # n2 그림자 변환단
        items = [f'<img src="{char_url}" class="char-img">' for _ in range(filled)] + [f'<div class="shadow-img-box"></div>' for _ in range(unfilled)]
        for i in range(0, len(items), 5):
            html_add += "<div class='five-group'>" + "".join(items[i:i+5]) + "</div>"
        html_add += "</div>"
        st.markdown(html_add, unsafe_allow_html=True)
        
        if unfilled > 0:
            if st.button("그림 터치용 숨김 스위치 B", key="img_touch_add_action", label_visibility="collapsed"):
                st.session_state.plus_clicks += 1
                st.session_state.balloon_msg = f"+{st.session_state.plus_clicks} 🎈"
                st.session_state.balloon_active = True
                st.rerun()
    st.markdown("---")
else:
    st.markdown("<p style='text-align: center; color: #88AABB; margin:0;'>중급/고급은 머릿속 주머니로 계산해요! 💪</p>", unsafe_allow_html=True)
    st.markdown("---")

# 정답 판독 레이어 알림창
disp = st.session_state.input_buffer if st.session_state.input_buffer else "?"
st.markdown(f"<div class='ans-display'>{disp}</div>", unsafe_allow_html=True)


# --- 🛠️ [신호 유실 없는 완벽한 하이브리드 파이썬 통신 터널 개통] ---
# 가로 정렬 형태의 외형은 HTML로 잡고, 실제 터치 조작 신호는 스트림릿 표준 쿼리를 사용해 전송 차단 현상을 박멸했습니다.
query_trigger = st.query_params
if "press" in query_trigger:
    val = query_trigger["press"]
    st.query_params.clear() # 다음 입력을 위해 즉시 비우기
    
    if val in ["1","2","3","4","5","6","7","8","9","0"]:
        if not (val == "0" and not st.session_state.input_buffer):
            st.session_state.input_buffer += val
        st.rerun()
    elif val == "clear":
        st.session_state.input_buffer = ""
        st.session_state.plus_clicks = 0
        st.session_state.minus_clicks = 0
        st.rerun()
    elif val == "submit":
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

# 📱 어떤 스마트폰에서도 절대 무너지지 않고 100% 가로 와이드 정렬을 유지하는 기하학적 키패드
st.markdown(f"""
<div class="html-keypad-outer">
    <div class="html-num-zone">
        <div class="html-btn-row">
            <div class="html-btn" onclick="window.location.href='?press=1'">1</div>
            <div class="html-btn" onclick="window.location.href='?press=2'">2</div>
            <div class="html-btn" onclick="window.location.href='?press=3'">3</div>
            <div class="html-btn" onclick="window.location.href='?press=4'">4</div>
            <div class="html-btn" onclick="window.location.href='?press=5'">5</div>
        </div>
        <div class="html-btn-row">
            <div class="html-btn" onclick="window.location.href='?press=6'">6</div>
            <div class="html-btn" onclick="window.location.href='?press=7'">7</div>
            <div class="html-btn" onclick="window.location.href='?press=8'">8</div >
            <div class="html-btn" onclick="window.location.href='?press=9'">9</div>
            <div class="html-btn" onclick="window.location.href='?press=0'">0</div>
        </div>
    </div>
    <div class="html-action-zone">
        <div class="html-btn clear" onclick="window.location.href='?press=clear'">지우기</div>
        <div class="html-btn submit" onclick="window.location.href='?press=submit'">제출</div>
    </div>
</div>
""", unsafe_allow_html=True)