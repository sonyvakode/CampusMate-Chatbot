import streamlit as st
from utils.chat import ask_dify  # Replace with your actual function
import random

# --------- PAGE CONFIG ---------
st.set_page_config(page_title="CampusMate Chatbot", layout="wide")

# --------- SESSION STATE INIT ---------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "otp" not in st.session_state:
    st.session_state.otp = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "language_pref" not in st.session_state:
    st.session_state.language_pref = "English"
if "chat_input" not in st.session_state:
    st.session_state.chat_input = ""
if "username" not in st.session_state:
    st.session_state.username = "User"
if "password" not in st.session_state:
    st.session_state.password = "1234"


# --------- LOGIN PAGE ---------
if not st.session_state.logged_in:
    st.title("📚 CampusMate Login")

    phone = st.text_input("Enter Phone Number", max_chars=10)
    if st.button("Send OTP"):
        if phone.isdigit() and len(phone) == 10:
            st.session_state.otp = str(random.randint(1000, 9999))
            st.info(f"OTP sent to {phone} (Demo OTP: {st.session_state.otp})")
        else:
            st.error("Please enter a valid 10-digit phone number")

    otp_entered = st.text_input("Enter OTP", type="password")
    if st.button("Login"):
        if otp_entered == st.session_state.otp:
            st.session_state.logged_in = True
            st.success("Login successful ✅")
            st.rerun()
        else:
            st.error("Invalid OTP")
    st.stop()


# --------- STYLING ---------
st.markdown(
    """
    <style>
    /* Whole app background */
    .stApp {
        background: #ffffff;
    }

    /* Sidebar clean white */
    section[data-testid="stSidebar"] {
        background-color: white !important;
    }

    /* Chat container */
    div[data-testid="stVerticalBlock"] > div:first-child {
        background: #ffffff;
        padding: 20px;
        border-radius: 10px;
    }

    /* Fixed bottom input bar */
    .stBottomContainer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        padding: 10px 15px;
        border-top: 1px solid #ddd;
        display: flex;
        align-items: center;
        gap: 10px;
        z-index: 100;
    }

    /* Chat input styling */
    .chat-box {
        flex: 1;
        border: 1px solid #ccc;
        border-radius: 25px;
        padding: 8px 15px;
    }

    /* Black send button */
    .send-btn {
        background-color: black !important;
        color: white !important;
        border: none;
        padding: 8px 14px;
        border-radius: 50%;
        font-size: 18px;
        cursor: pointer;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------- SIDEBAR ---------
with st.sidebar:
    st.title("CampusMate")
    st.markdown("Your personal AI assistant for campus needs.")

    st.subheader("Language")
    lang = st.selectbox(
        "Choose your preferred language",
        ["English", "Hindi", "Telugu", "Marathi", "Other"],
        index=["English", "Hindi", "Telugu", "Marathi", "Other"].index(
            st.session_state.language_pref
        ),
    )
    st.session_state.language_pref = lang

    st.markdown("---")
    st.subheader("Settings ⚙️")
    new_username = st.text_input("Change Username", st.session_state.username)
    new_password = st.text_input("Change Password", type="password")
    if st.button("Save Settings"):
        if new_username:
            st.session_state.username = new_username
        if new_password:
            st.session_state.password = new_password
        st.success("Settings updated ✅")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.chat_history = []
        st.success("Logged out successfully")
        st.rerun()

    st.markdown("---")
    st.caption("Recent Conversations")
    if not st.session_state.chat_history:
        st.info("No previous chats yet.")
    else:
        for sender, msg in st.session_state.chat_history[-5:]:
            if sender == "You":
                st.markdown(f"- **You:** {msg[:40]}...")


# --------- MAIN CHAT AREA ---------
st.markdown("### 💬 CampusMate Chat")
st.divider()

chat_container = st.container()
with chat_container:
    if st.session_state.chat_history:
        for sender, msg in st.session_state.chat_history:
            with st.chat_message("user" if sender == "You" else "assistant"):
                st.markdown(msg)
    else:
        st.info("No conversation yet. Start chatting below!")


# --------- BOTTOM INPUT BAR ---------
st.markdown('<div class="stBottomContainer">', unsafe_allow_html=True)

col1, col2 = st.columns([10, 1])

with col1:
    user_input = st.text_input(
        "Ask anything about studies...",
        value=st.session_state.chat_input,
        key="chat_input",
        label_visibility="collapsed",
        placeholder="Ask anything about studies...",
    )

with col2:
    send_pressed = st.button("⬆️", key="send_btn", help="Send", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)


# --------- HANDLE SEND ---------
if (send_pressed or user_input.strip()) and user_input:
    with st.spinner("Thinking..."):
        response = ask_dify(f"[Language: {st.session_state.language_pref}] {user_input}")

    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("CampusMate", response))

    st.session_state["chat_input"] = ""  # clear input after send
    st.rerun()
