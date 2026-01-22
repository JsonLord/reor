Working behaviour and prompt context for Jules. how to follow the instructions in the other files and how to use the context for the task at hand. 
Add: to never delete a hf_upload.py file once created. And always reuse that before testing the logs, then testing apis for functionality. Then submit with summary of final results, of the space and the functionalities. 

Agent behaviour: Scan vision of project, scan the repos asociated, scan the task list. Build component by component. Test components. Identify where components interact. Test the internal interaction. Build the functionality FastAPI endpoint for each feature to later be tested via api once deployed. Then test the overall app from start to finish. Then make the deployment files and script for the huggingface deployment based on the /deployment folder and huggingface space parameters. Then expose the FASTAPis in the way it is recommended. Gradio=gradio endpoints. Docker= space url endpoints /health etc. Then deploy. Then check the build logs, then the run logs. Fix failures until successfully running. Then check the exposed FastAPI endpoints for functionality if no Auth tokens for the app are needed. If they are needed. Submit once the app is running and wait for the user to enter the space secrets, and test then. 


## important!
The current codebase you are working in is to be adapted following the vision of the project transformation in the /jules folder. The current application should be kept and only slightly changed, improved, expanded by the features described in /jules folder. The tasks files give a starting point, but judge for yourself. Develop tests to run to first see the current application feature, how it is working and make a plan to implement the features requested in /jules folder to develop the current application inside the repo towards the vision described to achieve expansion of the current app with functionalities described in the /jules folder. Adapt your coding implemententation to the coding language used by the project, and try to go with that. Test the full app within this working space. 

See what huggingface sdk from gradio over streamlit to docker fits best and use that, configure the README.md file accordingly and prepare to upload the file app, not just the new features, but the full app expanded with these new features, to the huggingface space. Monitor deployment and once it is running, test the api endpoints you had set to see the functionality of the app inside that huggingface space.

## Project Specific Instructions
# AGENTS.md

This document outlines specific instructions for deploying and managing the **HarvestHealth Magnetic UI** Hugging Face Space project, which integrates a Gradio-based frontend with an external OpenAI-compatible LLM endpoint (`helmholtz-blablador.fz-juelich.de/v1`). It also defines how agents (both human and automated) can interact with and manage the application during development, testing, and production phases.

---

## 🧠 Overview

The **HarvestHealth Magnetic UI** is a containerized web application hosted on [Hugging Face Spaces](https://huggingface.co/spaces), designed to provide both a user-friendly interface (via Gradio) and a programmable backend (via FastAPI + Reverse Proxy). The application communicates with an external LLM via a secure API key, exposing both its UI and backend APIs over HTTPS.

---

## 🔧 Deployment Instructions

### 1. Environment Setup

Ensure the following environment variables are set in your Hugging Face Space settings:

| Variable Name         | Description                                  |
|-----------------------|----------------------------------------------|
| `BLABLADOR_API_KEY`   | Secure API key for accessing `helmholtz-blablador.fz-juelich.de/v1` |

> ⚠️ Never hardcode secrets in code or commit them to version control.

### 2. Docker Image Build Process

Use the provided `Dockerfile` to build and deploy your image:

```bash
docker build -t harvesthealth/magnetic-ui .
```

> This image includes:
> - Gradio for the frontend UI
> - FastAPI for backend proxying
> - Nginx for reverse proxying external traffic
> - All necessary dependencies and startup scripts

### 3. Running Locally (for Testing)

To test locally before deployment:

```bash
docker-compose up
```

Access:
- Gradio UI: [http://localhost:7860](http://localhost:7860)
- API Endpoints: [http://localhost:7860/api](http://localhost:7860/api)

Ensure all services start successfully and logs do not show errors related to missing keys or failed connections.

---

## 🛠️ Components & Interaction Flow

| Component              | Role                                                                 |
|------------------------|----------------------------------------------------------------------|
| **Gradio UI**          | Serves the frontend interface on port 7860                           |
| **FastAPI Proxy**      | Handles internal and external API requests to LLM endpoint           |
| **Reverse Proxy (Nginx/Caddy)** | Routes traffic from `https://harvesthealth-magnetic-ui.hf.space` to internal services |
| **Environment Manager** | Loads and validates `BLABLADOR_API_KEY`                              |

### ✅ Interaction Flow

1. User interacts with Gradio UI → Sends HTTP POST to `/api/llm`
2. FastAPI receives request → Injects `Authorization: Bearer <KEY>` into headers
3. FastAPI forwards request to `https://api.helmholtz-blablador.fz-juelich.de/v1`
4. LLM returns response → FastAPI sends it back to Gradio or external client
5. External clients access `/api/llm`, `/api/health`, etc., via `https://harvesthealth-magnetic-ui.hf.space/api`

---

## 🧪 Testing Guidelines

Each component should be tested independently and together in full pipeline scenarios.

### 1. Gradio UI Component

- **Test:** Load page at `https://harvesthealth-magnetic-ui.hf.space`
- **Success:** UI renders properly, chat box is visible, submit button works

- **Test:** Submit sample prompt
  ```json
  {
    "messages": [
      {"role": "user", "content": "What is quantum computing?"}
    ],
    "model": "alias-large"
  }
  ```
- **Success:** Streaming or final response appears in chat window

### 2. FastAPI Proxy Component

- **Test:** Send POST to `/api/llm` with valid payload
- **Success:** Returns 200 OK with valid JSON from LLM

- **Test:** Send invalid request (malformed JSON or missing fields)
- **Success:** Returns 400 Bad Request with clear error message

### 3. Environment Manager

- **Test:** Deploy without setting `BLABLADOR_API_KEY`
- **Success:** Application fails gracefully or logs error

- **Test:** Deploy with correct key
- **Success:** LLM calls succeed, no exposure in logs or responses

### 4. Docker Container Layer

- **Test:** Run `docker-compose up`
- **Success:** All containers start without crash; ports open

- **Test:** Check logs for startup confirmation
- **Success:** Logs indicate successful initialization of:
  - Gradio (port 7860)
  - FastAPI (