Working behaviour and prompt context for Jules. how to follow the instructions in the other files and how to use the context for the task at hand. 
Add: to never delete a hf_upload.py file once created. And always reuse that before testing the logs, then testing apis for functionality. Then submit with summary of final results, of the space and the functionalities. 

Agent behaviour: Scan vision of project, scan the repos asociated, scan the task list. Build component by component. Test components. Identify where components interact. Test the internal interaction. Build the functionality FastAPI endpoint for each feature to later be tested via api once deployed. Then test the overall app from start to finish. Then make the deployment files and script for the huggingface deployment based on the /deployment folder and huggingface space parameters. Then expose the FASTAPis in the way it is recommended. Gradio=gradio endpoints. Docker= space url endpoints /health etc. Then deploy. Then check the build logs, then the run logs. Fix failures until successfully running. Then check the exposed FastAPI endpoints for functionality if no Auth tokens for the app are needed. If they are needed. Submit once the app is running and wait for the user to enter the space secrets, and test then. 


## Project Specific Instructions
Here’s a structured `AGENTS.md` file with specific instructions tailored to your project context:

```markdown
# AGENTS.md

## Agent Instructions for Reor Backend Deployment on Hugging Face Spaces

### 1. Working Behavior for This Project
- **Primary Objective**: Deploy the reor backend (https://github.com/reorproject/reor.git) as a containerized API service on Hugging Face Spaces.
- **Key Constraints**:
  - No frontend or UI components; backend-only deployment.
  - Must expose all backend functionalities via REST API endpoints.
  - Integrate with OpenAI-compatible endpoints (`https://api.helmholtz-blablador.fz-juelich.de/v1`) using model alias `large`.
  - Securely handle `BLABLADOR_API_KEY` via environment variables.
  - Log warnings if `BLABLADOR_API_KEY` is missing at startup.

### 2. Key Project-Specific Context
- **Deployment Target**: Hugging Face Space (`reorproject/reorproject/reor`).
- **Tech Stack**:
  - Backend: Python (reor core logic).
  - API Framework: FastAPI (preferred) or Gradio.
  - Containerization: Docker (compatible with Hugging Face Spaces).
  - AI Integration: OpenAI-compatible API with model alias `large`.
- **Critical Dependencies**:
  - `BLABLADOR_API_KEY` environment variable (required for AI endpoint access).
  - Port `7860` (default for Hugging Face Spaces).

### 3. Tips for Best Results
#### **Deployment Preparation**
- **Environment Variables**:
  - Set `BLABLADOR_API_KEY` in Hugging Face Space secrets.
  - Example `.env` for local testing:
    ```ini
    BLABLADOR_API_KEY=your_api_key_here
    ```
- **Docker Optimization**:
  - Use multi-stage builds to minimize image size.
  - Example `Dockerfile` snippet:
    ```dockerfile
    FROM python:3.10-slim
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    COPY . .
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
    ```

#### **API Design**
- **Endpoint Standards**:
  - Use `/api/` prefix for all endpoints (e.g., `/api/health`, `/api/ai/inference`).
  - Return JSON responses with consistent structure:
    ```json
    {
      "status": "success/error",
      "data": {...},
      "error": "optional_message"
    }
    ```
- **Health Check**:
  - Endpoint: `GET /api/health`
  - Response:
    ```json
    {
      "status": "ok",
      "ai_key_set": true/false,
      "backend_version": "x.y.z"
    }
    ```

#### **AI Integration**
- **Blablador API Client**:
  - Use `httpx` or `requests` with async support.
  - Example request:
    ```python
    import httpx

    async def call_blablador(prompt: str, max_tokens: int = 100):
        headers = {"Authorization": f"Bearer {os.getenv('BLABLADOR_API_KEY')}"}
        data = {"model": "large", "prompt": prompt, "max_tokens": max_tokens}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.helmholtz-blablador.fz-juelich.de/v1/completions",
                json=data,
                headers=headers,
                timeout=30.0
            )
        return response.json()
    ```
- **Error Handling**:
  - Gracefully handle missing `BLABLADOR_API_KEY` (return `503 Service Unavailable`).
  - Log all AI endpoint errors with timestamps.

#### **Logging**
- **Startup Warnings**:
  - Log to `stdout` (Hugging Face captures this):
    ```python
    import logging

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    if not os.getenv("BLABLADOR_API_KEY"):
        logger.warning("BLABLADOR_API_KEY not set in environment. AI features disabled.")
    ```
- **Request Logging**:
  - Log API requests/errors with:
    - Request ID (for tracing).
    - Latency metrics.
    - Error details (without sensitive data).

#### **Testing**
- **Local Testing**:
  - Use `pytest` or `httpx` to test endpoints.
  - Example test for `/api/