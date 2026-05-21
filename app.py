import streamlit as st
import random

# 페이지 기본 설정 (스마트폰 최적화 및 타이틀 아이콘 변경)
st.set_page_config(page_title="말랑말랑 레벨업 수학", page_icon="🎨", layout="centered")

# --- [디자인 치트키] 알록달록 파스텔톤 테마 적용 ---
st.markdown("""
<style>
    /* 전체 배경색: 따뜻한 파스텔크림 */
    .stApp {
        background-color: #FAF8F1;
    }
    /* 사이드바 배경색: 파스텔라벤더 */
    [data-testid="stSidebar"] {
        background-color: #E6E6FA;
    }
    /* 큰 타이틀 텍스트: 말랑말랑한 폰트 느낌 */
    h1 {
        color: #554488;
        font-family: 'MapleStory', sans-serif;
    }
    /* 서브 타이틀: 진한 파스텔블루 */
    h3 {
        color: #4466AA;
    }
    /* 점수판 박스 디자인 */
    .score-box {
        background-color: #FFE0F0; /* 파스텔핑크 */
        padding: 10px;
        border-radius: 15px;
        border: 2px solid #FFC0CB;
        text-align: center;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- [캐릭터 치트키] 말랑말랑한 귀여운 일러스트 아이콘 (Flaticon 이미지 URL 사용) ---
# ※ 이 이미지는 무료 아이콘 사이트인 Flaticon의 이미지를 참고용으로 사용했습니다.
CHARACTER_URLS = {
    "bunny": "https://cdn-icons-png.flaticon.com/512/3261/3261168.png", # 말랑토끼
    "bear": "https://cdn-icons-png.flaticon.com/512/1000/1000966.png",  # 말랑곰
    "apple": "https://cdn-icons-png.flaticon.com/512/2909/2909787.png", # 말랑사과
    "berry": "https://cdn-icons-png.flaticon.com/512/2316/2316886.png", # 말랑딸기
    "cat": "https://cdn-icons-png.flaticon.com/512/616/616430.png",    # 말랑고양이
    "duck": "https://cdn-icons-png.flaticon.com/512/4392/4392476.png"   # 말랑오리
}
CHAR_KEYS = list(CHARACTER_URLS.keys())

# 세션 상태(기억장치) 초기화
if "score" not in st.session_state:
    st.session_state.score = 0
if "num1" not in st.session_state:
    st.session_state.num1 = 0
if "num2" not in st.session_state:
    st.session_state.num2 = 0
if "operator" not in st.session_state:
    st.session_state.operator = "+"
if "char_key" not in st.session_state:
    st.session_state.char_key = random.choice(CHAR_KEYS)
if "message" not in st.session_state:
    st.session_state.message = ""
if "msg_type" not in st.session_state:
    st.session_state.msg_type = "info"
if "needs_new_question" not in st.session_state:
    st.session_state.needs_new_question = True

# 문제 생성 함수
def generate_question(game_mode, level):
    st.session_state.char_key = random.choice(CHAR_KEYS)
    
    if game_mode == "1. 덧셈, 뺄셈":
        op = random.choice(["+", "-"])
    else:
        op = random.choice(["+", "-", "×", "÷"])
        
    st.session_state.operator = op
    
    if op in ["+", "-"]:
        if level == "1단계 (초급)":
            if op == "+":
                n1, n2 = random.randint(0, 10), random.randint(0, 10) # 1학년 난이도로 더 하향조절
            else:
                n1 = random.randint(0, 20)
                n2 = random.randint(0, n1)
        elif level == "2단계 (중급)":
            if op == "+":
                n1, n2 = random.randint(0, 50), random.randint(0, 50)
            else:
                n1 = random.randint(0, 100)
                n2 = random.randint(0, n1)
        else: # 3단계 고급
            n1, n2 = random.randint(0, 500), random.randint(0, 500)
                
    elif op == "×":
        if level == "1단계 (초급)":
            n1, n2 = random.randint(1, 9), random.randint(1, 5)
        elif level == "2단계 (중급)":
            n1, n2 = random.randint(2, 19), random.randint(1, 10)
        else:
            n1, n2 = random.randint(10, 50), random.randint(2, 20)
            
    elif op == "÷":
        if level == "1단계 (초급)":
            n2 = random.randint(1, 5)
            ans = random.randint(1, 5)
            n1 = n2 * ans
        elif level == "2단계 (중급)":
            n2 = random.randint(2, 9)
            ans = random.randint(2, 10)
            n1 = n2 * ans
        else:
            n2 = random.randint(5, 20)
            ans = random.randint(5, 30)
            n1 = n2 * ans

    st.session_state.num1 = n1
    st.session_state.num2 = n2
    st.session_state.needs_new_question = False

# 사이드바 설정창 (파스텔색 적용)
st.sidebar.markdown("<h2 style='color: #6644AA;'>⚙️ 게임 설정</h2>", unsafe_allow_html=True)
game_mode = st.sidebar.selectbox("연산 종류 선택", ["1. 덧셈, 뺄셈", "2. 덧셈, 뺄셈, 곱셈, 나눗셈"])
level = st.sidebar.selectbox("난이도 선택", ["1단계 (초급)", "2단계 (중급)", "3단계 (고급)"])

if st.sidebar.button("🎨 새로운 게임 시작하기") or st.session_state.needs_new_question:
    generate_question(game_mode, level)

# 메인 화면 디자인
st.markdown("<h1 style='text-align: center;'>🎨 말랑말랑 레벨업 수학</h1>", unsafe_allow_html=True)

# 점수판 (알록달록 박스)
st.markdown(f"""
<div class='score-box'>
    <h4 style='color: #EE6688; margin: 0;'>현재 설정: {game_mode} / {level}</h4>
    <h2 style='color: #CC4488; margin: 5px 0;'>✨ 내 점수: {st.session_state.score}점 ✨</h2>
</div>
""", unsafe_allow_html=True)

# 현재 문제 불러오기
char_key = st.session_state.char_key
char_url = CHARACTER_URLS[char_key]
n1 = st.session_state.num1
n2 = st.session_state.num2
op = st.session_state.operator

# 정답 계산
if op == "+": correct = n1 + n2
elif op == "-": correct = n1 - n2
elif op == "×": correct = n1 * n2
elif op == "÷": correct = n1 // n2

# 문제 대형 표시 (색상 변경)
st.markdown("<h1 style='text-align: center; color: #6644AA; font-size: 75px;'> %d %s %d = ? </h1>" % (n1, op, n2), unsafe_allow_html=True)
st.markdown("---")

# [핵심 변경] 초급 단계에서만 귀여운 캐릭터 일러스트 힌트 제공
if level == "1단계 (초급)":
    st.markdown("### 💡 말랑말랑 힌트 창")
    
    # 캐릭터 이미지를 가로로 나열하는 HTML
    if op == "+":
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**앞의 숫자 ({n1}) 만큼:**")
            html_str = "".join([f'<img src="{char_url}" width="35" style="margin: 2px;">' for _ in range(n1)])
            st.markdown(html_str, unsafe_allow_html=True)
        with col2:
            st.markdown(f"**뒤의 숫자 ({n2}) 만큼:**")
            html_str = "".join([f'<img src="{char_url}" width="35" style="margin: 2px;">' for _ in range(n2)])
            st.markdown(html_str, unsafe_allow_html=True)
            
    elif op == "-":
        st.markdown(f"**전체 {n1}개 중에서 {n2}개를 지워보세요!**")
        html_str = "".join([f'<img src="{char_url}" width="40" style="margin: 3px;">' for _ in range(n1)])
        st.markdown(html_str, unsafe_allow_html=True)
        
    elif op == "×":
        st.markdown(f"**{n1}개씩 {n2} 묶음이에요!**")
        for i in range(n2):
            html_str = f"📍 {i+1}층: " + "".join([f'<img src="{char_url}" width="30" style="margin: 2px;">' for _ in range(n1)])
            st.markdown(html_str, unsafe_allow_html=True)
            
    elif op == "÷":
        st.markdown(f"**전체 {n1}개를 {n2}명이 똑같이 나누어 가질 거예요.**")
        st.image(char_url, width=60, caption="이 귀여운 친구들이 나눠 가져요!")
    st.markdown("---")
else:
    st.markdown("<p style='text-align: center; color: #88AABB;'>중급/고급 단계는 그림 힌트 없이 머릿속으로 계산해봐요! 💪</p>", unsafe_allow_html=True)
    st.markdown("---")

# 정답 입력창 및 확인 버튼 (디자인 변경)
with st.form(key="game_form", clear_on_submit=True):
    user_ans = st.number_input("정답 숫자를 적고 확인 버튼을 눌러주세요!", min_value=0, max_value=2000, step=1, value=0)
    
    # 버튼 색상 변경 (파스텔블루)
    st.markdown("""
    <style>
        div.stButton > button:first-child {
            background-color: #55AADD;
            color: white;
            border-radius: 20px;
            border: none;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)
    submit_btn = st.form_submit_button(label="정답 확인! 👍")

# 정답 피드백 메시지 (알록달록 풍선)
if submit_btn:
    if user_ans == correct:
        st.session_state.score += 10
        st.session_state.message = f"🎉 딩동댕! 정답이에요! [{n1} {op} {n2} = {correct}] 참 잘했어요! (+10점)"
        st.session_state.msg_type = "success"
        st.session_state.needs_new_question = True
        st.rerun()
    else:
        st.session_state.message = "😮 조금만 더 생각해볼까요? 숫자를 다시 확인해보세요!"
        st.session_state.msg_type = "error"

# 결과 피드백 메시지 띄우기 (알록달록)
if st.session_state.message:
    if st.session_state.msg_type == "success":
        st.balloons() # 성공 시 풍선 애니메이션 추가
        st.success(st.session_state.message)
    else:
        st.error(st.session_state.message)