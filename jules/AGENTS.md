Working behaviour and prompt context for Jules. how to follow the instructions in the other files and how to use the context for the task at hand. 
Add: to never delete a hf_upload.py file once created. And always reuse that before testing the logs, then testing apis for functionality. Then submit with summary of final results, of the space and the functionalities. 

Agent behaviour: Scan vision of project, scan the repos asociated, scan the task list. Build component by component. Test components. Identify where components interact. Test the internal interaction. Build the functionality FastAPI endpoint for each feature to later be tested via api once deployed. Then test the overall app from start to finish. Then make the deployment files and script for the huggingface deployment based on the /deployment folder and huggingface space parameters. Then expose the FASTAPis in the way it is recommended. Gradio=gradio endpoints. Docker= space url endpoints /health etc. Then deploy. Then check the build logs, then the run logs. Fix failures until successfully running. Then check the exposed FastAPI endpoints for functionality if no Auth tokens for the app are needed. If they are needed. Submit once the app is running and wait for the user to enter the space secrets, and test then. 


## important!
The current codebase you are working in is to be EXPANDED and ADAPTED following the vision of the project transformation in the /jules folder. You are NOT authorized to rewrite or replace the core logic of the existing application. Instead, you must:
1. **Understand & Preserve**: First, investigate the existing codebase to understand its current features and architecture.
2. **Expand & Integrate**: Implement the new features described in the /jules folder by expanding the existing backend logic and integrating new components into the current structure.
3. **Enhance**: Improve and expand existing functionalities rather than replacing them. Use phrases in your plan like "Expand the backend logic by..." or "Enhance the existing UI with...".
4. **Consistency**: Adapt your coding implementation to the coding language and style used by the project.
5. **Document**: You MUST document all adaptations and expansions made to the project in the original README.md file by adding a new section titled '## Adaptations & Expansions' at the end of the file. Describe what was added and how the original project was improved.

Develop tests to run to first see the current application feature, how it is working, and then verify how your expansions integrate with the original code. Test the full, expanded app within this working space. 

See what huggingface sdk from gradio over streamlit to docker fits best and use that, configure the README.md file accordingly and prepare to upload the FULL expanded app to the huggingface space.

## Project Specific Instructions
Here’s a **comprehensive `AGENTS.md` file** tailored to your `reor` → Hugging Face integration, covering **specific instructions for agents**, **context**, and **best-practice workflows**:

---

# **AGENTS.md**
**Project:** Reor + BLABLADOR on Hugging Face
**Role:** Agent Guidelines for Development, Testing, and Deployment

---

## **1. Core Context & Objectives**
### **Key Adaptations**
| Area               | Original Reor | Hugging Face Adaptation                     |
|--------------------|---------------|--------------------------------------------|
| **LLM Backend**    | Ollama/OpenAI | BLABLADOR (`alias-large`) via OpenAI API   |
| **Deployment**     | Local-only    | Hugging Face Spaces (`harvesthealth-magnetic-ui.hf.space`) |
| **API Exposure**   | None          | Port `7860` forwarded via FastAPI proxy    |
| **Auth**           | Local         | `BLABLADOR_API_KEY` (Space secrets)       |

### **Agent-Specific Tasks**
- **LLM Integration Agent**: Modify `llm-service.ts` to proxy BLABLADOR API calls.
- **API Proxy Agent**: Build `proxy.py` (FastAPI/Flask) to forward Hugging Face requests.
- **Docker Agent**: Containerize Reor + proxy; expose port `7860`.
- **Deploy Agent**: Configure Hugging Face Space secrets and port forwarding.

---

## **2. Agent Instructions**
### **2.1 LLM Integration Agent**
#### **Critical Tasks**
1. **Replace Ollama/OpenAI Logic**:
   - Replace `http://localhost:11434/api` with `https://api.helmholtz-blablador.fz-juelich.de/v1`.
   - Update `llm-service.ts` to use `fetch` with `BLABLADOR_API_KEY` (from env vars).
   - Example:
     ```ts
     const response = await fetch("https://api.helmholtz-blablador.fz-juelich.de/v1/chat/completions", {
       headers: { "Authorization": `Bearer ${process.env.BLABLADOR_API_KEY}` },
       method: "POST",
       body: JSON.stringify({ model: "alias-large", messages: [...] })
     });
     ```

2. **Error Handling**:
   - Retry on `429` (rate limits); log `401` errors for missing keys.

3. **Embeddings**:
   - Use BLABLADOR’s `/embeddings` endpoint for vector generation (replace `transformers.js` if needed).

4. **Cache Locally**:
   - Cache embeddings to avoid redundant API calls (e.g., `lru-cache` library).

#### **Test Cases**
- **Test 1**: Verify `alias-large` completions match expected output.
- **Test 2**: Ensure RAG responses use retrieved context (LanceDB + BLABLADOR).
- **Test 3**: Validate no hardcoded API keys in code.

---

### **2.2 API Proxy Agent**
#### **Critical Tasks**
1. **Build Proxy (`proxy.py`)**:
   - Use FastAPI/Flask to forward requests to Reor’s `7860` port.
   - Example (FastAPI):
     ```python
     from fastapi import FastAPI, HTTPException, Depends, Header
     import httpx

     app = FastAPI()

     async def get_auth_token(api_key: str = Header(...)):
         return api_key

     @app.post("/qa")
     async def rag_qa(query: str, token: str = Depends(get_auth_token)):
         if token != os.getenv("BLABLADOR_API_KEY"):
             raise HTTPException(status_code=401, detail="Unauthorized")
         async with httpx.AsyncClient() as client:
             resp = await client.post("http://localhost:7860/qa", json={"query": query})
             return resp.json()
     ```

2. **Security**:
   - Require `Authorization: Bearer <key>` for write endpoints (`/notes`, `/qa`).
   - Validate `BLABLADOR_API_KEY` against Space secrets.

3. **Endpoints**:
   | Reor Endpoint | Proxy Path | Auth Required |
   |---------------|------------|---------------|
   | `/notes`      | `/notes`   | Optional      |
   | `/qa`         | `/qa`      | API Key       |
   | `/search`     | `/search`  | Optional      |

#### **Test Cases**
- **Test 1**: Forward `/notes` to Reor’s internal endpoint.
- **Test 2**: Reject unauthorized `POST /qa` requests.
- **