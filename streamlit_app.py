import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 건강 상담 챗봇")
st.write(
    "이 챗봇은 오픈AI의 GPT-4o mini 모델을 사용하여 건강 관련 질문에 답변합니다. "
    "오픈AI API 키를 입력하고 시작하세요. "
    "API 키는 [여기](https://platform.openai.com/account/api-keys)에서 "
    "발급받을 수 있습니다."
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": (
            "당신은 친절한 건강 상담 전문가입니다. "
            "사용자 질문에 한글로 답변하세요."
        )}]

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_input := st.chat_input("건강 관련 질문을 입력하세요..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_messages("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("답변을 생성 중입니다..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=st.session_state.messages,
                )
                assistant_message = response.choices[0].message.content

        st.session_state.messages.append({"role": "assistant", "content": assistant_message})
