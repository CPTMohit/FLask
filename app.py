"""
Tic-Tac-Toe - a tiny Streamlit web game
Run with:  streamlit run app.py
"""

import streamlit as st

st.set_page_config(page_title="Tic-Tac-Toe", page_icon="❌", layout="centered")


def init_state():
    if "board" not in st.session_state:
        st.session_state.board = [""] * 9
    if "turn" not in st.session_state:
        st.session_state.turn = "X"
    if "winner" not in st.session_state:
        st.session_state.winner = None
    if "scores" not in st.session_state:
        st.session_state.scores = {"X": 0, "O": 0, "Draws": 0}


def check_winner(board):
    lines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
        (0, 4, 8), (2, 4, 6),             # diagonals
    ]
    for a, b, c in lines:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    if "" not in board:
        return "Draw"
    return None


def make_move(i):
    if st.session_state.board[i] == "" and not st.session_state.winner:
        st.session_state.board[i] = st.session_state.turn
        result = check_winner(st.session_state.board)
        if result:
            st.session_state.winner = result
            if result == "Draw":
                st.session_state.scores["Draws"] += 1
            else:
                st.session_state.scores[result] += 1
        else:
            st.session_state.turn = "O" if st.session_state.turn == "X" else "X"


def reset_board():
    st.session_state.board = [""] * 9
    st.session_state.turn = "X"
    st.session_state.winner = None


init_state()

st.title("❌⭕ Tic-Tac-Toe")

c1, c2, c3 = st.columns(3)
c1.metric("Player X", st.session_state.scores["X"])
c2.metric("Draws", st.session_state.scores["Draws"])
c3.metric("Player O", st.session_state.scores["O"])

if st.session_state.winner:
    if st.session_state.winner == "Draw":
        st.info("It's a draw! 🤝")
    else:
        st.success(f"Player {st.session_state.winner} wins! 🎉")
else:
    st.subheader(f"Turn: {st.session_state.turn}")

# Render the 3x3 board as buttons
board = st.session_state.board
for row in range(3):
    cols = st.columns(3, gap="small")
    for col in range(3):
        i = row * 3 + col
        label = board[i] if board[i] else " "
        cols[col].button(
            label,
            key=f"cell_{i}",
            use_container_width=True,
            on_click=make_move,
            args=(i,),
            disabled=board[i] != "" or st.session_state.winner is not None,
        )

st.button("🔄 New Round", on_click=reset_board)

if st.button("♻️ Reset Scores"):
    st.session_state.scores = {"X": 0, "O": 0, "Draws": 0}
    reset_board()
