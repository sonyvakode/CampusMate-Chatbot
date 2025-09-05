import streamlit as st
from utils.chat import ask_dify  # Replace with your actual function

# --------- PAGE CONFIG ---------
st.set_page_config(page_title="CampusMate Chatbot", layout="wide")

# --------- SESSION STATE INIT ---------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "edited_input" not in st.session_state:
    st.session_state.edited_input = ""
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Light"
if "language_pref" not in st.session_state:
    st.session_state.language_pref = "English"

# --------- SIDEBAR ---------
with st.sidebar:
    st.title("CampusMate")
    st.markdown("Your personal AI assistant for campus needs.")

    st.subheader("Theme")
    theme = st.radio("Choose theme", ["Light", "Dark"], index=0 if st.session_state.theme_mode == "Light" else 1)
    st.session_state.theme_mode = theme

    st.subheader("Language")
    lang = st.selectbox(
        "Choose your preferred language",
        ["English", "Hindi", "Telugu", "Marathi", "Other"],
        index=["English", "Hindi", "Telugu", "Marathi", "Other"].index(st.session_state.language_pref),
    )
    st.session_state.language_pref = lang

    st.markdown("---")
    st.caption("Recent Conversations")
    if not st.session_state.chat_history:
        st.info("No previous chats yet.")
    else:
        for sender, msg in st.session_state.chat_history[-5:]:
            if sender == "You":
                st.markdown(f"- **You:** {msg[:40]}...")

# --------- MAIN CHAT AREA ---------
st.markdown("### CampusMate Chat")
st.divider()

chat_container = st.container()
with chat_container:
    if st.session_state.chat_history:
        for sender, msg in st.session_state.chat_history:
            with st.chat_message("user" if sender == "You" else "assistant"):
                st.markdown(msg)
    else:
        st.info("No conversation yet. Start chatting below!")

# --------- BOTTOM CHAT INPUT (Updated to ChatGPT style) ---------
st.markdown(
    """
    <style>
    .stBottomContainer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: white;
        padding: 8px 12px;
        border-top: 1px solid #ddd;
        display: flex;
        align-items: center;
        gap: 8px;
        z-index: 100;
    }
    .chat-box {
        flex: 1;
        border: 1px solid #ddd;
        border-radius: 25px;
        padding: 8px 15px;
    }
    .chat-btn {
        font-size: 18px;
        cursor: pointer;
        border: none;
        background: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.container():
    st.markdown('<div class="stBottomContainer">', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns([0.5, 9, 0.7, 0.7])

    with col1:
        st.markdown("➕")  # Plus icon (left)

    with col2:
        user_input = st.text_input(
            "Ask anything",
            value=st.session_state.edited_input,
            label_visibility="collapsed",
            key="chat_input",
            placeholder="Ask anything...",
        )

    with col3:
        audio_pressed = st.button("🎤", key="audio_btn")

    with col4:
        send_pressed = st.button("⬆️", key="send_btn")

    st.markdown('</div>', unsafe_allow_html=True)

# --------- HANDLE SEND ---------
if send_pressed and user_input.strip():
    with st.spinner("Thinking..."):
        response = ask_dify(f"[Language: {st.session_state.language_pref}] {user_input}")
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("CampusMate", response))
    st.session_state.edited_input = ""  # clear input after send
    st.rerun()

# --------- AUDIO PLACEHOLDER ---------
if audio_pressed:
    st.info("🎤 Voice input feature coming soon!")
