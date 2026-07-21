import streamlit as st
import time


# -------------------------------
# Page Config
# -------------------------------

st.set_page_config(
    page_title="Personal Banking AI",
    page_icon="🤖",
    layout="wide"
)


# -------------------------------
# CSS
# -------------------------------

st.markdown(
"""
<style>

/* Hide Streamlit default UI */

#MainMenu {
    display:none;
}

header {
    display:none;
}

footer {
    display:none;
}


/* Main chat width */

.block-container {

    max-width:1100px;

    padding-bottom:180px;

}



/* Chat bubbles */

.user-message {

    background:#DCF8C6;

    padding:12px 18px;

    border-radius:15px;

    margin:10px 0;

    width:fit-content;

    max-width:80%;

    margin-left:auto;

}


.bot-message {

    background:#F1F1F1;

    padding:12px 18px;

    border-radius:15px;

    margin:10px 0;

    width:fit-content;

    max-width:80%;

}


/* Fixed input section */


.input-area {

    position: fixed;

    bottom: 0;

    left: 0;

    right: 0;

    background: white;

    padding: 12px 10%;

    border-top: 1px solid #ddd;

    z-index: 9999;

}


/* Send button */

.stFormSubmitButton button {

    border-radius: 50%;

    width: 45px;

    height: 45px;

    font-size: 22px;

    padding: 0;

}


/* Remove default form spacing */

.stForm {

    margin-bottom:0;

}


/* Error popup style */

.chat-alert {

    position: fixed;

    bottom: 170px;

    left: 50%;

    transform: translateX(-50%);

    background:#fff3cd;

    color:#664d03;

    padding:12px 20px;

    border-radius:10px;

    box-shadow:0px 4px 12px rgba(0,0,0,0.15);

    z-index:10000;

}

/* prevent textbox from shifting */

.input-area textarea {


    width:100% !important;

}
/* Make textboxes wider */


.stTextArea textarea {


    font-size:16px;


}


</style>
""",
unsafe_allow_html=True
)



# -------------------------------
# Session Memory
# -------------------------------

if "chat_history" not in st.session_state:

    st.session_state.chat_history=[]


if "json_value" not in st.session_state:
    st.session_state.json_value = ""   



# -------------------------------
# Sidebar
# -------------------------------


with st.sidebar:


    st.title("🤖 Banking AI")


    st.write("")


    if st.button("📂 Upload File"):

        st.switch_page(
            "pages/Upload_File.py"
        )


    st.divider()


    if st.button("🗑 Clear Chat"):

        st.session_state.chat_history=[]

        st.rerun()




# -------------------------------
# Header
# -------------------------------


st.title(
    "Personal Banking Assistant"
)


st.caption(
    "Ask questions related to banking services"
)



# -------------------------------
# Display Chat History
# -------------------------------


for chat in st.session_state.chat_history:


    if chat["role"] == "user":

        request_text = ""

        if chat.get("request"):

            request_text = f"""
            
            <br>
            📄 Request:
            <pre>{chat["request"]}</pre>

            """

        st.markdown(

            f"""
            <div class="user-message">

            👤 {chat["message"]}

            {request_text}

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


# -------------------------------
# Fixed Input Area
# -------------------------------


# -------------------------------
# Fixed Input Area
# -------------------------------

# -------------------------------
# Fixed Input Area
# -------------------------------

# -------------------------------
# Fixed Input Area
# -------------------------------

st.markdown(
    """
    <div class="input-area">
    """,
    unsafe_allow_html=True
)


# JSON Request Box

json_request = st.text_area(
    "JSON Request (Optional)",
    value=st.session_state.json_value,
    placeholder='Example: {"customer_id":"12345"}',
    height=80
)



# Prompt Box

with st.form(
    key="chat_form",
    clear_on_submit=False
):

    prompt = st.text_input(
        "Message",
        placeholder="Ask something..."
    )


    submit = st.form_submit_button(
    "➤"
)



# Submit Logic

if submit:


    # JSON only case

    if json_request and not prompt:


        st.warning(
            "Please send a query along with the JSON request."
        )


    else:


        request_payload = None


        # Validate JSON

        if json_request:


            import json


            try:

                request_payload = json.loads(
                    json_request
                )


            except json.JSONDecodeError:


                st.markdown(
                """
                <div class="chat-alert">
                ❌ Invalid JSON format. Please correct your JSON request.
                </div>
                """,
                unsafe_allow_html=True
)

                st.stop()



        # Save user message

        st.session_state.chat_history.append(
            {
                "role": "user",
                "message": prompt,
                "request": request_payload
            }
        )


        # Backend response placeholder

        response = (
            "Received your request successfully."
        )


        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "message": response
            }
        )


        # Clear JSON textbox

        st.session_state.json_value = ""


        st.rerun()



st.markdown(
    """
    </div>
    """,
    unsafe_allow_html=True
)