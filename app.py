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
    st.session_state.username = None


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
            st.session_state.username = phone
            st.success("Login successful ✅")
            st.rerun()
        else:
            st.error("Invalid OTP")
    st.stop()


# --------- SIDEBAR STYLING ---------
st.markdown(
    """
    <style>
    section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, #004080, #0066cc);
        color: white !important;
    }
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------- SIDEBAR ---------
with st.sidebar:
    st.title("CampusMate")
    st.markdown("Your personal AI assistant for campus needs.")

    st.subheader("Theme")
    theme = st.radio("Choose theme", ["Light", "Dark"], index=0)

    st.subheader("Language")
    lang = st.selectbox(
        "Choose your preferred language",
        ["English", "Hindi", "Telugu", "Marathi", "Other"],
        index=0,
    )
    st.session_state.language_pref = lang

    st.markdown("---")
    st.subheader("Account")
    st.write(f"📱 Logged in as: **{st.session_state.username}**")
    if st.button("↩️ Logout"):
        st.session_state.logged_in = False
        st.session_state.chat_history = []
        st.session_state.username = None
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


# --------- BOTTOM CHAT INPUT WITH ENTER TO SEND ---------
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input(
        "Ask anything about studies...",
        key="chat_input",
        label_visibility="collapsed",
        placeholder="Ask anything about studies...",
    )
    send_pressed = st.form_submit_button("Send")  # Enter key works here

# --------- HANDLE SEND ---------
if send_pressed and user_input:
    with st.spinner("Thinking..."):
        response = ask_dify(f"[Language: {st.session_state.language_pref}] {user_input}")

    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("CampusMate", response))

    # Clear input handled automatically by clear_on_submit=True
    st.rerun()
