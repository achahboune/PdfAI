import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure Gemini API
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Please set GOOGLE_API_KEY in your .env file")

try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Error configuring Gemini API: {str(e)}")
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
        prompt = f"""You are a helpful AI assistant that helps users understand PDF documents.
        Answer questions based on the PDF content provided.
        PDF content: {pdf_content}
        Question: {input_text}
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return "I apologize, but I encountered an error while processing your request. Please try again."

# Streamlit UI
st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="📚"
)

# Custom CSS
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
    </style>
    """, unsafe_allow_html=True)

# Header
st.title("📚 AI Chat Assistant")
st.markdown("🎯 Upload a PDF for document-specific answers, or just chat about any topic 🎯")

# File upload
pdf_file = st.file_uploader("", type="pdf")

if pdf_file is not None:
    try:
        # Extract text from PDF
        pdf_content = get_pdf_text(pdf_file)
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input
        if prompt := st.chat_input("Ask me anything! I can help with PDF content or general questions..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)

            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = get_gemini_response(prompt, pdf_content)
                    st.markdown(response)
                
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})

    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
else:
    st.info("Please upload a PDF file to begin chatting about its contents.")
