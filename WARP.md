# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project overview

This repository contains a small Streamlit web application that uses OpenAI's Chat Completions API (GPT-3.5 Turbo) to act as an NCERT and CBSE problem-solving tutor. The app presents a chat-style interface where students can ask curriculum-related questions and receive step-by-step explanations.

Key points:
- UI and logic are implemented in a single file: `app.py`.
- The app runs entirely via Streamlit; there is no separate backend service beyond the Streamlit process itself.
- OpenAI credentials are read from Streamlit secrets (`st.secrets["OPENAI_API_KEY"]`).

## Development setup & commands

Dependencies are managed with `pip` and listed in `requirements.txt`.

Common commands:
- Install dependencies:
  - `pip install -r requirements.txt`
- Run the Streamlit app (development server with auto-reload):
  - `streamlit run app.py`

Configuration:
- Streamlit secrets are required for the app to work:
  - Create a `.streamlit` directory at the project root.
  - Inside it, create `secrets.toml` with:
    - `OPENAI_API_KEY = "your-openai-api-key-here"`

Testing and linting:
- There is currently no test suite or linting configuration defined in this repository.

## App architecture & data flow

Everything is implemented in `app.py`, organized around a single Streamlit page and a helper function for calling OpenAI.

High-level flow:
1. **Page setup and OpenAI client**
   - The page title is configured via `st.set_page_config` and `st.title`.
   - An OpenAI `client` is created at import time using `OpenAI(api_key=st.secrets["OPENAI_API_KEY"])`.

2. **Session state for chat history**
   - Chat history is stored in `st.session_state["messages"]`, initialized as a list of message dicts with shape `{ "role": <"user"|"assistant">, "content": <str> }`.
   - This list represents the conversation from the user's perspective and is used both to render previous messages and to build the prompt for the model.

3. **Model interaction (`get_response`)**
   - `get_response(history, user_input)` constructs the messages sent to OpenAI:
     - Starts with a **system** message that defines the tutor's role and behavior (NCERT/CBSE-focused, step-by-step explanations, adjusting to student level).
     - Appends prior conversation messages from `history`.
     - Adds the new **user** message.
   - Calls `client.chat.completions.create` with:
     - `model="gpt-3.5-turbo"`
     - The full `messages` list
     - `temperature=0.7`
   - Returns `response.choices[0].message.content` as the assistant's reply.

4. **Rendering and interaction loop**
   - On each page load, existing messages from `st.session_state["messages"]` are rendered using `st.chat_message(role)` and `st.markdown(content)`.
   - `st.chat_input("Ask your NCERT/CBSE question here...")` captures the next user input.
   - When `user_input` is provided:
     - The user message is immediately displayed via `st.chat_message("user")`.
     - `get_response` is called with the current history plus the new user input.
     - Both the user message and assistant reply are appended to `st.session_state["messages"]`.
     - The assistant reply is displayed via `st.chat_message("assistant")`.
   - Streamlit's rerun behavior ensures that, on subsequent interactions, the full conversation stored in session state is re-rendered.

5. **State and persistence characteristics**
   - Chat history is **session-scoped**: it lives in `st.session_state` and is not persisted to disk or a database.
   - Refreshing the browser session or clearing Streamlit state will reset the conversation.

## Notes for future Warp agents

- When modifying the conversation behavior (e.g., changing the model, temperature, or system prompt), keep the shape of `messages` consistent (`{"role": ..., "content": ...}`) so session history continues to work.
- If you introduce new functionality (e.g., multiple pages or richer tutoring modes), consider factoring logic out of `app.py` into separate modules while keeping the Streamlit UI layer thin and stateful via `st.session_state`.
- Any change that touches authentication or API usage should respect that the API key is expected to come from `st.secrets["OPENAI_API_KEY"]` and not from environment variables or hard-coded values, unless you also update the README and this file accordingly.
