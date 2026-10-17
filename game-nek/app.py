import base64
import os
import random
import numpy as np
import streamlit as st

# 1. Cấu hình trang Streamlit
st.set_page_config(
    page_title="Game của Thucute 🌸",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# 2. Hàm đọc tệp sang Base64 an toàn
def get_file_b64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""


# Đọc dữ liệu ảnh và âm thanh
banner_b64 = get_file_b64("assets/home_banner.png")  # Ảnh 3
bg_b64 = get_file_b64("assets/background.png")  # Ảnh 4

bgm_b64 = get_file_b64("sounds_bgm.mp3")
click_b64 = get_file_b64("sounds_click.mp3")
win_b64 = get_file_b64("sounds_win.mp3")
lose_b64 = get_file_b64("sounds_lose.mp3")


# 3. Hàm nhúng trình phát âm thanh HTML5 / JS
def play_sound(sound_b64, loop=False, volume=0.6):
    if sound_b64:
        loop_attr = "loop" if loop else ""
        audio_html = f"""
            <audio autoplay {loop_attr} style="display:none;">
                <source src="data:audio/mp3;base64,{sound_b64}" type="audio/mp3">
            </audio>
            <script>
                var audios = document.getElementsByTagName('audio');
                if (audios.length > 0) {{ audios[audios.length - 1].volume = {volume}; }}
            </script>
        """
        st.components.v1.html(audio_html, height=0)


# 4. Khởi tạo Trạng thái (Session State)
if "page" not in st.session_state:
    st.session_state.page = "home"  # Các trang: 'home', 'select_game', 'playing'
if "current_game" not in st.session_state:
    st.session_state.current_game = "tile"
if "level" not in st.session_state:
    st.session_state.level = 1
if "bgm_enable" not in st.session_state:
    st.session_state.bgm_enable = True

# Phát BGM nếu đang bật
if st.session_state.bgm_enable and bgm_b64:
    play_sound(bgm_b64, loop=True, volume=0.3)


# 5. Cấu hình CSS Nền & Chữ To Rõ
if st.session_state.page in ["home", "select_game"]:
    # Nền cho Trang chủ và Trang chọn game: Dùng Ảnh 3 (home_banner.png)
    current_bg = banner_b64
else:
    # Nền cho Giao diện trong Game: Dùng Ảnh 4 (background.png)
    current_bg = bg_b64

custom_css = f"""
<style>
/* Đặt Nền Toàn Màn Hình */
.stApp {{
    background: url("data:image/png;base64,{current_bg}") no-repeat center center fixed !important;
    background-size: cover !important;
}}

/* Sidebar trong suốt */
[data-testid="stSidebar"] {{
    background-color: rgba(255, 255, 255, 0.85) !important;
    backdrop-filter: blur(8px);
    border-right: 3px solid #f2a6b4;
}}

/* Chữ to rõ ràng hơn toàn hệ thống */
html, body, [class*="css"], .stMarkdown, p, div, span {{
    font-size: 22px !important;
    font-weight: 600 !important;
    color: #4a2c32 !important;
}}

h1, h2, h3 {{
    font-size: 34px !important;
    font-weight: 800 !important;
    color: #c94c68 !important;
    text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
}}

/* Nút bấm giao diện */
.stButton > button {{
    background: linear-gradient(135deg, #f7a8b8, #e88299) !important;
    color: white !important;
    font-size: 24px !important;
    font-weight: bold !important;
    border-radius: 25px !important;
    border: 3px solid #ffffff !important;
    padding: 12px 30px !important;
    box-shadow: 0px 6px 15px rgba(232, 130, 153, 0.5) !important;
    transition: all 0.3s ease !important;
    width: 100%;
}}

.stButton > button:hover {{
    transform: scale(1.05) !important;
    background: linear-gradient(135deg, #e88299, #d46b82) !important;
}}

/* Khung trò chơi trong suốt */
.game-card {{
    background-color: rgba(255, 255, 255, 0.8) !important;
    border-radius: 25px !important;
    padding: 30px !important;
    border: 3px solid #f7b2bd !important;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1) !important;
    backdrop-filter: blur(6px) !important;
    text-align: center !important;
    margin-bottom: 20px !important;
}}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)


# --- 1. TRANG CHỦ (MENU CHÍNH - BẤM TRỰC TIẾP VÀO PLAY NOW NẰM TRÊN BANNER) ---
def show_home():
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 3, 1])

    with c2:
        # Nhúng Ảnh 3 làm Banner kèm Bản đồ tọa độ Image Map nhấp vào chữ Play Now
        banner_html = f"""
        <div style="text-align: center; position: relative;">
            <img src="data:image/png;base64,{banner_b64}" usemap="#playmap" style="width: 100%; border-radius: 20px; box-shadow: 0 10px 25px rgba(212,107,130,0.3);">
            <map name="playmap">
                <!-- Vùng phủ chữ PLAY NOW ở chính giữa ảnh -->
                <area shape="rect" coords="150,150,850,500" alt="Play Now" href="javascript:void(0);" onclick="document.getElementById('start_game_trigger').click();">
            </map>
        </div>
        """
        st.markdown(banner_html, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Nút bấm chuyển trang (được kích hoạt khi nhấp vào chữ play now trên ảnh)
        if st.button("🌸 CHỌN GAME ĐỂ CHƠI 🌸", key="start_game_trigger"):
            play_sound(click_b64, volume=0.7)
            st.session_state.page = "select_game"
            st.rerun()


# --- 2. TRANG LỰA CHỌN GAME RIÊNG (GAME SELECTION PAGE) ---
def show_select_game():
    st.markdown(
        """
        <div class='game-card'>
            <h1>🌸 DANH SÁCH TRÒ CHƠI 🌸</h1>
            <p style='font-size: 24px !important;'>Hãy chọn một trò chơi bạn yêu thích bên dưới để bắt đầu!</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    # Thẻ Game 1: Tile Match
    with col1:
        st.markdown(
            """
            <div class='game-card'>
                <h2>🧩 Tile Match</h2>
                <p>Ghép 3 hình hoa quả giống nhau để xóa khỏi khay!</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Chơi Tile Match 🌸", key="btn_tile"):
            play_sound(click_b64, volume=0.7)
            st.session_state.current_game = "tile"
            st.session_state.page = "playing"
            st.rerun()

    # Thẻ Game 2: Sudoku
    with col2:
        st.markdown(
            """
            <div class='game-card'>
                <h2>🔢 Sudoku</h2>
                <p>Thử thách trí tuệ điền số vào lưới 4x4 đầy thú vị!</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Chơi Sudoku 🌸", key="btn_sudoku"):
            play_sound(click_b64, volume=0.7)
            st.session_state.current_game = "sudoku"
            st.session_state.page = "playing"
            st.rerun()

    # Thẻ Game 3: Block Blast
    with col3:
        st.markdown(
            """
            <div class='game-card'>
                <h2>💥 Block Blast</h2>
                <p>Xếp các khối hoa vào hàng hoặc cột để ghi điểm cao!</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Chơi Block Blast 🌸", key="btn_block"):
            play_sound(click_b64, volume=0.7)
            st.session_state.current_game = "block"
            st.session_state.page = "playing"
            st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        if st.button("🏠 Quay Về Màn Hình Chính", key="back_home_btn"):
            play_sound(click_b64, volume=0.6)
            st.
