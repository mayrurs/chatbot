import streamlit as st
import requests
import json

# Set the Ollama API endpoint
OLLAMA_API_URL = 'http://ollama:11434/api/generate'

# Function to interact with Ollama with streaming output
def get_ollama_response(prompt, placeholder, model='llama3.2'):
    payload = {
        'model': model,
        'prompt': prompt
    }
    headers = {'Content-Type': 'application/json'}

    try:
        # Stream the response from the Ollama API
        with requests.post(OLLAMA_API_URL, headers=headers, json=payload, stream=True) as response:
            if response.status_code == 200:
                # Initialize the full response
                full_response = ''
                # Stream and update the response in real-time
                for line in response.iter_lines(decode_unicode=True):
                    if line:
                        # Ollama streams JSON lines, each representing a part of the response
                        json_data = json.loads(line)
                        content = json_data.get('response', '')
                        full_response += content
                        # Update the placeholder with the new content
                        placeholder.markdown(f"**Bot:** {full_response}")
                return full_response.strip()
            else:
                error_message = f"Error {response.status_code}: {response.text}"
                placeholder.markdown(f"**Bot:** {error_message}")
                return error_message
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        placeholder.markdown(f"**Bot:** {error_message}")
        return error_message

# Initialize Streamlit app
st.title("Ollama Chatbot")

# Initialize conversation history
if 'history' not in st.session_state:
    st.session_state['history'] = []

# Create a container for the conversation
conversation_container = st.container()

# Create a form for user input
with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input("Type your message:")
    submit_button = st.form_submit_button(label='Send')

if submit_button and user_input:
    # Append user message to history
    st.session_state['history'].append({'role': 'user', 'content': user_input})

    # Prepare the conversation prompt
    conversation = ''
    for msg in st.session_state['history']:
        if msg['role'] == 'user':
            conversation += f"User: {msg['content']}\n"
        else:
            conversation += f"Assistant: {msg['content']}\n"
    conversation += "Assistant:"

    # Create a placeholder for the assistant's streaming response
    with conversation_container:
        # Display the conversation history excluding the current assistant's response
        for message in st.session_state['history']:
            if message['role'] == 'user':
                st.markdown(f"**You:** {message['content']}")
            else:
                st.markdown(f"**Bot:** {message['content']}")
        # Placeholder for the assistant's response
        response_placeholder = st.empty()

    # Get response from Ollama with streaming
    response = get_ollama_response(conversation, response_placeholder)

    # Append assistant response to history
    st.session_state['history'].append({'role': 'assistant', 'content': response})

    # Rerun the app to update the conversation history
    st.rerun()
else:
    # Display the conversation history
    with conversation_container:
        for message in st.session_state['history']:
            if message['role'] == 'user':
                st.markdown(f"**You:** {message['content']}")
            else:
                st.markdown(f"**Bot:** {message['content']}")

