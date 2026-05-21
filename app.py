import streamlit as st
import random

# 페이지 기본 설정 (스마트폰 화면에 맞춤)
st.set_page_config(page_title="말랑말랑 수학 게임", page_icon="🍎", layout="centered")

# 귀여운 캐릭터 목록
CHARACTERS = ["🍎", "🍌", "🍓", "🍉", "🥕", "🥦", "🐱", "🐶", "🦁", "🐰", "🐻", "🐥"]

# 세션 상태(컴퓨터의 기억장치) 초기화
if "score" not in st.session_state:
    st.session_state.score = 0
if "num1" not in st.session_state:
    st.session_state.num1 = random.randint(1, 8)
if "num2" not in st.session_state:
    st.session_state.num2 = random.randint(1, 10 - st.session_state.num1)
if "operator" not in st.session_state:
    st.session_state.operator = random.choice(["+", "-"])
    if st.session_state.operator == "-":
        st.session_state.num1 = random.randint(2, 10)
        st.session_state.num2 = random.randint(1, st.session_state.num1 - 1)
if "char_pic" not in st.session_state:
    st.session_state.char_pic = random.choice(CHARACTERS)
if "message" not in st.session_state:
    st.session_state.message = ""
if "msg_type" not in st.session_state:
    st.session_state.msg_type = "info"

def next_question():
    st.session_state.char_pic = random.choice(CHARACTERS)
    st.session_state.operator = random.choice(["+", "-"])
    if st.session_state.operator == "+":
        st.session_state.num1 = random.randint(1, 8)
        st.session_state.num2 = random.randint(1, 10 - st.session_state.num1)
    else:
        st.session_state.num1 = random.randint(2, 10)
        st.session_state.num2 = random.randint(1, st.session_state.num1 - 1)

# 화면 디자인 구성
st.title("🎮 말랑말랑 동물 과일 수학 게임")
st.subheader(f"✨ 내 점수: {st.session_state.score}점 ✨")

# 시각적 힌트 그림 그려주기
char = st.session_state.char_pic
n1 = st.session_state.num1
n2 = st.session_state.num2
op = st.session_state.operator

st.markdown("---")
if op == "+":
    st.markdown(f"### {char * n1}")
    st.markdown("## ➕ 더하기")
    st.markdown(f"### {char * n2}")
    correct = n1 + n2
else:
    st.markdown(f"### {char * n1}")
    st.markdown("## ➖ 빼기")
    st.markdown(f"### {char * n2}")
    correct = n1 - n2
st.markdown("---")

# 정답 입력받기 및 확인 버튼
with st.form(key="game_form", clear_on_submit=True):
    user_ans = st.number_input("정답은 무엇일까요? 숫자를 적어주세요!", min_value=0, max_value=20, step=1, value=0)
    submit_btn = st.form_submit_button(label="정답 확인! 👍")

if submit_btn:
    if user_ans == correct:
        st.session_state.score += 10
        st.session_state.message = "🎉 정답이에요! 참 잘했어요! (+10점)"
        st.session_state.msg_type = "success"
        next_question()
        st.rerun()
    else:
        st.session_state.message = "😮 조금만 더 생각해볼까요? 다시 한번 세어보세요!"
        st.session_state.msg_type = "error"

# 결과 피드백 메시지 띄우기
if st.session_state.message:
    if st.session_state.msg_type == "success":
        st.success(st.session_state.message)
    else:
        st.error(st.session_state.message)