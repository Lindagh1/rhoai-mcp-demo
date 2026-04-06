import streamlit as st
from llama_stack_client import LlamaStackClient

# Page Config
st.set_page_config(page_title="RHOAI Support Assistant", page_icon="🤖")
st.title("🤖 Support Assistant (RHOAI v3 + MCP)")

# Initialisation du client Llama Stack
# On pointe vers le service interne OpenShift
client = LlamaStackClient(
    base_url="http://llama-stack-service:5000" 
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage du chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about JIRA-404, JIRA-123..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        try:
            # Utilisation de l'API Agents (plus haut niveau pour le MCP)
            # C'est la méthode recommandée pour que l'IA utilise les outils automatiquement
            response = client.agents.create_agent_turn(
                agent_id="support-agent", # L'ID défini dans ta config Llama Stack
                messages=[{
                    "role": "user",
                    "content": prompt
                }],
                stream=False
            )
            
            # Extraction propre de la réponse
            full_response = response.output_message.content
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Error: {str(e)}")