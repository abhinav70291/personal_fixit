import streamlit as st
import requests


st.title('Welcome to Fixit Ai, your personal docbot!')

PARSE_PDF_ENDPOINT = "https://personal-fixit.onrender.com/parse_pdf_create_vector_database"
QUERY_ENDPOINT = "https://personal-fixit.onrender.com/query"
DOCUMENT_LIST_ENDPOINT = "https://personal-fixit.onrender.com/document_list"


try:
    doc_list_response = requests.get(DOCUMENT_LIST_ENDPOINT)
    if doc_list_response.status_code == 200:
        document_list = doc_list_response.json()

        if "ALL" not in document_list:
            document_list.insert(0, "ALL")
    else:
        document_list = ["ALL"]
        st.sidebar.error("No documents currently available.")
except requests.exceptions.RequestException as e:
    document_list = ["ALL"]
    st.sidebar.error("Error fetching document list.")

# Sidebar for file upload and document list
with st.sidebar:
    st.header("PDF Upload")
    uploaded_files = st.file_uploader("Choose PDF files", accept_multiple_files=True, type='pdf')

    st.header("Documents in Use")
    for doc_name in document_list:
        if doc_name != "ALL":  # Skip "ALL" in the sidebar list
            st.write(doc_name)

# Main page for query and document selection
st.header("Search and Select Document")
query = st.text_input("Enter your query here", key="query")
selected_document = st.selectbox("Choose a document:", document_list, key="document_selector")
submit_button = st.button("Search", key="submit")


if uploaded_files:
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        response = requests.post(
            PARSE_PDF_ENDPOINT,
            files={"file": (uploaded_file.name, bytes_data)},
        )
        if response.status_code == 200:
            st.success(f"Processed {uploaded_file.name}: {response.json()}")
        else:
            st.error(f"Failed to process {uploaded_file.name}")

# Send query and display response when the submit button is clicked
if submit_button and query:
    payload = {
        "text": query,
        "file_name": f'{selected_document}'
    }
    response = requests.post(QUERY_ENDPOINT, json=payload)
    if response.status_code == 200:
        data = response.json()
        st.write(data['response'])
        with st.expander("Chunks"):
            st.write(data['chunks'])
    else:
        st.error("Failed to get a response from the query endpoint")

