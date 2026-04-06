import streamlit as st
from llama_stack_client import LlamaStackClient
import os

# Configuration de la page
st.set_page_config(page_title="RHOAI Support Assistant", page_icon="🤖")
st.title("🤖 Support Assistant (RHOAI v3 + MCP)")

# Connexion au serveur Llama Stack (Service interne OpenShift)
client = LlamaStackClient(
    base_url="http://llama-stack-service:5000"
)

# Initialisation de l'historique
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des messages précédents
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrée utilisateur
if prompt := st.chat_input("How can I help you with Jira today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        response_placeholder.markdown("⏳ *Querying Llama Stack & Jira...*")
        
        try:
            # Appel via l'API Chat Completion du SDK
            response = client.chat.completions.create(
                model="meta-llama/Meta-Llama-3-8B-Instruct",
                messages=st.session_state.messages,
                stream=False
            )
            
            # Extraction de la réponse
            full_response = response.choices[0].message.content
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Error connecting to Llama Stack: {str(e)}")