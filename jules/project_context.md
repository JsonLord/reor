# Project Context

## Project Description
### **Project Description**

#### **Vision**
Deploy a Gradio-based LLM interface on Hugging Face Spaces with seamless integration of the **Helmholtz BLABLADOR API** (OpenAI-compatible endpoint). The app will preserve its original language processing logic while exposing externally accessible APIs for programmatic management, enabling AI-driven use cases with secure and scalable infrastructure.

#### **Concrete Goals**
1. **API Compatibility**:
   - Replace hardcoded OpenAI API calls in `reor.git` with the **Helmholtz BLABLADOR API** (`api.helmholtz-blablador.fz-juelich.de/v1`) using the model alias `large`.
   - Ensure full OpenAI API compatibility (e.g., `/v1/completions` endpoint support).

2. **Security & Deployment**:
   - Load the **`BLABLADOR_API_KEY`** securely from Hugging Face Space environment variables.
   - Deploy the app to **Hugging Face Spaces** (`harvesthealth-magnetic-ui.hf.space`) with:
     - Gradio UI accessible at port `7860`.
     - Externally exposed APIs via the Space URL (e.g., `/api/generate`).

3. **AI-Centric Implementation**:
   - Retain the original app’s **language logic** and **model interaction** workflows.
   - Optimize backend logic for AI feature-rich interactions (e.g., prompt handling, temperature, max tokens).

4. **API Exposure & Forwarding**:
   - Implement a **reverse proxy system** to route external requests to internal Gradio APIs.
   - Ensure APIs are accessible at `https://harvesthealth-magnetic-ui.hf.space/api/{endpoint}`.

---

#### **Future Use Cases**
1. **Scalable AI Workflows**:
   - Integrate with **Hugging Face Hub** for model versioning and collaborative updates.
   - Support **multi-modal interactions** (e.g., audio-to-text, code generation) by extending the BLABLADOR API usage.

2. **Enterprise & Research Applications**:
   - **Healthcare/Life Sciences**: Deploy in **HarvestHealth** pipelines for clinical NLP tasks (e.g., report summarization, patient query responses).
   - **Research**: Enable reproducible experiments with BLABLADOR’s large-scale language models.

3. **Programmatic Access**:
   - **Automated Systems**: Use APIs for batch processing (e.g., generating responses for customer service bots).
   - **Third-Party Integrations**: Connect with tools like **Notion**, **Slack**, or **Zapier** via webhooks.

4. **Multi-Backend Support**:
   - Extend to other OpenAI-compatible APIs (e.g., **Azure OpenAI**, **vLLM**, or local models) via a plugin system.

5. **Monitoring & Analytics**:
   - Log API usage, errors, and performance metrics for debugging and optimization.
   - Integrate with Hugging Face’s **Datasets** or **Spaces Analytics** for tracking adoption.

---

#### **Potential Integrations**
| **Integration**               | **Purpose**                                                                 | **Compatibility**                          |
|-------------------------------|-----------------------------------------------------------------------------|---------------------------------------------|
| **Helmholtz BLABLADOR API**   | Primary LLM backend (`/v1/completions`), model alias `large`.              | OpenAI-compatible                          |
| **Hugging Face Spaces**       | Hosting (Docker, reverse proxy, environment variables).                    | Gradio, FastAPI, or Streamlit-compatible.  |
| **Gradio/FastAPI**            | Backend API framework for exposing endpoints (`/api/generate`, `/health`). | Extends Gradio’s native API capabilities.  |
| **Hugging Face Hub**          | Model versioning and collaborative development.                            | Git-like workflows.                       |
| **OpenAI-Compatible APIs**    | Fallback/alternative backends (e.g., Azure OpenAI, local models).          | Standardized API contracts.                |
| **Monitoring Tools**          | Log API calls, errors, and performance (e.g., Prometheus, Datadog).        | Metrics/observability stack.               |
| **Third-Party Apps**          | Connect to Slack, Notion, or custom workflows via webhooks.               | HTTP API endpoints.                        |

## Tasks and Tests
### **1. Estimation of Project Scope (1-10)**
**Score: 8/10**
**Core parts**:
1. **API Integration** – Replace OpenAI calls with Helmholtz BLABLADOR API (`/v1/completions`) using `BLABLADOR_API_KEY` from Hugging Face environment variables.
2. **Gradio-to-HF-Spaces Adaptation** – Modify existing Gradio app for Docker deployment on Hugging Face with port `7860` exposed.
3. **Reverse Proxy & API Forwarding** – Ensure external API access via `harvesthealth-magnetic-ui.hf.space` (e.g., `/api/generate`).
4. **Security** – Validate API keys, rate-limit endpoints, and ensure HTTPS.
5. **Testing & Monitoring** – Validate full pipeline (input → Helmholtz API → output) and log deployment issues.

---

### **2. Project Description**
**Vision**:
Deploy an OpenAI-compatible LLM interface (originally from `reor.git`) on Hugging Face Spaces, using the **Helmholtz BLABLADOR API** as the backend. The app will retain its language logic (e.g., prompt processing, temperature controls) while exposing APIs for external management (e.g., programmatic text generation).

**Concrete Goals**:
1. **Functional**:
   - Replace all OpenAI API calls in the Gradio app with Helmholtz BLABLADOR API requests (`/v1/completions`).
   - Securely fetch `BLABLADOR_API_KEY` from Hugging Face Space environment variables.
   - Expose APIs (e.g., `/api/generate`, `/api/health`) alongside the Gradio UI.
2. **Compatibility**:
   - Maintain OpenAI-compatible parameters (e.g., `max_tokens`, `temperature`).
   - Support Hugging Face Spaces’ Docker deployment constraints (port `7860`).
3. **Accessibility**:
   - UI at `https://harvesthealth-magnetic-ui.hf.space` (port `7860`).
   - APIs accessible via the same domain (e.g., `https://harvesthealth-magnetic-ui.hf.space/api/generate`).

**Future Use Cases**:
- **Extensibility**: Add support for other OpenAI-compatible APIs (e.g., Azure OpenAI) via a plugin system.
- **Scalability**: Deploy multiple instances for load balancing.
- **Monitoring**: Log API usage and errors for debugging (integrate with Hugging Face Datasets).

**Future Integrations**:
1. **OpenAI-Compatible APIs**: Backend swappability (e.g., local models via `vLLM`).
2. **Hugging Face Hub**: Model versioning and updates.
3. **Authentication**: Add API key authentication for `/api/generate`.

---

### **3. Other Projects/API Endpoints for Integration**
| **Component**               | **Endpoint/API**                          | **Type**               | **Integration Notes**                                                                 |
|-----------------------------|-------------------------------------------|------------------------|--------------------------------------------------------------------------------------|
| Helmholtz BLABLADOR API     | `https://api.helmholtz-blablador.fz-juelich.de/v1/completions` | OpenAI-compatible LLM  | Replace all OpenAI API calls. Model alias: `large`. Auth: Bearer token (`BLABLADOR_API_KEY`). |
| Hugging Face Spaces         | `https://harvesthealth-magnetic-ui.hf.space` | Deployment Platform    | Docker-based Gradio app. Reverse proxy for API forwarding.                          |
| Gradio                     | Port `7860` (default)                     | UI Framework           | Existing app logic preserved. Environment variables for `BLABLADOR_API_KEY`.        |

---

### **4. Components & Subtasks**
#### **4.1 Components to Build**
1. **API Integration Layer**
   - Replaces OpenAI calls with Helmholtz BLABLADOR API requests.
   - Handles authentication via `BLABLADOR_API_KEY`.
   - *Interaction*: Called by Gradio frontend and exposed API endpoints.

2. **Gradio App Adapter**
   - Modifies `reor.git` to load `BLABLADOR_API_KEY` from environment variables.
   - Ensures compatibility with Hugging Face Spaces Docker template.
   - *Interaction*: Frontend UI + API layer.

3. **Reverse Proxy & API Forwarding**
   - Configures Hugging Face Spaces to expose internal APIs (e.g., `/api/generate`) via the Space URL.
   - *Interaction*: Routes external requests to Gradio’s internal endpoints.

4. **Security Middleware**
   - Validates `BLABLADOR_API_KEY` before BLABLADOR API calls.
   - Rate-limits `/api/generate` to avoid abuse.
   - *Interaction*: Intercepts API requests before processing.

5. **Deployment Scripts**
   - Updates `Dockerfile` for Hugging Face Spaces (port `7860` exposed).
   - Sets up CI/CD (e.g., automated testing on push).
   - *Interaction*: Deploys the app to `harvesthealth-magnetic-ui.hf.space`.

---

#### **4.2 Subtasks per Component**
| **Component**               | **Subtasks**                                                                                                                                                                                                 |
|-----------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **API Integration Layer**   |                                                                                                                                                                                                      |
|                             | - Audit `reor.git` for OpenAI API calls (e.g., `openai.Completion.create`).                                                                                                                             |
|                             | - Replace with `requests.post()` to Helmholtz BLABLADOR API (`/v1/completions`) using `BLABLADOR_API_KEY`.                                                                                               |
|                             | - Add error handling for API failures (e.g., rate limits, invalid keys).                                                                                                                                 |
|                             | - Mock BLABLADOR API responses locally for testing.                                                                                                                                                           |
|                             | - Protocol: Use `os.environ.get("BLABLADOR_API_KEY")` with validation.                                                                                                                                  |
| **Gradio App Adapter**      |                                                                                                                                                                                                      |
|                             | - Fork `JsonLord/reor` → `harvesthealth-ai/reor`.                                                                                                                                                           |
|                             | - Modify `app.py` to load `BLABLADOR_API_KEY` from environment variables.                                                                                                                               |
|                             | - Test locally with a dummy key (`export BLABLADOR_API_KEY="test123"`).                                                                                                                                     |
|                             | - Update `requirements.txt` if new dependencies (e.g., `requests`) are needed.                                                                                                                               |
| **Reverse Proxy**           |                                                                                                                                                                                                      |
|                             | - Configure Hugging Face Spaces to proxy `/api/*` to Gradio’s internal endpoints (e.g., `http://localhost:7860/api/generate`).                                                                         |
|                             | - Test forwarding with `curl -X POST "https://harvesthealth-magnetic-ui.hf.space/api/generate"`.                                                                                                           |
|                             | - Protocol: Use Hugging Face’s built-in reverse proxy or Nginx in Docker.                                                                                                                                |
| **Security Middleware**     |                                                                                                                                                                                                      |
|                             | - Add API key validation for `/api/generate` (e.g., check `Authorization: Bearer` header).                                                                                                               |
|                             | - Implement rate limiting (e.g., 10 requests/minute).                                                                                                                                                          |
|                             | - Use HTTPS for all external communications.                                                                                                                                                                   |
| **Deployment Scripts**      |                                                                                                                                                                                                      |
|                             | - Update `Dockerfile` to expose port `7860`.                                                                                                                                                                |
|                             | - Add `.hf` secrets for `BLABLADOR_API_KEY` (Hugging Face Space environment).                                                                                                                              |
|                             | - Create a CI script (e.g., GitHub Actions) to test locally before deploying.                                                                                                                            |
|                             | - Fork repository to `harvesthealth-ai` with updated `README.md` (includes setup instructions).                                                                                                          |

---
**Note on External Code**:
- **Helmholtz BLABLADOR API**: Full integration is possible (no need to mirror code). Use their `/v1/completions` endpoint directly.
- **Gradio**: Existing code can be adapted without mirroring (only environment variable and API replacement needed).

---

#### **4.3 Tests per Component**
| **Component**               | **Test Description**                                                                                                                                                                                                 | **Success Criteria**                                                                                                                                                                                                 |
|-----------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **API Integration Layer**   |                                                                                                                                                                                                                       |                                                                                                                                                                                                                       |
|                             | 1. **API Call Test**: Send a mock prompt to BLABLADOR API with `BLABLADOR_API_KEY`.                                                                                                                                    | Returns valid completion text with `text` and `usage` fields.                                                                                                                                                         |
|                             | 2. **Key Validation Test**: Pass an invalid/missing `BLABLADOR_API_KEY`.                                                                                                                                       | Returns `401 Unauthorized` or clear error message.                                                                                                                                                               |
|                             | 3. **Parameter Test**: Test OpenAI-compatible params (e.g., `max_tokens=50`, `temperature=0.7`).                                                                                                               | BLABLADOR API respect params and returns expected output.                                                                                                                                                           |
| **Gradio App Adapter**      |                                                                                                                                                                                                                       |                                                                                                                                                                                                                       |
|

## GitHub Repos
- `JsonLord/reor`
- `harvesthealth-ai/reor-hf-deployment`

## Functionality Expectations
### **Functionality Expectations of the Deployed Application**

1. **Core LLM Functionality**
   - Retain the original app’s language generation capabilities (e.g., prompt processing, text completion).
   - Support OpenAI-compatible parameters (e.g., `prompt`, `temperature`, `max_tokens`).

2. **API-Driven Management**
   - Expose the following endpoints for external interaction:
     - **`POST /api/generate`**: Generate text using the Helmholtz BLABLADOR API (requires `BLABLADOR_API_KEY`).
     - **`GET /api/model`**: Return model metadata (e.g., `alias: large`).
     - **`GET /api/health`**: Health check endpoint (no auth).
   - **Authentication**: API endpoints (except health/model) may require API key validation.

3. **Hugging Face Spaces Integration**
   - **UI Accessibility**: Gradio interface available at:
     `https://harvesthealth-magnetic-ui.hf.space` (port `7860`).
   - **API Accessibility**: External APIs accessible via the same domain:
     `https://harvesthealth-magnetic-ui.hf.space/api/{endpoint}`.
   - **Reverse Proxy Forwarding**: Hugging Face Spaces handles routing to internal ports (e.g., `7860`).

4. **Security & Environment Handling**
   - Load `BLABLADOR_API_KEY` securely from Hugging Face Space environment variables.
   - Validate API keys and rate-limit endpoints to prevent abuse.

5. **OpenAI-Compatible LLM Endpoint**
   - Replace OpenAI API calls with Helmholtz BLABLADOR API (`api.helmholtz-blablador.fz-juelich.de/v1`).
   - Use model alias `large` for backend requests.

6. **Deployment Constraints**
   - **Main Port**: `7860` (Gradio default).
   - **Docker-Based Deployment**: Adopt Hugging Face Spaces’ Docker template with exposed port `7860`.
   - **Forwarding System**: Ensure external requests to `/api/*` are routed to the backend.

7. **Future Extensibility**
   - Support for additional OpenAI-compatible APIs (e.g., Azure OpenAI, local models).
   - Plugin system for custom LLM backends.

## API Endpoints
```json
[
  {
    "method": "POST",
    "endpoint": "/api/generate",
    "description": "Generate text using the Helmholtz BLABLADOR API (OpenAI-compatible endpoint).",
    "auth_required": "Yes",
    "parameters": {
      "prompt": "Required string: Input text prompt.",
      "max_tokens": "Optional int: Maximum tokens to generate.",
      "temperature": "Optional float: Controls randomness (0.0–1.0).",
      "model": "Fixed string: 'large' (alias for BLABLADOR's large model)."
    },
    "example_request": {
      "url": "https://harvesthealth-magnetic-ui.hf.space/api/generate",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json"
      },
      "body": {
        "prompt": "Hello, how are you?",
        "max_tokens": 50
      }
    }
  },
  {
    "method": "GET",
    "endpoint": "/api/model",
    "description": "Retrieve model metadata (e.g., alias, provider details).",
    "auth_required": "No",
    "response_example": {
      "model_alias": "large",
      "provider": "helmholtz-blablador",
      "max_tokens": 4096,
      "status": "available"
    }
  },
  {
    "method": "GET",
    "endpoint": "/api/health",
    "description": "Health check for backend services (BLABLADOR API and app status).",
    "auth_required": "No",
    "response_example": {
      "status": "healthy",
      "api_connection": "active",
      "timestamp": "2023-11-15T12:00:00Z"
    }
  },
  {
    "method": "GET",
    "endpoint": "/",
    "description": "Gradio UI interface (main app interface, port 7860).",
    "auth_required": "No",
    "notes": "Exposes the original language logic of `reor.git` (no direct API access)."
  },
  {
    "method": "POST",
    "endpoint": "/v1/completions",
    "description": "Legacy OpenAI-compatible endpoint (alias for BLABLADOR API).",
    "auth_required": "Yes",
    "notes": "Internal use only; mirrors Helmholtz BLABLADOR's `/v1/completions` for backward compatibility."
  }
]
```

## HF Deployment Data
Profile: harvesthealth

Space: magnetic-ui
