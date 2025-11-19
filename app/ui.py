import streamlit as st

def pdf_uploader():
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf",accept_multiple_files=True,help="Upload PDF files for processing.")
    if uploaded_file is not None:
        return uploaded_file
    return None