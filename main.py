# main.py

import os
import requests
import json
import datetime
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from whitenoise import WhiteNoise

# --- Flask App Initialization (Final, Bulletproof Version) ---

# Get the absolute path of the directory where this file lives.
# Inside the Docker container, this will be '/app'.
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the absolute paths to the templates and static folders.
TEMPLATE_DIR = os.path.join(ROOT_DIR, 'templates')
STATIC_DIR = os.path.join(ROOT_DIR, 'static')

# Initialize Flask with these absolute paths.
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
CORS(app)
app.wsgi_app = WhiteNoise(app.wsgi_app)


# --- Configuration Constants (Final, Hardcoded Version) ---
API_KEY = "sIuhGRaC8JlSkdLkNzB9gZZAfVNsVXUN"
EXTERNAL_USER_ID = "665e32c0516a19e2faddef17"
BASE_URL = "https://api.on-demand.io/chat/v1"
RESPONSE_MODE = "sync"
AGENT_IDS = [
    "agent-1712327325", "agent-1713924030", "agent-1713962163",
    "agent-1716164040", "agent-1722260873", "agent-1746427905",
    "agent-1747218812", "agent-1750747741"
]
ENDPOINT_ID = "predefined-openai-gpt4o"
REASONING_MODE = "deepturbo"
TEMPERATURE = 0.7
MAX_TOKENS = 10000

# --- Load "Donna" Dossier Prompt from external file (Final, Bulletproof Version) ---
try:
    # Build the absolute path to the prompt file.
    prompt_file_path = os.path.join(ROOT_DIR, 'Prompt.txt')
    with open(prompt_file_path, 'r', encoding='utf-8') as file:
        DONNA_PROMPT_TEMPLATE = file.read()
except FileNotFoundError:
    print(f"FATAL ERROR: Prompt.txt not found at path: {prompt_file_path}. The application cannot start.")
    raise

# --- API Helper Functions (No Change) ---
def create_chat_session():
    url = f"{BASE_URL}/sessions"
    body = {"agentIds": AGENT_IDS, "externalUserId": EXTERNAL_USER_ID}
    headers = {"apikey": API_KEY, "Content-Type": "application/json"}
    try:
        res = requests.post(url, headers=headers, json=body, timeout=15)
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
        "modelConfigs": {"temperature": TEMPERATURE, "maxTokens": MAX_TOKENS},
    }
    headers = {"apikey": API_KEY, "Content-Type": "application/json"}
    try:
        res = requests.post(url, headers=headers, json=body, timeout=300)
        
        if res.status_code != 200:
            print(f"!!! CRITICAL API ERROR: Status Code {res.status_code}")
            print(f"!!! API RESPONSE: {res.text}")
            return f"The AI server returned an error. Status: {res.status_code}, Message: {res.text}"

        response_data = res.json()
        print("--> AI has responded successfully.")
        return response_data.get("data", {}).get("answer")
        
    except requests.exceptions.Timeout:
        return "An error occurred while communicating with the AI. The request timed out."
    except requests.exceptions.RequestException as e:
        return "A fatal network error occurred while communicating with the AI."

# --- Routes (No Change) ---
@app.route('/')
def serve_ui():
    return render_template('index.html')

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
        return jsonify({"dossier": "Error: Could not initialize a chat session with the AI service."}), 500

    dossier_content = submit_dossier_request(session_id, final_prompt)
    if not dossier_content:
        return jsonify({"dossier": "Error: Received no content from the AI service."}), 500
    
    if "The AI server returned an error" in dossier_content:
         return jsonify({"dossier": dossier_content}), 500

    return jsonify({"dossier": dossier_content})

# --- Main entry point (No Change) ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
