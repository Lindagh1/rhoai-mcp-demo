import streamlit as st
import requests

st.set_page_config(page_title="RHOAI Support Assistant", page_icon="🤖")
st.title("🤖 Support Assistant (RHOAI v3 + MCP)")

# Internal OpenShift Service URL
Llama_URL = "http://llama-stack-service:5000/v1/chat/completions"

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("How can I help you?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("⏳ *Querying Llama Stack...*")
        
        try:
            payload = {
                "model": "meta-llama/Meta-Llama-3-8B-Instruct",
                "messages": st.session_state.messages,
                "stream": False
            }
            
            response = requests.post(Llama_URL, json=payload, timeout=30)
            
            if response.status_code == 200:
                full_response = response.json()['choices'][0]['message']['content']
                placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                placeholder.error(f"Error {response.status_code}: {response.text}")
                
        except Exception as e:
            placeholder.error(f"Connection Error: {str(e)}")