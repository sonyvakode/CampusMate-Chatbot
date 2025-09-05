import streamlit as st
from utils.chat import ask_dify  # Replace with your actual function

# --------- PAGE CONFIG ---------
st.set_page_config(page_title="CampusMate Chatbot", layout="wide")

# --------- SESSION STATE INIT ---------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False
if "edited_input" not in st.session_state:
    st.session_state.edited_input = ""
if "search_term" not in st.session_state:
    st.session_state.search_term = ""
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

# --------- CHAT INPUT (BOTTOM BAR) ---------
st.markdown(
    """
    <style>
    .stBottomContainer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: white;
        padding: 10px;
        border-top: 1px solid #ddd;
        z-index: 100;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.container():
    st.markdown('<div class="stBottomContainer">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([10, 1, 1])

    with col1:
        user_input = st.text_input(
            "Type your message...",
            value=st.session_state.edited_input if st.session_state.edit_mode else "",
            label_visibility="collapsed",
            key="chat_input",
        )
    with col2:
        send_pressed = st.button("⬆️", key="send_btn")
    with col3:
        audio_pressed = st.button("🎤", key="audio_btn")

    st.markdown('</div>', unsafe_allow_html=True)

# --------- HANDLE INPUT ---------
if (send_pressed or user_input.strip()) and not st.session_state.edit_mode:
    with st.spinner("Thinking..."):
        response = ask_dify(f"[Language: {st.session_state.language_pref}] {user_input}")
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("CampusMate", response))
    st.session_state.edited_input = ""
    st.rerun()

# --------- AUDIO PLACEHOLDER ---------
if audio_pressed:
    st.info("🎤 Voice input feature coming soon!")
