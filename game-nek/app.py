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

# 2. Khởi tạo Trạng thái Trang
if "page" not in st.session_state:
    st.session_state.page = "home"
if "current_game" not in st.session_state:
    st.session_state.current_game = "tile"
if "level" not in st.session_state:
    st.session_state.level = 1

# 3. CSS Giao diện Hoa Đào Tươi Sáng & Chữ To Rõ
custom_css = """
<style>
/* Nền màu hồng hoa đào pastel dịu nhẹ (thay thế nếu chưa nhận file ảnh) */
.stApp {
    background: linear-gradient(135deg, #fff0f3, #ffe3e8, #f7d6de) !important;
}

[data-testid="stSidebar"] {
    background-color: rgba(255, 240, 243, 0.95) !important;
    border-right: 3px solid #f2a6b4;
}

html, body, [class*="css"], .stMarkdown, p, div, span {
    font-size: 22px !important;
    font-weight: 600 !important;
    color: #5c2a38 !important;
}

h1, h2, h3 {
    font-size: 34px !important;
    font-weight: 800 !important;
    color: #d46b82 !important;
}

.stButton > button {
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
}

.stButton > button:hover {
    transform: scale(1.05) !important;
    background: linear-gradient(135deg, #e88299, #d46b82) !important;
}

.game-card {
    background-color: rgba(255, 255, 255, 0.85) !important;
    border-radius: 25px !important;
    padding: 30px !important;
    border: 3px solid #f7b2bd !important;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1) !important;
    text-align: center !important;
    margin-bottom: 20px !important;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)


# --- 1. TRANG CHỦ (MENU CHÍNH) ---
def show_home():
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])

    with c2:
        st.markdown(
            """
            <div class='game-card'>
                <h1 style='font-size: 40px !important;'>🌸 GAME CỦA THUCUTE 🌸</h1>
                <p>Chào mừng bạn đến với thế giới trò chơi dễ thương!</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🌸 PLAY NOW 🌸", key="play_now_btn"):
            st.session_state.page = "select_game"
            st.rerun()


# --- 2. TRANG LỰA CHỌN GAME RIÊNG ---
def show_select_game():
    st.markdown(
        """
        <div class='game-card'>
            <h1>🌸 DANH SÁCH TRÒ CHƠI 🌸</h1>
            <p>Hãy chọn một trò chơi bên dưới để bắt đầu thử thách nhé!</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class='game-card'>
                <h2>🧩 Tile Match</h2>
                <p>Ghép 3 hình hoa quả giống nhau!</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Chơi Tile Match 🌸", key="btn_tile"):
            st.session_state.current_game = "tile"
            st.session_state.page = "playing"
            st.rerun()

    with col2:
        st.markdown(
            """
            <div class='game-card'>
                <h2>🔢 Sudoku</h2>
                <p>Thử thách điền số vào lưới 4x4!</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Chơi Sudoku 🌸", key="btn_sudoku"):
            st.session_state.current_game = "sudoku"
            st.session_state.page = "playing"
            st.rerun()

    with col3:
        st.markdown(
            """
            <div class='game-card'>
                <h2>💥 Block Blast</h2>
                <p>Xếp khối hoa vào hàng để ghi điểm!</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Chơi Block Blast 🌸", key="btn_block"):
            st.session_state.current_game = "block"
            st.session_state.page = "playing"
            st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        if st.button("🏠 Quay Về Màn Hình Chính", key="back_home_btn"):
            st.session_state.page = "home"
            st.rerun()


# --- 3. GIAO DIỆN TRONG GAME ---
def play_tile_game(level):
    st.markdown(
        f"""
        <div class='game-card'>
            <h2>🌸 Tile Match - Màn {level}</h2>
            <p>Ghép 3 ô giống nhau để hoàn thành màn chơi!</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    icons = ["🌸", "🌺", "🌹", "🌻", "🌼", "🌷", "🍁"][: level + 2]
    grid = [random.choice(icons) for _ in range(level * 4)]
    grid_str = " ".join([f"[{icon}]" for icon in grid])

    st.markdown(
        f"""
        <div class='game-card'>
            <h3>Các ô hoa trên bàn:</h3>
            <h1 style='letter-spacing: 10px;'>{grid_str}</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Hoàn thành màn 🎉", key="win_tile"):
            if level < 5:
                st.success(f"Chúc mừng bạn đã vượt qua Màn {level}!")
                st.session_state.level = level + 1
            else:
                st.balloons()
                st.success("Bạn đã xuất sắc thắng toàn bộ 5 màn Tile Match! 🎉")

    with c2:
        if st.button("Thử lại / Thua ❌", key="lose_tile"):
            st.error("Rất tiếc! Hãy thử lại màn này nhé!")


def play_sudoku_game(level):
    st.markdown(
        f"""
        <div class='game-card'>
            <h2>🌸 Floral Sudoku - Màn {level}</h2>
            <p>Điền số phù hợp vào các ô trống!</p>
        </div>
        """,
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
        if st.button("Kiểm tra đáp án ✨", key="win_sudoku"):
            if level < 5:
                st.success(f"Chính xác! Đã mở Màn {level+1}!")
                st.session_state.level = level + 1
            else:
                st.balloons()
                st.success("Chúc mừng bạn đã hoàn thành 5 màn Sudoku! 🎉")
    with c2:
        if st.button("Sai rồi / Thua ❌", key="lose_sudoku"):
            st.error("Đáp án chưa đúng rồi, bạn chọn lại nhé!")


def play_block_blast(level):
    st.markdown(
        f"""
        <div class='game-card'>
            <h2>🌸 Block Blast - Màn {level}</h2>
            <p>Xếp các khối hoa vào hàng hoặc cột để ghi điểm!</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for r in range(5):
        cols = st.columns(5)
        for c in range(5):
            cols[c].markdown("🌸" if (r + c) % 2 == 0 else "⬜")

    st.write("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Xóa hàng ghi điểm 💥", key="win_block"):
            if level < 5:
                st.success(f"Xuất sắc! Vượt qua Màn {level}!")
                st.session_state.level = level + 1
            else:
                st.balloons()
                st.success("Chúc mừng bạn đã phá đảo Block Blast! 🎉")
    with c2:
        if st.button("Hết ô trống / Thua ❌", key="lose_block"):
            st.error("Không còn vị trí đặt khối! Game Over!")


def show_playing_screen():
    st.sidebar.title("🌸 ĐIỀU HƯỚNG GAME")

    if st.sidebar.button("🎮 Chọn Trò Chơi Khác"):
        st.session_state.page = "select_game"
        st.rerun()

    if st.sidebar.button("🏠 Về Trang Chủ"):
        st.session_state.page = "home"
        st.rerun()

    st.sidebar.write("---")
    st.sidebar.subheader("Chọn Màn (Level 1 - 5):")
    st.session_state.level = st.sidebar.slider("Màn", 1, 5, st.session_state.level)

    if st.session_state.current_game == "tile":
        play_tile_game(st.session_state.level)
    elif st.session_state.current_game == "sudoku":
        play_sudoku_game(st.session_state.level)
    elif st.session_state.current_game == "block":
        play_block_blast(st.session_state.level)


# --- ĐIỀU HƯỚNG TRANG CHÍNH ---
if st.session_state.page == "home":
    show_home()
elif st.session_state.page == "select_game":
    show_select_game()
elif st.session_state.page == "playing":
    show_playing_screen()
