import json
import os
import urllib.request
import urllib.error
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from copilot import run_studlyf_copilot

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------
# FEATURE 9: CHAT COPILOT
# ----------------------------------------------------
class UserRequest(BaseModel):
    question: str

@app.post("/api/chat")
def chat_with_copilot(request: UserRequest):
    return json.loads(run_studlyf_copilot(request.question))

# ----------------------------------------------------
# FEATURE 11 & 12: FOUNDER & STARTUP PROFILE
# ----------------------------------------------------
@app.get("/api/profile")
def get_founder_profile():
    return {
        "founder_name": "Santhosh",
        "startup_status": "Idea Stage",
        "progress_metrics": {"roadmap_completion": "25%", "validation_reports": 1, "funding_applications": 0},
        "history": ["How to get first 100 users?", "Startup India Seed Fund info"]
    }

# ----------------------------------------------------
# FEATURE 10: STARTUP RESOURCES LIBRARY (Complete CMS)
# ----------------------------------------------------
RESOURCES_DB = {
    "interview-script": {
        "title": "Customer Interview Script Template",
        "type": "Guide",
        "content": "1. Introduction (2 mins)\n2. Uncover the Problem (10 mins): 'Tell me about the last time you tried to [solve problem]?'\n3. Evaluate Current Solutions (5 mins): 'What are you currently using?'\n4. Closing (3 mins): 'Who else should I talk to?'"
    },
    "problem-framing": {
        "title": "Problem Framing Guide",
        "type": "Framework",
        "content": "Use the 'How Might We' framework:\n\n1. Who is the user?\n2. What is the specific bottleneck?\n3. What is the emotional toll of this problem?\n\nDraft: 'How might we help [User] overcome [Bottleneck] so they can avoid [Emotional Toll]?'"
    },
    "persona-canvas": {
        "title": "Customer Persona Canvas",
        "type": "Template",
        "content": "Profile Name: \nAge/Demographics: \nJob Title: \n\nGoals:\n1.\n2.\n\nFrustrations/Pain Points:\n1.\n2.\n\nWhere they hang out online: "
    },
    "mvp-scope": {
        "title": "MVP Scope Template",
        "type": "Template",
        "content": "Core Value Proposition:\n\nMust-Have Features (Limit to 3):\n1.\n2.\n3.\n\nOut of Scope (Do Not Build Yet):\n- \n- "
    },
    "stack-decision": {
        "title": "Tech Stack Decision Tree",
        "type": "Guide",
        "content": "1. Need complex custom logic? -> React + Python/Node.js\n2. Marketplace / Directory? -> Webflow + Memberstack or Bubble\n3. Mobile-first requirement? -> Flutter or React Native\n4. Internal admin tool? -> Retool"
    },
    "ux-wireframes": {
        "title": "UX Flow Wireframes",
        "type": "Guide",
        "content": "Keep it to 4 core screens:\n1. Landing Page / Authentication\n2. The Core Action (e.g., uploading a file, searching a database)\n3. The Result / Output\n4. User Settings / Billing"
    },
    "tracking-setup": {
        "title": "Analytics Tracking Setup",
        "type": "Guide",
        "content": "KPIs to track on Day 1:\n1. Pageviews (Google Analytics / Plausible)\n2. Sign-up conversion rate\n3. Primary Action completion rate (Mixpanel / PostHog)"
    },
    "beta-script": {
        "title": "Beta Outreach Script",
        "type": "Template",
        "content": "Subject: Quick question about [Problem]\n\nHi [Name],\n\nI noticed you work in [Industry]. I've been researching [Problem] and just built a rough prototype to solve it.\n\nWould you be open to clicking around it for 5 minutes? No sales pitch, just looking for brutal feedback from experts like you.\n\nThanks,\n[Your Name]"
    }
}

@app.get("/api/resources/{resource_id}")
def get_resource(resource_id: str):
    return RESOURCES_DB.get(resource_id, {"error": "Resource not found"})

# ----------------------------------------------------
# FEATURE 2: FOUNDER ROADMAP (Complete 8-Week Plan)
# ----------------------------------------------------
# ----------------------------------------------------
# FEATURE 2: FOUNDER ROADMAP (Fully Mapped to PRD)
# ----------------------------------------------------
ROADMAP_DATA = {
    "Idea Stage": [
        {"week": 1, "task": "Conduct 20 customer interviews", "resource_name": "Interview Script Template", "resource_link": "resource.html?id=interview-script"},
        {"week": 2, "task": "Define the core problem statement", "resource_name": "Problem Framing Guide", "resource_link": "resource.html?id=problem-framing"},
        {"week": 3, "task": "Identify primary customer persona", "resource_name": "Persona Canvas", "resource_link": "resource.html?id=persona-canvas"},
        {"week": 4, "task": "Create MVP scope document", "resource_name": "MVP Scope Template", "resource_link": "resource.html?id=mvp-scope"}
    ],
    "Validation": [
        {"week": 1, "task": "Launch landing page & collect waitlist", "resource_name": "UX Flow Wireframes", "resource_link": "resource.html?id=ux-wireframes"},
        {"week": 2, "task": "Validate pricing with 5 potential buyers", "resource_name": "Interview Script Template", "resource_link": "resource.html?id=interview-script"}
    ],
    "MVP": [
        {"week": 1, "task": "Select tech stack or no-code tools", "resource_name": "Stack Decision Tree", "resource_link": "resource.html?id=stack-decision"},
        {"week": 2, "task": "Build core user journey", "resource_name": "UX Flow Wireframes", "resource_link": "resource.html?id=ux-wireframes"},
        {"week": 3, "task": "Integrate analytics tracking", "resource_name": "Tracking Setup Guide", "resource_link": "resource.html?id=tracking-setup"},
        {"week": 4, "task": "Launch to 10 beta testers", "resource_name": "Beta Outreach Script", "resource_link": "resource.html?id=beta-script"}
    ],
    "Revenue": [
        {"week": 1, "task": "Set up payment gateway tracking", "resource_name": "Tracking Setup Guide", "resource_link": "resource.html?id=tracking-setup"},
        {"week": 2, "task": "Convert beta testers to paid users", "resource_name": "Beta Outreach Script", "resource_link": "resource.html?id=beta-script"}
    ],
    "Fundraising": [
        {"week": 1, "task": "Finalize Cap Table & Legal Docs", "resource_name": "Problem Framing Guide", "resource_link": "resource.html?id=problem-framing"},
        {"week": 2, "task": "Begin warm outreach to investors", "resource_name": "Beta Outreach Script", "resource_link": "resource.html?id=beta-script"}
    ]
}

@app.get("/api/roadmap/{stage}")
def get_roadmap(stage: str):
    return {"stage": stage, "tasks": ROADMAP_DATA.get(stage, [])}

# ----------------------------------------------------
# FEATURE 4: FUNDING DATABASE (Complete List)
# ----------------------------------------------------
FUNDING_OPPORTUNITIES = [
    {
        "id": 1, "name": "Startup India Seed Fund Scheme", "stage": "Idea Stage", "sector": "Tech", "deadline": "Rolling",
        "equity_terms": "Convertible Debenture", "application_link": "https://seedfund.startupindia.gov.in/",
        "status": "Not Applied", "eligibility_breakdown": ["Must be DPIIT recognized", "Not received > 10L support", "Innovative startup"]
    },
    {
        "id": 2, "name": "Women Entrepreneur Grant", "stage": "MVP", "sector": "General", "deadline": "2026-12-31",
        "equity_terms": "Non-dilutive Grant", "application_link": "https://example-grant.com",
        "status": "Not Applied", "eligibility_breakdown": ["Founder must be woman", "Proof of concept ready"]
    },
    {
        "id": 3, "name": "DeepTech Innovation Scheme", "stage": "MVP", "sector": "Tech", "deadline": "2026-09-15",
        "equity_terms": "Equity-free Grant", "application_link": "https://example-deeptech.com",
        "status": "Not Applied", "eligibility_breakdown": ["Patent pending or filed", "Hardware or heavy-tech software"]
    }
]

@app.get("/api/funding")
def get_funding(sector: str = None, stage: str = None):
    results = FUNDING_OPPORTUNITIES
    if sector: results = [f for f in results if f["sector"] == sector]
    if stage: results = [f for f in results if f["stage"] == stage]
    return {"opportunities": results}

# ----------------------------------------------------
# FEATURE 3: AI BUILD ADVISOR (Complete Logic)
# ----------------------------------------------------
class BuildAdvisorRequest(BaseModel):
    startup_type: str

@app.post("/api/build-advisor")
def get_build_plan(data: BuildAdvisorRequest):
    BUILD_TEMPLATES = {
        "SaaS": {
            "stack": {"frontend": "React / Next.js", "backend": "FastAPI (Python)", "db": "PostgreSQL"}, 
            "cost": "$22/month base infrastructure"
        },
        "AI Startup": {
            "stack": {"frontend": "Next.js Tailwind", "backend": "FastAPI", "db": "Supabase (pgvector)"}, 
            "cost": "$45/month with vector optimization"
        },
        "Marketplace": {
            "stack": {"frontend": "Next.js Mobile-Optimized", "backend": "Node.js or FastAPI", "db": "PostgreSQL"}, 
            "cost": "$27/month with high-availability routing"
        }
    }
    return BUILD_TEMPLATES.get(data.startup_type, BUILD_TEMPLATES["SaaS"])

# ----------------------------------------------------
# FEATURE 1: STARTUP VALIDATION (Bug-Free Version)
# ----------------------------------------------------
class StartupIdea(BaseModel):
    idea: str; problem: str; segment: str; geo: str

@app.post("/api/validate")
def validate_startup(data: StartupIdea):
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key: 
            return {"error": "API Key missing."}
            
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
        
        # STRICT PROMPT FOR VISUAL UI PARSING
        prompt = f"""
        Act as an elite venture capital analyst evaluating this startup:
        Idea: {data.idea} | Problem: {data.problem} | Target: {data.segment} | Geo: {data.geo}
        
        Return EXACTLY this JSON structure, no markdown formatting, no backticks:
        {{
            "overall_score": 85,
            "validation_score": {{ "demand": 80, "competition": 60, "scalability": 90, "revenue": 75 }},
            "market_research": "A 3-sentence deep dive into market dynamics.",
            "competitors": [
                {{"name": "Competitor 1", "weakness": "Their specific flaw"}},
                {{"name": "Competitor 2", "weakness": "Their specific flaw"}}
            ]
        }}
        """
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
        
        with urllib.request.urlopen(req) as response:
            text_content = json.loads(response.read().decode('utf-8'))["candidates"][0]["content"]["parts"][0]["text"]
            
        clean_json = text_content.replace('```json', '').replace('```', '').strip()
        return json.loads(clean_json)
        
    except Exception as e:
        return {"error": "Data generation failed. Ensure API key is valid."}
# FEATURE 5, 6, & 7: NETWORK MODULE
# ----------------------------------------------------
class NetworkRequest(BaseModel):
    idea: str
    stage: str

@app.post("/api/network")
def scan_network(data: NetworkRequest):
    import urllib.request
    import urllib.error
    import json
    import os
    
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key: 
            return {"error": "API Key missing in terminal."}
            
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
        
        # Single-line prompt to prevent string literal errors
        prompt = f"Act as an elite startup ecosystem matchmaker for a {data.stage} startup building: '{data.idea}'. Return EXACTLY this JSON structure: {{\"investors\": [{{\"name\": \"Fund Name\", \"focus\": \"Sector\", \"ticket_size\": \"$X - $Y\"}}], \"mentors\": [{{\"name\": \"Mentor Role\", \"expertise\": \"Domain\"}}], \"outreach_strategy\": \"A 3-step actionable plan for cold outreach.\"}}"
        
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
        
        with urllib.request.urlopen(req) as response:
            text_content = json.loads(response.read().decode('utf-8'))["candidates"][0]["content"]["parts"][0]["text"]
            
        clean_json = text_content.replace('```json', '').replace('```', '').strip()
        return json.loads(clean_json)
        
    except urllib.error.HTTPError as e:
        if e.code == 429:
            return {"error": "⚠️ API Rate Limit Exceeded. Please wait 60 seconds."}
        return {"error": f"Network Error: HTTP {e.code}"}
    except Exception as e:
        return {"error": "Ecosystem scan failed. Please try again."}
# ----------------------------------------------------
# FEATURE 8: GO-TO-MARKET ASSET BUILDER
# ----------------------------------------------------
class GTMRequest(BaseModel):
    product_name: str
    target_audience: str
    core_benefit: str

@app.post("/api/gtm")
def build_gtm_assets(data: GTMRequest):
    import urllib.request
    import urllib.error
    import json
    import os
    
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key: 
            return {"error": "API Key missing in terminal."}
            
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
        
        prompt = f"Act as a viral tech marketing expert. Product: {data.product_name}. Audience: {data.target_audience}. Benefit: {data.core_benefit}. Return EXACTLY this JSON structure: {{\"tagline\": \"A punchy 5-word hook\", \"linkedin_post\": \"A highly engaging, formatting-rich LinkedIn launch post without hashtags\", \"launch_channels\": [\"Channel 1\", \"Channel 2\", \"Channel 3\"]}}"
        
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
        
        with urllib.request.urlopen(req) as response:
            text_content = json.loads(response.read().decode('utf-8'))["candidates"][0]["content"]["parts"][0]["text"]
            
        clean_json = text_content.replace('```json', '').replace('```', '').strip()
        return json.loads(clean_json)
        
    except urllib.error.HTTPError as e:
        if e.code == 429:
            return {"error": "⚠️ API Rate Limit Exceeded. Please wait 60 seconds."}
        return {"error": f"Network Error: HTTP {e.code}"}
    except Exception as e:
        return {"error": "Asset generation failed."}
