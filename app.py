import streamlit as st
from openai import OpenAI

# Configure the page
st.set_page_config(page_title="NCERT and CBSE problem solving tutor ")

# Initialize OpenAI client using API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set the app title
st.title("NCERT and CBSE problem solving tutor ")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []


def get_response(history, user_input: str) -> str:
    """Send conversation history and new user input to OpenAI and return the response."""
    # Start with a system message to guide the assistant's behavior
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful tutor specializing in NCERT and CBSE curriculum. "
                "Explain concepts clearly, solve problems step by step, and adjust your "
                "explanations to the student's level."
            ),
        }
    ]

    # Add previous conversation history
    messages.extend(history)

    # Add the new user message
    messages.append({"role": "user", "content": user_input})

    # Call OpenAI Chat Completions API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
    )

    return response.choices[0].message.content


# Display existing chat history
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# Input box for the user message
user_input = st.chat_input("Ask your NCERT/CBSE question here...")

if user_input:
    # Show the user's message immediately
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get assistant response using history + new user input
    assistant_reply = get_response(st.session_state["messages"], user_input)

    # Append to session state chat history
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.session_state["messages"].append({"role": "assistant", "content": assistant_reply})

    # Display assistant reply
    with st.chat_message("assistant"):
        st.markdown(assistant_reply)
