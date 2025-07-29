# backend/main.py

import requests
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime

# --- Configuration Constants ---
# NOTE: For production, it's highly recommended to move the API_KEY 
# to an environment variable instead of hardcoding it.
API_KEY = "sIuhGRaC8JlSkdLkNzB9gZZAfVNsVXUN"
EXTERNAL_USER_ID = "665e32c0516a19e2faddef17"
BASE_URL = "https://api.on-demand.io/chat/v1"
RESPONSE_MODE = "sync" 

# --- New Agent IDs as per your request ---
AGENT_IDS = [
    "agent-1712327325", "agent-1713924030", "agent-1713962163", 
    "agent-1716164040", "agent-1722260873", "agent-1746427905", 
    "agent-1747218812", "agent-1750747741"
]

ENDPOINT_ID = "predefined-openai-gpt4.1"
REASONING_MODE = "sota"
TEMPERATURE = 0.7
MAX_TOKENS = 10000 # Increased for potentially long dossier output

# --- The "Donna" Master Prompt ---
# This f-string will be populated with data from the frontend.
DONNA_PROMPT_TEMPLATE = """
🧠 YOUR ROLE
You are The Donna — an elite AI sales consigliere. Your mission is to generate a comprehensive intelligence dossier based on the target company, the solutions being positioned, and the rep's pre-defined sales territory. Your output must be deeply territory-specific, solution-aligned, and strategically actionable — designed to support deal execution, CRM updates, and sales planning at an elite level.

🔁 INPUT FORMAT
The rep has already provided the following during setup:
Name: {rep_name}
LinkedIn URL: {rep_linkedin}
Company URL: {rep_company_url}
Products/Services sold: {rep_products_services}
Territories covered: {rep_territories}
A free-text positioning pitch (their elevator pitch on steroids): {rep_pitch}

You will now receive only the opportunity-specific inputs:
Company URL: {target_company_url}
Solutions to Position: {solutions_to_position}
Opportunity Name: {opportunity_name}

📌 GUIDING PRINCIPLES
The Territory must always reflect the region pre-defined by the rep (e.g., Canada, UAE, France, APAC, etc.)
All regulatory, financial, organizational, and personal insights should be localized to this territory
All content must align to the positioned solutions — surfacing relevance, urgency, compliance gaps, or tech/strategic fit
Every paragraph must be sales-relevant, detailed (150–200 words minimum), and fact-driven
Cite sources wherever possible (e.g., LinkedIn, Crunchbase, SEDAR, regional news, financial filings)

📋 INTELLIGENCE DOSSIER STRUCTURE
1. EXECUTIVE SUMMARY
Company: [Target Company Name]
Territory: {rep_territories}
Opportunity: {opportunity_name}
Sales Rep: {rep_name}
Date Created: {today_date}
Last Updated: {today_date}

2. COMPANY PROFILE
2.1 BASIC COMPANY INFORMATION
Full Legal Name
Industry/Industries
Founded
Global HQ Location & Regional HQ Location
Website
LinkedIn Page
Stock Symbol (if applicable)
Legal Structure
Business Model
Include regional subsidiary information (based on rep's territory)
Indicate whether decisions are centralized (HQ) or localized

2.2 MARKET INTELLIGENCE
Four detailed paragraphs (150–200 words each) localized to the rep's territory:
1. REGULATORY LANDSCAPE
2. FINANCIAL & MARKET CONDITIONS
3. INDUSTRY DYNAMICS
4. MARKET TIMING FACTORS

2.3 FIRMOGRAPHIC INTELLIGENCE
Four detailed paragraphs focused on operations in the rep's territory:
1. FINANCIAL PROFILE
2. ORGANIZATIONAL STRUCTURE
3. OPERATIONAL FOOTPRINT
4. STRATEGIC DIRECTION

2.4 TECHNOGRAPHIC PROFILE
Four paragraphs aligned to your solutions:
1. CORE INFRASTRUCTURE
2. DIGITAL MATURITY
3. VENDOR ECOSYSTEM
4. GAPS & OPPORTUNITIES

2.5 RECENT DEVELOPMENTS & NEWS
Four paragraphs focused on last 6–12 months:
1. STRATEGIC ANNOUNCEMENTS
2. OPERATIONAL DEVELOPMENTS
3. COMPETITIVE & MARKET POSITIONING
4. TIMING INDICATORS

2.6 STRATEGIC ASSESSMENT (SWOT)
Four structured paragraphs, focused on territorial market relevance:
Strengths, Weaknesses, Opportunities, Threats

2.7 ORGANIZATIONAL CHART
Comprehensive organizational structure gathered from online sources.

3. KEY PERSONNEL INTELLIGENCE
Generate 6 detailed paragraphs each for 2–3 territory-responsible decision-makers.

4. OPPORTUNITY ANALYSIS
4.1 OPPORTUNITY OVERVIEW
4.2 STRATEGIC FIT ANALYSIS (Five detailed paragraphs)
4.3 BUYING COMMITTEE (Map 4 stakeholder types)
4.4 COMPETITIVE INTELLIGENCE (Three detailed paragraphs)
4.5 TIMING ANALYSIS (Two detailed paragraphs)

5. ACTION INTELLIGENCE
5.1 RECOMMENDED NEXT STEPS (5 prioritized actions)
5.2 CONVERSATION STARTERS & RAPPORT (Per key contact)
5.3 OBJECTION HANDLING (For each common objection category)

6. INTELLIGENCE METADATA
6.1 SOURCE TRACKING
6.2 UPDATE TRACKING

🧠 OUTPUT REQUIREMENTS
Quality Standards: Minimum 150–200 words per paragraph, Territory-specific, Cite sources, Solution alignment, Confidence tagging, Actionable intelligence.
Formatting Requirements: Use consistent markdown formatting.
Content Depth: Detailed intelligence, specific examples, no generic statements.
"""

# --- API Helper Functions ---
def create_chat_session():
    """Creates a new, isolated chat session for a single dossier request."""
    url = f"{BASE_URL}/sessions"
    body = { "agentIds": AGENT_IDS, "externalUserId": EXTERNAL_USER_ID }
    headers = {"apikey": API_KEY, "Content-Type": "application/json"}
    try:
        res = requests.post(url, headers=headers, json=body, timeout=10)
        res.raise_for_status() # Raises an exception for bad status codes (4xx or 5xx)
        data = res.json()
        session_id = data.get("data", {}).get("id")
        if session_id:
            print(f"Chat session created: {session_id}")
            return session_id
        else:
            print(f"Error: 'data.id' not found in response. Full response: {res.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error creating chat session: {e}")
        return None

def submit_dossier_request(session_id, prompt):
    """Submits the fully constructed dossier prompt to the API."""
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
        print("Submitting dossier request to API...")
        res = requests.post(url, headers=headers, json=body, timeout=300) # 5-min timeout for long requests
        res.raise_for_status()
        response_data = res.json()
        # The API returns the dossier in the 'answer' field
        return response_data.get("data", {}).get("answer")
    except requests.exceptions.RequestException as e:
        print(f"Error submitting dossier request: {e}")
        return "An error occurred while communicating with the AI. The request may have timed out or failed."

# --- Flask Server Logic ---
app = Flask(__name__)
CORS(app) # Enable Cross-Origin Resource Sharing

@app.route('/research', methods=['POST'])
def generate_dossier():
    """Endpoint to receive frontend data and generate the intelligence dossier."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON input"}), 400

    # Format the current date
    today_date = datetime.date.today().strftime("%B %d, %Y")

    # Construct the final prompt using the template and frontend data
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

    # Each request gets a fresh session for clean context
    session_id = create_chat_session()
    if not session_id:
        return jsonify({"dossier": "Error: Could not initialize a session with the AI service."}), 500

    # Submit the request and get the dossier
    dossier_content = submit_dossier_request(session_id, final_prompt)
    if not dossier_content:
        return jsonify({"dossier": "Error: Received no content from the AI service."}), 500
    
    # Return the AI's response to the frontend
    return jsonify({"dossier": dossier_content})

if __name__ == '__main__':
    # The Dockerfile CMD will use gunicorn, so this part is mainly for local development
    if not API_KEY or API_KEY == "sIuhGRaC8JlSkdLkNzB9gZZAfVNsVXUN":
         print("API Key is set. Starting server...")
    else: 
        print("Please ensure API_KEY is set correctly.")
        exit(1)
        
    # Run on port 8080 to match the Dockerfile configuration
    app.run(host='0.0.0.0', port=8080, debug=True)
