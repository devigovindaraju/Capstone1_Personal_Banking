import streamlit as st
from services.api_client import send_query


def chat_box():

    st.markdown(
        """
    <style>

    /* Keep input section visible */
    div[data-testid="stTextInput"],
    div[data-testid="stTextArea"],
    div[data-testid="stButton"] {
        position: relative;
        z-index: 10;
    }


    /* Add space at bottom so chat is not hidden */
    .block-container {
        padding-bottom: 180px;
    }

    </style>
    """,
        unsafe_allow_html=True,
    )

    # -----------------------------
    # Session chat storage
    # -----------------------------

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "clear_inputs" not in st.session_state:
        st.session_state.clear_inputs = False

    # -----------------------------
    # Display previous messages
    # -----------------------------

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.write(message["content"])

    st.divider()

    # -----------------------------
    # Two input boxes
    # -----------------------------

    st.markdown('<div class="fixed-input">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("#### 💬 Simple Query")

        simple_query = st.text_input(
            "Ask your question", key="simple_query", placeholder="Example: What is RAG?"
        )

    with col2:

        st.markdown("#### 📝 Query with Request")

        request_query = st.text_area(
            "Enter your request",
            key="request_query",
            placeholder="""
Example:
- Summarize this document
- Generate SQL query
- Analyze customer feedback
- Create a report
            """,
            height=120,
        )

    st.write("")

    # -----------------------------
    # Submit Button
    # -----------------------------

    button_col1, button_col2, button_col3 = st.columns([1, 1, 1])

    with button_col2:

        submit = st.button("🚀 Submit")
    st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------
    # Process Query
    # -----------------------------

    if submit:

        if simple_query.strip() and request_query.strip():

            st.warning("Please use only one input box at a time.")
            return

        elif simple_query.strip():

            query = simple_query.strip()
            query_type = "simple"

        elif request_query.strip():

            query = request_query.strip()
            query_type = "request"

        else:

            st.warning("Please enter a query")
            return
            # Save user message

        st.session_state.messages.append({"role": "user", "content": query})

        # Call backend/mock service

        with st.spinner("Thinking..."):

            response = send_query(query, query_type)

        # Save assistant message

        st.session_state.messages.append(
            {"role": "assistant", "content": response["answer"]}
        )

        st.rerun()
