Working behaviour and prompt context for Jules. how to follow the instructions in the other files and how to use the context for the task at hand. 
Add: to never delete a hf_upload.py file once created. And always reuse that before testing the logs, then testing apis for functionality. Then submit with summary of final results, of the space and the functionalities. 

Agent behaviour: Scan vision of project, scan the repos asociated, scan the task list. Build component by component. Test components. Identify where components interact. Test the internal interaction. Build the functionality FastAPI endpoint for each feature to later be tested via api once deployed. Then test the overall app from start to finish. Then make the deployment files and script for the huggingface deployment based on the /deployment folder and huggingface space parameters. Then expose the FASTAPis in the way it is recommended. Gradio=gradio endpoints. Docker= space url endpoints /health etc. Then deploy. Then check the build logs, then the run logs. Fix failures until successfully running. Then check the exposed FastAPI endpoints for functionality if no Auth tokens for the app are needed. If they are needed. Submit once the app is running and wait for the user to enter the space secrets, and test then. 


## important!
The current codebase you are working in is to be adapted following the vision of the project transformation in the /jules folder. The current application should be kept and only slightly changed, improved, expanded by the features described in /jules folder. The tasks files give a starting point, but judge for yourself. Develop tests to run to first see the current application feature, how it is working and make a plan to implement the features requested in /jules folder to develop the current application inside the repo towards the vision described to achieve expansion of the current app with functionalities described in the /jules folder. Adapt your coding implemententation to the coding language used by the project, and try to go with that. Test the full app within this working space. 

See what huggingface sdk from gradio over streamlit to docker fits best and use that, configure the README.md file accordingly and prepare to upload the file app, not just the new features, but the full app expanded with these new features, to the huggingface space. Monitor deployment and once it is running, test the api endpoints you had set to see the functionality of the app inside that huggingface space.

## Project Specific Instructions
Here’s a structured **`AGENTS.md`** file tailored to your project, including specific instructions for agents (e.g., CI/CD pipelines, deployment scripts, or monitoring bots) to automate tasks while respecting your context:

---

# **AGENTS.md**
*Automation Guidelines for Helmholtz BLABLADOR + Gradio Integration*

---

## **1. Agent Roles & Responsibilities**
Agents in this project must:
1. **Replace OpenAI API calls** with Helmholtz BLABLADOR API (`/v1/completions`).
2. **Securely handle credentials** via Hugging Face Secrets/Environment Variables.
3. **Deploy to Hugging Face Spaces** with reverse proxy support for `/api/*` endpoints.
4. **Validate and log** API responses, errors, and performance metrics.

| **Agent Type**       | **Purpose**                                                                 | **Key Tasks**                                                                 |
|----------------------|-----------------------------------------------------------------------------|--------------------------------------------------------------------------------|
| **API-Adapter Agent** | Replaces OpenAI calls with BLABLADOR API logic.                            | Audit `reor.git`, replace API calls, mock BLABLADOR locally.                   |
| **Gradio Config Agent** | Adapts Gradio for Hugging Face Spaces (Docker, env vars).                   | Update `app.py`, `Dockerfile`, test with `BLABLADOR_API_KEY`.                |
| **Deployment Agent**  | Deploys to Hugging Face Spaces with reverse proxy for APIs.               | Expose port `7860`, configure `/api/*` forwarding, set up CI/CD.              |
| **Security Agent**    | Validates API keys, rate-limits endpoints, ensures HTTPS.                   | Add auth middleware, log failures, enforce rate limits.                       |
| **Monitoring Agent**  | Logs API usage, errors, and performance metrics.                           | Integrate with Hugging Face Datasets or Prometheus for analytics.             |

---

## **2. Agent-Specific Instructions**

### **A. API-Adapter Agent**
**Goal**: Replace OpenAI API calls with Helmholtz BLABLADOR API.

#### **Steps**:
1. **Audit `reor.git`**:
   - Search for `openai.Completion.create` or API keys hardcoded in the repo.
   - Example:
     ```python
     # BEFORE:
     response = openai.Completion.create(
         engine="text-davinci-003",
         prompt="Hello",
         max_tokens=50
     )

     # AFTER:
     import os
     import requests

     headers = {"Authorization": f"Bearer {os.environ['BLABLADOR_API_KEY']}"}
     response = requests.post(
         "https://api.helmholtz-blablador.fz-juelich.de/v1/completions",
         json={
             "prompt": "Hello",
             "max_tokens": 50,
             "model": "large"  # Required BLABLADOR alias
         },
         headers=headers
     ).json()
     ```

2. **Validate BLABLADOR API Key**:
   - Add a helper function to check `BLABLADOR_API_KEY`:
     ```python
     def validate_blablador_key():
         if not os.environ.get("BLABLADOR_API_KEY"):
             raise ValueError("BLABLADOR_API_KEY not set in environment variables.")
     ```

3. **Mock BLABLADOR API Locally**:
   - Use `responses` library to simulate API responses during testing:
     ```python
     import responses

     @responses.activate
     def test_blablador_logic():
         responses.add(
             responses.POST,
             "https://api.helmholtz-blablador.fz-juelich.de/v1/completions",
             json={"choices": [{"text": "Mock response"}]}
         )
         # Test your logic here...
     ```

---

### **B. Gradio Config Agent**
**Goal**: Adapt Gradio for Hugging Face Spaces (Docker, env vars).

#### **Steps**:
1. **Load `BLABLADOR_API_KEY` from Env Vars**:
   - Update `app.py` to fetch the key:
     ```python
     BLABLADOR_API_KEY = os.environ.get("BLABLADOR_API_KEY")
     if not BLABLADOR_API_KEY:
         raise EnvironmentError("BLABLADOR_API_KEY is required!")
     ```

2. **Test Locally**:
   - Set the key temporarily:
     ```bash
     export BLABLADOR_API_KEY="your_key_here"
     python app.py
     ```
   - Verify the Gradio UI loads without errors.

3. **Update `requirements.txt`**:
   - Add dependencies (if needed):
     ```
