Working behaviour and prompt context for Jules. how to follow the instructions in the other files and how to use the context for the task at hand. 
Add: to never delete a hf_upload.py file once created. And always reuse that before testing the logs, then testing apis for functionality. Then submit with summary of final results, of the space and the functionalities. 

Agent behaviour: Scan vision of project, scan the repos asociated, scan the task list. Build component by component. Test components. Identify where components interact. Test the internal interaction. Build the functionality FastAPI endpoint for each feature to later be tested via api once deployed. Then test the overall app from start to finish. Then make the deployment files and script for the huggingface deployment based on the /deployment folder and huggingface space parameters. Then expose the FASTAPis in the way it is recommended. Gradio=gradio endpoints. Docker= space url endpoints /health etc. Then deploy. Then check the build logs, then the run logs. Fix failures until successfully running. Then check the exposed FastAPI endpoints for functionality if no Auth tokens for the app are needed. If they are needed. Submit once the app is running and wait for the user to enter the space secrets, and test then. 


## important!
The current codebase you are working in is to be adapted following the vision of the project transformation in the /jules folder. The current application should be kept and only slightly changed, improved, expanded by the features described in /jules folder. The tasks files give a starting point, but judge for yourself. Develop tests to run to first see the current application feature, how it is working and make a plan to implement the features requested in /jules folder to develop the current application inside the repo towards the vision described to achieve expansion of the current app with functionalities described in the /jules folder. Adapt your coding implemententation to the coding language used by the project, and try to go with that. Test the full app within this working space. 

See what huggingface sdk from gradio over streamlit to docker fits best and use that, configure the README.md file accordingly and prepare to upload the file app, not just the new features, but the full app expanded with these new features, to the huggingface space. Monitor deployment and once it is running, test the api endpoints you had set to see the functionality of the app inside that huggingface space.

## Project Specific Instructions
Here’s a detailed **AGENTS.md** expansion based on your project context, structured for clarity and actionability. This file would guide developers, testers, and deployment agents in understanding their roles, responsibilities, and technical expectations for the **Reor Hugging Face Deployment**.

---

# **AGENTS.md**
## **Role Definitions & Responsibilities**
This document outlines the roles, responsibilities, and instructions for agents involved in deploying and maintaining **Reor on Hugging Face Spaces** with **BLABLADOR LLM integration**. Each agent type (Developer, Tester, Deployer, Security Auditor) has specific tasks aligned with the project’s technical and operational goals.

---

## **1. Developer Roles & Instructions**
### **1.1 Backend Developer (FastAPI)**
**Responsibilities**:
- Implement the **OpenAI-compatible API wrapper** for BLABLADOR (`alias-large`).
- Develop `/api/query`, `/api/embeddings`, and `/api/search` endpoints with:
  - Input validation (e.g., `text` field required).
  - Error handling (e.g., BLABLADOR rate limits, API key failures).
  - Logging (e.g., `user_id:query_text` for monitoring).
- Integrate **LanceDB** for vector storage and **Transformers.js** as a fallback for embeddings.
- Add **rate limiting** (100 reqs/hour) and **health checks** (`/api/health`).

**Specific Instructions**:
1. **BLABLADOR API Integration**:
   - Use the `BLABLADOR_API_KEY` from Hugging Face Space environment variables.
   - Validate the key on startup (fail if missing).
   - Example call:
     ```python
     import requests
     response = requests.post(
         "https://api.helmholtz-blablador.fz-juelich.de/v1/chat/completions",
         json={"model": "alias-large", "messages": [{"role": "user", "content": "Summarize my notes."}]},
         headers={"Authorization": f"Bearer {os.getenv('BLABLADOR_API_KEY')}"}
     )
     ```
2. **FastAPI Endpoint Specifications**:
   - `/api/embeddings`:
     - Input: `{"text": "Sample note"}`
     - Output: `{"embeddings": [0.1, -0.2, ...]}` (shape `(1, 768)` for `alias-large`).
     - Use `transformers.js` if BLABLADOR fails.
   - `/api/query`:
     - Input: `{"text": "Query here"}`
     - Output: `{"answer": "...", "related_notes": [...]}` (LanceDB-backed).
   - `/api/search`:
     - Input: `{"query": "AI", "k": 3}`
     - Output: `[{"note_id": "x", "score": 0.9}]`.
3. **LanceDB Integration**:
   - Chunk notes → embed with BLABLADOR → store in LanceDB.
   - Example:
     ```python
     import lancedb
     db = lancedb.connect("./data")
     table = db.open_table("notes")
     ```
4. **Dockerfile**:
   - Multi-stage build with dependencies:
     ```dockerfile
     FROM python:3.9-slim
     WORKDIR /app
     COPY requirements.txt .
     RUN pip install fastapi lancedb transformers requests
     COPY . .
     CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
     ```

---

### **1.2 Frontend Developer (Gradio)**
**Responsibilities**:
- Adapt the **Obsidian-like markdown editor** for Hugging Face Spaces.
- Implement the **AI Assistant sidebar** with:
  - Auto-summarization of notes.
  - Real-time suggestions of related notes (via `/api/search`).
- Integrate with FastAPI via `requests.get()` calls.

**Specific Instructions**:
1. **Gradio UI Adjustments**:
   - Add a toggle for the AI sidebar:
     ```python
     def display_ai_sidebar():
         if gradio.inputs.Checkbox(label="Enable AI Assistant"):
             # Fetch related notes via FastAPI
             response = requests.get("http://localhost:8000/api/search", json={"query": "AI"})
             return response.json()
     ```
   - Use `gr.Interface` for the editor:
     ```python
     interface = gr.Interface(
         fn=process_note,
         inputs="text",
         outputs="text",
         title="Reor - AI Knowledge Manager"
     )
     ```
2. **Real-Time Features**:
   - WebSocket