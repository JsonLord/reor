Working behaviour and prompt context for Jules. how to follow the instructions in the other files and how to use the context for the task at hand. 
Add: to never delete a hf_upload.py file once created. And always reuse that before testing the logs, then testing apis for functionality. Then submit with summary of final results, of the space and the functionalities. 

Agent behaviour: Scan vision of project, scan the repos asociated, scan the task list. Build component by component. Test components. Identify where components interact. Test the internal interaction. Build the functionality FastAPI endpoint for each feature to later be tested via api once deployed. Then test the overall app from start to finish. Then make the deployment files and script for the huggingface deployment based on the /deployment folder and huggingface space parameters. Then expose the FASTAPis in the way it is recommended. Gradio=gradio endpoints. Docker= space url endpoints /health etc. Then deploy. Then check the build logs, then the run logs. Fix failures until successfully running. Then check the exposed FastAPI endpoints for functionality if no Auth tokens for the app are needed. If they are needed. Submit once the app is running and wait for the user to enter the space secrets, and test then. 


## important!
The current codebase you are working in is to be adapted following the vision of the project transformation in the /jules folder. The current application should be kept and only slightly changed, improved, expanded by the features described in /jules folder. The tasks files give a starting point, but judge for yourself. Develop tests to run to first see the current application feature, how it is working and make a plan to implement the features requested in /jules folder to develop the current application inside the repo towards the vision described to achieve expansion of the current app with functionalities described in the /jules folder. Adapt your coding implemententation to the coding language used by the project, and try to go with that. Test the full app within this working space. 

See what huggingface sdk from gradio over streamlit to docker fits best and use that, configure the README.md file accordingly and prepare to upload the file app, not just the new features, but the full app expanded with these new features, to the huggingface space. Monitor deployment and once it is running, test the api endpoints you had set to see the functionality of the app inside that huggingface space.

## Project Specific Instructions
Here’s a structured **`AGENTS.md`** file tailored to your Reor + Hugging Face Spaces adaptation, with specific instructions for agents (e.g., developers, testers, or bots) to interact with the project:

---

# **AGENTS.md: Reor for Hugging Face Spaces**
*Guidelines for Agents Interacting with the System*

This document outlines **roles, responsibilities, and operational protocols** for agents (human or automated) interacting with **Reor’s Hugging Face Spaces deployment**. Key focus areas include:
1. **API Usage** (LLM, notes, embeddings).
2. **Data Handling** (privacy, storage, semantic search).
3. **Deployment Constraints** (Hugging Face Spaces limits, cold starts).
4. **Error Handling** (fallbacks, rate limits).

---

## **1. Agent Roles & Responsibilities**
| **Role**               | **Purpose**                                                                                                                                                                                                                                                                                     | **Key Actions**                                                                                                                                                                                                 |
|-------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **API Client Agent**   | Interacts with `/api/v1/*` endpoints (notes, Q&A, embeddings).                                                                                                                                                                                                                     | - Authenticate via `BLABLADOR_API_KEY` (secrets-only).<br>- Respect rate limits (5 LLM calls/minute).<br>- Handle 429/503 errors (fallback to Ollama).                                                           |
| **Data Ingestion Agent** | Populates LanceDB with note embeddings and metadata.                                                                                                                                                                                                                           | - Validate markdown/frontmatter syntax.<br>- Chunk text for embedding (max 512 tokens).<br>- Sync with local filesystem (directory-based storage).                                                                   |
| **RAG Agent**          | Powers semantic Q&A by combining embeddings + LLM context.                                                                                                                                                                                                                           | - Retrieve top-3 similar notes via `/api/v1/similar`.<br>- Enrich prompts with context (RAG).<br>- Cache responses to reduce BLABLADOR API calls.                                                        |
| **Deployment Agent**   | Manages Hugging Face Spaces + Docker/NGINX setup.                                                                                                                                                                                                                           | - Monitor cold starts (pre-load lightweight embeddings).<br>- Update `Dockerfile` for dependencies.<br>- Test `/api/v1/*` forwarding via NGINX.                                                          |
| **Security Agent**     | Enforces privacy (local-first) and compliance.                                                                                                                                                                                                                               | - Block external API calls via CORS.<br>- Audit `BLABLADOR_API_KEY` exposure.<br>- Log failed LLM requests (abuse detection).                                                                                 |

---

## **2. API Interaction Protocols**
### **A. Authentication & Rate Limiting**
- **API Key**:
  - Fetch `BLABLADOR_API_KEY` from Hugging Face Space **secrets** (never hardcode).
  - Example (Python):
    ```python
    import os
    API_KEY = os.getenv("BLABLADOR_API_KEY")  # Raised if missing
    ```
- **Rate Limits**:
  - **BLABLADOR API**: Max 5 requests/minute (cached responses recommended).
  - **Fallback**: Use [Ollama](https://github.com/ollama/ollama) if BLABLADOR returns 429/503.

### **B. Endpoint-Specific Workflows**
#### **1. Notes Management (`/api/v1/notes`)**
- **CRUD Operations**:
  ```bash
  # Create (markdown + frontmatter)
  POST /api/v1/notes
  {
    "content": "# Note Title\n---\nmetadata: {key: value}",
    "path": "path/to/note.md"
  }
  ```
- **Validation**:
  - Reject empty `content` or invalid frontmatter (YAML parsing).
  - Store files in `./data/notes/` (directory-based).

#### **2. LLM Q&A (`/api/v1/qa`)**
- **RAG Workflow**:
  ```python
  # Step 1: Retrieve context
  response = requests.post(
      "https://harvesthealth-magnetic-ui.hf.space/api/v1/similar",
      json={"query": "explain study methodology", "top_k": 3}
  )
  similar_notes = response.json()["results"]

  # Step 2: Enrich prompt with context
  context = "\n\n".join([note["content"] for note in similar_notes])

  # Step 3: Call LLM
  llm_response = requests.post(
      "https://harvesthealth-magnetic-ui.hf.space/api/v1/qa",
