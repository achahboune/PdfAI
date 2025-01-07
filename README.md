# PdfAI - PDF Chat Assistant

A Streamlit-based application that allows users to chat with their PDF documents using Google's Gemini 2.0 AI model.

## Features

- PDF document upload and processing
- Interactive chat interface
- Context-aware responses based on PDF content
- Modern and user-friendly UI

## Local Development

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root and add your Google API key:
```
GOOGLE_API_KEY=your_api_key_here
```

3. Run the application locally:
```bash
streamlit run app.py
```

## Deployment on Streamlit Cloud

1. Push your code to GitHub:
   - Create a new repository
   - Initialize git and push your code
   - Make sure `.env` is in `.gitignore`

2. Visit [Streamlit Cloud](https://streamlit.io/cloud)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set the main file path as `app.py`
   - Add your secrets in the Streamlit Cloud dashboard

## Environment Variables

The following secrets need to be set in Streamlit Cloud:
- `GOOGLE_API_KEY`: Your Google API key for Gemini

## Requirements

- Python 3.7+
- Streamlit
- Google Generative AI
- PyPDF2
- python-dotenv
