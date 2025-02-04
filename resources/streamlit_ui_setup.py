import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Streamlit UI setup
st.set_page_config(page_title="Chat with API", layout="centered")
st.title("Chat API Interface")
load_dotenv()

# Fetch the API key securely
TAMM_SEARCH_KEY_GovAcademy = os.getenv("TAMM_SEARCH_KEY_GOV_ACADEMY")

# Function to call API
def call_api(user_input):
    api_url = "https://tamm-convai-dev-apigw.azure-api.net/conv-ai-engine/rag_search"
    
    api_payload = {
        "prompt_name": "gov-academy-course-query",
        "index_configs": [
            {
                "name": "gov-academy-courses",
                "number_of_results": 10,
                "select_fields": [
                    "Name", "Summary", "Type", "Skills", "Language", "Proficiency", "Duration", "URL"
                ],
                "full_text_fields": ["FullText"],
                "vector_fields": ["FullTextVector"]
            }
        ],
        "messages": [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages]
    }

    headers = {
        "Content-Type": "application/json",
        "x-tamm-search-key": TAMM_SEARCH_KEY_GovAcademy  # Secure API key storage
    }

    try:
        response = requests.post(api_url, json=api_payload, headers=headers, timeout=10)
        response.raise_for_status()  # Raise error for 4xx/5xx responses
        response_data = response.json()

        # Extract agent response correctly
        return response_data.get("data", {}).get("agent_response", "No agent response received.")

    except requests.exceptions.Timeout:
        return "API request timed out. Please try again."
    except requests.exceptions.HTTPError as e:
        return f"HTTP Error: {str(e)}"
    except requests.exceptions.ConnectionError:
        return "Connection error. Please check your internet."
    except requests.exceptions.RequestException as e:
        return f"API Request Error: {str(e)}"
    except Exception as e:
        return f"Unexpected Error: {str(e)}"
    
# Initialize chat history if not already present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Ask something...")
if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Call API and get response
    response = call_api(user_input)
    
    # Add API response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)