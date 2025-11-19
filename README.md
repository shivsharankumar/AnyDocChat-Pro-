# AnyDocChat Pro

AnyDocChat Pro is your intelligent document assistant—beautiful, fast, and trustworthy. Built on Streamlit, it lets clinicians, researchers, and operations teams converse with the contents of medical PDFs. Uploaded documents are chunked, embedded with Hugging Face sentence transformers, indexed in FAISS, and queried through either Groq or EuriAI chat models via LangChain.

## Features
- Upload one or many PDF files directly from the Streamlit UI.
- Extract and chunk PDF text before building a FAISS similarity index backed by Hugging Face embeddings.
- Ask natural-language questions and stream answers from Groq (`mixtral-8x7b`, `llama3-70b`, etc.) or EuriAI hosted models.
- Keep credentials in a `.env` file while `.gitignore` prevents accidental commits.
- Includes `sample_data/` with synthetic medical histories for quick demos.

## Project Layout
```
.
├── app/
│   ├── chat_utils.py          # LLM provider selection & invocation helpers
│   ├── pdf_utils.py           # PDF extraction utilities
│   ├── ui.py                  # Streamlit file uploader widget
│   └── vectorstore_utils.py   # Embedding + FAISS helpers
├── main.py                    # Streamlit entrypoint (UI & chat flow)
├── requirements.txt
├── sample_data/               # Example PDFs for demos
└── README.md
```

## Prerequisites
- Python 3.10+
- `pip` (or `uv`/`pipx` if you prefer)
- Optional: `virtualenv`/`venv` for isolated environments

## Setup
1. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```
2. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. **Configure API keys**  
   Create a `.env` file in the project root and add whichever keys you have access to:
   ```
   groq_api_key="your-groq-key"
   euri_api_key="your-euriai-key"
   ```
   Only one needs to be present, depending on the `platform` you choose in `chat_utils.get_chat_model`.

## Running the app
```bash
streamlit run main.py
```

The Streamlit UI provides:
1. **Upload PDFs** through the sidebar uploader (`Upload your documents`).
2. **Process Documents**, which extracts text, chunks it (RecursiveCharacterTextSplitter), and builds a FAISS vector store.
3. **Chat** using `st.chat_message`, where each user prompt retrieves relevant chunks and forwards a context-rich prompt to the configured LLM.

## Sample data
`sample_data/` hosts several anonymized medical history PDFs. Use them for demos or testing by uploading through the UI.

## Development tips
- `app/pdf_utils.py` currently uses `pypdf` for text extraction; swap in the more advanced (commented) PyMuPDF routine if you need layout-aware blocks.
- `app/vectorstore_utils.py` defaults to `sentence-transformers/all-MiniLM-L6-v2`; adjust `embedding_model_name` if you need higher recall.
- Extend `app/chat_utils.py` to register additional model providers or change temperatures/system prompts for domain-specific tone.

## Troubleshooting
- **No model available**: confirm that the relevant API key is exported or stored in `.env`.
- **FAISS import errors**: reinstall `faiss-cpu` or ensure your Python version matches the wheel availability.
- **PDF extraction returns empty text**: fall back to the PyMuPDF-based method noted in `pdf_utils.py` for scanned/complex layouts.
