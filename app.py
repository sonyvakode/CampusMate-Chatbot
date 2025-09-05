import streamlit as st
from utils.chat import ask_dify  # Replace with your actual function

# --------- PAGE CONFIG ---------
st.set_page_config(page_title="CampusMate Chatbot", layout="wide")

# --------- SESSION STATE INIT ---------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --------- CHAT DISPLAY ---------
st.title("CampusMate Chat")
chat_container = st.container()

with chat_container:
    if st.session_state.chat_history:
        for sender, msg in st.session_state.chat_history:
            with st.chat_message("user" if sender == "You" else "assistant"):
                st.markdown(msg)
    else:
        st.info("No conversation yet. Start chatting below!")

# --------- FIXED BOTTOM CHAT BAR ---------
st.markdown(
    """
    <style>
    .chat-input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        display: flex;
        align-items: center;
        background-color: white;
        padding: 8px;
        border-top: 1px solid #ddd;
        z-index: 100;
    }
    .chat-input-box {
        flex: 1;
        border: 1px solid #ddd;
        border-radius: 25px;
        padding: 8px 15px;
        margin: 0 8px;
    }
    .chat-icon {
        font-size: 20px;
        cursor: pointer;
        margin: 0 5px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Create layout using HTML inside Streamlit
st.markdown(
    """
    <div class="chat-input-container">
        <span class="chat-icon">➕</span>
        <input type="text" id="user_input" placeholder="Ask anything" class="chat-input-box" />
        <span class="chat-icon">🎤</span>
        <button id="send_btn" class="chat-icon">⬆️</button>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------- HANDLE INPUT ---------
user_input = st.session_state.get("last_input", "")

# JavaScript hack to capture input & send button
st.markdown(
    """
    <script>
    const inputBox = document.getElementById("user_input");
    const sendBtn = document.getElementById("send_btn");

    if (sendBtn) {
        sendBtn.onclick = function() {
            const text = inputBox.value;
            if (text.trim() !== "") {
                fetch("/send_input?text=" + encodeURIComponent(text))
                inputBox.value = "";
            }
        }
    }
    </script>
    """,
    unsafe_allow_html=True,
)
