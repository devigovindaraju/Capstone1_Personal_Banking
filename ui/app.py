import streamlit as st
import os

from utils.chat_history import (
    initialize_chat,
    add_user_message,
    add_bot_message,
    get_history,
    clear_history
)

from utils.validators import validate_json


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Personal Banking AI",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# LOAD CSS
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

CSS_FILE = os.path.join(
    BASE_DIR,
    "static",
    "styles.css"
)

with open(
    CSS_FILE,
    "r",
    encoding="utf-8"
) as f:

    css = f.read()


st.markdown(
    f"<style>{css}</style>",
    unsafe_allow_html=True
)


# =========================================================
# INITIALIZE CHAT
# =========================================================

initialize_chat()

if "clear_json" not in st.session_state:
    st.session_state.clear_json = False


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🤖 Banking AI")

    st.divider()

    if st.button(
        "🗑 Clear Chat",
        use_container_width=True
    ):

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
    unsafe_allow_html=True
)


# =========================================================
# CHAT HISTORY
# =========================================================

for chat in get_history():

    if chat["role"] == "user":

        st.markdown(
            f"""
            <div class="user-message">
                👤 {chat["message"]}
            </div>
            """,
            unsafe_allow_html=True
        )


        if chat.get("request"):

            st.markdown(
                f"""
                <div class="user-message">

                📄 Request:

                <pre>{chat["request"]}</pre>

                </div>
                """,
                unsafe_allow_html=True
            )


    else:

        st.markdown(
            f"""
            <div class="bot-message">
                🤖 {chat["message"]}
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================================
# JSON REQUEST BOX
# =========================================================

if st.session_state.clear_json:

    st.session_state.json_request_box = ""

    st.session_state.clear_json = False


json_request = st.text_area(
    "JSON Request (Optional)",
    placeholder='Example: {"customer_id":"12345"}',
    height=80,
    key="json_request_box"
)

# =========================================================
# NATIVE STREAMLIT CHAT INPUT
# =========================================================

prompt = st.chat_input(
    "Ask something..."
)


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

        st.warning(
            "Please enter a query."
        )

        st.stop()


    # =====================================================
    # VALIDATE JSON
    # =====================================================

    request_payload = None


    if json_request:

        request_payload = validate_json(
            json_request
        )


        if request_payload is None:

            st.error(
                "Invalid JSON format. Please correct your JSON request."
            )

            st.stop()
            

        if request_payload == {}:

            st.error(
                "JSON Request cannot be empty."
            )    

            st.stop()


    # =====================================================
    # SAVE USER MESSAGE
    # =====================================================

    add_user_message(
        message=prompt,
        request=request_payload
    )


    # =====================================================
    # BACKEND RESPONSE
    # =====================================================

    if request_payload is not None:

        response = (
            f"Received query:\n\n"
            f"{prompt}\n\n"
            f"Request:\n\n"
            f"{request_payload}"
        )

    else:

        response = (
            f"Received query:\n\n"
            f"{prompt}"
        )


    # =====================================================
    # SAVE ASSISTANT MESSAGE
    # =====================================================

    add_bot_message(
        response
    )


    # =====================================================
    # CLEAR JSON BOX
    # =====================================================

    st.session_state.clear_json = True



    # =====================================================
    # REFRESH
    # =====================================================

    st.rerun()