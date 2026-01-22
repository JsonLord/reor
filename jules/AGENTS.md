Working behaviour and prompt context for Jules. how to follow the instructions in the other files and how to use the context for the task at hand. 
Add: to never delete a hf_upload.py file once created. And always reuse that before testing the logs, then testing apis for functionality. Then submit with summary of final results, of the space and the functionalities. 

Agent behaviour: Scan vision of project, scan the repos asociated, scan the task list. Build component by component. Test components. Identify where components interact. Test the internal interaction. Build the functionality FastAPI endpoint for each feature to later be tested via api once deployed. Then test the overall app from start to finish. Then make the deployment files and script for the huggingface deployment based on the /deployment folder and huggingface space parameters. Then expose the FASTAPis in the way it is recommended. Gradio=gradio endpoints. Docker= space url endpoints /health etc. Then deploy. Then check the build logs, then the run logs. Fix failures until successfully running. Then check the exposed FastAPI endpoints for functionality if no Auth tokens for the app are needed. If they are needed. Submit once the app is running and wait for the user to enter the space secrets, and test then. 


## Project Specific Instructions
# AGENTS.md

This file provides detailed instructions for configuring and managing the `reor` backend agent deployed on Hugging Face Spaces. These instructions cover environment setup, deployment specifics, API usage, and monitoring practices tailored to the project's unique requirements.

---

## 🔧 Environment Setup & Dependencies

### Prerequisites
- Python 3.9+
- FastAPI
- Uvicorn (ASGI server)
- Requests or HTTPX for external API calls
- Pydantic (for request validation)

### Required Packages
Install these in your `requirements.txt`:

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
httpx==0.25.0
pydantic==2.5.0
```

> ✅ *Ensure all dependencies are listed in `requirements.txt` for Hugging Face compatibility.*

---

## 🛠️ Deployment Instructions

### Containerization with `Containerfile`
Use the following `Containerfile` to ensure compatibility with Hugging Face Spaces:

```Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

> ⚠️ Make sure `main.py` contains your FastAPI app entry point.

---

## 📦 Secrets Management

### Using Hugging Face Space Secrets
Store your `BLABLADOR_API_KEY` securely using Hugging Face Spaces secrets:

1. Go to your Hugging Face Space settings.
2. Navigate to **Secrets** tab.
3. Add a new secret named `BLABLADOR_API_KEY`.
4. Paste your actual API key value.

> 🔐 Never hardcode secrets in source code. Always use environment variables via Hugging Face Secrets.

---

## 🌐 API Endpoints Overview

| Method | Path         | Description |
|--------|--------------|-------------|
| GET    | `/health`    | Liveness probe to confirm backend is running |
| POST   | `/configure` | Dynamically update AI configuration (model, endpoint) |
| POST   | `/generate`  | Trigger AI inference using configured settings |

---

## 🧠 AI Configuration Logic

### `/configure` Payload Example:
```json
{
  "model": "small",
  "endpoint": "https://api.helmholtz-blablador.fz-juelich.de/v1"
}
```

> 💡 This endpoint allows runtime modification of AI parameters without restarting the service.

### `/generate` Payload Example:
```json
{
  "prompt": "Explain quantum computing simply."
}
```

> 🔄 The generated response comes directly from the Helmholtz-Blabladot API using current configuration.

---

## 📜 Logging Strategy

All logs will be written to standard output (`stdout`) which is automatically captured by Hugging Face Spaces.

### Key Log Events:
- **Startup Check**: If `BLABLADOR_API_KEY` is missing, log an error:
  ```log
  ERROR: Missing BLABLADOR_API_KEY. Please set it in Space Secrets.
  ```

- **Inference Activity**: Log each `/generate` request with basic metadata:
  ```log
  INFO: Generating text with model 'small' at endpoint 'https://api.helmholtz-blablador.fz-juelich.de/v1'
  ```

> 📊 Use Hugging Face Logs viewer to monitor activity and troubleshoot issues.

---

## 🧪 Testing Instructions

### Local Testing Steps:
1. Start the FastAPI server locally:
   ```bash
   uvicorn main:app --reload
   ```
2. Test endpoints using tools like Postman or curl:
   - Health check:
     ```bash
     curl http://localhost:8000/health
     ```
   - Configure AI settings:
     ```bash
     curl -X POST http://localhost:8000/configure \
          -H "Content-Type: application/json" \
          -d '{"model":"small","endpoint":"https://api.helmholtz-blablador.fz-juelich.de/v1"}'
     ```
   - Generate content:
     ```bash
     curl -X POST http://localhost:8000/generate \
          -H "Content-Type: application/json" \
          -d '{"prompt":"Hello, how are you?"}'
     ```

### Expected Responses:
- `/health`: `{"status": "OK"}`
- `/configure`: `{"status": "updated"}`
- `/generate`: `{"result": "<AI-generated-text>"}`

> 🧪 Ensure that both `/configure` and `/generate` work correctly after setting up the