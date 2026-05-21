import streamlit as st
import random
import time

# 페이지 설정
st.set_page_config(page_title="말랑말랑 레벨업 수학", page_icon="🎨", layout="centered")

# --- [고정 화면 & 풍선 애니메이션 & 테두리 칸 CSS] ---
st.markdown("""
<style>
    /* 스크롤 절대 방지 */
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
        padding: 0.4rem 0.6rem !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        height: 100vh !important;
    }
    
    [data-testid="stVerticalBlock"] { gap: 0.05rem !important; }
    hr { margin: 0.15rem 0 !important; opacity: 0.2; }
    h1 { color: #554488; font-size: 1.1rem !important; text-align: center; margin: 0 !important; }
    
    .score-box { 
        background-color: white; padding: 2px 6px; border-radius: 8px; 
        border: 1.5px solid #FFC0CB; text-align: center; margin: 0.1rem auto !important; width: 80%;
    }
    .score-box h2 { font-size: 0.85rem !important; margin: 0 !important; color: #CC4488; font-weight: bold; }

    .quiz-text {
        color: #6644AA; font-size: 2.1rem !important; font-weight: bold; text-align: center; margin: 0.1rem 0 !important;
    }

    /* 5개 주머니 스타일 */
    .five-group {
        display: inline-flex; background-color: rgba(255, 255, 255, 0.6);
        padding: 2px 4px; border-radius: 8px; margin: 1px 2px; border: 1px dashed #FFB6C1;
    }
    
    /* [애니메이션] 일반 생생한 아이콘 */
    .char-img { 
        width: 22px !important; height: 22px !important; margin: 1px; 
        cursor: pointer; transition: transform 0.1s;
    }
    
    /* [애니메이션] 덧셈용 검은 그림자 빈칸 */
    .shadow-img {
        width: 22px !important; height: 22px !important; margin: 1px;
        filter: brightness(0) drop-shadow(0 0 1px #888); opacity: 0.25; cursor: pointer;
    }
    
    /* [애니메이션] 숫자가 뿅 날아가는 풍선 이펙트 */
    .balloon-pop {
        position: absolute; color: #FF477E; font-weight: bold; font-size: 0.8rem;
        animation: floatUp 0.6s ease-out forwards; pointer-events: none;
    }
    @keyframes floatUp {
        0% { opacity: 1; transform: translateY(0) scale(1); }
        100% { opacity: 0; transform: translateY(-25px) scale(1.4); }
    }

    .hint-title { font-size: 0.75rem !important; font-weight: bold; color: #4466AA; margin: 0 !important; text-align: center; }

    /* 정답 모니터 창 */
    .ans-display {
        background-color: #F0F9FF; border: 2px solid #7DD3FC; border-radius: 10px;
        padding: 2px; text-align: center; font-size: 1.3rem !important;
        font-weight: bold; color: #0369A1; min-height: 32px; margin: 0.15rem auto !important; width: 75%;
    }

    /* --- [게임기형 키패드 테두리 네모칸 디자인] --- */
    .keypad-container {
        border: 2px solid #93C5FD; background-color: rgba(239, 246, 255, 0.85);
        border-radius: 12px; padding: 6px; margin: 0 auto; width: 100%; max-width: 340px;
    }

    div[data-testid="column"] button {
        background-color: #FEF08A !important; color: #854D0E !important;
        border: 1.5px solid #FDE047 !important; border-radius: 6px !important;
        font-size: 0.95rem !important; font-weight: bold !important;
        height: 36px !important; padding: 0 !important; width: 100% !important;
    }
    
    /* 오른쪽 기능 버튼 제어 */
    div.clear-btn button { background-color: #FCA5A5 !important; color: #7F1D1D !important; border-color: #F87171 !important; font-size: 0.85rem !important;}
    div.ok-btn button { background-color: #86EFAC !important; color: #14532D !important; border-color: #4ADE80 !important; font-size: 0.85rem !important;}
    
    button p { margin: 0 !important; line-height: 36px !important; }
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

# 상태 저장 보관함
if "score" not in st.session_state: st.session_state.score = 0
if "needs_new_question" not in st.session_state: st.session_state.needs_new_question = True
if "input_buffer" not in st.session_state: st.session_state.input_buffer = ""

# [애니메이션 카운터 변수] 아이가 손으로 누른 횟수 기억하기
if "plus_clicks" not in st.session_state: st.session_state.plus_clicks = 0
if "minus_clicks" not in st.session_state: st.session_state.minus_clicks = 0
if "last_action" not in st.session_state: st.session_state.last_action = ""

def generate_question(game_mode, level):
    st.session_state.char_key = random.choice(CHAR_KEYS)
    if game_mode == "1. 덧셈, 뺄셈": op = random.choice(["+", "-"])
    else: op = random.choice(["+", "-", "×", "÷"])
    st.session_state.operator = op
    
    if level == "1단계 (초급)":
        if op == "+":
            n1 = random.randint(1, 10)
            n2 = random.randint(1, 10)
        else:
            n1 = random.randint(2, 14) # 14-7 예시 수용하도록 조율
            n2 = random.randint(1, n1)
    else:
        n1, n2 = random.randint(10, 50), random.randint(1, 9)

    st.session_state.num1, st.session_state.num2 = n1, n2
    st.session_state.needs_new_question = False
    st.session_state.input_buffer = ""
    st.session_state.plus_clicks = 0
    st.session_state.minus_clicks = 0
    st.session_state.last_action = ""

# 설정창
game_mode = st.sidebar.selectbox("연산 선택", ["1. 덧셈, 뺄셈", "2. 덧셈, 뺄셈, 곱셈, 나눗셈"])
level = st.sidebar.selectbox("난이도 선택", ["1단계 (초급)", "2단계 (중급)", "3단계 (고급)"])

if st.session_state.needs_new_question:
    generate_question(game_mode, level)

# 상단 인터페이스
st.markdown("<h1>🎨 말랑말랑 수학</h1>", unsafe_allow_html=True)
st.markdown(f"<div class='score-box'><h2>✨ 점수: {st.session_state.score}점 ✨</h2></div>", unsafe_allow_html=True)

char_url = CHARACTER_URLS[st.session_state.char_key]
n1, n2, op = st.session_state.num1, st.session_state.num2, st.session_state.operator

# 문제 출제
st.markdown(f"<div class='quiz-text'>{n1} {op} {n2} = ?</div>", unsafe_allow_html=True)
st.markdown("---")

# 4. [체험형 덧셈/뺄셈 인터랙티브 힌트 영역]
if level == "1단계 (초급)":
    st.markdown("<div class='hint-title'>💡 그림을 터치해서 직접 계산해봐요!</div>", unsafe_allow_html=True)
    
    # 💥 효과음 대용 날아가는 풍선 이펙트 마크업
    if st.session_state.last_action == "minus":
        st.markdown(f"<div class='balloon-pop' style='left:50%; top:35%;'>-{st.session_state.minus_clicks} 🎈</div>", unsafe_allow_html=True)
    elif st.session_state.last_action == "plus":
        st.markdown(f"<div class='balloon-pop' style='left:50%; top:35%;'>+{st.session_state.plus_clicks} 🎈</div>", unsafe_allow_html=True)

    # --- 뺄셈 모드 (-1, -2 풍선 날리기) ---
    if op == "-":
        # 남은 개수 계산 (전체에서 누른 만큼 제외)
        visible_count = max(0, n1 - st.session_state.minus_clicks)
        
        # 5개씩 묶어서 그리기
        html = "<div style='text-align: center;'>"
        for i in range(visible_count // 5):
            html += "<div class='five-group'>" + f'<img src="{char_url}" class="char-img">'*5 + "</div>"
        if visible_count % 5 > 0:
            html += "<div class='five-group'>" + f'<img src="{char_url}" class="char-img">'*(visible_count%5) + "</div>"
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)
        
        # 보이지 않게 지워진 것들은 회색 빈칸 처리
        if st.session_state.minus_clicks > 0:
            st.markdown(f"<p style='text-align:center; margin:0; font-size:0.75rem; color:#FF477E;'>{st.session_state.minus_clicks}개 지워짐!</p>", unsafe_allow_html=True)
            
        # [터치 트리거] 동물/과일을 누르면 하나씩 없어지는 가상 버튼
        if visible_count > 0:
            if st.button("👇 과일/동물 꾹 누르기 (하나씩 지우기)", key="sub_click"):
                st.session_state.minus_clicks += 1
                st.session_state.last_action = "minus"
                st.rerun()
                
    # --- 덧셈 모드 (그림자 칸 채우며 +1, +2 풍선 띄우기) ---
    elif op == "+":
        # n1은 기본 오픈
        st.markdown("<div style='text-align:center; font-size:0.7rem; margin:0;'>[앞의 수만큼]</div>", unsafe_allow_html=True)
        html_n1 = "<div style='text-align: center;'>"
        for _ in range(n1 // 5): html_n1 += "<div class='five-group'>" + f'<img src="{char_url}" class="char-img">'*5 + "</div>"
        if n1 % 5 > 0: html_n1 += "<div class='five-group'>" + f'<img src="{char_url}" class="char-img">'*(n1%5) + "</div>"
        html_n1 += "</div>"
        st.markdown(html_n1, unsafe_allow_html=True)
        
        st.markdown("<div style='text-align:center; font-size:0.7rem; margin:0;'>➕ [뒤의 수만큼 채우기]</div>", unsafe_allow_html=True)
        
        # 뒤의 수(n2)만큼 검은 그림자 칸을 만들고, 아이가 클릭한 만큼 실물로 복원
        filled = st.session_state.plus_clicks
        unfilled = max(0, n2 - filled)
        
        html_n2 = "<div style='text-align: center;'>"
        # 5개 단위 그룹 계산을 위해 전체 채울 영역 구조화
        all_items = [f'<img src="{char_url}" class="char-img">' for _ in range(filled)] + [f'<div class="shadow-img" style="display:inline-block;"><img src="{char_url}" style="width:100%; filter:brightness(0); opacity:0.2;"></div>' for _ in range(unfilled)]
        
        # 5개씩 쪼개서 담기
        for i in range(0, len(all_items), 5):
            chunk = all_items[i:i+5]
            html_n2 += "<div class='five-group'>" + "".join(chunk) + "</div>"
        html_n2 += "</div>"
        st.markdown(html_n2, unsafe_allow_html=True)
        
        if unfilled > 0:
            if st.button("👇 그림자 빈칸 꾹 누르기 (하나씩 채우기)", key="add_click"):
                st.session_state.plus_clicks += 1
                st.session_state.last_action = "plus"
                st.rerun()
                
    st.markdown("---")
else:
    st.markdown("<p style='text-align: center; color: #88AABB; margin:0; font-size:0.8rem;'>머릿속으로 주머니를 계산해요! 💪</p>", unsafe_allow_html=True)
    st.markdown("---")

# 정답 모니터 창
disp = st.session_state.input_buffer if st.session_state.input_buffer else "?"
st.markdown(f"<div class='ans-display'>{disp}</div>", unsafe_allow_html=True)

# --- 5×2 레이아웃 + 우측 세로형 기능 버튼 [게임기 네모칸 일체형] ---
st.markdown("<div class='keypad-container'>", unsafe_allow_html=True)

# 메인 레이아웃 쪼개기: 왼쪽은 숫자 영역(col_left), 오른쪽은 버튼 영역(col_right)
col_left, col_right = st.columns([4, 1])

with col_left:
    # 숫자 패드 1층: 0, 1, 2, 3, 4
    r1_1, r1_2, r1_3, r1_4, r1_5 = st.columns(5)
    with r1_1:
        if st.button("0"):
            if st.session_state.input_buffer: st.session_state.input_buffer += "0"; st.rerun()
    with r1_2:
        if st.button("1"): st.session_state.input_buffer += "1"; st.rerun()
    with r1_3:
        if st.button("2"): st.session_state.input_buffer += "2"; st.rerun()
    with r1_4:
        if st.button("3"): st.session_state.input_buffer += "3"; st.rerun()
    with r1_5:
        if st.button("4"): st.session_state.input_buffer += "4"; st.rerun()

    # 숫자 패드 2층: 5, 6, 7, 8, 9
    r2_1, r2_2, r2_3, r2_4, r2_5 = st.columns(5)
    with r2_1:
        if st.button("5"): st.session_state.input_buffer += "5"; st.rerun()
    with r2_2:
        if st.button("6"): st.session_state.input_buffer += "6"; st.rerun()
    with r2_3:
        if st.button("7"): st.session_state.input_buffer += "7"; st.rerun()
    with r2_4:
        if st.button("8"): st.session_state.input_buffer += "8"; st.rerun()
    with r2_5:
        if st.button("9"): st.session_state.input_buffer += "9"; st.rerun()

with col_right:
    # 우측 위: 지우기 버튼
    st.markdown("<div class='clear-btn'>", unsafe_allow_html=True)
    if st.button("지우기"): 
        st.session_state.input_buffer = ""
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 우측 아래: 제출 버튼
    st.markdown("<div class='ok-btn'>", unsafe_allow_html=True)
    submit_btn = st.button("제출")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True) # 네모칸 닫기

# 정답 및 오답 판정 시스템
if submit_btn:
    if st.session_state.input_buffer:
        ans = int(st.session_state.input_buffer)
        correct = (n1 + n2) if op == "+" else (n1 - n2)
        if ans == correct:
            st.session_state.score += 10
            st.balloons()
            st.success("🎉 정답입니다! 참 잘했어요!")
            st.session_state.needs_new_question = True
            time.sleep(0.6); st.rerun()
        else:
            st.error("😮 다시 한번 세어보아요!")
            st.session_state.input_buffer = ""
            st.session_state.plus_clicks = 0
            st.session_state.minus_clicks = 0
            time.sleep(0.6); st.rerun()