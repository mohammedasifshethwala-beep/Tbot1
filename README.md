# NCERT and CBSE problem solving tutor

This is a simple Streamlit web app that uses OpenAI's GPT-3.5 Turbo model to act as an NCERT and CBSE problem-solving tutor.

## Features
- Initializes an OpenAI client using `st.secrets["OPENAI_API_KEY"]`.
- Maintains chat history using `st.session_state`.
- Displays conversation using `st.chat_message`.
- Uses `st.chat_input` for entering user messages.

## Setup
1. Create a virtual environment (optional but recommended).
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure your OpenAI API key in Streamlit secrets:
   - Create a `.streamlit` folder in the project directory.
   - Inside it, create a file named `secrets.toml` with:
     ```toml
     OPENAI_API_KEY = "your-openai-api-key-here"
     ```

## Run the app
```bash
streamlit run app.py
```
