from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

class QAState(TypedDict):
    run_id: str
    file_path: str
    extracted_requirements: Optional[str]
    generated_tests: Optional[str]
    execution_logs: Optional[str]
    compliance_report: Optional[str]

# Import nodes here to avoid circular dependencies during initialization
from backend.agents.architect import architect_node
from backend.agents.coder import coder_node
from backend.sandbox.e2b_manager import execute_in_sandbox
from backend.agents.auditor import auditor_node

# Build the graph
workflow = StateGraph(QAState)

workflow.add_node("architect", architect_node)
workflow.add_node("coder", coder_node)
workflow.add_node("executor", execute_in_sandbox)
workflow.add_node("auditor", auditor_node)

workflow.set_entry_point("architect")
workflow.add_edge("architect", "coder")
workflow.add_edge("coder", "executor")
workflow.add_edge("executor", "auditor")
workflow.add_edge("auditor", END)

qa_app = workflow.compile()

def run_qa_pipeline(file_path: str) -> str:
    """
    Initializes and triggers the LangGraph workflow for QA & Compliance.
    """
    run_id = str(uuid.uuid4())
    
    initial_state = QAState(
        run_id=run_id,
        file_path=file_path,
        extracted_requirements="",
        generated_tests="",
        execution_logs="",
        compliance_report=""
    )
    
    # Run the compiled LangGraph app
    # We can invoke it asynchronously or synchronously
    # For now, invoking synchronously and letting it process
    final_state = qa_app.invoke(initial_state)
    
    print(f"Pipeline completed for run {run_id}")
    return run_id
