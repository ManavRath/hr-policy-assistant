import streamlit as st
from rag import generate_answer

st.set_page_config(page_title="HR Policy Assistant", page_icon="🏢")
st.title("🏢 HR Policy Assistant")

# Session state: maintain per-user chat history (fixes cross-session pollution)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
query = st.chat_input("Ask an HR policy question...")

if query:
    # Guard: empty/whitespace query
    if not query.strip():
        st.warning("Please enter a valid question.")
    else:
        # Show user message
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.write(query)

        # Generate response with spinner
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_answer(
                    query,
                    chat_history=st.session_state.chat_history
                )

            st.write(response)

        # Update history
        st.session_state.chat_history.append(f"User: {query}")
        st.session_state.chat_history.append(f"Assistant: {response}")
        st.session_state.messages.append({"role": "assistant", "content": response})