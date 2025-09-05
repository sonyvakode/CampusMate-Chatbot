import streamlit as st
import random

from utils.chat import ask_dify  # Replace with your actual function

# --------- PAGE CONFIG ---------
st.set_page_config(page_title="CampusMate Chatbot", layout="wide")

# --------- SESSION STATE INIT ---------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "otp_sent" not in st.session_state:
    st.session_state.otp_sent = False
if "generated_otp" not in st.session_state:
    st.session_state.generated_otp = None
if "phone_number" not in st.session_state:
    st.session_state.phone_number = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Light"
if "language_pref" not in st.session_state:
    st.session_state.language_pref = "English"

# --------- LOGIN WITH PHONE + OTP ---------
if not st.session_state.authenticated:
    st.title("📱 CampusMate Login")

    phone = st.text_input("Enter Phone Number", value=st.session_state.phone_number)

    if st.button("Send OTP"):
        if phone.strip().isdigit() and len(phone) >= 10:
            otp = random.randint(1000, 9999)  # generate 4-digit OTP
            st.session_state.generated_otp = str(otp)
            st.session_state.phone_number = phone
            st.session_state.otp_sent = True
            st.success(f"✅ OTP sent to {phone} (for demo: {otp})")  # show OTP for demo
        else:
            st.error("Enter a valid phone number.")

    if st.session_state.otp_sent:
        otp_input = st.text_input("Enter OTP", type="password")
        if st.button("Verify OTP"):
            if otp_input == st.session_state.generated_otp:
                st.session_state.authenticated = True
                st.session_state.otp_sent = False
                st.success("🎉 Login successful!")
                st.rerun()
            else:
                st.error("Invalid OTP. Try again.")
    st.stop()

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

    st.markdown("---")
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.chat_history = []
        st.rerun()

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

# --------- CUSTOM STYLE ---------
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #e3f2fd, #ffffff);
    }
    .stBottomContainer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: #f9f9f9;
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
        background: black;
        color: white;
        border-radius: 50%;
        width: 36px;
        height: 36px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------- BOTTOM CHAT INPUT ---------
with st.container():
    st.markdown('<div class="stBottomContainer">', unsafe_allow_html=True)

    col1, col2 = st.columns([9, 1])

    with col1:
        user_input = st.text_input(
            "Ask anything about studies...",
            key="chat_input",
            placeholder="Ask anything about studies...",
        )

    with col2:
        send_pressed = st.button("⬆️", key="send_btn", help="Send")

    st.markdown('</div>', unsafe_allow_html=True)

# --------- HANDLE SEND ---------
if (send_pressed or user_input) and user_input.strip():
    with st.spinner("Thinking..."):
        response = ask_dify(f"[Language: {st.session_state.language_pref}] {user_input}")
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("CampusMate", response))
    st.session_state.chat_input = ""  # clear input after send
    st.rerun()
