from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from backend.orchestrator import QAState
import re

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.1)

def coder_node(state: QAState) -> QAState:
    """
    Coder Node: Generates pytest python code based on the Architect's requirements.
    """
    print(f"--- Coder Agent generating tests for run: {state['run_id']} ---")
    
    prompt = PromptTemplate.from_template(
        "You are an expert Python SDET and Test Automation Engineer.\n"
        "Given the following highly structured software requirements and compliance standards,\n"
        "generate a complete, runnable Python script using `pytest`.\n"
        "If it's a UI requirement, use `pytest-playwright`.\n"
        "If it's a data pipeline, use `pandas` or standard Python assertions.\n"
        "Include all necessary imports and mock data if needed.\n\n"
        "Requirements:\n{requirements}\n\n"
        "Output ONLY the python code enclosed in ```python ... ``` tags."
    )
    
    chain = prompt | llm
    result = chain.invoke({"requirements": state["extracted_requirements"]})
    
    # Extract the code block from the response
    code_match = re.search(r"```python\n(.*?)\n```", result.content, re.DOTALL)
    if code_match:
        state["generated_tests"] = code_match.group(1)
    else:
        state["generated_tests"] = result.content # Fallback
        
    return state
