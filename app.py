import streamlit as st
from PIL import Image
import os
import json

# 라벨링 옵션
options = [
    ["스쿠프넥", "라운드넥", "브이넥", "터틀넥", "카라넥", "오프숄더", "기타"],
    ["민소매", "반팔", "7부", "긴팔", "기타"],
    ["크롭", "넣어입기", "일반", "기타"],
]

# 이미지 폴더 경로 설정
image_folder = "./dataset/"
images = os.listdir(image_folder)
total_images = len(images)

# 라벨링 데이터를 저장할 JSON 파일
json_file = "result.json"

# 라벨링 데이터 초기화
if not os.path.exists(json_file):
    with open(json_file, "w") as file:
        json.dump({}, file)

# 현재 이미지 인덱스를 관리하는 Session State
if "current_image_index" not in st.session_state:
    st.session_state.current_image_index = 0
if "labels" not in st.session_state:
    st.session_state.labels = [None, None, None]


# 이미지 라벨링 함수
def label_image(image_path, labels):
    with open(json_file, "r") as file:
        data = json.load(file)

    data[os.path.basename(image_path)] = labels

    with open(json_file, "w") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


# 이전 이미지로 넘어가는 함수
def prev_image():
    if st.session_state.current_image_index > 0:
        st.session_state.current_image_index -= 1
        st.session_state.labels = [None, None, None]
        st.experimental_rerun()
    else:
        st.warning("This is the first image.")


# 다음 이미지로 넘어가는 함수
def next_image():
    if st.session_state.current_image_index < total_images - 1:
        st.session_state.current_image_index += 1
        st.session_state.labels = [None, None, None]
        st.experimental_rerun()
    else:
        st.success("All images have been labeled.")


# 현재 이미지 불러오기
current_image_path = os.path.join(
    image_folder, images[st.session_state.current_image_index]
)
current_image = Image.open(current_image_path)
current_image = current_image.resize((200, 200))

# 이전 이미지 불러오는 버튼
if st.button("Previous"):
    prev_image()


# 이미지와 진행 상황 표시
st.image(current_image)
progress_bar = st.progress(st.session_state.current_image_index / total_images)
st.write(f"Image {st.session_state.current_image_index + 1} of {total_images}")
st.write(
    " | ".join(map(lambda x: x if x is not None else "None", st.session_state.labels))
)


# 사용자 입력 받기
for i in range(len(options)):
    for j, col in enumerate(st.columns(len(options[i]), gap="small")):
        with col:
            if st.button(
                options[i][j],
                key=f"label_{i}_{options[i][j]}",
            ):
                st.session_state.labels[i] = options[i][j]
                st.experimental_rerun()


# 세 개의 라벨이 모두 선택되었는지 확인하고 다음 이미지로 넘어감
if all(st.session_state.labels):
    label_image(current_image_path, st.session_state.labels)
    next_image()
