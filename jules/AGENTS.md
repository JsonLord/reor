Working behaviour and prompt context for Jules. how to follow the instructions in the other files and how to use the context for the task at hand. 
Add: to never delete a hf_upload.py file once created. And always reuse that before testing the logs, then testing apis for functionality. Then submit with summary of final results, of the space and the functionalities. 

Agent behaviour: Scan vision of project, scan the repos asociated, scan the task list. Build component by component. Test components. Identify where components interact. Test the internal interaction. Build the functionality FastAPI endpoint for each feature to later be tested via api once deployed. Then test the overall app from start to finish. Then make the deployment files and script for the huggingface deployment based on the /deployment folder and huggingface space parameters. Then expose the FASTAPis in the way it is recommended. Gradio=gradio endpoints. Docker= space url endpoints /health etc. Then deploy. Then check the build logs, then the run logs. Fix failures until successfully running. Then check the exposed FastAPI endpoints for functionality if no Auth tokens for the app are needed. If they are needed. Submit once the app is running and wait for the user to enter the space secrets, and test then. 


## important!
The current codebase you are working in is to be adapted following the vision of the project transformation in the /jules folder. The current application should be kept and only slightly changed, improved, expanded by the features described in /jules folder. The tasks files give a starting point, but judge for yourself. Develop tests to run to first see the current application feature, how it is working and make a plan to implement the features requested in /jules folder to develop the current application inside the repo towards the vision described to achieve expansion of the current app with functionalities described in the /jules folder. Adapt your coding implemententation to the coding language used by the project, and try to go with that. Test the full app within this working space. 

See what huggingface sdk from gradio over streamlit to docker fits best and use that, configure the README.md file accordingly and prepare to upload the file app, not just the new features, but the full app expanded with these new features, to the huggingface space. Monitor deployment and once it is running, test the api endpoints you had set to see the functionality of the app inside that huggingface space.

## Project Specific Instructions
Here’s an expanded **`AGENTS.md`** file with **specific instructions** tailored for the Reor project’s Hugging Face deployment, incorporating the context provided. This document assumes you’re implementing AI agents (e.g., backend APIs, UI components, or CI/CD pipelines) for Reor’s adapted vision:

---
# **AGENTS.md: Reor Deployment Agents & Roles**
*Rules of operation for the Reor project’s Hugging Face deployment.*

---

## **1. Project Overview**
Reor is transitioning from a **local-first** to a **cloud-deployable, API-first** knowledge management system, leveraging:
- **BLABLADOR’s OpenAI-compatible API** (`alias-large`) for LLM inference.
- **FastAPI** as the backend, with **Hugging Face Spaces** hosting the frontend (Gradio).
- **LanceDB** for vector embeddings and semantic search.
- **Docker** for containerization and deployment.

**Key Adaptations**:
- Replace Ollama with `BLABLADOR_API_KEY` (no local models).
- Expose `/chat`, `/search`, and `/notes` endpoints for **programmatic access**.
- Maintain local data storage while enabling cloud-hosted UI.

---

## **2. Agent Roles & Responsibilities**
Each "agent" (component/module) has a specific role in the deployment pipeline.

### **Agent 1: Backend API (FastAPI)**
**Purpose**: Serve `/chat`, `/search`, and `/notes` endpoints, integrating with BLABLADOR and LanceDB.

#### **Specific Instructions**
- **Replace Ollama with BLABLADOR**:
  - Replace all Ollama calls with HTTP requests to:
    ```python
    endpoint = "https://helmholtz-blablador.fz-juelich.de/v1"
    headers = {"Authorization": f"Bearer {os.getenv('BLABLADOR_API_KEY')}"}
    ```
  - Use `requests.post(f"{endpoint}/chat/completions", json={...})` for completions.

- **Implement RAG Pipeline**:
  - **Chunking**: Split notes into `512-token` chunks (e.g., using `langchain.text_splitter`).
  - **Embedding**: Send chunks to BLABLADOR’s `/embeddings` endpoint.
  - **Storage**: Save embeddings in LanceDB with metadata (note_id, chunk_id).

- **FastAPI Endpoints**:
  | Endpoint          | Method | Implementation Notes                                                                                     |
  |-------------------|--------|--------------------------------------------------------------------------------------------------------|
  | `/chat`           | POST   | Retrieve top-k chunks from LanceDB → pass to BLABLADOR → return response.                              |
  | `/search`         | GET    | Query LanceDB for semantic matches (e.g., `query="RAG"` → return chunks with `similarity > 0.8`).       |
  | `/notes`          | POST   | Save markdown to disk → auto-chunk/embed → update LanceDB.                                             |
  | `/notes/{id}`     | GET    | Return markdown content + metadata.                                                                    |

- **Security**:
  - Never hardcode `BLABLADOR_API_KEY`. Use Hugging Face Space environment variables:
    ```python
    BLABLADOR_API_KEY = os.getenv("BLABLADOR_API_KEY")
    if not BLABLADOR_API_KEY:
        raise ValueError("Missing BLABLADOR_API_KEY!")
    ```

- **Testing**:
  - Test `/chat` with:
    ```bash
    curl -X POST http://localhost:7860/chat \
      -H "Content-Type: application/json" \
      -d '{"prompt": "What is RAG?"}'
    ```
  - Verify `/search` returns LanceDB matches with `similarity` scores.

---

### **Agent 2: Frontend UI (Gradio/Streamlit)**
**Purpose**: Deliver an Obsidian-like editor with RAG/AI features via Hugging Face Spaces.

#### **Specific Instructions**
- **UI Components**:
  - **Markdown Editor**: Use `gradio.Textbox` or `gradio.Markdown` for editing.
  - **Chat Interface**: `gradio.Textbox` (input) + `gradio.HTML` (output) for LLM responses.
  - **Related Notes Sidebar**:
    ```python
    def load_related_notes(query):
        response = requests.get(f"http://localhost:7860/search?query={query}")
        return "\n".join(f"**{n['title']}** (Score: {n['score']:.2f})" for n in response.json())
    ```

- **Connect to Backend**:
  - Call `/chat` for LLM responses:
    ```python
    def generate