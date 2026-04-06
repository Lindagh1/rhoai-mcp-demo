import streamlit as st
import requests
import json

# Page Setup
st.set_page_config(page_title="RHOAI Support Assistant", page_icon="🤖")
st.title("🤖 Support Assistant (RHOAI v3 + MCP)")
st.markdown("---")

# Llama Stack Internal URL (Port 5000 from our Service)
URL = "http://llama-stack-service:5000/v1/chat/completions"

# Initialize Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
if prompt := st.chat_input("Ask about JIRA-404..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        response_placeholder.markdown("⏳ *Querying Llama Stack (Standard HTTP)...*")
        
        try:
            # Standard OpenAI-compatible payload
            payload = {
                "model": "llama-scout-17b",
                "messages": st.session_state.messages,
                "stream": False
            }
            
            # Simple POST request without problematic LlamaStack headers
            response = requests.post(URL, json=payload, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                answer = data['choices'][0]['message']['content']
                response_placeholder.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                response_placeholder.error(f"❌ Server Error {response.status_code}: {response.text}")
                
        except Exception as e:
            response_placeholder.error(f"⚠️ Connection Error: {str(e)}")