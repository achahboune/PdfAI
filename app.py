import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()

# Configurer l'API Gemini
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Veuillez définir GOOGLE_API_KEY dans votre fichier .env")

try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Erreur de configuration de l'API Gemini : {str(e)}")
    st.stop()

def get_pdf_text(pdf_file):
    text = ""
    pdf_reader = PdfReader(pdf_file)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def get_gemini_response(input_text, pdf_content):
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"""Vous êtes un assistant IA qui aide les utilisateurs à comprendre les documents PDF.
        Répondez aux questions en vous basant sur le contenu du PDF fourni.
        Contenu du PDF : {pdf_content}
        Question : {input_text}
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Erreur lors de la génération de la réponse : {str(e)}")
        return "Je m'excuse, mais j'ai rencontré une erreur lors du traitement de votre demande. Veuillez réessayer."

# Interface Streamlit
st.set_page_config(
    page_title="Assistant IA Chat",
    page_icon="📚"
)

# CSS personnalisé
st.markdown("""
    <style>
    .stApp {
        max-width: 800px;
        margin: 0 auto;
    }
    .upload-btn {
        background-color: #9146FF !important;
        color: white !important;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        background-color: #f0f2f6;
    }
    .stMarkdown {
        font-size: 16px !important;
    }
    /* Personnalisation de la zone de dépôt de fichiers */
    [data-testid="stFileUploader"] {
        width: 100%;
    }
    [data-testid="stFileUploader"] section {
        padding: 1rem;
        border: 2px dashed #9146FF;
        border-radius: 0.5rem;
        background: #f8f9fa;
    }
    [data-testid="stFileUploader"] section [data-testid="stMarkdownContainer"] p {
        font-size: 1.1em;
        color: #666;
        text-align: center;
    }
    /* Masquer le texte par défaut en anglais */
    [data-testid="stFileUploader"] section div:has(+ div p) {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

# En-tête
st.title("📚 Assistant IA Chat")
st.markdown("🎯 Déposez votre PDF pour obtenir des réponses personnalisées 🎯")

# Upload de fichier
st.markdown("<p style='text-align: center; color: #666; margin-bottom: 10px;'>💫 Glissez-déposez votre fichier PDF ici 💫</p>", unsafe_allow_html=True)
pdf_file = st.file_uploader("", type="pdf")

if pdf_file is not None:
    try:
        # Extraire le texte du PDF
        pdf_content = get_pdf_text(pdf_file)
        
        # Initialiser l'historique du chat
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Afficher l'historique du chat
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Entrée du chat
        if prompt := st.chat_input("Posez votre question sur le contenu du PDF..."):
            # Ajouter le message de l'utilisateur à l'historique
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Afficher le message de l'utilisateur
            with st.chat_message("user"):
                st.markdown(prompt)

            # Obtenir la réponse de l'IA
            with st.chat_message("assistant"):
                with st.spinner("Réflexion en cours..."):
                    response = get_gemini_response(prompt, pdf_content)
                    st.markdown(response)
                
            # Ajouter la réponse de l'assistant à l'historique
            st.session_state.messages.append({"role": "assistant", "content": response})

    except Exception as e:
        st.error(f"Erreur lors du traitement du PDF : {str(e)}")
else:
    st.info("Veuillez télécharger un fichier PDF pour commencer la conversation.")
