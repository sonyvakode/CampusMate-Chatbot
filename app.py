import streamlit as st
from utils.chat import ask_dify

# --------- THEME TOGGLE SETUP ---------
st.set_page_config(page_title="🎓 CampusMate Chatbot", layout="wide")
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Light"

# --------- SIDEBAR (Left Panel) ---------
with st.sidebar:
    st.image("baf60389-f069-438c-9d7a-391a52da9b10.png", width=100)  # CampusMate logo
    st.title("🤖 CampusMate")
    st.markdown("Your AI Assistant for Campus Life")
    
    st.subheader("🎨 Theme")
    theme = st.radio("Choose theme", ["Light", "Dark"], index=0 if st.session_state.theme_mode == "Light" else 1)
    st.session_state.theme_mode = theme

    st.markdown("---")
    st.caption("📜 Chat History")
    if not st.session_state.get("chat_history"):
        st.info("No previous chats yet.")
    else:
        for i, (sender, msg) in enumerate(st.session_state.chat_history[-5:]):
            st.markdown(f"**{sender}:** {msg[:25]}...")

# --------- MAIN TITLE ---------
st.title("🎓 CampusMate – AI Assistant (Gemini 2.0 Flash)")

# --------- SESSION STATE ---------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False
if "edited_input" not in st.session_state:
    st.session_state.edited_input = ""
if "search_term" not in st.session_state:
    st.session_state.search_term = ""

# --------- NEW CHAT BUTTON ---------
if st.button("🧹 New Chat"):
    st.session_state.chat_history.clear()
    st.session_state.edit_mode = False
    st.session_state.edited_input = ""
    st.session_state.search_term = ""
    st.rerun()

st.divider()

# --------- CHAT INPUT ---------
if not st.session_state.edit_mode:
    user_input = st.text_input("🧑‍🎓 You:", key="input_box")
else:
    user_input = st.text_input("✏️ Edit your previous question:", st.session_state.edited_input, key="edit_box")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Send") and user_input.strip():
        with st.spinner("🤖 CampusMate is thinking..."):
            response = ask_dify(user_input)
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("CampusMate", response))
        st.session_state.edit_mode = False
        st.session_state.edited_input = ""
        st.rerun()

with col2:
    if st.session_state.chat_history:
        if st.button("✏️ Edit Last"):
            for i in reversed(range(len(st.session_state.chat_history))):
                if st.session_state.chat_history[i][0] == "You":
                    st.session_state.edited_input = st.session_state.chat_history[i][1]
                    st.session_state.chat_history = st.session_state.chat_history[:i]
                    st.session_state.edit_mode = True
                    break
            st.rerun()

st.divider()

# --------- CHAT HISTORY + SEARCH ---------
if st.session_state.chat_history:
    search_input = st.text_input("🔍 Search Chat History", value=st.session_state.search_term, key="search_bar")
    st.session_state.search_term = search_input.strip()

    filtered_history = [
        (sender, msg) for sender, msg in st.session_state.chat_history
        if st.session_state.search_term.lower() in msg.lower()
    ] if st.session_state.search_term else st.session_state.chat_history

    if filtered_history:
        st.subheader("💬 Chat History")
        for sender, msg in filtered_history:
            if sender == "You":
                with st.chat_message("user"):
                    st.markdown(f"**🧑‍🎓 You:** {msg}")
            else:
                with st.chat_message("assistant"):
                    st.markdown(f"**🤖 CampusMate:** {msg}")
    else:
        st.warning("No results found in chat history.")
