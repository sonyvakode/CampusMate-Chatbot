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
    st.session_state.username = "SONY vakode"
if "plan" not in st.session_state:
    st.session_state.plan = "Free"


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
    /* App background */
    .stApp {
        background: #ffffff;
    }

    /* Sidebar Blue */
    section[data-testid="stSidebar"] {
        background-color: #004080 !important;  /* Blue */
        color: white !important;
    }

    /* Sidebar text white */
    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Sidebar buttons */
    .sidebar-btn {
        background: none;
        border: none;
        color: white !important;
        text-align: left;
        font-size: 16px;
        padding: 8px 12px;
        cursor: pointer;
        width: 100%;
    }
    .sidebar-btn:hover {
        background: #0059b3;
        border-radius: 5px;
    }

    /* User info at bottom */
    .user-info {
        position: absolute;
        bottom: 20px;
        left: 20px;
        font-size: 14px;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------- SIDEBAR MENU ---------
with st.sidebar:
    st.markdown("### CampusMate Menu")

    if st.button("⚙️ Settings", key="settings", help="Change preferences", use_container_width=True):
        st.info("Settings page coming soon...")

    if st.button("❓ Help", key="help", help="Get help", use_container_width=True):
        st.info("Help section coming soon...")

    if st.button("↩️ Logout", key="logout", help="Log out", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.chat_history = []
        st.rerun()

    # User info at bottom
    st.markdown(
        f"""
        <div class="user-info">
            <b>{st.session_state.username}</b><br>
            {st.session_state.plan}
        </div>
        """,
        unsafe_allow_html=True,
    )


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
st.markdown(
    """
    <div class="stBottomContainer">
    """,
    unsafe_allow_html=True,
)

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

st.markdown("</div>", unsafe_allow_html=True)


# --------- HANDLE SEND ---------
if (send_pressed or user_input.strip()) and user_input:
    with st.spinner("Thinking..."):
        response = ask_dify(f"[Language: {st.session_state.language_pref}] {user_input}")

    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("CampusMate", response))

    st.session_state["chat_input"] = ""  # clear input after send
    st.rerun()
