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

# --------- SIDEBAR ---------
with st.sidebar:
    st.title("🎓 CampusMate")
    st.markdown("Your personal AI assistant for campus needs.")

    st.subheader("🎨 Theme")
    theme = st.radio("Choose theme", ["Light", "Dark"], index=0 if st.session_state.theme_mode == "Light" else 1)
    st.session_state.theme_mode = theme

    st.markdown("---")
    st.caption("🕘 Recent Conversations")
    if not st.session_state.chat_history:
        st.info("No previous chats yet.")
    else:
        for sender, msg in st.session_state.chat_history[-5:]:
            if sender == "You":
                st.markdown(f"- **You:** {msg[:30]}...")

# --------- MAIN CHAT AREA ---------
st.markdown("### 💬 Talk to CampusMate")
st.markdown("Ask me anything about campus facilities, deadlines, or student help!")

st.divider()

# --------- CHAT DISPLAY ---------
chat_container = st.container()

with chat_container:
    if st.session_state.chat_history:
        for sender, msg in st.session_state.chat_history:
            with st.chat_message("user" if sender == "You" else "assistant"):
                st.markdown(msg)
    else:
        st.info("No conversation yet. Start chatting below!")

# --------- CHAT INPUT BAR ---------
st.markdown("""<style>
.chat-input-container {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: #f9f9f9;
    padding: 10px 30px;
    border-top: 1px solid #ddd;
    z-index: 999;
}
input[type="text"] {
    width: 80%;
    padding: 10px;
    margin-right: 10px;
    border-radius: 8px;
    border: 1px solid #ccc;
}
button.send-button {
    background-color: #4CAF50;
    border: none;
    color: white;
    padding: 10px 15px;
    border-radius: 8px;
    cursor: pointer;
}
</style>""", unsafe_allow_html=True)

with st.container():
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([6, 1])
        with col1:
            user_input = st.text_input("Say something to Rick...", value=st.session_state.edited_input if st.session_state.edit_mode else "", label_visibility="collapsed")
        with col2:
            submitted = st.form_submit_button("📤", use_container_width=True)

    if submitted and user_input.strip():
        with st.spinner("🤖 Thinking..."):
            response = ask_dify(user_input)
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("CampusMate", response))
        st.session_state.edit_mode = False
        st.session_state.edited_input = ""
        st.rerun()

# --------- ACTION BUTTONS ---------
colA, colB = st.columns([1, 1])
with colA:
    if st.button("🧹 New Chat"):
        st.session_state.chat_history.clear()
        st.session_state.edit_mode = False
        st.session_state.edited_input = ""
        st.session_state.search_term = ""
        st.rerun()

with colB:
    if st.session_state.chat_history and st.button("✏️ Edit Last"):
        for i in reversed(range(len(st.session_state.chat_history))):
            if st.session_state.chat_history[i][0] == "You":
                st.session_state.edited_input = st.session_state.chat_history[i][1]
                st.session_state.chat_history = st.session_state.chat_history[:i]
                st.session_state.edit_mode = True
                break
        st.rerun()

# --------- SEARCH ---------
st.divider()
search_input = st.text_input("🔍 Search in chat", value=st.session_state.search_term)
st.session_state.search_term = search_input.strip()

if st.session_state.search_term:
    filtered = [
        (sender, msg) for sender, msg in st.session_state.chat_history
        if st.session_state.search_term.lower() in msg.lower()
    ]
    if filtered:
        st.subheader("🔎 Search Results")
        for sender, msg in filtered:
            with st.chat_message("user" if sender == "You" else "assistant"):
                st.markdown(f"**{sender}:** {msg}")
    else:
        st.warning("No results found.")
