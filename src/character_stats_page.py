import requests
import streamlit as st
import pandas as pd

from url import create_url


def show_loser_history_by_character(character_name):
    st.title("꼴찌한 전체 데이터")

    response = requests.get(create_url("/races/loser-history"), params={"character_name": character_name})
    if response.status_code == 200:
        loser_history = response.json()
        df = pd.DataFrame(loser_history)
        df = df[["created_at", "group_uuid", "character_name", "total_rank"]]
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.error(f"데이터를 가져오지 못했습니다. error_code: {response.status_code}")