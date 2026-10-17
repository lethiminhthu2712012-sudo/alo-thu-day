import base64
import random
import numpy as np
import streamlit as st

# 1. Cấu hình trang Streamlit
st.set_page_config(
    page_title="Game của Thucute 🌸",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
)


# 2. Hàm hỗ trợ đọc và chuyển đổi tệp sang Base64
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return ""


# Đọc ảnh nền toàn trang (Ảnh 6)
bg_img_b64 = get_base64_of_bin_file("assets/background.png")


# 3. Hàm phát hiệu ứng âm thanh
def play_sound(sound_file, loop=False, volume=0.5):
    sound_b64 = get_base64_of_bin_file(sound_file)
    if sound_b64:
        loop_attr = "loop" if loop else ""
        audio_html = f"""
            <audio autoplay {loop_attr} style="display:none;">
                <source src="data:audio/mp3;base64,{sound_b64}" type="audio/mp3">
            </audio>
            <script>
                var audioElements = document.getElementsByTagName('audio');
                if (audioElements.length > 0) {{
                    audioElements[audioElements.length - 1].volume = {volume};
                }}
            </script>
        """
        st.components.v1.html(audio_html, height=0)


# 4. CSS Tùy chỉnh giao diện hoa đào
custom_css = f"""
<style>
/* Dùng Ảnh 6 làm hình nền toàn bộ trang web */
.stApp {{
    background: url("data:image/png;base64,{bg_img_b64}") no-repeat center center fixed !important;
    background-size: cover !important;
}}

/* Tùy chỉnh Sidebar trong suốt */
[data-testid="stSidebar"] {{
    background-color: rgba(255, 255, 255, 0.75) !important;
    backdrop-filter: blur(6px);
    border-right: 2px solid #f2a6b4;
}}

/* Tùy chỉnh phong cách nút bấm chung */
.stButton > button {{
    background: linear-gradient(135deg, #f7a8b8, #e88299);
    color: white !important;
    font-size: 18px !important;
    font-weight: bold !important;
    border-radius: 20px !important;
    border: 2px solid #ffffff !important;
    padding: 8px 24px !important;
    box-shadow: 0px 4px 10px rgba(232, 130, 153, 0.4);
    transition: all 0.3s ease;
}}

.stButton > button:hover {{
    transform: scale(1.05);
    background: linear-gradient(135deg, #e88299, #d46b82);
    box-shadow: 0px 6px 15px rgba(232, 130, 153, 0.6);
}}

/* Khung trò chơi */
.game-container {{
    background-color: rgba(255, 255, 255, 0.65);
    border-radius: 20px;
    padding: 25px;
    border: 2px solid rgba(247, 178, 189, 0.8);
    box-shadow: 0 8px 20px rgba(0,0,0,0.05);
    backdrop-filter: blur(4px);
    text-align: center;
}}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 5. Khởi tạo Trạng thái Ứng dụng
if "page" not in st.session_state:
    st.session_state.page = "home"
if "current_game" not in st.session_state:
    st.session_state.current_game = "tile"
if "level" not in st.session_state:
    st.session_state.level = 1
if "bgm_enable" not in st.session_state:
    st.session_state.bgm_enable = True

# Bật nhạc nền BGM
if st.session_state.bgm_enable:
    play_sound("sounds_bgm.mp3", loop=True, volume=0.2)


# --- TRANG CHỦ (HOME PAGE - TÍCH HỢP CLICK TRỰC TIẾP VÀO BANNER) ---
def show_home():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2.5, 1])

    with col2:
        # Chuyển đổi ảnh Banner (Ảnh 1) thành dạng base64 để nhúng vào thẻ HTML có gắn sự kiện click
        banner_b64 = get_base64_of_bin_file("assets/home_banner.png")

        # Tạo một khung HTML chứa ảnh banner và hiệu ứng khi di chuột vào (tạo cảm giác nút bấm)
        click_banner_html = f"""
        <div style="text-align: center; cursor: pointer;" onclick="document.getElementById('hidden_play_btn').click();">
            <img src="data:image/png;base64,{banner_b64}" style="width: 100%; border-radius: 20px; box-shadow: 0 10px 25px rgba(232, 130, 153, 0.4); transition: transform 0.2s ease;" onmouseover="this.style.transform='scale(1.02)';" onmouseout="this.style.transform='scale(1.0)';">
        </div>
        """
        st.markdown(click_banner_html, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Nút bấm phụ ẩn/hiện ngay dưới banner để đồng bộ sự kiện chuyển trang khi click vào ảnh
        # (Streamlit xử lý sự kiện Python thông qua nút này khi HTML kích hoạt)
        if st.button(
            "🌸 BẮT ĐẦU CHƠI NGAY (PLAY NOW) 🌸", key="hidden_play_btn"
        ):
            play_sound("sounds_click.mp3", volume=0.6)
            st.session_state.page = "game"
            st.rerun()


# --- CÁC TRÒ CHƠI ---


# Game 1: Tile Match
def play_tile_game(level):
    st.markdown(
        f"<div class='game-container'><h3>🌸 Tile Match - Màn {level}</h3><p>Ghép 3 hình giống nhau để xóa khỏi khay!</p></div>",
        unsafe_allow_html=True,
    )

    icons = ["🌸", "🌺", "🌹", "🌻", "🌼", "🌷", "🍁"][: level + 2]
    st.write("---")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("### Các ô hoa trên bàn chơi:")
        grid = [random.choice(icons) for _ in range(level * 4)]
        st.write(" ".join([f"[{icon}]" for icon in grid]))

    with col2:
        if st.button("Hoàn thành màn 🎉"):
            play_sound("sounds_win.mp3", volume=0.8)
            if level < 5:
                st.success(f"Chúc mừng bạn vượt qua màn {level}!")
                st.session_state.level = level + 1
            else:
                st.balloons()
                st.success("Bạn đã chiến thắng toàn bộ 5 màn Tile Match! 🎉")

        if st.button("Thử lại / Thua ❌"):
            play_sound("sounds_lose.mp3", volume=0.7)
            st.error("Rất tiếc! Hãy thử lại màn này nhé!")


# Game 2: Sudoku
def play_sudoku_game(level):
    st.markdown(
        f"<div class='game-container'><h3>🌸 Floral Sudoku - Màn {level}</h3><p>Điền số từ 1 đến 4 vào lưới!</p></div>",
        unsafe_allow_html=True,
    )

    boards = {
        1: [[1, 2, 3, 0], [3, 4, 0, 2], [0, 1, 4, 3], [4, 0, 2, 1]],
        2: [[1, 0, 0, 4], [0, 4, 1, 0], [0, 3, 2, 0], [2, 0, 0, 1]],
        3: [[0, 2, 0, 0], [0, 0, 4, 0], [0, 1, 0, 0], [0, 0, 3, 0]],
        4: [[0, 0, 3, 0], [1, 0, 0, 0], [0, 0, 0, 2], [0, 4, 0, 0]],
        5: [[0, 0, 0, 0], [0, 2, 0, 1], [3, 0, 4, 0], [0, 0, 0, 0]],
    }
    board = boards.get(level, boards[1])
    st.write("---")

    cols = st.columns(4)
    for r in range(4):
        for c in range(4):
            val = board[r][c]
            with cols[c]:
                if val != 0:
                    st.button(f"🌸 {val}", key=f"s_{r}_{c}", disabled=True)
                else:
                    st.number_input(
                        "",
                        min_value=1,
                        max_value=4,
                        key=f"in_{r}_{c}",
                        label_visibility="collapsed",
                    )

    st.write("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Kiểm tra đáp án ✨"):
            play_sound("sounds_win.mp3", volume=0.8)
            if level < 5:
                st.success(f"Chính xác! Đã mở màn {level+1}!")
                st.session_state.level = level + 1
            else:
                st.balloons()
                st.success("Chúc mừng bạn đã hoàn thành 5 màn Sudoku! 🎉")
    with c2:
        if st.button("Sai rồi / Thua ❌"):
            play_sound("sounds_lose.mp3", volume=0.7)
            st.error("Đáp án chưa đúng rồi, bạn chọn lại nhé!")


# Game 3: Block Blast
def play_block_blast(level):
    st.markdown(
        f"<div class='game-container'><h3>🌸 Block Blast - Màn {level}</h3><p>Xếp khối hoa vào hàng hoặc cột để ghi điểm!</p></div>",
        unsafe_allow_html=True,
    )

    st.write("---")
    for r in range(5):
        cols = st.columns(5)
        for c in range(5):
            cols[c].markdown("🌸" if (r + c) % 2 == 0 else "⬜")

    st.write("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Xóa hàng ghi điểm 💥"):
            play_sound("sounds_win.mp3", volume=0.8)
            if level < 5:
                st.success(f"Xuất sắc! Vượt qua Màn {level}!")
                st.session_state.level = level + 1
            else:
                st.balloons()
                st.success("Chúc mừng bạn phá đảo toàn bộ Block Blast! 🎉")
    with c2:
        if st.button("Hết ô trống / Thua ❌"):
            play_sound("sounds_lose.mp3", volume=0.7)
            st.error("Không còn vị trí đặt khối! Game Over!")


# --- TRANG CHƠI GAME & THANH ĐIỀU HƯỚNG ---
def show_game_screen():
    st.sidebar.title("🌸 MENU TRÒ CHƠI")

    st.session_state.bgm_enable = st.sidebar.checkbox(
        "🔊 Bật nhạc nền BGM", value=st.session_state.bgm_enable
    )

    if st.sidebar.button("🏠 Về Trang Chủ"):
        play_sound("sounds_click.mp3", volume=0.5)
        st.session_state.page = "home"
        st.rerun()

    st.sidebar.write("---")
    st.sidebar.subheader("Chọn trò chơi:")

    game_choice = st.sidebar.radio(
        "Danh sách Game:",
        [
            "1. Tile Match (Ảnh 2)",
            "2. Sudoku (Ảnh 3)",
            "3. Block Blast (Ảnh 4)",
        ],
    )

    if "Tile Match" in game_choice and st.session_state.current_game != "tile":
        play_sound("sounds_click.mp3", volume=0.5)
        st.session_state.current_game = "tile"
    elif "Sudoku" in game_choice and st.session_state.current_game != "sudoku":
        play_sound("sounds_click.mp3", volume=0.5)
        st.session_state.current_game = "sudoku"
    elif (
        "Block Blast" in game_choice
        and st.session_state.current_game != "block"
    ):
        play_sound("sounds_click.mp3", volume=0.5)
        st.session_state.current_game = "block"

    st.sidebar.write("---")
    st.sidebar.subheader("Chọn Màn (Level 1 - 5):")
    st.session_state.level = st.sidebar.slider("Màn", 1, 5, st.session_state.level)

    if st.session_state.current_game == "tile":
        play_tile_game(st.session_state.level)
    elif st.session_state.current_game == "sudoku":
        play_sudoku_game(st.session_state.level)
    elif st.session_state.current_game == "block":
        play_block_blast(st.session_state.level)


# --- ĐIỀU HƯỚNG TRANG ---
if st.session_state.page == "home":
    show_home()
else:
    show_game_screen()