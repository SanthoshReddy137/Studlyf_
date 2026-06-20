import json
import os
from typing import List, Dict
from pydantic import BaseModel, Field
import google.generativeai as genai

class CopilotResponse(BaseModel):
    response_text: str = Field(description="The core markdown formatted answer for the founder screen.")
    is_verified: bool = Field(description="True only if data was pulled from Studlyf's internal database entries.")
    sources_used: List[str] = Field(description="Exact title of the verified database records used.")
    suggested_follow_ups: List[str] = Field(description="Exactly two relative follow-up questions.")

api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# CRITICAL FIX: Pure Python keyword matching instead of API-heavy embeddings to prevent Error 429
def find_verified_context(user_query: str) -> Dict:
    if not os.path.exists("database.json"): return {}
    try:
        with open("database.json", "r") as f: 
            database = json.load(f)
            
        query_words = set(user_query.lower().split())
        best_match, highest_score = {}, 0
        
        for item in database:
            content_words = set(item["content"].lower().split())
            score = len(query_words.intersection(content_words))
            if score > highest_score:
                highest_score, best_match = score, item
                
        return best_match if highest_score > 0 else {}
    except Exception:
        return {}

def run_studlyf_copilot(user_input_question: str) -> str:
    if not os.environ.get("GEMINI_API_KEY"):
        return json.dumps({
            "response_text": "SYSTEM ERROR: API Key missing in terminal. Please restart server.",
            "is_verified": False, "sources_used": [], "suggested_follow_ups": []
        })

    #  PASTE THIS CLEAN, PERFECTLY ALIGNED BLOCK INSTEAD:
    try:
        clean_query = user_input_question.strip()[:400]
        matched_db_record = find_verified_context(clean_query)
        
        if matched_db_record:
            # FIX: Allow the AI to elaborate on the provided context
            system_instructions = f"You are a startup dvisor and have excillent knowledge in build startups from screch to all the nessarry things with the excillent intalligence in this feild .all related to startups and advisor. Base your answer fundamentally on this internal data: '{matched_db_record['title']} - {matched_db_record['content']}'. You MUST use your expertise to elaborate on this data to directly answer the user's specific query."
            is_verified_flag, sources_list = True, [matched_db_record["title"]]
        else:
            # STRICT GUARDRAIL: Release to general knowledge but enforce startup domains only
            system_instructions = """You are the Studlyf AI Founder Copilot, an elite advisor for startups. 
            Your domains are STRICTLY limited to: startups, business strategy, funding, venture capital, product development, growth marketing, go-to-market, and tech stacks.
            If the user asks a question OUTSIDE these domains (e.g., general trivia, cooking, movies, personal health), you MUST politely refuse to answer. State that you are specifically engineered for startup growth, and redirect them to ask a relevant business question.
            Provide highly actionable, concise, and professional advice."""
            is_verified_flag, sources_list = False, []

        model = genai.GenerativeModel(model_name='gemini-2.5-flash', system_instruction=system_instructions)
        response = model.generate_content(
            clean_query,
            generation_config=genai.GenerationConfig(response_mime_type="application/json", response_schema=CopilotResponse, temperature=0.1 if is_verified_flag else 0.7)
        )
        output_data = json.loads(response.text)
        output_data["is_verified"], output_data["sources_used"] = is_verified_flag, sources_list
        return json.dumps(output_data, indent=2)

    except Exception as e:
        return json.dumps({"response_text": f"Error: {str(e)}", "is_verified": False, "sources_used": [], "suggested_follow_ups": []}, indent=2)