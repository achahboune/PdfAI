import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import os

# Configuration initiale
load_dotenv()

# Configuration de l'API Gemini
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("❌ La clé API GOOGLE_API_KEY n'est pas définie dans le fichier .env")

try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"❌ Erreur de configuration de l'API Gemini : {str(e)}")
    st.stop()

def get_pdf_text(pdf_file):
    """Extraction du texte depuis le PDF"""
    text = ""
    pdf_reader = PdfReader(pdf_file)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def get_gemini_response(input_text, pdf_content):
    """Génération de la réponse via l'API Gemini"""
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"""En tant qu'assistant immobilier expert, analysez ce document PDF et répondez aux questions.
        Basez vos réponses uniquement sur le contenu du document fourni.
        
        Document : {pdf_content}
        Question : {input_text}
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"❌ Erreur lors de l'analyse : {str(e)}")
        return "Désolé, je n'ai pas pu analyser votre demande. Veuillez réessayer."

# Configuration de la page
st.set_page_config(
    page_title="Assistant PDF Immobilier",
    page_icon="🏠",
    layout="centered"
)

# Style personnalisé
st.markdown("""
    <style>
    .stApp {
        max-width: 1000px;
        margin: 0 auto;
        padding: 1rem;
        background-color: white;
    }
    .main-title {
        text-align: center;
        color: #1E88E5;
        margin-bottom: 2rem;
    }
    .upload-zone {
        background-color: white;
        text-align: center;
        padding: 1rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        background-color: white;
        border-left: 5px solid #1E88E5;
    }
    .stMarkdown {
        font-size: 16px !important;
    }
    [data-testid="stFileUploader"] section {
        border: none !important;
        padding: 0 !important;
        background: none !important;
    }
    [data-testid="stFileUploader"] section div:first-child {
        display: none;
    }
    /* Suppression des éléments non désirés */
    .st-emotion-cache-r421ms {
        background-color: white !important;
    }
    .stApp > header {
        background-color: transparent !important;
    }
    .stApp {
        background-color: white !important;
    }
    div[data-testid="stToolbar"] {
        display: none;
    }
    .st-emotion-cache-18ni7ap {
        background-color: white !important;
    }
    .st-emotion-cache-1dp5vir {
        background-color: white !important;
    }
    .st-emotion-cache-1wbqy5l {
        background-color: white !important;
    }
    footer {
        display: none;
    }
    /* Personnalisation de la zone de dépôt */
    [data-testid="stFileUploader"] {
        width: 100%;
    }
    .uploadfile-container {
        border: none !important;
        background: none !important;
    }
    .uploadfile-container:hover {
        border: none !important;
        background: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# En-tête de l'application
st.markdown('<h1 class="main-title">🏠 Assistant PDF Immobilier</h1>', unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; padding: 1rem;'>
        <p style='font-size: 1.2em; color: #666;'>
            Analysez vos documents immobiliers en quelques secondes
        </p>
    </div>
""", unsafe_allow_html=True)

# Zone de téléchargement simplifiée
with st.container():
    st.markdown('<div class="upload-zone">', unsafe_allow_html=True)
    pdf_file = st.file_uploader("", type="pdf")
    if not pdf_file:
        st.markdown("_Glissez-déposez votre fichier ou cliquez pour le sélectionner_")
    st.markdown('</div>', unsafe_allow_html=True)

# Zone de chat
if pdf_file is not None:
    try:
        # Extraction du texte
        pdf_content = get_pdf_text(pdf_file)
        
        # Initialisation de l'historique
        if "messages" not in st.session_state:
            st.session_state.messages = []
            st.session_state.messages.append({
                "role": "assistant",
                "content": "👋 J'ai analysé votre document. Que souhaitez-vous savoir ?"
            })

        # Affichage des messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Zone de saisie
        if prompt := st.chat_input("💭 Posez votre question sur le document..."):
            # Message utilisateur
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Réponse de l'assistant
            with st.chat_message("assistant"):
                with st.spinner("🤔 Analyse en cours..."):
                    response = get_gemini_response(prompt, pdf_content)
                    st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

    except Exception as e:
        st.error(f"❌ Erreur lors de l'analyse du PDF : {str(e)}")
else:
    st.info("👆 Commencez par télécharger un document PDF pour l'analyser")
