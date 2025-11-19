# import streamlit as st
# from app.ui import pdf_uploader
# from app.pdf_utils import extract_pdf_text
# from app.chat_utils import get_chat_model, ask_chat_model
# from app.vectorstore_utils import create_faiss_index, retrive_relevant_docs_faiss as retrive_relevant_docs
# import dotenv
# import os
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# import time
# # from app.config import euri_api_key as api_key
# dotenv.load_dotenv()
# api_key = os.getenv("euri_api_key")
# # api_key=euri_api_key

# st.set_page_config(page_title="File-QA — Upload & Ask", page_icon="📄🤖", layout="wide",initial_sidebar_state="expanded")

# st.markdown("""
# <style>
#     .chat-message {
#         padding: 1rem;
#         border-radius: 0.5rem;
#         margin-bottom: 1rem;
#         display: flex;
#         flex-direction: column;
#     }
#     .chat-message.user {
#         background-color: #2b313e;
#         color: white;
#     }
#     .chat-message.assistant {
#         background-color: #f0f2f6;
#         color: black;
#     }
#     .chat-message .avatar {
#         width: 2rem;
#         height: 2rem;
#         border-radius: 50%;
#         margin-right: 0.5rem;
#     }
#     .chat-message .message {
#         flex: 1;
#     }
#     .chat-message .timestamp {
#         font-size: 0.8rem;
#         opacity: 0.7;
#         margin-top: 0.5rem;
#     }
#     .stButton > button {
#         background-color: #ff4b4b;
#         color: white;
#         border-radius: 0.5rem;
#         border: none;
#         padding: 0.5rem 1rem;
#         font-weight: bold;
#     }
#     .stButton > button:hover {
#         background-color: #ff3333;
#     }
#     .upload-section {
#         background-color: #f8f9fa;
#         padding: 1rem;
#         border-radius: 0.5rem;
#         margin-bottom: 1rem;
#     }
#     .status-success {
#         background-color: #d4edda;
#         color: #155724;
#         padding: 0.5rem;
#         border-radius: 0.25rem;
#         margin: 0.5rem 0;
#     }
# </style>
# """, unsafe_allow_html=True)

# if "messages" not in st.session_state:
#     st.session_state.messages = []
# if "vectorstore" not in st.session_state:
#     st.session_state.vectorstore = None
# if "chat_model" not in st.session_state:
#     st.session_state.chat_model = None


# st.markdown("""
# <div style="text-align: center; padding: 2rem 0;">
#     <h1 style="color: #ff4b4b; font-size: 3rem; margin-bottom: 0.5rem;">🏥 AnyDocChat Pro</h1>
#     <p style="font-size: 1.2rem; color: #666; margin-bottom: 2rem;">Your Intelligent  Document Assistant</p>
# </div>
# """, unsafe_allow_html=True)

# # Sidebar for document upload
# with st.sidebar:
#     st.markdown("### 📁 Document Upload")
#     st.markdown("Upload your  documents to start chatting!")
    
#     uploaded_files = pdf_uploader()
    
    
#     if uploaded_files:
#         st.success(f"📄 {len(uploaded_files)} document(s) uploaded")
        
#         # Process documents
#         if st.button("🚀 Process Documents", type="primary"):
#             with st.spinner("Processing your  documents..."):
#                 # Extract text from all PDFs
#                 all_texts = []
#                 for file in uploaded_files:
#                     text = extract_pdf_text(file)
#                     # text = extract_pdf(file)
#                     all_texts.append(text)
                
#                 # Split texts into chunks
#                 text_splitter = RecursiveCharacterTextSplitter(
#                     chunk_size=1000,
#                     chunk_overlap=200,
#                     length_function=len,
#                 )
                
#                 chunks = []
#                 for text in all_texts:
#                     chunks.extend(text_splitter.split_text(text))
                
#                 # Create FAISS index
#                 vectorstore = create_faiss_index(chunks)
#                 st.session_state.vectorstore = vectorstore
                
#                 # Initialize chat model
#                 chat_model = get_chat_model(api_key)
#                 st.session_state.chat_model = chat_model
                
#                 st.success("✅ Documents processed successfully!")
#                 st.balloons()

# # Main chat interface
# st.markdown("### 💬 Chat with Your  Documents")


# # Display chat messages
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])
#         st.caption(message["timestamp"])

# # Chat input
# if prompt := st.chat_input("Ask about your  documents..."):
#     # Add user message to chat history
#     timestamp = time.strftime("%H:%M")
#     st.session_state.messages.append({
#         "role": "user", 
#         "content": prompt, 
#         "timestamp": timestamp
#     })
    
#     # Display user message
#     with st.chat_message("user"):
#         st.markdown(prompt)
#         st.caption(timestamp)
    
#     # Generate response
#     if st.session_state.vectorstore and st.session_state.chat_model:
#         with st.chat_message("assistant"):
#             with st.spinner("🔍 Searching documents..."):
#                 # Retrieve relevant documents
#                 relevant_docs = retrive_relevant_docs(st.session_state.vectorstore, prompt)
                
#                 # Create context from relevant documents
#                 context = "\n\n".join([doc.page_content for doc in relevant_docs])
                
#                 # Create prompt with context
#                 system_prompt = f"""You are MediChat Pro, an intelligent  document assistant. 
#                 Based on the following  documents, provide accurate and helpful answers. 
#                 If the information is not in the documents, clearly state that.
#                 when you are giving an answer make sure that try to take help of llm and give me a full diagnosis of the problem.
                

#                  Documents:
#                 {context}

#                 User Question: {prompt}

#                 Answer:"""
                
#                 response = ask_chat_model(st.session_state.chat_model, system_prompt)
            
#             st.markdown(response)
#             st.caption(timestamp)
            
#             # Add assistant message to chat history
#             st.session_state.messages.append({
#                 "role": "assistant", 
#                 "content": response, 
#                 "timestamp": timestamp
#             })
#     else:
#         with st.chat_message("assistant"):
#             st.error("⚠️ Please upload and process documents first!")
#             st.caption(timestamp)

# # Footer
# st.markdown("---")
# st.markdown("""
# <div style="text-align: center; color: #666; font-size: 0.9rem;">
#     <p>🤖 Powered by AI & LangChain | 🏥  Document Intelligence</p>
# </div>
# """, unsafe_allow_html=True)
import streamlit as st
from app.ui import pdf_uploader
from app.pdf_utils import extract_pdf_text
from app.chat_utils import get_chat_model, ask_chat_model
from app.vectorstore_utils import create_faiss_index, retrive_relevant_docs_faiss as retrive_relevant_docs
import dotenv
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
import time

# dotenv.load_dotenv()
# api_key = os.getenv("euri_api_key")

st.set_page_config(
    page_title="AnyDocChat Pro",
    page_icon="📄🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Stunning Modern CSS ----------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* {
  font-family: 'Inter', sans-serif;
}

/* Animated gradient background */
html, body, [data-testid="stAppViewContainer"] > .main {
  background: linear-gradient(-45deg, #0a0e27, #1a1f3a, #2d1b4e, #1e293b);
  background-size: 400% 400%;
  animation: gradientShift 15s ease infinite;
  color: #e2e8f0;
}

@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

/* Premium header with glow */
.header {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(59, 130, 246, 0.15) 100%);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(139, 92, 246, 0.3);
  border-radius: 24px;
  padding: 32px;
  box-shadow: 0 20px 60px rgba(139, 92, 246, 0.2), 0 0 40px rgba(59, 130, 246, 0.1);
  color: white;
  position: relative;
  overflow: hidden;
  animation: headerFloat 3s ease-in-out infinite;
}

@keyframes headerFloat {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-5px); }
}

.header::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(139, 92, 246, 0.1) 0%, transparent 70%);
  animation: rotateGlow 10s linear infinite;
}

@keyframes rotateGlow {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.header > div {
  position: relative;
  z-index: 1;
}

.header h1 {
  margin: 0;
  font-size: 2.8rem;
  font-weight: 800;
  background: linear-gradient(135deg, #a78bfa 0%, #60a5fa 50%, #34d399 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.02em;
}

.app-subtitle {
  color: #cbd5e1;
  opacity: 0.9;
  margin-top: 8px;
  font-size: 1.1rem;
  font-weight: 400;
}

/* Premium glass card */
.glass {
  background: rgba(30, 41, 59, 0.4);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.05);
  transition: all 0.3s ease;
}

.glass:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 48px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.08);
  border-color: rgba(139, 92, 246, 0.3);
}

/* Elegant chat bubbles */
.chat-bubble {
  padding: 18px 22px;
  border-radius: 18px;
  margin-bottom: 16px;
  max-width: 85%;
  display: inline-block;
  font-size: 1rem;
  line-height: 1.6;
  animation: fadeInUp 0.4s ease;
  position: relative;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.chat-user {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(99, 102, 241, 0.2) 100%);
  color: #f1f5f9;
  border: 1px solid rgba(139, 92, 246, 0.3);
  border-bottom-right-radius: 6px;
  box-shadow: 0 4px 16px rgba(139, 92, 246, 0.1);
}

.chat-assistant {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(6, 182, 212, 0.15) 100%);
  color: #f0fdfa;
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-bottom-left-radius: 6px;
  box-shadow: 0 4px 16px rgba(16, 185, 129, 0.1);
}

/* Timestamp styling */
.timestamp {
  font-size: 0.75rem;
  opacity: 0.5;
  margin-top: 8px;
  font-weight: 500;
  letter-spacing: 0.5px;
}

/* Premium buttons */
.stButton>button {
  background: linear-gradient(135deg, #8b5cf6 0%, #3b82f6 100%);
  color: white;
  border: none;
  padding: 14px 28px;
  border-radius: 14px;
  font-weight: 600;
  font-size: 0.95rem;
  box-shadow: 0 8px 24px rgba(139, 92, 246, 0.3);
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.stButton>button:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(139, 92, 246, 0.4);
  filter: brightness(1.1);
}

.stButton>button:active {
  transform: translateY(0px);
}

/* Sidebar styling */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%);
  backdrop-filter: blur(20px);
  border-right: 1px solid rgba(139, 92, 246, 0.2);
}

[data-testid="stSidebar"] h3 {
  color: #a78bfa;
  font-weight: 700;
  font-size: 1.3rem;
  margin-bottom: 16px;
  letter-spacing: -0.01em;
}

[data-testid="stSidebar"] .small-muted {
  color: #94a3b8;
  opacity: 0.8;
  font-size: 0.88rem;
  line-height: 1.5;
}

/* Radio button styling */
.stRadio > div {
  background: rgba(30, 41, 59, 0.4);
  border-radius: 12px;
  padding: 8px;
}

.stRadio [role="radiogroup"] {
  gap: 12px;
}

.stRadio label {
  background: rgba(139, 92, 246, 0.1);
  border: 1px solid rgba(139, 92, 246, 0.3);
  border-radius: 10px;
  padding: 10px 20px;
  color: #cbd5e1;
  font-weight: 600;
  transition: all 0.3s ease;
}

.stRadio label:hover {
  background: rgba(139, 92, 246, 0.2);
  border-color: rgba(139, 92, 246, 0.5);
  transform: translateY(-2px);
}

.stRadio [data-checked="true"] label {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.3) 0%, rgba(59, 130, 246, 0.3) 100%);
  border-color: rgba(139, 92, 246, 0.6);
  color: #e0e7ff;
}

/* Multiselect and input styling */
.stMultiSelect [data-baseweb="select"] {
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(139, 92, 246, 0.3);
  border-radius: 12px;
}

.stTextInput input, .stChatInput input {
  background: rgba(30, 41, 59, 0.6) !important;
  border: 1px solid rgba(139, 92, 246, 0.3) !important;
  border-radius: 12px !important;
  color: #e2e8f0 !important;
  padding: 12px 16px !important;
  font-size: 0.95rem !important;
}

.stTextInput input:focus, .stChatInput input:focus {
  border-color: rgba(139, 92, 246, 0.6) !important;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1) !important;
}

/* Success and info messages */
.stSuccess {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(5, 150, 105, 0.15) 100%);
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: 12px;
  color: #6ee7b7;
}

.stInfo {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(37, 99, 235, 0.15) 100%);
  border: 1px solid rgba(59, 130, 246, 0.3);
  border-radius: 12px;
  color: #93c5fd;
}

/* Spinner */
.stSpinner > div {
  border-top-color: #8b5cf6 !important;
}

/* Scrollbar */
::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}

::-webkit-scrollbar-track {
  background: rgba(30, 41, 59, 0.3);
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #8b5cf6 0%, #3b82f6 100%);
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #7c3aed 0%, #2563eb 100%);
}

/* Upload section enhancement */
.uploadedFile {
  background: rgba(139, 92, 246, 0.1);
  border: 1px solid rgba(139, 92, 246, 0.3);
  border-radius: 10px;
}

/* Model badge styling */
.model-badge {
  display: inline-block;
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(59, 130, 246, 0.2) 100%);
  border: 1px solid rgba(139, 92, 246, 0.4);
  padding: 6px 14px;
  border-radius: 20px;
  margin: 4px;
  font-size: 0.85rem;
  font-weight: 600;
  color: #c4b5fd;
}

/* Section divider */
hr {
  border: none;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.3), transparent);
  margin: 20px 0;
}

/* Footer enhancement */
.footer-text {
  text-align: center;
  color: #94a3b8;
  font-size: 0.9rem;
  padding: 16px 0;
  opacity: 0.8;
}

/* Pulsing indicator for active status */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.status-indicator {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #10b981;
  animation: pulse 2s ease-in-out infinite;
  margin-right: 8px;
}

/* Card hover glow effect */
.glass::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 20px;
  padding: 1px;
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.5), rgba(59, 130, 246, 0.5));
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.glass:hover::after {
  opacity: 1;
}
</style>
""",
    unsafe_allow_html=True,
)

# ---------- Header ----------
import base64

def load_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo = load_base64("icon.png")
st.markdown(
    f"""
<div class="header">
  <div style="display:flex; align-items:center; justify-content:space-between;">
    <div>
      <div style="display:flex; align-items:center; gap:12px; margin-bottom:10px;">
    <img src="data:image/png;base64,{logo}" 
         style="height:60px; border-radius:6px;">
    <h1 style="margin:0; font-size:1.9rem; color:#f8fafc; font-weight:700;">
        AnyDocChat Pro
    </h1>
</div>
      <div class="app-subtitle">Your Intelligent Document Assistant — beautiful, fast, trustworthy</div>
    </div>
    <div style="text-align:right;">
      <div style="font-size:0.95rem; margin-bottom:4px; color: #cbd5e1; font-weight: 500;">Model Selector</div>
      <div style="font-weight:700; font-size:1.05rem; color: #a78bfa;">Choose & compare AI models</div>
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)
# st.markdown(
#     f"""
# <div style="display:flex; align-items:center; gap:12px; margin-bottom:10px;">
#     <img src="data:image/png;base64,{logo}" 
#          style="height:60px; border-radius:6px;">
#     <h1 style="margin:0; font-size:1.9rem; color:#f8fafc; font-weight:700;">
#         AnyDocChat Pro
#     </h1>
# </div>
# """,
#     unsafe_allow_html=True
# )

# ---------- Session state ----------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "chat_model" not in st.session_state:
    st.session_state.chat_model = None
if "selected_models" not in st.session_state:
    st.session_state.selected_models = ["gpt-5-nano-2025-08-07"]
if "platform" not in st.session_state:
    st.session_state.platform = "euriai"

# ---------- Sidebar: Upload + Model Selection ----------
with st.sidebar:
    st.markdown("### 📁 Upload & Settings", unsafe_allow_html=True)
    # st.markdown('<div class="glass" style="position: relative;">', unsafe_allow_html=True)
    st.markdown(
    """
    <style>
        .white-line {
            width: 100%;
            height: 2px;
            background-color: #cbd5e1;
            margin: 20px 0;
        }
    </style>
    <div class="white-line"></div>
    """,
    unsafe_allow_html=True
    )

    st.markdown("**Upload documents (PDF)**")
    uploaded_files = pdf_uploader()
    if uploaded_files:
        st.success(f"📄 {len(uploaded_files)} file(s) uploaded")

    st.markdown("---")
    st.markdown("### 🌐 Choose Platform")
    st.markdown('<div class="small-muted">Select the AI platform provider</div>', unsafe_allow_html=True)
    
    platform = st.radio(
        "Platform",
        options=["euriai", "groq"],
        index=0 if st.session_state.platform == "euriai" else 1,
        horizontal=True
    )
    
    # Update platform and reset models if platform changed
    if platform != st.session_state.platform:
        st.session_state.platform = platform
        st.session_state.selected_models = []
    
    st.markdown("---")
    st.markdown("### 🤖 Choose AI Model(s)")
    st.markdown('<div class="small-muted">Pick one or more models to query. Multiple selection = ensemble compare.</div>', unsafe_allow_html=True)
    
    # Define models based on platform
    if st.session_state.platform == "euriai":
        model_options = [
            "gpt-5-nano-2025-08-07",
            "gemini-2.0-flash",
            "llama-4-scout-17b-16e-instruct",
            "deepseek-r1-distill-llama-70b"
        ]
        default_model = "gpt-5-nano-2025-08-07"
    else:  # groq
        model_options = [
            "groq/compound-mini",
            "groq/llama-3.3-70b-versatile",
            "groq/mixtral-8x7b-32768",
            "groq/gemma2-9b-it",
            "openai/gpt-oss-20b"
        ]
        default_model = "groq/compound-mini"
    
    # Set default if no models selected
    if not st.session_state.selected_models:
        st.session_state.selected_models = [default_model]
    
    selected_models = st.multiselect(
        "Models", 
        options=model_options, 
        default=st.session_state.selected_models if st.session_state.selected_models else [default_model]
    )
    st.session_state.selected_models = selected_models if selected_models else [default_model]
    st.markdown("---")
    st.markdown("### ⚙️ Index / Process")
    if uploaded_files:
        if st.button("🚀 Process Documents"):
            with st.spinner("Processing documents and building index..."):
                all_texts = []
                for file in uploaded_files:
                    text = extract_pdf_text(file)
                    all_texts.append(text)

                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200,
                    length_function=len,
                )
                chunks = []
                for text in all_texts:
                    chunks.extend(text_splitter.split_text(text))

                vectorstore = create_faiss_index(chunks)
                st.session_state.vectorstore = vectorstore

                st.session_state.chat_model = None
                st.success("✅ Documents processed. Ready to chat!")
                st.balloons()
    else:
        st.info("Upload PDF files to enable processing.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ℹ️ Tips")
    st.write("- Try asking: *'Summarize the findings', 'List key diagnosis', 'What steps are recommended?'*")
    st.caption("Model ensemble will query each selected provider and show labeled responses.")

# ---------- Layout: Chat area + Right panel ----------
left_col, right_col = st.columns([3, 1])

with left_col:
    st.markdown("### 💬 Chat with your documents", unsafe_allow_html=True)
    # st.markdown('<div class="glass" style="position: relative;">', unsafe_allow_html=True)
    st.markdown(
    """
    <style>
        .white-line {
            width: 100%;
            height: 2px;
            background-color: #cbd5e1;
            margin: 1px 0;
        }
    </style>
    <div class="white-line"></div>
    """,
    unsafe_allow_html=True
    )

    # Display chat history
    for message in st.session_state.messages:
        role = message.get("role", "assistant")
        content = message.get("content", "")
        timestamp = message.get("timestamp", "")
        css_class = "chat-user" if role == "user" else "chat-assistant"
        label = "You" if role == "user" else "Assistant"
        icon = "👤" if role == "user" else "🤖"
        st.markdown(f"""
            <div style="margin-bottom:12px;">
                <div style="display:flex; gap:12px; align-items:flex-start;">
                    <div style="font-size:1.5rem;">{icon}</div>
                    <div style="flex:1;">
                        <div style="font-weight:600; margin-bottom:6px; color: #cbd5e1;">{label}</div>
                        <div class="chat-bubble {css_class}">{content}</div>
                        <div class="timestamp">{timestamp}</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Chat input
    prompt = st.chat_input("Ask about your documents (press enter to send)...")
    if prompt:
        timestamp = time.strftime("%H:%M")
        st.session_state.messages.append({"role": "user", "content": prompt, "timestamp": timestamp})
        st.rerun()

with right_col:
    st.markdown("### ⚡ Quick Actions", unsafe_allow_html=True)
    # st.markdown('<div class="glass" style="position: relative;">', unsafe_allow_html=True)
    st.markdown(
    """
    <style>
        .white-line {
            width: 100%;
            height: 2px;
            background-color: #cbd5e1;
            margin: 1px 0;
        }
    </style>
    <div class="white-line"></div>
    """,
    unsafe_allow_html=True
    )
    st.write("**Selected models:**")
    for model in st.session_state.selected_models:
        st.markdown(f'<span class="model-badge">{model}</span>', unsafe_allow_html=True)

    st.markdown("---")
    st.write("**Document status**")
    if st.session_state.vectorstore:
        st.markdown('<div><span class="status-indicator"></span><span style="color: #10b981; font-weight: 600;">FAISS index ready</span></div>', unsafe_allow_html=True)
    else:
        st.info("No index yet — process documents first.")

    st.markdown("---")
    st.write("**Controls**")
    if st.session_state.messages and st.session_state.vectorstore:
        if st.button("🔁 Regenerate Last Answer"):
            for i in range(len(st.session_state.messages)-1, -1, -1):
                if st.session_state.messages[i]["role"] == "user":
                    last_user = st.session_state.messages[i]
                    break
            else:
                last_user = None

            if last_user:
                prompt_text = last_user["content"]
                st.session_state.messages = st.session_state.messages[: i+1 ]
                st.session_state._regenerate = prompt_text
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- Generation logic ----------
trigger_prompt = None
if "_regenerate" in st.session_state:
    trigger_prompt = st.session_state.pop("_regenerate")

if not trigger_prompt:
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        generate = True
        if st.session_state.messages:
            if len(st.session_state.messages) >= 2 and st.session_state.messages[-1]["role"] == "user":
                trigger_prompt = st.session_state.messages[-1]["content"]

if trigger_prompt:
    prompt_text = trigger_prompt
    timestamp = time.strftime("%H:%M")
    st.session_state.messages.append({"role": "assistant", "content": "⏳ Generating response...", "timestamp": timestamp})
    st.rerun()

if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant" and st.session_state.messages[-1]["content"] == "⏳ Generating response...":
    if len(st.session_state.messages) >= 2 and st.session_state.messages[-2]["role"] == "user":
        user_prompt = st.session_state.messages[-2]["content"]
        timestamp = time.strftime("%H:%M")
        if st.session_state.vectorstore:
            with st.spinner("🔍 Retrieving relevant documents and querying models..."):
                relevant_docs = retrive_relevant_docs(st.session_state.vectorstore, user_prompt)
                context = "\n\n".join([doc.page_content for doc in relevant_docs])
                system_prompt = f"""You are AnyDocChat Pro, an intelligent document assistant.
Based on the following documents, provide accurate and helpful answers. If the information is not in the documents, clearly state that.
When you answer, try to use the LLM(s) to give a full diagnosis or summary where appropriate.

Documents:
{context}

User Question: {user_prompt}

Answer:"""

                model_responses = []
                print("check",st.session_state.platform)
                # import pdb; pdb.set_trace()
                for provider in st.session_state.selected_models:
                    try:
                        model_obj = get_chat_model(platform=st.session_state.platform, provider=provider)
                    except TypeError:
                        model_obj = get_chat_model(platform=st.session_state.platform, provider=provider)

                    try:
                        resp = ask_chat_model(model_obj,st.session_state.platform, system_prompt)
                    except Exception as e:
                        resp = f"Error from {provider}: {e}"
                    model_responses.append((provider, resp))

                if len(model_responses) == 1:
                    final_response = model_responses[0][1]
                else:
                    parts = []
                    for prov, ans in model_responses:
                        parts.append(f"### Response from **{prov.upper()}**\n{ans}\n")
                    final_response = "\n---\n".join(parts)

                st.session_state.messages[-1] = {"role": "assistant", "content": final_response, "timestamp": timestamp}
                st.rerun()
        else:
            st.session_state.messages[-1] = {"role": "assistant", "content": "⚠️ Please upload and process documents first!", "timestamp": timestamp}
            st.rerun()

# ---------- Footer ----------
st.markdown("---")
st.markdown(
    """
<div class="footer-text">
    🤖 Powered by AI & LangChain | 🏥 Document Intelligence — AnyDocChat Pro
</div>
""",
    unsafe_allow_html=True,
)
