# Studlyf 

An AI-driven intelligence layer for startup founders that evaluates venture viability, generates execution roadmaps, and maps ecosystem graphs.

## 🛠️ Project Architecture
This project uses a decoupled micro-architecture designed for performance and reliability:
* **Backend:** FastAPI (Python) – Handles API routing, structured JSON synthesis, and Gemini 2.5 Flash integration.
* **Frontend:** Vanilla HTML/JS – State-managed SPA utilizing Chart.js for data visualization.
* **Dependencies:** Managed via `requirements.txt`.

## 🚀 Quick-Start Guide

### 1. Installation
Open your terminal in the project root directory and install the necessary dependencies:
```bash
  pip install -r requirements.txt

### 2. Configure Environment Variables
This application requires a Google Gemini API Key. You must set this in your terminal session before starting the backend:
Mac / Linux:
export GEMINI_API_KEY="your_actual_api_key_here"
Windows (PowerShell):
$env:GEMINI_API_KEY="your_actual_api_key_here"

###3. Launch the System
Start the Backend Server: in terminal type 
uvicorn main:app --reload


Access the Interface:
Once the server indicates it is running (usually on http://127.0.0.1:8000), open dashboard.html in your web browser.
 Troubleshooting & Notes
CORS Compliance: Always ensure the uvicorn backend is fully active before opening dashboard.html to allow the frontend to communicate with the API.
Dependencies: If the server fails to initialize, re-run pip install -r requirements.txt to ensure your environment is synchronized.
API Limits: If the intelligence layer fails to generate a response, verify your API key balance and ensure your terminal has the environment variable exported correctly.
