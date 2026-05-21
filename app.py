import streamlit as st
import random
import time

# 페이지 설정
st.set_page_config(page_title="말랑말랑 레벨업 수학", page_icon="🎨", layout="centered")

# --- [모바일 가로고정 키패드 및 여백 최적화 테마 CSS] ---
st.markdown("""
<style>
    /* 1. 모바일 스크롤 완벽 차단 */
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
    
    /* 요소들이 너무 붙지 않도록 위아래 균등 분배 패딩 조절 */
    .block-container {
        padding: 0.6rem 0.8rem !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        height: 100vh !important;
    }
    
    [data-testid="stVerticalBlock"] { gap: 0.2rem !important; }
    hr { margin: 0.3rem 0 !important; opacity: 0.2; }
    h1 { color: #554488; font-size: 1.3rem !important; text-align: center; margin: 0 !important; }
    
    .score-box { 
        background-color: white; padding: 4px 8px; border-radius: 10px; 
        border: 1.5px solid #FFC0CB; text-align: center; margin: 0.2rem auto !important; width: 85%;
    }
    .score-box h2 { font-size: 1rem !important; margin: 0 !important; color: #CC4488; font-weight: bold; }

    /* 문제 수식 크기 및 여백 시원하게 조절 */
    .quiz-text {
        color: #6644AA; font-size: 2.5rem !important; font-weight: bold; text-align: center; margin: 0.3rem 0 !important;
    }

    /* 5개 주머니 묶음 레이아웃 간격 확보 */
    .five-group {
        display: inline-flex; background-color: rgba(255, 255, 255, 0.75);
        padding: 6px 8px; border-radius: 12px; margin: 4px 5px; border: 1.5px dashed #FFB6C1;
    }
    
    /* 💥 캐릭터 그림 크기 확대 고정 (터치하기 좋게 최적화) */
    .char-img { 
        width: 38px !important;
        height: 38px !important;
        margin: 2px;
    }
    
    /* 덧셈용 그림자 빈칸 주머니 큼직하게 변경 */
    .shadow-img-box {
        display: inline-block;
        width: 38px !important;
        height: 38px !important;
        margin: 2px;
        background-color: rgba(0, 0, 0, 0.12);
        border-radius: 50%;
        border: 1px dashed #aaa;
    }
    
    /* 🎈 펑 터지며 솟아오르는 대형 풍선 애니메이션 효과 */
    .balloon-pop {
        position: absolute;
        left: 50%;
        top: 30%;
        transform: translate(-50%, -50%);
        color: #FF477E;
        font-weight: bold;
        font-size: 2.8rem !important;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.25);
        animation: floatUp 0.8s ease-out forwards;
        pointer-events: none;
        z-index: 9999;
    }
    @keyframes floatUp {
        0% { opacity: 0; transform: translate(-50%, 0px) scale(0.6); }
        20% { opacity: 1; transform: translate(-50%, -20px) scale(1.2); }
        100% { opacity: 0; transform: translate(-50%, -80px) scale(1.4); }
    }

    .hint-title { font-size: 0.85rem !important; font-weight: bold; color: #4466AA; margin: 0.2rem 0 !important; text-align: center; }

    /* 정답 모니터 창 크기 확대 */
    .ans-display {
        background-color: #F0F9FF; border: 2.5px solid #7DD3FC; border-radius: 12px;
        padding: 4px; text-align: center; font-size: 1.7rem !important;
        font-weight: bold; color: #0369A1; min-height: 42px; margin: 0.4rem auto !important; width: 80%;
    }

    /* --- 📱 모바일 세로 쪼개짐 철저 방지 가로형 키패드 폼 --- */
    .keypad-outer-box {
        border: 2.5px solid #93C5FD; 
        background-color: rgba(239, 246, 255, 0.95);
        border-radius: 14px; 
        padding: 10px; 
        margin: 0 auto 0.5rem auto; 
        width: 100%; 
        max-width: 360px;
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
        flex: 1.4 !important;
        gap: 8px !important;
    }

    /* 누르기 편한 단추 디자인 */
    .custom-key-btn {
        width: 100% !important;
        height: 44px !important;
        background-color: #FEF08A !important;
        color: #854D0E !important;
        border: 1.5px solid #FDE047 !important;
        border-radius: 8px !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    .custom-key-btn.clear { background-color: #FCA5A5 !important; color: #7F1D1D !important; border-color: #F87171 !important; font-size: 0.9rem !important;}
    .custom-key-btn.submit { background-color: #86EFAC !important; color: #14532D !important; border-color: #4ADE80 !important; font-size: 0.9rem !important;}
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

# 앱 상태 보관
if "score" not in st.session_state: st.session_state.score = 0
if "needs_new_question" not in st.session_state: st.session_state.needs_new_question = True
if "input_buffer" not in st.session_state: st.session_state.input_buffer = ""

if "plus_clicks" not in st.session_state: st.session_state.plus_clicks = 0
if "minus_clicks" not in st.session_state: st.session_state.minus_clicks = 0
if "balloon_trigger" not in st.session_state: st.session_state.balloon_trigger = False
if "balloon_text" not in st.session_state: st.session_state.balloon_text = ""

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
    st.session_state.balloon_trigger = False

# 대시보드 옵션창
game_mode = st.sidebar.selectbox("연산 선택", ["1. 덧셈, 뺄셈", "2. 덧셈, 뺄셈, 곱셈, 나눗셈"])
level = st.sidebar.selectbox("난이도 선택", ["1단계 (초급)", "2단계 (중급)", "3단계 (고급)"])

if st.session_state.needs_new_question:
    generate_question(game_mode, level)

# 타이틀 및 스코어 보드
st.markdown("<h1>🎨 말랑말랑 수학</h1>", unsafe_allow_html=True)
st.markdown(f"<div class='score-box'><h2>✨ 점수: {st.session_state.score}점 ✨</h2></div>", unsafe_allow_html=True)

char_url = CHARACTER_URLS[st.session_state.char_key]
n1, n2, op = st.session_state.num1, st.session_state.num2, st.session_state.operator

st.markdown(f"<div class='quiz-text'>{n1} {op} {n2} = ?</div>", unsafe_allow_html=True)
st.markdown("---")

# 🎈 펑 터지는 실시간 풍선 컴포넌트
if st.session_state.balloon_trigger:
    st.markdown(f"<div class='balloon-pop'>{st.session_state.balloon_text}</div>", unsafe_allow_html=True)
    st.session_state.balloon_trigger = False

# 1단계 인터랙티브 주머니 터치 빌더
if level == "1단계 (초급)":
    st.markdown("<div class='hint-title'>💡 버튼을 눌러 숫자를 세어보세요!</div>", unsafe_allow_html=True)
    
    if op == "-":
        visible_count = max(0, n1 - st.session_state.minus_clicks)
        html = "<div style='text-align: center; min-height: 60px;'>"
        for i in range(visible_count // 5):
            html += "<div class='five-group'>" + f'<img src="{char_url}" class="char-img">'*5 + "</div>"
        if visible_count % 5 > 0:
            html += "<div class='five-group'>" + f'<img src="{char_url}" class="char-img">'*(visible_count%5) + "</div>"
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)
        
        if visible_count > 0:
            if st.button(f"👇 누르면 하나씩 펑 사라져요! (남은개수: {visible_count})", key="act_sub"):
                st.session_state.minus_clicks += 1
                st.session_state.balloon_text = f"-{st.session_state.minus_clicks} 🎈"
                st.session_state.balloon_trigger = True
                st.rerun()
                
    elif op == "+":
        html_n1 = "<div style='text-align: center;'>"
        for _ in range(n1 // 5): html_n1 += "<div class='five-group'>" + f'<img src="{char_url}" class="char-img">'*5 + "</div>"
        if n1 % 5 > 0: html_n1 += "<div class='five-group'>" + f'<img src="{char_url}" class="char-img">'*(n1%5) + "</div>"
        html_n1 += "</div>"
        st.markdown(html_n1, unsafe_allow_html=True)
        
        filled = st.session_state.plus_clicks
        unfilled = max(0, n2 - filled)
        
        html_n2 = "<div style='text-align: center; min-height: 60px;'>"
        items = [f'<img src="{char_url}" class="char-img">' for _ in range(filled)] + [f'<div class="shadow-img-box"></div>' for _ in range(unfilled)]
        for i in range(0, len(items), 5):
            html_n2 += "<div class='five-group'>" + "".join(items[i:i+5]) + "</div>"
        html_n2 += "</div>"
        st.markdown(html_n2, unsafe_allow_html=True)
        
        if unfilled > 0:
            if st.button(f"👇 그림자 칸 채우기! (남은빈칸: {unfilled})", key="act_add"):
                st.session_state.plus_clicks += 1
                st.session_state.balloon_text = f"+{st.session_state.plus_clicks} 🎈"
                st.session_state.balloon_trigger = True
                st.rerun()
    st.markdown("---")
else:
    st.markdown("<p style='text-align: center; color: #88AABB; margin:0;'>중급/고급은 머릿속으로 계산해요! 💪</p>", unsafe_allow_html=True)
    st.markdown("---")

# 정답 판독기 디스플레이 창
disp = st.session_state.input_buffer if st.session_state.input_buffer else "?"
st.markdown(f"<div class='ans-display'>{disp}</div>", unsafe_allow_html=True)


# --- 백엔드 연결용 단추 (에러 유발 소지였던 'gap' 파라미터 완전 삭제) ---
if 'hidden_click' not in st.session_state: st.session_state.hidden_click = None

col_keys = st.columns(12)
key_labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "clear", "submit"]

for idx, label in enumerate(key_labels):
    with col_keys[idx]:
        if st.button(label, key=f"hid_{label}", label_visibility="collapsed"):
            st.session_state.hidden_click = label
            st.rerun()

if st.session_state.hidden_click:
    click_val = st.session_state.hidden_click
    st.session_state.hidden_click = None
    
    if click_val in ["1","2","3","4","5","6","7","8","9","0"]:
        if click_val == "0" and not st.session_state.input_buffer:
            pass
        else:
            st.session_state.input_buffer += click_val
            st.rerun()
    elif click_val == "clear":
        st.session_state.input_buffer = ""
        st.session_state.plus_clicks = 0
        st.session_state.minus_clicks = 0
        st.rerun()
    elif click_val == "submit":
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

# 📱 윗줄 [1,2,3,4,5], 아랫줄 [6,7,8,9,0] 가로 절대보장 특제 UI 드로잉
st.markdown(f"""
<div class="keypad-outer-box">
    <div class="flex-row-container">
        <div class="number-grid-area">
            <div class="number-row">
                <button class="custom-key-btn" onclick="document.getElementById('root').querySelector('button[key=\"hid_1\"]').click();">1</button>
                <button class="custom-key-btn" onclick="document.getElementById('root').querySelector('button[key=\"hid_2\"]').click();">2</button>
                <button class="custom-key-btn" onclick="document.getElementById('root').querySelector('button[key=\"hid_3\"]').click();">3</button>
                <button class="custom-key-btn" onclick="document.getElementById('root').querySelector('button[key=\"hid_4\"]').click();">4</button>
                <button class="custom-key-btn" onclick="document.getElementById('root').querySelector('button[key=\"hid_5\"]').click();">5</button>
            </div>
            <div class="number-row">
                <button class="custom-key-btn" onclick="document.getElementById('root').querySelector('button[key=\"hid_6\"]').click();">6</button>
                <button class="custom-key-btn" onclick="document.getElementById('root').querySelector('button[key=\"hid_7\"]').click();">7</button>
                <button class="custom-key-btn" onclick="document.getElementById('root').querySelector('button[key=\"hid_8\"]').click();">8</button>
                <button class="custom-key-btn" onclick="document.getElementById('root').querySelector('button[key=\"hid_9\"]').click();">9</button>
                <button class="custom-key-btn" onclick="document.getElementById('root').querySelector('button[key=\"hid_0\"]').click();">0</button>
            </div>
        </div>
        <div class="action-button-area">
            <button class="custom-key-btn clear" onclick="document.getElementById('root').querySelector('button[key=\"hid_clear\"]').click();">지우기</button>
            <button class="custom-key-btn submit" onclick="document.getElementById('root').querySelector('button[key=\"hid_submit\"]').click();">제출</button>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)