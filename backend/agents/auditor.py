from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from backend.orchestrator import QAState
import json
import os

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.1)

def auditor_node(state: QAState) -> QAState:
    """
    Auditor Node: Evaluates the E2B logs against the compliance rules and saves the report.
    """
    print(f"--- Auditor Agent evaluating logs for run: {state['run_id']} ---")
    
    prompt = PromptTemplate.from_template(
        "You are an expert Security Auditor and Compliance Officer.\n"
        "Evaluate the following execution logs against the original requirements.\n"
        "Identify any security vulnerabilities, failing tests, or compliance gaps.\n\n"
        "Original Requirements & Compliance Rules:\n{requirements}\n\n"
        "Execution Logs:\n{logs}\n\n"
        "Generate a final assessment report in Markdown format summarizing your findings."
    )
    
    chain = prompt | llm
    result = chain.invoke({
        "requirements": state["extracted_requirements"],
        "logs": state["execution_logs"]
    })
    
    report = result.content
    state["compliance_report"] = report
    
    # Save to local JSON/Markdown file
    os.makedirs("runs", exist_ok=True)
    report_path = f"runs/report_{state['run_id']}.md"
    with open(report_path, "w") as f:
        f.write(f"# QA & Compliance Report (Run ID: {state['run_id']})\n\n")
        f.write(report)
        f.write("\n\n## Generated Pytest Code\n```python\n")
        f.write(state.get("generated_tests", ""))
        f.write("\n```\n")
        
    print(f"Report saved to {report_path}")
    return state
