import streamlit as st
from llama_stack_client import LlamaStackClient
import os

# Page Configuration
st.set_page_config(page_title="RHOAI Support Assistant", page_icon="🤖")
st.title("🤖 Support Assistant (RHOAI v3 + MCP)")

# Connexion au serveur Llama Stack via le service interne OpenShift
# Port 5000 car c'est celui que nous avons exposé dans notre Service YAML
client = LlamaStackClient(
    base_url="http://llama-stack-service:5000"
)

# Initialisation de l'historique de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrée utilisateur
if prompt := st.chat_input("Ask about JIRA-404, JIRA-123..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        response_placeholder.markdown("⏳ *Querying Llama Stack...*")
        
        try:
            # Appel de l'API Chat Completion (Standard RHOAI v3)
            response = client.chat.completions.create(
                model="meta-llama/Meta-Llama-3-8B-Instruct",
                messages=st.session_state.messages,
                stream=False
            )
            
            # Extraction du contenu de la réponse
            full_response = response.choices[0].message.content
            
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Error: {str(e)}")