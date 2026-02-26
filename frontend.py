# import streamlit as st
# import requests

# API_URL = "http://127.0.0.1:8000/placementbot" 

# st.title("Placement DAIICT 2026 Batch")
# st.markdown("We are here to help you regarding placement details, dont try to access personal information!")

# # Input fields
# prompt = st.text_input('Enter Your Query Here')

# if st.button("Click here to get the result"):
#     input_data = {
#         "query": prompt
#     }

#     try:
#         response = requests.post(API_URL, json=input_data)
#         result = response.json()

#         # if response.status_code == 200 and "response" in result:
#         #     prediction = result["response"]
#         #     st.success(f"Predicted Insurance Premium Category: **{prediction['predicted_category']}**")
#         #     st.write("🔍 Confidence:", prediction["confidence"])
#         #     st.write("📊 Class Probabilities:")
#         #     st.json(prediction["class_probabilities"])

#         #above code will not work as we are getting 'predicted_category' in the contect of JSON response

#         if response.status_code == 200: # and "final_output" in result:
#             st.success(f"result : {result['Bot response']}")
        
#         else:
#             st.error(f"API Error: {response.status_code}")
#             st.write(result)

#     except requests.exceptions.ConnectionError:
#         st.error("❌ Could not connect to the FastAPI server. Make sure it's running.")

import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/placementbot" 
CLEAR_URL = "http://127.0.0.1:8000/clear_chat"

st.title("Placement DAIICT 2026 Batch")
st.markdown("We are here to help you regarding placement details, dont try to access personal information!")

# Initialize chat history in session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display all previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# # Input field
# prompt = st.chat_input("Enter your query here")

# Chat input
prompt = st.chat_input("Enter your query here")

# Close chat button below input
if st.button("🗑️ Close Chat"):
    # Clear backend session
    try:
        requests.post(CLEAR_URL)
    except:
        pass
    # Clear frontend messages
    st.session_state.messages = []
    st.success("Chat cleared!")
    st.rerun()

if prompt:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Send to backend
    try:
        response = requests.post(API_URL, json={"query": prompt})
        
        if response.status_code == 200:
            result = response.json()
            bot_response = result['Bot response']
            
            # Add bot response to chat
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
            with st.chat_message("assistant"):
                st.markdown(bot_response)
        else:
            st.error(f"API Error: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to the FastAPI server.")