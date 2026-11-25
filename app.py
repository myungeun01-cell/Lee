import streamlit as st
import random

# 페이지 설정
st.set_page_config(page_title="숫자 야구 게임", page_icon="⚾")

# 게임 초기화 함수
def init_game():
    st.session_state.target = random.sample(range(0, 10), 3)
    st.session_state.attempts = []
    st.session_state.game_over = False

# 세션 상태 초기화 (앱 최초 실행 시)
if 'target' not in st.session_state:
    init_game()

st.title("⚾ 숫자 야구 게임")
st.write("서로 다른 **3자리 숫자**를 맞춰보세요! (0~9 사용)")

# 새 게임 버튼
if st.button("🔄 새 게임 시작"):
    init_game()
    st.rerun()

# 게임 진행 폼 (엔터키 입력 지원)
if not st.session_state.game_over:
    with st.form(key='guess_form', clear_on_submit=True):
        guess_str = st.text_input("3자리 숫자를 입력하세요 (예: 123)", max_chars=3)
        submit_button = st.form_submit_button(label="던지기! ⚾")

    if submit_button:
        # 입력값 검증
        if len(guess_str) != 3 or not guess_str.isdigit():
            st.error("정확히 3자리 숫자를 입력해주세요.")
        elif len(set(guess_str)) != 3:
            st.error("중복되지 않는 서로 다른 숫자를 입력해주세요.")
        else:
            guess = [int(d) for d in guess_str]
            target = st.session_state.target
            
            # 스트라이크, 볼 판정
            strikes = sum(1 for g, t in zip(guess, target) if g == t)
            balls = sum(1 for g in guess if g in target) - strikes
            
            # 결과 기록
            if strikes == 3:
                result = "🎉 3 STRIKE! 홈런!"
                st.session_state.game_over = True
            elif strikes == 0 and balls == 0:
                result = "OUT ❌"
            else:
                result = f"{strikes}S {balls}B"
                
            st.session_state.attempts.insert(0, (guess_str, result))

# 정답 맞췄을 때 축하 효과
if st.session_state.game_over:
    st.balloons()
    st.success(f"축하합니다! {len(st.session_state.attempts)}번 만에 정답({''.join(map(str, st.session_state.target))})을 맞췄습니다!")

# 이전 시도 기록 출력
if st.session_state.attempts:
    st.subheader("📋 기록지")
    for idx, (g, res) in enumerate(st.session_state.attempts):
        attempt_num = len(st.session_state.attempts) - idx
        st.write(f"**{attempt_num}회차:** `{g}` ➔ **{res}**")
