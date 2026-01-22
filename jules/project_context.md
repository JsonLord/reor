# Project Context

## Project Description
### **Project Description**

#### **Vision**
Deploy a Gradio-based Hugging Face Space app that integrates with an external OpenAI-compatible LLM endpoint (`helmholtz-blablador.fz-juelich.de/v1`) using the `alias-large` model. The app must maintain its existing language logic while adapting the deployment strategy to expose backend APIs externally for remote management and interaction. The deployment should leverage Docker, with the interface accessible via port `7860`, and APIs forwarded through a proxy to `https://harvesthealth-magnetic-ui.hf.space`.

#### **Concrete Goals**
1. **LLM Integration**: Replace the existing LLM backend with calls to `https://api.helmholtz-blablador.fz-juelich.de/v1` using the `alias-large` model.
2. **Secure API Key Handling**: Load the `BLABLADOR_API_KEY` from Hugging Face Space environment variables.
3. **External API Exposure**: Expose backend APIs via `https://harvesthealth-magnetic-ui.hf.space/api` using a reverse proxy (e.g., Nginx or Caddy) within the Docker container.
4. **UI Accessibility**: Serve the Gradio interface on port `7860`, ensuring it is accessible via the Hugging Face Space URL.
5. **Deployment Strategy**: Use Docker for consistent deployment, with Gradio as the frontend and a lightweight proxy (FastAPI or Nginx) for API routing.

#### **Future Use Cases**
- Remote management of the app via RESTful APIs.
- Integration with third-party tools or workflows that require programmatic access to the LLM.
- Scalable deployment for AI-powered language tasks (e.g., chat, summarization, translation) using the external LLM endpoint.
- Potential extension to support multiple models or endpoints via configuration.

#### **Potential Integrations**
- **Hugging Face Spaces**: For hosting and managing the app with environment variables and Docker.
- **FastAPI or Nginx**: As a reverse proxy to forward external API requests to the LLM endpoint.
- **Gradio**: For building and serving the interactive UI.
- **External LLM Endpoint**: `https://api.helmholtz-blablador.fz-juelich.de/v1` with `alias-large` model.
- **Docker**: For containerized deployment, ensuring reproducibility and portability.
- **Caddy or Nginx**: For handling HTTPS and routing traffic to the appropriate services.

## Tasks and Tests
1. Estimation of Project Scope from 1-10 and with a presentation of the core parts  
Project scope: 8/10  
Core parts:  
- Backend logic adaptation to use OpenAI-compatible LLM endpoint at `https://api.helmholtz-blablador.fz-juelich.de/v1` with model `alias-large`  
- Secure retrieval of `BLABLADOR_API_KEY` from Hugging Face Space environment variables  
- Deployment on Hugging Face Space with exposed API endpoints for external connectivity  
- Implementation of a forwarding system to expose backend APIs externally via `https://harvesthealth-magnetic-ui.hf.space`  
- Preservation of original app language logic while replacing LLM backend  
- Use of Docker-based deployment with Gradio (preferred) or Streamlit frontend and FastAPI/Nginx for API exposure on port 7860  

2. Project Description w/ vision for the project, concrete goals what it should be capable of, and future use cases, and future integrations into other projects  
Vision: Deploy a functional, AI-powered application on Hugging Face Spaces that maintains its core language interface while integrating securely with an external OpenAI-compatible LLM service. The app should be remotely manageable via exposed API endpoints.  
Concrete goals:  
- App must route all LLM queries through `helmholtz-blablador.fz-juelich.de/v1` using `alias-large` model  
- `BLABLADOR_API_KEY` must be loaded securely from Hugging Face Space environment  
- Full backend API functionality must be accessible externally via `https://harvesthealth-magnetic-ui.hf.space/api`  
- UI must remain functional on port 7860 via Gradio  
- Application must run in a Docker container deployed on Hugging Face Space  
Future use cases:  
- Remote orchestration of the app via API calls from external dashboards or agents  
- Integration into larger AI workflows (e.g., healthcare NLP pipelines)  
- Multi-model routing based on input type or user role  
Future integrations:  
- Connection to internal HelmHoltz AI governance tools  
- Logging and monitoring via centralized AI observability platforms  

3. Other Projects or api endpoints that will be integrated into the project to act as part components to the overall project  
- OpenAI-compatible API endpoint: `https://api.helmholtz-blablador.fz-juelich.de/v1` (used for LLM inference)  
- Hugging Face Spaces platform (hosting environment with secret management)  
- Gradio (UI framework with built-in API exposure capability)  
- FastAPI (for custom backend API routing and proxying if needed)  
- Nginx or Caddy (for reverse proxying and external API exposure in Docker setup)  

4. A list of components that need to be built and how they interact  
- **Gradio UI Component**: Serves the user interface on port 7860; sends LLM requests to the backend proxy  
- **FastAPI Proxy Component**: Receives internal and external API calls; forwards them to the LLM endpoint with proper authentication  
- **Environment Manager**: Loads `BLABLADOR_API_KEY` from `os.environ` and injects it into API headers  
- **Docker Container Layer**: Bundles Gradio, FastAPI, and proxy server; exposes port 7860 and `/api` routes  
- **Reverse Proxy (Nginx/Caddy)**: Forwards external traffic from `https://harvesthealth-magnetic-ui.hf.space` to internal services (port 7860 and `/api`)  
- **API Exposure Layer**: Ensures all backend functions are reachable via HTTP endpoints for external management  

Interaction flow:  
External request → Hugging Face Space → Nginx/Caddy → routes `/` to Gradio (port 7860), `/api/*` to FastAPI → FastAPI uses `BLABLADOR_API_KEY` to call `helmholtz-blablador.fz-juelich.de/v1` → response returned through chain  

4.2. A list of subtasks per components  
**Gradio UI Component**  
- Subtask: Clone or recreate UI logic from original (assumed) reor app  
- Subtask: Replace local LLM calls with HTTP requests to internal FastAPI endpoint (e.g., `http://localhost:8000/llm`)  
- Subtask: Ensure prompt formatting and language logic are preserved  
- Subtask: Confirm Gradio generates `/api` endpoints for all interface functions  

**FastAPI Proxy Component**  
- Subtask: Set up FastAPI app with `/v1/chat/completions` and other required LLM endpoints  
- Subtask: Implement secure header injection using `os.environ["BLABLADOR_API_KEY"]`  
- Subtask: Validate incoming request structure and forward to `https://api.helmholtz-blablador.fz-juelich.de/v1`  
- Subtask: Return responses with correct status codes and JSON structure  

**Environment Manager**  
- Subtask: Implement secure environment variable loading for `BLABLADOR_API_KEY`  
- Subtask: Add fallback or error handling if key is missing  
- Subtask: Ensure key is never logged or exposed in responses  

**Docker Container Layer**  
- Subtask: Create `Dockerfile` installing Python, Gradio, FastAPI, Uvicorn, and Nginx/Caddy  
- Subtask: Define startup script to launch Nginx, Uvicorn (FastAPI), and Gradio  
- Subtask: Expose port 7860 and configure `/api` path routing  
- Subtask: Set working directory and copy app files  

**Reverse Proxy (Nginx/Caddy)**  
- Subtask: Configure Nginx/Caddy to serve Gradio on `/` and FastAPI on `/api`  
- Subtask: Forward `https://harvesthealth-magnetic-ui.hf.space` to internal services  
- Subtask: Ensure WebSocket support for Gradio streaming  

**API Exposure Layer**  
- Subtask: Document all available API endpoints (from Gradio and FastAPI)  
- Subtask: Ensure CORS is configured to allow external domains if needed  
- Subtask: Implement health check endpoint `/health`  

4.3. A list of tests to be run per component to check it's working, without writing code, but describing the functionality that should be working and define a success  
**Gradio UI Component**  
- Test: Load UI at `https://harvesthealth-magnetic-ui.hf.space`  
- Success: Page renders, input fields visible, chat works when submitted  
- Test: Submit test prompt "Hello, how are you?"  
- Success: Response is received via streaming or full message from LLM backend  

**FastAPI Proxy Component**  
- Test: Send POST request to `https://harvesthealth-magnetic-ui.hf.space/api/llm` with chat payload  
- Success: Returns 200 OK and valid LLM response from `helmholtz-blablador`  
- Test: Send malformed request  
- Success: Returns 400 Bad Request with error message  

**Environment Manager**  
- Test: Deploy without `BLABLADOR_API_KEY` set  
- Success: App fails to start or logs clear error, does not expose key  
- Test: Deploy with correct key  
- Success: LLM requests succeed, key used in headers without logging  

**Docker Container Layer**  
- Test: Run `docker-compose up` locally  
- Success: Services start, port 7860 accessible, no crashes  
- Test: Check logs for startup completion  
- Success: Logs show Gradio running on 7860, FastAPI on 8000, Nginx active  

**Reverse Proxy (Nginx/Caddy)**  
- Test: Access `https://harvesthealth-magnetic-ui.hf.space`  
- Success: Serves Gradio UI  
- Test: Access `https://harvesthealth-magnetic-ui.hf.space/api/health`  
- Success: Returns 200 from FastAPI  

**API Exposure Layer**  
- Test: Call `/api/predict` (Gradio) and `/api/llm` (FastAPI) externally  
- Success: Both return correct responses  
- Test: Use curl or Postman to simulate external management  
- Success: App responds to API commands without UI interaction  

5. Task of Full Pipeline Test: A test description for the full interaction from input to output, without writing code, but determining hw success would look like, and write some mock-up input data to use for testing  
Task: Simulate end-to-end user and API interaction  
Mock-up input data:  
```json
{
  "messages": [
    {"role": "user", "content": "Explain quantum computing in simple terms."}
  ],
  "model": "alias-large"
}
```  
Test flow:  
1. User submits message via Gradio UI  
2. Frontend sends request to backend (FastAPI)  
3. FastAPI adds `Authorization: Bearer <BLABLADOR_API_KEY>` and forwards to `helmholtz-blablador.fz-juelich.de/v1`  
4. Response is streamed back to Gradio UI  
5. Separately, external API call sent to `/api/llm` with same payload  
6. Same response received via API  
Success criteria:  
- UI returns LLM response correctly  
- API returns same response with 200 status  
- No authentication leaks or errors in logs  
- Full round-trip time under 10 seconds  

6. Task of API: Based on API logs documentation, add api endpoints for all funct

## GitHub Repos


## Functionality Expectations
### **Functionality Expectations of the Application Once Deployed**

1. **LLM Endpoint Integration**  
   - The application must use the OpenAI-compatible LLM endpoint at `https://api.helmholtz-blablador.fz-juelich.de/v1` with model alias `large`.  
   - The `BLABLADOR_API_KEY` must be securely retrieved from Hugging Face Space environment variables.

2. **Backend API Exposure**  
   - The backend APIs must be exposed externally via the URL `https://harvesthealth-magnetic-ui.hf.space` to allow remote management and interaction.  
   - A forwarding/proxy system (e.g., Nginx or Caddy) must be implemented to route external API traffic to the backend.

3. **UI Interface**  
   - The frontend interface must be accessible on port `7860` (default for Gradio/Streamlit).  
   - The UI should retain the original language logic and functionality of the source application.

4. **Deployment Strategy**  
   - The application must be deployed using Docker on Hugging Face Spaces.  
   - The deployment should leverage Gradio or Streamlit for the UI, with FastAPI or similar for backend API proxying.

5. **Security & Configuration**  
   - The `BLABLADOR_API_KEY` must be injected securely via Hugging Face Space secrets and not hardcoded.  
   - The application must handle authentication and authorization for API endpoints as needed.

6. **External Accessibility**  
   - The deployed app must be reachable from outside the Hugging Face Space environment via the provided URL.  
   - The `/api` endpoint must be functional and accessible for external clients.

7. **AI-Centric Features**  
   - The core AI functionality (e.g., language processing, prompt handling) must be preserved and optimized for the new LLM endpoint.  
   - The app should support real-time interaction with the LLM via the exposed APIs.

8. **Testing & Validation**  
   - The application must be tested locally and in the Hugging Face Space environment to confirm:  
     - Successful LLM calls using the external endpoint.  
     - Correct loading of environment variables.  
     - Proper API forwarding and external accessibility.  
     - UI responsiveness and functionality.

## API Endpoints
- **`/api` endpoint**: Exposes backend APIs for external management and interaction with the app. Purpose: Enable remote control and integration with the deployed application via HTTP requests.
- **`/v1/chat/completions` (proxied)**: Forwarded to `https://api.helmholtz-blablador.fz-juelich.de/v1` using the `BLABLADOR_API_KEY` from environment. Purpose: Serve AI-generated responses using the OpenAI-compatible LLM endpoint.
- **Port 7860**: Default Gradio interface port. Purpose: Host the frontend UI accessible at `https://harvesthealth-magnetic-ui.hf.space` for user interaction.

## HF Deployment Data
Profile: harvesthealth
Space: magnetic-ui
