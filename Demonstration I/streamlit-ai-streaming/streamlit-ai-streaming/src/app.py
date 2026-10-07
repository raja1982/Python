import json
import requests
import streamlit as st
BACKEND_STREAM_URL = "http://127.0.0.1:8000/stream"
st.set_page_config(page_title="Live AI Chat Stream", layout="centered")
st.title("Live AI Chat Stream")
st.write("Ask a question and watch the response stream from a FastAPI backend using SSE.")
if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
prompt = st.chat_input("Ask something about Agentic AI...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        response_box = st.empty()
        full_response = ""
        try:
            response = requests.post(
                BACKEND_STREAM_URL,
                json={"messages": st.session_state.messages},
                stream=True,
                timeout=60,
            )
            response.raise_for_status()
            for line in response.iter_lines(decode_unicode=True):
                if not line:
                    continue
                if line.startswith("data: "):
                    data_str = line[len("data: "):]

                    if data_str == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data_str)
                        token = chunk.get("content", "")
                        full_response += token
                        response_box.markdown(full_response + "▌")
                    except json.JSONDecodeError:
                        continue
            response_box.markdown(full_response)
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )
        except requests.exceptions.RequestException as error:
            st.error(f"Backend request failed: {error}")
        except Exception as error:
            st.error(f"An error occurred: {error}")
            
            
            
            
            
            