from pypdf import PdfReader 
from typing import List
from fpdf import FPDF
from io import BytesIO
# pip install pymupdf
import fitz  # PyMuPDF
import os
import fitz  # PyMuPDF
import os

# def extract_pdf(file_name: str):
#     import pdb; pdb.set_trace()
#     # 1. Validation
#     print(file_name)
#     if not os.path.exists(file_name):
#         raise FileNotFoundError(f"File not found: {file_name}\nCurrent directory: {os.getcwd()}")

#     # 2. Open Document
#     doc = fitz.open(file_name)

#     print(f"Processing: {file_name} ({doc.page_count} pages)")

#     for page_no in range(doc.page_count):
#         page = doc[page_no]

#         # 3. Extract Blocks
#         # sort=True ensures text is read top-to-bottom, left-to-right
#         blocks = page.get_text("blocks", sort=True)

#         print(f"--- Page {page_no + 1} ---")
#         for b in blocks:
#             # x0, y0, x1, y1 are the bounding box coordinates
#             # txt is the actual content
#             # block_no is the block sequence number
#             # block_type is the type (0=text, 1=image)
#             x0, y0, x1, y1, txt, block_no, block_type = b

#             # Filter out image blocks (type 1) if you only want text
#             if block_type == 0:
#                 # repr() is used to show newlines explicitly (\n)
#                 print(f"Box {(x0, y0, x1, y1)} -> {txt[:50]!r}...")
# Change type hint to accept Streamlit's UploadedFile
# def extract_pdf(uploaded_file):
#     # 1. No need to check os.path.exists, just check if file is not None
#     if uploaded_file is None:
#         raise ValueError("No file uploaded")

#     # 2. Read bytes from the Streamlit object
#     # 'stream' takes the bytes, 'filetype' tells fitz it's a PDF
#     file_bytes = uploaded_file.read()
#     doc = fitz.open(stream=file_bytes, filetype="pdf")

#     print(f"Processing: {uploaded_file.name} ({doc.page_count} pages)")

#     for page_no in range(doc.page_count):
#         page = doc[page_no]
#         blocks = page.get_text("blocks", sort=True)

#         print(f"--- Page {page_no + 1} ---")
#         for b in blocks:
#             x0, y0, x1, y1, txt, block_no, block_type = b
#             if block_type == 0:  # Text only
#                 print(f"Box {(x0, y0, x1, y1)} -> {txt[:50]!r}...")

#     # 3. Important: Reset pointer if you plan to use the file again elsewhere
#     uploaded_file.seek(0)

def extract_pdf_text(file_name):
    reader = PdfReader(file_name)
    texts = ' '
    for page in reader.pages:
        texts += page.extract_text() or ""
    return texts
