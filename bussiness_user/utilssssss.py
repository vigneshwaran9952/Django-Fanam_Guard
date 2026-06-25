import bcrypt
import uuid
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
import os
import re



INTENTS = {
    "BUSINESS_GLOBAL_EXPANSION": {
        "description": "User intends to expand business operations internationally or globally",
        "utterances": [
           "I want to expand my business across the globe",
        "I wish to take my business global",
        "I plan to expand my business internationally",
        "I want my company to operate worldwide",
        "I am looking to expand my business globally",
 
        "I intend to pursue global business expansion",
        "Our organization plans to establish an international presence",
        "We aim to scale our operations globally",
        "The company seeks international market expansion",
        "We are planning worldwide business growth",
 
        "I want to scale my business to international markets",
        "I am planning cross-border business growth",
        "We are exploring global market entry strategies",
        "Our goal is to grow beyond domestic markets",
        "We want to build a multinational business presence",
 
        "How can I expand my business globally?",
        "What are the steps to take my business international?",
        "What is required to operate a business worldwide?",
        "How do companies expand across multiple countries?",
        "What should I consider before global expansion?",
 
        "I aspire to build a global business",
        "My long-term goal is to operate internationally",
        "I envision my company expanding worldwide",
        "I want my business to have a global footprint",
        "I see my company growing beyond national borders",
 
        "I want to register my business in multiple countries",
        "I am planning to open international branches",
        "I want to start operations in foreign markets",
        "I need to expand my business into other countries",
        "I plan to establish overseas subsidiaries",
 
        "I want to scale my startup globally",
        "I am preparing my company for international expansion",
        "We aim to attract global investors through expansion",
        "Our business is targeting international markets for growth",
        "We are planning global scaling to increase valuation",
 
        "I want my business to go global",
        "I’m thinking of taking my business worldwide",
        "I want to grow my business outside my country",
        "I want to sell my products internationally",
        "I’m planning to expand beyond my home market",
 
        "I want to expand my business into multiple jurisdictions",
        "I need to comply with international regulations for expansion",
        "I am planning cross-border operations for my business",
        "I want to operate under multiple regulatory frameworks",
        "I am exploring international licensing requirements"
            
        ]
    }
}


def hash_password(password: str) -> str:
    """Hash password with bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    try:
        return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
    except Exception:
        return False

def send_registration_email(name, email):
    """Send registration confirmation email"""
    try:
        subject = "Fanam Guard Registration Confirmation"
        message = f"""Dear {name},

Thank you for registering for Fanam Guard. Your account has been created successfully!

Your Username (Email): {email}

You can now log in using the password you set during registration.

Regards,
Fanam Guard Team"""
        
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send registration email: {e}")
        return False

def send_reset_token_email(name, email, token):
    """Send password reset token email"""
    try:
        subject = "Fanam Guard - Password Reset"
        message = f"""Dear {name},

You requested a password reset for your Fanam Guard account.

Your Reset Token: {token}

This token is valid for 1 hour. Please use it to reset your password.

If you didn't request this, please ignore this email.

Regards,
Fanam Guard Team"""
        
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send reset email: {e}")
        return False
    


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#DATA_FILE = os.path.join(BASE_DIR, "bussiness_user/combined_output_3.md")
DATA_FILE = "bussiness_user\combined_output_3.md"
MIN_KEYWORD_MATCH = 2



def normalize(text: str) -> set:
    """Convert text to a set of keywords"""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    return set(text.split())


def match_intent(user_question: str):
    user_tokens = normalize(user_question)

    for intent_name, intent_data in INTENTS.items():
        for example in intent_data["utterances"]:
            example_tokens = normalize(example)

            common_words = user_tokens.intersection(example_tokens)

            if len(common_words) >= MIN_KEYWORD_MATCH:
                return intent_name

    return None


def load_full_content():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return f.read()


def chat_com(question):
    print("\n=== Business Intent Matcher ===")
    #question = input("Ask your question: ")

    intent = match_intent(question)

    if intent:
        print(f"\n✅ Matched Intent: {intent}\n")
        return load_full_content()



