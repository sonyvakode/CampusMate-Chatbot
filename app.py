import streamlit as st
from utils.chat import ask_dify

st.set_page_config(page_title="🎓 CampusMate Chatbot")
st.title("🎓 CampusMate – AI Assistant (Gemini 2.0 Flash)")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Ask CampusMate:")

if st.button("Send") and user_input:
    with st.spinner("CampusMate is thinking..."):
        answer = ask_dify(user_input)
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("CampusMate", answer))

st.divider()

for sender, msg in st.session_state.chat_history:
    st.markdown(f"**{sender}:** {msg}")
