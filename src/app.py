from PIL import Image
from tracks import all_tracks
from utils import *

st.title("이클립스 서버 카트 대결")
add_new_line()

empty_count = 0
selected_total_count = st.selectbox("총 몇판 했는지 선택하세요.", [empty_count, 1, 2, 3, 4, 5, 6, 7])
add_new_line()

empty_track = "트랙을 선택하세요"
selected_track_list = []
uploaded_screenshot_list = []

for i in range(selected_total_count):
    tracks = [empty_track] + all_tracks
    korean_num = number_to_korean(i+1)
    selected_track = st.selectbox(
        f"{korean_num} 플레이한 트랙을 선택하세요.",
        tracks,
        key=f"selected_track_{i}"
    )
    selected_track_list.append(selected_track)

    screenshot = st.file_uploader(
        f"{korean_num} 랭킹 스크린샷을 첨부하세요.",
        type=["png", "jpg", "jpeg"],
        key=f"screenshot_{i}"
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
        korean_num = number_to_korean(i+1)
        if track == empty_track:
            st.warning(f"{korean_num} 트랙이 선택되지 않았습니다.")

    for i in range(len(uploaded_screenshot_list)):
        screenshot = uploaded_screenshot_list[i]
        korean_num = number_to_korean(i+1)
        if screenshot is None:
            st.warning(f"{korean_num} 랭킹이 첨부되지 않았습니다.")