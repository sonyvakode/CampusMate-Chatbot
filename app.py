import streamlit as st
from utils.chat import ask_dify

# Page setup
st.set_page_config(page_title="🎓 CampusMate Chatbot", layout="centered")

# Apply custom style
st.markdown("""
    <style>
    .stApp {
        background-color: #f2f4f8;
    }
    input[type="text"] {
        color: black !important;
        background-color: white !important;
    }
    .you-bubble {
        background-color: #ffffff;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 8px;
        border-left: 5px solid #00000010;
    }
    .bot-bubble {
        background-color: #d9fdd3;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 12px;
        border-left: 5px solid #34a853;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎓 CampusMate – AI Assistant (Gemini 2.0 Flash)")

# --- Session State Init ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False
if "edited_input" not in st.session_state:
    st.session_state.edited_input = ""
if "search_term" not in st.session_state:
    st.session_state.search_term = ""

# --- Header ---
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("🧹 New Chat"):
        st.session_state.chat_history.clear()
        st.session_state.edit_mode = False
        st.session_state.edited_input = ""
        st.session_state.search_term = ""
        st.rerun()

st.divider()

# --- Input Section ---
if not st.session_state.edit_mode:
    user_input = st.text_input("Ask CampusMate:", key="input_box")
else:
    user_input = st.text_input("Edit your previous question:", st.session_state.edited_input, key="edit_box")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Send") and user_input.strip():
        with st.spinner("CampusMate is thinking..."):
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

# --- Search Chat ---
if st.session_state.chat_history:
    search_input = st.text_input("🔍 Search Chat History", value=st.session_state.search_term, key="search_bar")
    st.session_state.search_term = search_input

    filtered_history = [
        (sender, msg) for sender, msg in st.session_state.chat_history
        if st.session_state.search_term.lower() in msg.lower()
    ] if st.session_state.search_term else st.session_state.chat_history

    if filtered_history:
        st.markdown("### 💬 Chat History")
        for sender, msg in filtered_history:
            if sender == "You":
                st.markdown(f"<div class='you-bubble'>🧑‍🎓 <strong>{sender}:</strong> {msg}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='bot-bubble'>🤖 <strong>{sender}:</strong> {msg}</div>", unsafe_allow_html=True)
    else:
        st.warning("No results found in chat history.")
