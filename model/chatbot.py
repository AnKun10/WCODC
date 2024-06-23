import streamlit as st
from hugchat import hugchat
from hugchat.login import Login


class Chatbot:
    def __init__(self):
        pass

    def __generate_response(self, inp, email, passwd):
        # Hugging Face Login
        sign = Login(email, passwd)
        cookies = sign.login()
        # Create Chatbot
        chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
        return chatbot.chat(inp)

    def display(self):
        # App title
        st.title('Chatbot')

        # Hugging Face Credentials
        with st.sidebar:
            st.title('Login HugChat')
            hf_email = st.text_input('Email')
            hf_password = st.text_input('Password', type='password')
            if not (hf_email and hf_password):
                st.warning('Please enter your account!')
            else:
                st.success('Proceed to entering your prompt message!')

        # Store LLM generated responses
        if "messages" not in st.session_state.keys():
            st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # User-provided prompt
        if prompt := st.chat_input(disabled=not (hf_email and hf_password)):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

        # Generates a new response if last message is not from assistant
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = self.__generate_response(prompt, hf_email, hf_password)
                    st.write(response)
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message)
