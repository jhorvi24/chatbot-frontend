import streamlit as st
import requests
import json

# Set page config
st.set_page_config(page_title="AWS Bedrock Chatbot", page_icon="🤖", layout="centered")

# Initialize session state for chat history
if 'messages' not in st.session_state:
  st.session_state.messages = []

# Function to send message to API Gateway
def send_message(prompt):
  api_gateway_url = "https://lkpud2h5xj.execute-api.us-east-1.amazonaws.com/test/siigo"
  headers = {
      "Content-Type": "application/json"
  }
  data = {
      "prompt": prompt #the prompt sent to the aws lambda function in the POST method
  }
  response = requests.post(api_gateway_url, headers=headers, data=json.dumps(data))
  return response.json()['response'] # response is the key of the lambda function when the api answers the request

# Streamlit UI
st.title("AWS Bedrock Chatbot")

# Display chat messages
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
      st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What's on your mind?"):
  # Add user message to chat history
  st.session_state.messages.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
      st.markdown(prompt)
  
  # Get bot response
  with st.chat_message("assistant"):
      message_placeholder = st.empty()
      full_response = ""
      with st.spinner("Thinking..."):
          bot_response = send_message(prompt)
      message_placeholder.markdown(bot_response)
  
  # Add bot response to chat history
  st.session_state.messages.append({"role": "assistant", "content": bot_response})

# Add a button to clear chat history
if st.button("Clear Chat History"):
  st.session_state.messages = []
  st.rerun()