import streamlit as st
import requests
import pandas as pd

from url import create_url


def show_today_losers():
    st.markdown("""
    <h2 style='text-align: center; color: orange; font-style: italic;'>
        🐌 오늘도 음료수를 지원해주신 <span style='color: tomato;'>꼴찌들!</span>
    </h2>
    """, unsafe_allow_html=True)
    st.caption("하루동안 내기를 2판 이상 한 경우에는 꼴찌가 2명 이상 표기됩니다.")


def show_recent_losers():
    st.title("최근 꼴찌들")
    response = requests.get(create_url("/races/recent-losers"))

    if response.status_code == 200:
        losers_data = response.json()

        df = pd.DataFrame(losers_data)
        df["created_at"] = pd.to_datetime(df["created_at"]).dt.strftime("%Y-%m-%d %H:%M")
        df = df[["created_at", "group_uuid", "character_name", "total_rank"]]
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.error(f"데이터를 가져오지 못했습니다. error_code: {response.status_code}")


def show_recent_games():
    st.title("최근 경기 기록")
    response = requests.get(create_url("/races/recent-races"))

    if response.status_code == 200:
        race_data = response.json()

        for race in race_data:
            st.subheader(race["track_name"])
            created_at = pd.to_datetime(race["created_at"]).strftime("%Y-%m-%d %H:%M")
            st.caption(f"{created_at}")

            df = pd.DataFrame(race["results"])
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.divider()
    else:
        st.error(f"데이터를 가져오지 못했습니다. error_code: {response.status_code}")
