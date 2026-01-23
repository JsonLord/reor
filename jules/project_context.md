# Project Context

## Project Description
### **Adapted Project Description: Reor for Hugging Face Spaces**

**Vision**
Reor is being adapted into a **Hugging Face Spaces-hosted AI knowledge management system**, leveraging an **OpenAI-compatible LLM endpoint** (`https://api.helmholtz-blablador.fz-juelich.de/v1`) while maintaining **local-first privacy** and **semantic note-linking** capabilities. The core hypothesis remains: *AI tools for thought should integrate seamlessly with external LLM APIs while preserving local data control*.

---

### **Concrete Goals**
1. **LLM Integration & Compatibility**
   - Replace or augment local Ollama/Transformers.js models with the **BLABLADOR API** (`model: alias-large`), accessed via `BLABLADOR_API_KEY` (fetched from Hugging Face Space environment variables).
   - Support **OpenAI-compatible endpoints** (e.g., `/v1/chat/completions`) for RAG workflows.

2. **Backend API Refinement**
   - **Expose core APIs externally** via Hugging Face Space URL (`https://harvesthealth-magnetic-ui.hf.space`), ensuring:
     - CRUD operations for notes (markdown + frontmatter).
     - Vector embeddings (LanceDB) and semantic retrieval.
     - LLM-powered Q&A with context-aware responses.
   - **Port forwarding**: Map external traffic to Gradio’s default port (`7860`).

3. **Frontend Adaptations**
   - Retain the **Obsidian-like markdown editor** and **related notes sidebar** (vector similarity-driven).
   - Ensure UI responsiveness for Hugging Face Spaces constraints (e.g., cold starts, resource limits).

4. **Deployment Strategy**
   - **Dockerize** the app with:
     - FastAPI/Flask backend for API routing.
     - Gradio frontend for UI (port `7860`).
     - NGINX reverse proxy to handle external requests.
   - Configure **Hugging Face Space secrets** for `BLABLADOR_API_KEY`.
   - Implement **API gateway** for external management (e.g., `/api/v1/notes`, `/api/v1/qa`).

---

### **Future Use Cases**
| **Use Case**               | **Implementation Focus**                                                                 |
|----------------------------|------------------------------------------------------------------------------------------|
| **Healthcare Knowledge Hub** | Semantic search across medical notes with RAG-powered Q&A (e.g., "Explain this study’s methodology"). |
| **Research Collaboration**  | Shared note repositories with LLM-assisted synthesis (BLABLADOR API for domain-specific models). |
| **API-Driven Workflows**    | Integrate with external tools via OpenAI-compatible endpoints (e.g., chatbots, automation). |
| **Cold-Start Optimization** | Pre-load lightweight vector embeddings to mitigate latency in Hugging Face Spaces.       |

---

### **Potential Integrations**
1. **External APIs**
   - **BLABLADOR API**: Default LLM endpoint for domain-specific inference.
   - **OpenAI-Compatible Services**: Fallback to Ollama/Oobabooga if BLABLADOR is unavailable.

2. **Data Storage**
   - **LanceDB**: Local vector database for embeddings (no cloud dependency).
   - **Hugging Face Hub**: Optional sync for collaborative workflows (future feature).

3. **Frontend Extensions**
   - **Gradio Components**: Custom UI elements for note linking/sidebar.
   - **React (Optional)**: For complex interactions if Gradio’s limits are hit.

4. **Security & Compliance**
   - **Environment-Based API Keys**: `BLABLADOR_API_KEY` restricted to Space secrets.
   - **Rate Limiting**: Prevent abuse of LLM endpoints.
   - **CORS Policies**: Restrict external API calls to trusted domains.

---
### **Key Adaptations from Original Reor**
| **Original Feature**               | **Adaptation for Hugging Face Spaces**                                                                 |
|------------------------------------|------------------------------------------------------------------------------------------------------|
| Local Ollama/Transformers.js models | **BLABLADOR API endpoint** with `BLABLADOR_API_KEY` (via environment variables).                   |
| Self-hosted vector DB              | **LanceDB** (local) + potential future cloud sync options.                                          |
| Desktop app                        | current front end
| Manual note imports                | **API-driven note CRUD** (e.g., `POST /api/v1/notes`) for programmatic ingestion.                 |
| Obsidian-like editor              | all functionalities of reor in tact

---
**Note**: The adaptation prioritizes **AI-driven features** (RAG, Q&A) while ensuring the app remains **privacy-preserving** (no cloud storage) and **API-exposable** for external workflows.

## Tasks and Tests
### **1. Estimation of Project Scope: 9/10**
**Core Parts:**
- **Backend (FastAPI)** – OpenAI-compatible LLM integration, LanceDB vector storage, RAG workflows.
- **Frontend (Gradio/React)** – Obsidian-like editor, related notes sidebar, UI for Q&A mode.
- **Hugging Face Deployment** – Dockerization, reverse proxy setup, API gateway (`/api/v1`).
- **API Layer** – CRUD for notes, embeddings, semantic search, and LLM Q&A.
- **Security** – Environment variable-based API key management, input validation, CORS restrictions.

---

### **2. Project Description**
**Vision:**
Reor is a **privacy-first, locally hosted AI knowledge management system** that augments note-taking with semantic search, RAG-based Q&A, and vector similarity. The Hugging Face deployment will expose its core AI features (RAG, embeddings, LLM inference) via an OpenAI-compatible API while preserving the app’s local-first architecture.

**Concrete Goals:**
- Deploy **Reor on Hugging Face Spaces** with `BLABLADOR_API_KEY` integration for LLM inference.
- Expose **FastAPI backend** via `/api/v1/*` endpoints (notes, Q&A, embeddings).
- Maintain **Gradio UI** (port `7860`) for user interaction, with optional React/Tailwind upgrades.
- Forward external traffic via **NGINX reverse proxy** to `harvesthealth-magnetic-ui.hf.space`.

**Future Use Cases:**
- **Enterprise Knowledge Bases** – Secure, self-hosted Q&A for internal documentation.
- **Research Collaboration** – Shared vector databases with controlled API access.
- **Educational Tools** – Semantic note-linking for students (e.g., linking lecture slides to study notes).

**Future Integrations:**
- **Zettlr/Obsidian Plugins** – Sync notes between Reor and existing markdown editors.
- **Slack/MS Teams Bots** – Trigger Q&A via chat platforms.
- **Custom Model Hosting** – Allow users to deploy fine-tuned LLMs alongside BLABLADOR.

---

### **3. External Projects/API Endpoints**
| **Component**               | **Integration Type**       | **API/Repo**                                                                 | **Notes**                                                                                     |
|-----------------------------|----------------------------|------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| **LLM API (BLABLADOR)**     | OpenAI-Compatible         | `https://api.helmholtz-blablador.fz-juelich.de/v1`                          | Model: `large`; Key: `BLABLADOR_API_KEY` (from HF Space secrets).                            |
| **Vector DB (LanceDB)**     | Local Storage              | [`lancedb/lancedb`](https://github.com/lancedb/lancedb)                      | Supports cosine similarity; no cloud dependency.                                             |
| **Markdown Processing**     | Frontend                  | [`markdown-it`](https://github.com/markdown-it/markdown-it)                 | For parsing Obsidian-like frontmatter.                                                       |
| **FastAPI**                 | Backend Framework          | [`fastapi`](https://github.com/tiangolo/fastapi)                            | For `/api/v1/*` endpoints; uses Uvicorn for ASGI.                                            |
| **Docker**                  | Deployment                 | Official images + HF Spaces SDK                                            | Multi-stage build: backend (Python) + frontend (Gradio).                                    |
| **NGINX**                   | Reverse Proxy              | Standard                                                                      | Forward `harvesthealth-magnetic-ui.hf.space` → `localhost:7860`.                            |

---

### **4. Components & Subtasks**
#### **4.1. Component List**
1. **Backend (FastAPI)**
   - Handles `/api/v1/notes`, `/api/v1/qa`, `/api/v1/embeddings`, `/api/v1/similar`.
   - Integrates BLABLADOR API and LanceDB.
   - **Interaction**: Frontend (Gradio) ↔ Backend (FastAPI) ↔ LLM/API → User.

2. **Frontend (Gradio)**
   - Obsidian-like editor + sidebar for related notes.
   - **Interaction**: Renders UI; sends/receives API calls to FastAPI.

3. **Vector Database (LanceDB)**
   - Stores note chunks as embeddings.
   - **Interaction**: Backend queries embeddings for semantic search/RAG.

4. **Deployment (Docker + Hugging Face)**
   - Dockerfile for multi-stage build (Python + Gradio).
   - NGINX reverse proxy for external URL.
   - **Interaction**: `harvesthealth-magnetic-ui.hf.space` → `localhost:7860`.

---

#### **4.2. Subtasks per Component**
| **Component**       | **Subtasks**                                                                                                                                                                                                                                                                 |
|---------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Backend**       keep original but:  | - **T1.1**: use new llm endpoint`POST /api/v1/chat/completions` (BLABLADOR API).                                                                                                                                                                                        |
|                     | - **T1.2**: use `BLABLADOR_API_KEY` to `.env` (Hugging Face Space secrets).                                                                                                                                                                                   |
|                     | - **T1.3**: Integrate LanceDB for embedding storage.                                                                                                                                                                                                   |
|                     | - **T1.4**: Build CRUD endpoints (`/api/v1/notes`).                                                                                                                                                                                                 |
|                     | - **T1.5**: Add RAG workflow (retrieve + generate).                                                                                                                                                                                                 |
| **Frontend**       Keep original 
                                                                                                                                                                                           |
| **Vector DB**       | - **T3.1**: Initialize LanceDB table with note chunks.                                                                                                                                                                                              |
|                     | - **T3.2**: Implement `POST /api/v1/embeddings` endpoint.                                                                                                                                                                                            |
|                     | - **T3.3**: Add cosine similarity search (`POST /api/v1/similar`).                                                                                                                                                                              |
| **Deployment**      | - **T4.1**: Dockerize FastAPI + Gradio (multi-stage).                                                                                                                                                                                              |
|                     | - **T4.2**: Configure Hugging Face Space secrets (`BLABLADOR_API_KEY`).                                                                                                                                                                           |
|                     | - **T4.3**: Set up NGINX reverse proxy (`7860` → external URL).                                                                                                                                                                                |
|                     | - **T4.4**: Test API gateway (`/api/v1/*` forwarding).                                                                                                                                                                                           |

---
#### **4.3. Security & Integration Protocols**
| **Component**       | **Protocol**                                                                                                                                                                                                                                                                 |
|---------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Backend**         | - **API Key**: Fetch `BLABLADOR_API_KEY` from HF Space secrets.                                                                                                                                                                                     |
|                     | - **Input Validation**: Sanitize markdown/frontmatter to prevent injection.                                                                                                                                                                       |
|                     | - **Rate Limiting**: Limit LLM API calls (e.g., 5/minute).                                                                                                                                                                                      |
| **Frontend**        | - **CORS**: Restrict API calls to `harvesthealth-magnetic-ui.hf.space`.                                                                                                                                                                           |
|                     | - **Sandboxing**: Local models only; no remote execution.                                                                                                                                                                                            |
| **Deployment**      | - **HTTPS**: Enforce via Hugging Face Space (automatic).                                                                                                                                                                                       |
|                     | - **Authentication**: HF Space JWT (if private space).                                                                                                                                                                                                  |

**Integration Notes:**
- **BLABLADOR API**: Full compatibility with OpenAI’s `/v1/chat/completions` schema.
- **LanceDB**: Use official Python client; no code mirroring needed.
- **Gradio/FastAPI**: Gradio will proxy to FastAPI for `/api/v1/*` routes.

---

### **4.4. Tests per Component**
| **Component**       | **Test Description**                                                                                                                                                                                                                                                                 | **Success Criteria**                                                                                                                                                                                                 |
|---------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Backend**         | - **T1.1**: Send `POST /api/v1/chat/completions` with `BLABLADOR_API_KEY`.                                                                                                                                                                           | Returns LLM response in OpenAI-compatible JSON.                                                                                                                                                                         |
|                     | - **T1.2**: Verify `.env` loads `BLABLADOR_API_KEY`.                                                                                                                                                                                             | `KeyError` raised if missing.                                                                                                                                                                                              |
|                     | - **T1.3**: Insert/Retrieve embeddings via LanceDB.                                                                                                                                                                                                        | Embeddings stored/retrieved with `cosine_similarity > 0.85`.                                                                                                                                                         |
| **Frontend**        | - **T2.1**: Render markdown with Gradio.                                                                                                                                                                                                                  | Displays syntax

## GitHub Repos
Here are the GitHub repositories mentioned in the original `README`:
1. **[Ollama](https://github.com/ollama/ollama)**
2. **[Transformers.js](https://github.com/xenova/Transformers.js)**
3. **[LanceDB](https://github.com/lancedb/lancedb)**

## Functionality Expectations
```json
{
  "functionality_expectations": [
    {
      "feature": "Private Knowledge Management",
      "description": "All notes/data stored locally (LanceDB). No cloud dependency."
    },
    {
      "feature": "Semantic Search",
      "description": "Retrieve notes via vector similarity (cosine similarity)."
    },
    {
      "feature": "LLM Q&A",
      "description": "Answer questions using retrieved context (RAG). Supports BLABLADOR API."
    },
    {
      "feature": "OpenAI-Compatible API",
      "description": "Backend exposes `/v1/chat/completions` endpoint for LLM calls."
    },
    {
      "feature": "Gradio UI",
      "description": "Obsidian-like editor with related notes sidebar."
    },
    {
      "feature": "Automatic Note Linking",
      "description": "Connect related notes based on vector similarity (AI-powered)."
    },
    {
      "feature": "Markdown Editor",
      "description": "Supports markdown with frontmatter (Obsidian-like syntax)."
    },
    {
      "feature": "Local LLM Integration",
      "description": "Interact with Ollama or OpenAI-compatible APIs for LLM generation."
    },
    {
      "feature": "Retrieval-Augmented Generation (RAG)",
      "description": "Generate answers by combining retrieved notes with LLM context."
    },
    {
      "feature": "Cross-Referenced Thinking",
      "description": "Toggle sidebar to reveal contextually related notes."
    },
    {
      "feature": "Directory-Based Data Storage",
      "description": "Notes stored as markdown files in a user-defined filesystem directory."
    }
  ]
}
```

## API Endpoints
```json
{
  "api_endpoints": [
    {
      "endpoint": "/api/v1/notes",
      "method": ["GET", "POST", "PUT", "DELETE"],
      "description": "Manage notes (CRUD). Supports markdown + frontmatter."
    },
    {
      "endpoint": "/api/v1/qa",
      "method": "POST",
      "description": "LLM-powered Q&A on notes (RAG)."
    },
    {
      "endpoint": "/api/v1/embeddings",
      "method": "POST",
      "description": "Generate embeddings for text chunks (LanceDB)."
    },
    {
      "endpoint": "/api/v1/similar",
      "method": "POST",
      "description": "Retrieve semantically similar notes."
    }
  ]
}
```

## HF Deployment Data
Profile: The Huggingface **Namespace/Profile name** (username) for deployment would be:
**`harvesthealth`** (from the URL `https://harvesthealth-magnetic-ui.hf.space`).
Space: `harvesthealth-magnetic-ui`
