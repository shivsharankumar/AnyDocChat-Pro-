from euriai.langchain import create_chat_model
from langchain_groq import ChatGroq as Groq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
import dotenv
import os
dotenv.load_dotenv()

def get_chat_model(platform:str,provider:str):
    
    if platform =="groq":
        api_key = os.getenv("groq_api_key")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY not found in environment. Set it in .env or export it.")
        return Groq(api_key=api_key, model_name=provider, temperature=0.7)
    elif platform =="euriai":
        api_key = os.getenv("euri_api_key")
        if not api_key:
            raise RuntimeError("EURI_API_KEY not found in environment. Set it in .env or export it.")
        return create_chat_model(api_key=api_key, model_name=provider, temperature=0.7)

def ask_chat_model(chat_model,platform, prompt:str):
    if platform =="groq":
        # pt=PromptTemplate.from_template(prompt)
        response=chat_model.invoke(prompt) 
        return response.content
    else:   
        response = chat_model.invoke(prompt)
        return response.content
