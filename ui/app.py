import streamlit as st
import json


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

#MainMenu {
    display:none;
}

header {
    display:none;
}

footer {
    display:none;
}


.block-container {

    max-width:1100px;

    padding-bottom:200px;

}


/* User message */

.user-message {

    background:#DCF8C6;

    padding:12px 18px;

    border-radius:15px;

    margin:10px 0;

    width:fit-content;

    max-width:80%;

    margin-left:auto;

}


/* Assistant message */

.bot-message {

    background:#F1F1F1;

    padding:12px 18px;

    border-radius:15px;

    margin:10px 0;

    width:fit-content;

    max-width:80%;

}


/* Wider textbox */

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

    st.session_state.chat_history = []



# -------------------------------
# Sidebar
# -------------------------------

with st.sidebar:


    st.title("🤖 Banking AI")


    # if st.button("📂 Upload File"):

    #     st.switch_page(
    #         "pages/Upload_File.py"
    #     )


    # st.divider()


    if st.button("🗑 Clear Chat"):

        st.session_state.chat_history = []

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
# Display History
# -------------------------------

for chat in st.session_state.chat_history:


    if chat["role"] == "user":


        request_text = ""


        if chat.get("request"):


            request_text = f"""

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
# Input Area
# -------------------------------


json_request = st.text_area(

    "JSON Request (Optional)",

    placeholder='Example: {"customer_id":"12345"}',

    height=90

)



with st.form(

    "chat_form",

    clear_on_submit=True

):


    prompt = st.text_input(

        "Message",

        placeholder="Ask something..."

    )


    submit = st.form_submit_button(

        "➤ Send"

    )



# -------------------------------
# Submit
# -------------------------------

if submit:


    if json_request and not prompt:


        st.warning(
            "Please send a query along with the JSON request."
        )


    else:


        request_payload = None


        if json_request:


            try:

                request_payload = json.loads(
                    json_request
                )


            except json.JSONDecodeError:


                st.error(
                    "Invalid JSON format."
                )

                st.stop()



        # Save user message

        st.session_state.chat_history.append(

            {
                "role":"user",
                "message":prompt,
                "request":request_payload
            }

        )


        # Replace with your API response

        response = f"""
Received query:

{prompt}

Request:

{request_payload}
"""


        # Save assistant response

        st.session_state.chat_history.append(

            {
                "role":"assistant",
                "message":response
            }

        )


        st.rerun()