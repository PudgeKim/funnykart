import requests
from PIL import Image

from clova import request_to_clova
from characters import all_characters
from url import create_url
from tracks import all_tracks
from utils import *


def show_main():
    track_key = "selected_track_"
    screenshot_key = "screenshot_"

    if st.session_state.get("reset"):
        for i in range(7):
            st.session_state[f"{track_key}{i}"] = "트랙을 선택하세요"
        st.session_state["reset"] = False

    st.title("이클립스 서버 카트 내기")
    add_new_line()

    empty_count = 0
    selected_total_count = st.selectbox("총 몇판 했는지 선택하세요.", [empty_count, 1, 2, 3, 4, 5, 6, 7])
    add_new_line()

    empty_track = "트랙을 선택하세요"
    selected_track_list = []
    uploaded_screenshot_list = []

    for i in range(selected_total_count):
        tracks = [empty_track] + all_tracks
        korean_num = number_to_korean(i + 1)
        selected_track = st.selectbox(
            f"{korean_num} 플레이한 트랙을 선택하세요.",
            tracks,
            key=f"{track_key}{i}"
        )
        selected_track_list.append(selected_track)

        screenshot = st.file_uploader(
            f"{korean_num} 랭킹 스크린샷을 첨부하세요.",
            type=["png", "jpg", "jpeg"],
            key=f"{screenshot_key}{i}"
        )
        uploaded_screenshot_list.append(screenshot)

        if screenshot is not None:
            image = Image.open(screenshot)
            st.image(image, caption="업로드된 랭킹", use_container_width=True)

        add_new_line()

    # 저장 버튼을 오른쪽에 배치하기 위함
    left, right = st.columns([10, 1])
    with right:
        is_clicked = st.button("저장")

    if is_clicked:
        for i in range(len(selected_track_list)):
            track = selected_track_list[i]
            korean_num = number_to_korean(i + 1)
            if track == empty_track:
                st.warning(f"{korean_num} 트랙이 선택되지 않았습니다.")
                return

        for i in range(len(uploaded_screenshot_list)):
            screenshot = uploaded_screenshot_list[i]
            korean_num = number_to_korean(i + 1)
            if screenshot is None:
                st.warning(f"{korean_num} 랭킹이 첨부되지 않았습니다.")
                return

        race_results = []

        for screenshot_idx in range(len(uploaded_screenshot_list)):
            uploaded_screenshot = uploaded_screenshot_list[screenshot_idx]
            clova_response = request_to_clova(uploaded_screenshot).json()
            clova_images = clova_response["images"]

            image = clova_images[0]
            image_name = image["name"]
            result = image["inferResult"]
            if result != 'SUCCESS':
                st.error(f"클로바 이미지 파싱 실패! image_name: {image_name}")
                return

            rank_list = []
            character_name_list = []
            finish_time_list = []

            fields = image["fields"]
            fields_length = len(fields)
            current_rank = 1
            current_index = 0

            while current_index < fields_length:
                field = fields[current_index]
                infer_text = field["inferText"]

                if infer_text in all_characters:
                    character_name_list.append(infer_text)
                    rank_list.append(current_rank)
                    current_rank += 1

                current_index += 1

            race_result = []
            for character_idx in range(len(character_name_list)):
                character_name = character_name_list[character_idx]
                rank = rank_list[character_idx]
                race_result.append({
                    "rank": rank,
                    "character_name": character_name
                })

            race_results.append({
                "track_name": selected_track_list[screenshot_idx],
                "results": race_result
            })

        response = requests.post(create_url("/races"), json=race_results)
        if response.status_code == 200:
            st.success("저장되었습니다")
            selected_track_list.clear()
            uploaded_screenshot_list.clear()
            st.session_state["reset"] = True
        else:
            st.error(f"저장 실패! error_code: {response.status_code}")
