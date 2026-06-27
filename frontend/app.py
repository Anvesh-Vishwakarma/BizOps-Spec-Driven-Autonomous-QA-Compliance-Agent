import chainlit as cl
import httpx
import os
import aiofiles

BACKEND_URL = "http://localhost:8000"

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="Welcome to the BizOps QA & Compliance Agent! Please upload a PDF or DOCX specification file to begin.").send()
    
    files = None
    while files is None:
        files = await cl.AskFileMessage(
            content="Upload your requirement document (PDF or DOCX)",
            accept=["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"],
            max_size_mb=20,
            timeout=300
        ).send()
        
    uploaded_file = files[0]
    
    msg = cl.Message(content=f"Uploading `{uploaded_file.name}` to the orchestrator...")
    await msg.send()
    
    # Send the file to the FastAPI backend
    try:
        async with httpx.AsyncClient() as client:
            with open(uploaded_file.path, "rb") as f:
                files = {"file": (uploaded_file.name, f, "application/octet-stream")}
                response = await client.post(f"{BACKEND_URL}/api/upload", files=files)
                response.raise_for_status()
                data = response.json()
                file_path = data["path"]
                
        msg.content = f"`{uploaded_file.name}` uploaded successfully! Starting the multi-agent workflow..."
        await msg.update()
        
        # Trigger the run
        async with httpx.AsyncClient() as client:
            run_resp = await client.post(f"{BACKEND_URL}/api/run?file_path={file_path}")
            run_resp.raise_for_status()
            run_data = run_resp.json()
            run_id = run_data["run_id"]
            
        await cl.Message(content=f"Workflow started! Run ID: `{run_id}`\n\nThe agents are now processing the specification...").send()
        
        # Here we will add the polling or websocket connection to stream the agent thought process
        
    except Exception as e:
        await cl.Message(content=f"An error occurred: {str(e)}").send()

@cl.on_message
async def on_message(message: cl.Message):
    # For now, just echo. Later we can add conversational abilities to query the state.
    await cl.Message(content=f"Received: {message.content}. Please wait for the QA pipeline to complete.").send()
