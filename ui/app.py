import json
import streamlit as st
import os
import requests
from pathlib import Path


from utils.chat_history import (
    initialize_chat,
    add_user_message,
    add_bot_message,
    get_history,
    clear_history,
)

from utils.validators import validate_json

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(page_title="Personal Banking AI", page_icon="", layout="wide")


# =========================================================
# LOAD CSS
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CSS_FILE = os.path.join(BASE_DIR, "static", "styles.css")

with open(CSS_FILE, "r", encoding="utf-8") as f:

    css = f.read()


st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


# =========================================================
# INITIALIZE CHAT
# =========================================================

initialize_chat()

if "clear_json" not in st.session_state:
    st.session_state.clear_json = False

if "pending_request" not in st.session_state:
    st.session_state.pending_request = None


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    if st.button("Clear Chat", use_container_width=True):

        clear_history()

        st.rerun()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="chat-header">
        Personal Banking Assistant
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# CHAT HISTORY
# =========================================================

for chat in get_history():

    if chat["role"] == "user":

        st.markdown(
            f"""
            <div class="user-message">
                {chat["message"]}
            </div>
            """,
            unsafe_allow_html=True,
        )

        if chat.get("request"):

            st.markdown(
                f"""
                <div class="user-message">


                <pre>{chat["request"]}</pre>

                </div>
                """,
                unsafe_allow_html=True,
            )



    else:

        if isinstance(chat["message"], dict):
            st.json(chat["message"])
        else:
            citation_html = ""
            if chat.get("citations"):
                citation_html += "<hr style='border-top: 1px solid #ccc; margin: 10px 0;'>"
                citation_html += "<p style='font-size: 0.85em; color: #666;'><strong> Sources:</strong></p><ul style='margin: 0; padding-left: 20px; font-size: 0.85em; color: #666;'>"
                for c in chat["citations"]:
                    file_name = Path(c['source']).name
                    page_num = c['page'] + 1
                    citation_html += f"<li>{file_name} (Page {page_num})</li>"
                citation_html += "</ul>"

            # 2. Render everything together inside your custom div
            st.markdown(
                f"""
                <div class="bot-message">
                    <p style="margin: 0;">{chat["message"]}</p>
                    {citation_html}
                </div>
                """,
                unsafe_allow_html=True
            )

if st.session_state.pending_request is not None:

    pending = st.session_state.pending_request

    with st.spinner("Processing your request..."):

        try:

            api_response = requests.post(
                "http://localhost:9000/api/v1/advisor/", json=pending["payload"]
            )

            result = api_response.json()

            # st.write("Backend result:", result)

            backend_response = result["response"] #json.loads(result["response"])

            response = backend_response["answer"]
            citations = backend_response["citations"]       
         
            if backend_response["json_input"]:

            # User input is JSON
                add_bot_message(backend_response, None)

            else:
            # User input is plain text
                add_bot_message(response, citations)   
          

        except requests.exceptions.RequestException as e:

            add_bot_message(f"Unable to process your request: {e}")

        finally:

            st.session_state.pending_request = None

            st.session_state.clear_json = True

            st.rerun()

# =========================================================
# JSON REQUEST BOX
# =========================================================

if st.session_state.clear_json:

    st.session_state.json_request_box = ""

    st.session_state.clear_json = False


json_request = st.text_area(
    "JSON Request",
    placeholder="Json Request",
    height=80,
    key="json_request_box",
    label_visibility="collapsed",
)
# =========================================================
# NATIVE STREAMLIT CHAT INPUT
# =========================================================

prompt = st.chat_input("Ask something...")

# =========================================================
# SUBMIT LOGIC
# =========================================================

if prompt is not None:

    prompt = prompt.strip()

    json_request = json_request.strip()

    # =====================================================
    # VALIDATE EMPTY PROMPT
    # =====================================================

    if not prompt:

        st.warning("Please enter a query.")

        st.stop()

    # =====================================================
    # VALIDATE JSON
    # =====================================================

    request_payload = None

    if json_request:

        request_payload = validate_json(json_request)

        if request_payload is None:

            st.error("Invalid JSON format. Please correct your JSON request.")

            st.stop()

        if request_payload == {}:

            st.error("JSON Request cannot be empty.")

            st.stop()

    # =====================================================
    # SAVE USER MESSAGE
    # =====================================================

    add_user_message(message=prompt, request=request_payload)

# =====================================================
# PREPARE BACKEND PAYLOAD
# =====================================================
if prompt is not None:
    payload = {"question": prompt}

    if request_payload is not None:
        payload["customer_profile"] = request_payload

    # =====================================================
    # STORE PENDING REQUEST
    # =====================================================

    st.session_state.pending_request = {"payload": payload}
    # =====================================================
    # RERUN TO SHOW USER MESSAGE
    # =====================================================

    st.rerun()
