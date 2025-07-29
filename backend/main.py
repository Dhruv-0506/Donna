# backend/main.py

import requests
import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import datetime

# --- Configuration Constants (No change) ---
# ... (all your constants like API_KEY, etc., remain here) ...

# --- Donna Prompt (No change) ---
# ... (your full prompt template remains here) ...

# ====================================================================
# === KEY CHANGE HERE: CONFIGURE FLASK FOR YOUR FILE STRUCTURE ===
#
# Tell Flask that the template folder (for index.html) and the static folder
# (for style.css, script.js) are one level UP ('../') from this file's location.
app = Flask(__name__, template_folder='../', static_folder='../')
# ====================================================================

CORS(app)

# === NEW ROUTE TO SERVE THE FRONTEND UI ===
@app.route('/')
def serve_frontend():
    """Serves the main index.html file from the root folder."""
    return render_template('index.html')

# === EXISTING ROUTE FOR THE API ===
@app.route('/research', methods=['POST'])
def generate_dossier():
    # ... (This entire function remains exactly the same) ...
    pass

# ... (The rest of your code, including function definitions and the __main__ block, remains the same) ...

# --- For clarity, including the full file content below ---

API_KEY = "sIuhGRaC8JlSkdLkNzB9gZZAfVNsVXUN"
EXTERNAL_USER_ID = "665e32c0516a19e2faddef17"
BASE_URL = "https://api.on-demand.io/chat/v1"
RESPONSE_MODE = "sync" 
AGENT_IDS = [
    "agent-1712327325", "agent-1713924030", "agent-1713962163", 
    "agent-1716164040", "agent-1722260873", "agent-1746427905", 
    "agent-1747218812", "agent-1750747741"
]
ENDPOINT_ID = "predefined-openai-gpt4.1-nano"
REASONING_MODE = "deepturbo"
TEMPERATURE = 0.7
MAX_TOKENS = 10000

DONNA_PROMPT_TEMPLATE = """
🧠 YOUR ROLE...
... [The entire prompt text remains here] ...
"""

@app.route('/research', methods=['POST'])
def generate_dossier():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON input"}), 400

    today_date = datetime.date.today().strftime("%B %d, %Y")
    
    try:
        final_prompt = DONNA_PROMPT_TEMPLATE.format(
            rep_name=data.get('name', 'N/A'),
            rep_linkedin=data.get('linkedinUrl', 'N/A'),
            rep_company_url=data.get('repCompanyUrl', 'N/A'),
            rep_products_services=data.get('productsServices', 'N/A'),
            rep_territories=data.get('territories', 'N/A'),
            rep_pitch=data.get('pitch', 'N/A'),
            target_company_url=data.get('targetCompanyUrl', 'N/A'),
            solutions_to_position=data.get('solutions', 'N/A'),
            opportunity_name=data.get('opportunityName', 'N/A'),
            today_date=today_date
        )
    except KeyError as e:
        return jsonify({"error": f"Missing required field in request: {e}"}), 400

    session_id = create_chat_session()
    if not session_id:
        return jsonify({"dossier": "Error: Could not initialize a session with the AI service."}), 500

    dossier_content = submit_dossier_request(session_id, final_prompt)
    if not dossier_content:
        return jsonify({"dossier": "Error: Received no content from the AI service."}), 500
    
    return jsonify({"dossier": dossier_content})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

def create_chat_session():
    url = f"{BASE_URL}/sessions"
    body = { "agentIds": AGENT_IDS, "externalUserId": EXTERNAL_USER_ID }
    headers = {"apikey": API_KEY, "Content-Type": "application/json"}
    try:
        res = requests.post(url, headers=headers, json=body, timeout=10)
        res.raise_for_status()
        data = res.json()
        session_id = data.get("data", {}).get("id")
        if session_id:
            print(f"Chat session created: {session_id}")
            return session_id
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error creating chat session: {e}")
        return None

def submit_dossier_request(session_id, prompt):
    url = f"{BASE_URL}/sessions/{session_id}/query"
    body = {
        "endpointId": ENDPOINT_ID,
        "query": prompt,
        "agentIds": AGENT_IDS,
        "responseMode": RESPONSE_MODE,
        "reasoningMode": REASONING_MODE,
        "modelConfigs": { "temperature": TEMPERATURE, "maxTokens": MAX_TOKENS },
    }
    headers = {"apikey": API_KEY, "Content-Type": "application/json"}
    try:
        res = requests.post(url, headers=headers, json=body, timeout=300)
        res.raise_for_status()
        response_data = res.json()
        return response_data.get("data", {}).get("answer")
    except requests.exceptions.RequestException as e:
        print(f"Error submitting dossier request: {e}")
        return "An error occurred while communicating with the AI. The request may have timed out or failed."
