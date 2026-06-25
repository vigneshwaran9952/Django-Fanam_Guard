import json
import os
import time
import re
import requests
from django.conf import settings
from langchain_google_genai import ChatGoogleGenerativeAI


def is_email_well_formed(email):
    """
    Checks if an email string follows a basic, well-formed pattern.
    """
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.fullmatch(email_regex, email))

def load_usage():
    """Loads usage data from the JSON file."""
    if not os.path.exists(settings.USAGE_FILE):
        return {}
    try:
        with open(settings.USAGE_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, Exception):
        return {}

def save_usage(data):
    """Saves usage data to the JSON file."""
    try:
        with open(settings.USAGE_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception:
        pass

def check_limit(user_id):
    """Checks the current usage limit for a user and resets if the cooldown has passed."""
    usage_data = load_usage()
    user_data = usage_data.get(user_id, {"usage_count": 0, "first_use_timestamp": None})

    if user_data["first_use_timestamp"]:
        elapsed = time.time() - user_data["first_use_timestamp"]
        if elapsed > settings.COOLDOWN_SECONDS:
            user_data = {"usage_count": 0, "first_use_timestamp": None}
    
    usage_data[user_id] = user_data
    save_usage(usage_data)
    return user_data

def update_usage(user_id):
    """Increments the usage count for a user."""
    usage_data = load_usage()
    user_data = usage_data.get(user_id, {"usage_count": 0, "first_use_timestamp": None})
    
    if user_data["first_use_timestamp"] is None:
        user_data["first_use_timestamp"] = time.time()
        
    user_data["usage_count"] += 1
    
    usage_data[user_id] = user_data
    save_usage(usage_data)

def get_llm_response(question, country, sector):
    """Gets the complete response from Google Gemini API via LangChain."""
    
    system_prompt = (
        f"You are a professional {sector} compliance and regulatory expert for {country}. "
        f"Answer questions about {sector} regulations, compliance, best practices, and industry standards in {country}.\n\n"
        
        f"If the question is not related to {sector} in {country}, politely inform the user that you can only help with {sector} matters in {country}.\n\n"
        
        "When answering:\n"
        "- Make sure while responding don't repeat user's questions\n"
        "- Provide clear, structured responses with headings and bullet points\n"
        "- Focus on regulatory compliance, legal requirements, and practical guidance\n"
        "- Include relevant examples and current industry practices\n"
        "- Be professional but easy to understand\n"
        "- Give complete, detailed answers\n"
    )
    
    try:
        # Initialize Gemini model
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.3
        )
        
        # Combine system prompt and question
        full_prompt = f"{system_prompt}\n\nQuestion: {question}\n\nAnswer:"
        
        # Get response from Gemini
        response = llm.invoke(full_prompt)
        
        # Extract the content from the response
        ai_response = response.content
        
        return ai_response.strip()
        
    except Exception as e:
        return f"Error: An unexpected error occurred while processing your request: {str(e)}"