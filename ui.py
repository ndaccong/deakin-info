import streamlit as st
from speech_to_text import voice_recognize
from chat import chat_completion

def response(query):
    output = chat_completion(query)
    st.session_state.messages.append({"role": "assistant", "content": output})
    st.chat_message("assistant").write(output)
    

st.title("💬 Chatbot")
st.caption("🚀 A chatbot for Deakin University. You can ask for unit information by voice or chat.")

if "messages" not in st.session_state:
    msg = "How can I help you?"
    st.session_state["messages"] = [{"role": "assistant", "content": msg}]
    st.chat_message("assistant").write(msg)
    
if st.button("🎤 Click here to ask by voice"):
    msg = "I'm listening..."
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
    
    is_reconized, recognized_text = voice_recognize()
    if is_reconized:
        st.session_state.messages.append({"role": "user", "content": recognized_text})
        st.chat_message("user").write(recognized_text)
        response(recognized_text)
    else:
        msg = "Sorry I could not hear you. Please try again."
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response(prompt)