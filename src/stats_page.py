import streamlit as st
import requests

from url import create_url


def show_today_losers():
    st.title("오늘의 꼴찌")


def show_recent_games():
    st.title("최근 경기 기록")
    response = requests.get(create_url("/races/recent-races"))

    if response.status_code == 200:
        race_data = response.json()

        for race in race_data:
            st.subheader(race["track_name"])
            st.write("날짜:", race["created_at"])

            st.markdown("**순위**")
            for result in race["results"]:
                st.write(f'{result["rank"]}위: {result["character_name"]} - {result["finish_time"]}')
            st.divider()
    else:
        st.error(f"데이터를 가져오지 못했습니다. error_code: {response.status_code}")
