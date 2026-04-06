import streamlit as st
import requests

st.set_page_config(page_title="Llama Stack Debugger", page_icon="🔍")
st.title("🔍 Llama Stack - Model Scanner")

# L'URL standard pour lister les modèles dans Llama Stack
MODELS_URL = "http://llama-stack-service:5000/v1/models"

st.info("This tool will check which models are actually registered in your Llama Stack server.")

if st.button("List Available Models"):
    try:
        # On fait une requête GET sur l'endpoint des modèles
        response = requests.get(MODELS_URL, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            st.success("✅ Connected to Llama Stack!")
            
            # On affiche le résultat brut pour ne rien rater
            st.write("### Internal Model Registry:")
            st.json(data)
            
            # Petit guide pour t'aider à lire le résultat
            if "data" in data and len(data["data"]) > 0:
                st.balloons()
                st.write("👉 **Look for the 'id' field.** That is the exact string you must use in your chat app.")
            else:
                st.warning("⚠️ The list is empty. Llama Stack doesn't see any models. Check your ConfigMap indentation.")
        else:
            st.error(f"❌ Server returned error {response.status_code}: {response.text}")
            
    except Exception as e:
        st.error(f"❌ Connection failed: {str(e)}")
        st.write("Check if 'llama-stack-service' is reachable on port 5000.")