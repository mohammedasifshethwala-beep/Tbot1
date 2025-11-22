from openai import OpenAI, RateLimitError
import time

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def get_response(history, user_input: str) -> str:
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
    messages.extend(history)
    messages.append({"role": "user", "content": user_input})

    # Simple retry loop for transient rate limits
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
            )
            return response.choices[0].message.content
        except RateLimitError:
            # Wait a bit and try again
            time.sleep(2 * (attempt + 1))

    # If still failing after retries, show a friendly message
    return (
        "The tutoring service is currently receiving too many requests. "
        "Please wait a bit and try again."
    )

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

