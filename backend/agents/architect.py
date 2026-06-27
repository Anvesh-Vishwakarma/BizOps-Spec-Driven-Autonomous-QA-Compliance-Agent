import os
import pdfplumber
import docx
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from backend.orchestrator import QAState

# Initialize the LLM (Requires GEMINI_API_KEY in environment)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.2)

def extract_text(file_path: str) -> str:
    """Extracts text from PDF or DOCX files."""
    text = ""
    if file_path.endswith('.pdf'):
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    elif file_path.endswith('.docx'):
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    return text

def architect_node(state: QAState) -> QAState:
    """
    Architect Node: Extracts and structures the requirements and compliance rules
    from the uploaded document.
    """
    print(f"--- Architect Agent processing: {state['file_path']} ---")
    
    raw_text = extract_text(state["file_path"])
    
    prompt = PromptTemplate.from_template(
        "You are an expert Software Architect and Compliance Officer.\n"
        "Extract the core software requirements and legal compliance standards from the following document text.\n"
        "Format the output into a highly structured JSON or Markdown format detailing:\n"
        "- Functionality requirements\n"
        "- Data handling rules (e.g., PII encryption)\n"
        "- Security standards\n\n"
        "Document Text:\n{raw_text}"
    )
    
    chain = prompt | llm
    result = chain.invoke({"raw_text": raw_text[:30000]}) # Limit to roughly context window if needed
    
    state["extracted_requirements"] = result.content
    return state
