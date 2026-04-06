import streamlit as st
import requests

st.set_page_config(page_title="RHOAI Support Assistant", page_icon="🤖")
st.title("🤖 Support Assistant (RHOAI + MCP)")
st.markdown("Ask me about a Jira ticket, for example: **What is the status of JIRA-404?**")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Enter your question here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("⏳ *Thinking and checking Jira via MCP...*")
        
        try:
            # Voici l'URL qui a été corrigée
            url = "http://llama-stack-service:5000/v1/chat/completions" 
            
            payload = {
                "model": "meta-llama/Meta-Llama-3-8B-Instruct",
                "messages": st.session_state.messages,
                "stream": False 
            }
            
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data.get("choices", [{}])[0].get("message", {}).get("content", "Sorry, I couldn't generate a response.")
            else:
                ai_response = f"⚠️ Llama Stack error (HTTP {response.status_code})."
                
            message_placeholder.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
        except Exception as e:
            message_placeholder.markdown(f"❌ Connection error to Llama Stack: {str(e)}")