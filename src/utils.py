import streamlit as st


def add_new_line():
    st.markdown("<br><br>", unsafe_allow_html=True)


def number_to_korean(num: int) -> str:
    if num < 1 or num > 10:
        return f"{num}번째"

    words = ["첫번째", "두번째", "세번째", "네번째", "다섯번째", "여섯번째", "일곱번째", "여덟번째", "아홉번째", "열번째"]
    return words[num - 1]
