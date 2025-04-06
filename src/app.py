import streamlit as st
from main_page import show_main
from utils import add_new_line
from stats_page import show_today_losers, show_recent_games, show_recent_losers

main_page_str = "순위 저장"
stats_page_str = "통계"

page = st.sidebar.radio(
    "페이지를 선택하세요",
    [
        main_page_str,
        stats_page_str,
    ]
)

if page == main_page_str:
    show_main()
elif page == stats_page_str:
    show_today_losers()
    add_new_line()

    show_recent_losers()
    add_new_line()

    show_recent_games()
