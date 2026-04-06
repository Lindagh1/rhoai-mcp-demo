import streamlit as st
import requests

# Page Configuration
st.set_page_config(page_title="RHOAI Support Assistant", page_icon="🤖")
st.title("🤖 Support Assistant (RHOAI + MCP)")
st.markdown("Ask me about a Jira ticket, for example: **What is the status of JIRA-404?**")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# When the user asks a question
if prompt := st.chat_input("Enter your question here..."):
    
    # Show user question in the UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI Response processing
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("⏳ *Thinking and checking Jira via MCP...*")
        
        try:
            # We call our Llama Stack orchestrator (internal OpenShift network)
            url = "http://llama-stack-service:5000/alpha/inference/chat_completion"
            
            payload = {
                "model": "meta-llama/Meta-Llama-3-8B-Instruct",
                "messages": st.session_state.messages
            }
            
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                # Get the AI's reply
                ai_response = data.get("completion_message", {}).get("content", "Sorry, I couldn't generate a response.")
            else:
                ai_response = f"⚠️ Llama Stack error (HTTP {response.status_code}). Please check OpenShift logs."
                
            message_placeholder.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
        except Exception as e:
            message_placeholder.markdown(f"❌ Connection error to Llama Stack: {str(e)}")