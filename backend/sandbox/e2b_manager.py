from e2b_code_interpreter import Sandbox
import os
from backend.orchestrator import QAState

def execute_in_sandbox(state: QAState) -> QAState:
    """
    Execution Engine Node: Connects to E2B, executes the pytest code, and captures logs.
    """
    print(f"--- E2B Sandbox Execution for run: {state['run_id']} ---")
    
    api_key = os.getenv("E2B_API_KEY")
    code = state.get("generated_tests", "")
    
    if not code:
        state["execution_logs"] = "Error: No code generated to execute."
        return state
        
    # We wrap the code in a shell command to run it as a pytest script
    # For a robust setup, we write it to a file and run pytest
    execution_script = f"""
import subprocess
with open('test_specs.py', 'w') as f:
    f.write(r'''{code}''')

result = subprocess.run(['pytest', 'test_specs.py', '-v'], capture_output=True, text=True)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
"""

    try:
        with Sandbox(api_key=api_key) as sandbox:
            # Optionally install dependencies in the sandbox
            # sandbox.process.start("pip install pytest playwright pandas")
            
            execution = sandbox.notebook.exec_cell(execution_script)
            
            logs = ""
            if execution.results:
                for res in execution.results:
                    logs += str(res.text) + "\n"
            if execution.logs.stdout:
                logs += "\n".join(execution.logs.stdout)
            if execution.logs.stderr:
                logs += "\n" + "\n".join(execution.logs.stderr)
                
            state["execution_logs"] = logs if logs else "Executed with no output."
    except Exception as e:
        state["execution_logs"] = f"E2B Execution Failed: {str(e)}"
        
    return state
