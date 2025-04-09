import streamlit as st
from main_page import show_main
from character_stats_page import show_loser_history_by_character
from utils import add_new_line
from stats_page import show_today_losers, show_recent_games, show_recent_losers, show_all_tracks_count

main_page_str = "순위 저장"
stats_page_str = "통계"
character_stats_page_str = "캐릭터별 통계"

page = st.sidebar.radio(
    "페이지를 선택하세요",
    [
        main_page_str,
        stats_page_str,
        character_stats_page_str,
    ]
)

if page == main_page_str:
    show_main()
elif page == stats_page_str:
    show_today_losers()
    add_new_line()

    show_recent_losers()
    add_new_line()

    show_all_tracks_count()
    add_new_line()

    show_recent_games()
elif page == character_stats_page_str:
    with st.form("character_form"):
        character_name = st.text_input("캐릭터명을 입력하세요")
        submitted = st.form_submit_button("확인")

    if submitted:
        show_loser_history_by_character(character_name)

