import ollama
import streamlit as st


MODEL_NAME="neoai-8b-chat"
SYSTEM="ハンターハンターのゴン＝フリークスになりきって"
GON_IMAGE="gon.png"
ME_IMAGE="me.jpg"


if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "俺はゴン＝フリークス！"}]


for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message(msg["role"], avatar=ME_IMAGE).write(msg["content"])
    else:
        st.chat_message(msg["role"], avatar=GON_IMAGE).write(msg["content"])

def generate_response():
    user_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
    responses = ollama.chat(
        model=MODEL_NAME,
        stream=True,
        messages=[
            {"role": "system", "content": SYSTEM}
        ] + user_messages)
    for partial_resp in responses:
        token = partial_resp["message"]["content"]
        st.session_state["full_message"] += token
        yield token

if prompt := st.chat_input():
    st.session_state.messages.append(
        {"role": "user", "content": prompt})
    st.chat_message("user", avatar=ME_IMAGE).write(prompt)
    st.session_state["full_message"] = ""
    st.chat_message("assistant", avatar=GON_IMAGE).write_stream(generate_response)
    st.session_state.messages.append(
        {"role": "assistant", "content": st.session_state["full_message"]})


