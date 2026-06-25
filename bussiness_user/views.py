from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.test import APIRequestFactory
import json
from django.db.models.functions import TruncMonth
from django.db.models import Count
from .models import ComplianceRuleStatus
import psycopg2
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
import os
import time
import uuid
import base64
from datetime import datetime
from random import uniform
from dotenv import load_dotenv
from deep_translator import GoogleTranslator
import yagmail
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import traceback
import re
import asyncio
import pandas as pd
import csv
import requests
import tempfile
from google import genai
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
#from intent_matcher import match_intent, load_full_content

from .utilssssss import *
#from . import utilssssss
from bussiness_user.models import User, UserSettings, ChatSession, Feedback
#from bussiness_user.models import UserSettings as BusinessUserSettings
from guest_user.models import UserSettings as GuestUserUserSettings
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.parsers import MultiPartParser, FormParser

from django.conf import settings


from .serializers import *
from .serializers import NewChatResponseSerializer
from .serializers import (
    LoadSessionRequestSerializer,
    LoadSessionResponseSerializer,
)


from bussiness_user.models import User, RegulatoryUser


"""from .serializers import (
    SaveSettingsSerializer,
    SaveSettingsResponseSerializer
)"""

from .serializers import (
    FeedbackSubmitRequestSerializer,
    FeedbackSubmitResponseSerializer,
)


from .serializers import ChatRequestSerializer, ChatResponseSerializer
from .models import ChatSession, UserSettings
from .serializers import VoiceToTextResponseSerializer
from .serializers import TextToSpeechRequestSerializer, TextToSpeechResponseSerializer

class RewriteRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    session_id = serializers.CharField()
    question = serializers.CharField()



from .serializers import (
    ClickSuggestionRequestSerializer,
    ClickSuggestionResponseSerializer,
)

from .serializers import (
    ChatHistoryResponseSerializer,
    AllSessionsResponseSerializer,
    LogoutResponseSerializer,
    GetSettingsResponseSerializer,
    HealthCheckResponseSerializer,
    # ... your other imports
)

#cache
from .cache_utils import get_cached_response, save_to_cache

# Import your existing modules (make sure they're accessible)
# Change these lines in chatapp/views.py
from . import enhance
from . import deep
from . import vtt_utils
from . import tts
from . import stm_handler
from . import ltm_handler
from . import intent

from .serializers import VoiceToTextRequestSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, UserSettings
from .serializers import UserTypeResponseSerializer

DB_CONFIG = {
    "dbname": "fanam_guard",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432",
}

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
YAGMAIL_USER = os.getenv("YAGMAIL_USER")
YAGMAIL_PASS = os.getenv("YAGMAIL_PASS")
client = genai.Client(api_key=GOOGLE_API_KEY) 

#Azure
AZURE_ACCOUNT_NAME = os.getenv("AZURE_ACCOUNT_NAME")
AZURE_ACCESS_KEY = os.getenv("AZURE_ACCESS_KEY")
AZURE_CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME")
AZURE_CONTAINER_NAME_1 = os.getenv("AZURE_CONTAINER_NAME_1") 
# Azure Storage Connection String
AZURE_CONNECTION_STRING = f"DefaultEndpointsProtocol=https;AccountName={AZURE_ACCOUNT_NAME};AccountKey={AZURE_ACCESS_KEY};EndpointSuffix=core.windows.net"
AZURE_CONNECTION_STRING_1 = f"DefaultEndpointsProtocol=https;AccountName={AZURE_ACCOUNT_NAME};AccountKey={AZURE_ACCESS_KEY};EndpointSuffix=core.windows.net"

# Constants
FULL_CONTENT_JSON = os.path.join(settings.BASE_DIR, "merged_content.json")
SUMMARY_FAISS_PATH = os.path.join(settings.BASE_DIR, "data1", "faiss_index_summary")
CONTENT_FAISS_PATH = os.path.join(settings.BASE_DIR, "data1", "faiss_index_content")

LANGUAGE_CSV = "language_code.csv"

ALLOWED_COUNTRIES = {"India", "China", "US", "UAE"}
ALLOWED_SECTORS = {"Banking", "Finance", "Healthcare", "Environment", "Shariat", "Ancillary Service Providers","Banking and Fintech", "Cryptocurrency and Blockchain related Services", "Financial Advisory Services", "Fund Management & Custodian", "Insurtech", "Investment and wealth management platforms", "Lending platforms", "Payment service providers", "Regtech"}

fallback_phrases = [
    "sorry, no detailed content found",
    "sorry, no relevant information",
    "no relevant information is available",
    "provided context does not contain",
    "i am sorry",
    "no relevant data found",
    "no detailed content found",
    "no information found"
]

# Global variables for RAG
EMBEDDING_MODEL = None
SUMMARY_VECTORDB = None
CONTENT_VECTORDB = None
FULL_DATA = []
LLM = None


LANGUAGES = [
    "English",

    "Afrikaans",
    "Arabic",
    "Basque",
    "Bengali",
    "Bulgarian",
    "Catalan",
    "Chinese (Simplified)",
    "Chinese (Traditional)",
    "Czech",
    "Danish",
    "Dutch",
    "Estonian",
    "Filipino (Tagalog)",
    "Finnish",
    "French",
    "Galician",
    "German",
    "Greek",
    "Gujarati",
    "Hindi",
    "Hungarian",
    "Icelandic",
    "Indonesian",
    "Italian",
    "Japanese",
    "Kannada",
    "Kazakh",
    "Khmer",
    "Korean",
    "Kurdish (Kurmanji)",
    "Kurdish (Sorani)",
    "Lao",
    "Latvian",
    "Lithuanian",
    "Luxembourgish",
    "Macedonian",
    "Malagasy",
    "Malay",
    "Maltese",
    "Maori",
    "Marathi",
    "Mongolian",
    "Nepali",
    "Norwegian",
    "Pashto",
    "Persian",
    "Polish",
    "Portuguese",
    "Punjabi (Gurmukhi)",
    "Romanian",
    "Russian",
    "Samoan",
    "Scots Gaelic",
    "Serbian",
    "Sesotho",
    "Shona",
    "Sindhi",
    "Sinhala",
    "Slovak",
    "Slovenian",
    "Somali",
    "Spanish",
    "Sundanese",
    "Swahili",
    "Swedish",
    "Tajik",
    "Tamil",
    "Tatar",
    "Telugu",
    "Thai",
    "Turkish",
    "Turkmen",
    "Ukrainian",
    "Urdu",
    "Uyghur",
    "Uzbek",
    "Vietnamese",
    "Welsh",
    "Xhosa",
    "Yiddish",
    "Yoruba",
    "Zulu"
]

COUNTRY_FILE_MAP = {
    "india": "data/INDIA_BANKING_FINTECH_REGULATORY_COMPLIANCE.pdf",
    "united states": "data/UNITED_STATES_BANKING_FINTECH_REGULATORY_COMPLIANCE.pdf",
    "usa": "data/UNITED_STATES_BANKING_FINTECH_REGULATORY_COMPLIANCE.pdf",
    "singapore": "data/SINGAPORE_BANKING_FINTECH_REGULATORY_COMPLIANCE.pdf",
    "uk": "data/UNITED_KINGDOM_BANKING_FINTECH_REGULATORY_COMPLIANCE.pdf",
    "australia": "data/AUSTRALIA_BANKING_FINTECH_REGULATORY_COMPLIANCE.pdf",
}

PROMPT_EXPANSION="""You are a cross-border business expansion and regulatory gap analyst.

OBJECTIVE:
Identify ONLY the additional, different, or stricter regulatory requirements that apply when expanding
from the home jurisdiction (baseline) into the target jurisdiction.

BASELINE RULES:
- Treat the home jurisdiction as fully compliant.
- Do NOT restate baseline requirements unless materially different or stricter in the target jurisdiction.
- Focus ONLY on expansion-impacting regulatory gaps.

MULTI-COUNTRY OUTPUT RULE (MANDATORY):
- The first uploaded item represents the home jurisdiction.
- Each additional uploaded item represents ONE target jurisdiction.
- For EACH target jurisdiction:
  - Output a section titled exactly:
    "### Expansion into <Country Name>"
  - Under that heading, output EXACTLY ONE table in the required format.
- Do NOT merge jurisdictions.
- Do NOT mix jurisdictions within the same table.

OUTPUT FORMAT (MANDATORY):

| Area | Home Jurisdiction | Target Jurisdiction | Expansion Impact | Mandatory Steps for Compliance |

MANDATORY STEPS COLUMN RULE:
- Populate "Mandatory Steps for Compliance" with enforceable regulatory actions.
- Write steps as separate lines within the same table cell.
- Use declarative, regulator-facing language only.
- Do NOT use advisory or optional language ("should", "may", "consider").
- Do NOT include timelines, costs, sequencing, or opinions.
- If no additional action is required, state exactly:
  "No additional steps required".

EXPANSION IMPACT VALUES (STRICT):
✔ Already satisfied  
⚠ Modified requirement  
❌ New mandatory obligation  
🚫 Restriction or constraint  

CONTENT RULES:
- Each row represents one regulatory area.
- Do NOT include narrative text before or after tables.
- Do NOT include summaries.
- Do NOT include bullet lists outside the table.
- Do NOT include introductory phrases.

VALIDATION:
- Output is INVALID if fewer tables are produced than target jurisdictions.
"""




PROMPT_COMPARISON="""
You are a senior regulatory analyst stating binding regulatory conditions.
 
VOICE CONSTRAINT:
- State regulatory obligations only.
- Use declarative, regulator-facing language.
- Do NOT explain, interpret, or add commentary.
- Do NOT provide opinions or strategic content.
 
MULTI-JURISDICTION RULE (MANDATORY):
- The first uploaded item is the reference jurisdiction.
- Each additional uploaded item is ONE comparison jurisdiction.
- The number of comparison sections MUST match the number of comparison jurisdictions.
 
OUTPUT STRUCTURE (MANDATORY ORDER):
 
## Regulatory Comparison
 
### Common Requirements (As a summary)
- MUST be written as ONE concise paragraph.
- MUST reflect ONLY regulatory coverage explicitly present in BOTH jurisdictions.
- MUST NOT enumerate individual requirements.
- MUST NOT restate table entries.
- MUST NOT introduce new obligations.
- MUST use declarative, regulator-facing language.
- If no overlap exists, state exactly: "Not specified".
 
### Comparison with <Country Name> (As a summary)
- MUST be written as ONE concise paragraph.
- MUST reflect ONLY jurisdiction-specific regulatory coverage.
- MUST NOT duplicate Common Requirements.
- MUST NOT enumerate individual requirements.
- MUST NOT restate table entries.
- MUST NOT introduce new obligations.
- MUST use declarative, regulator-facing language.
- If no jurisdiction-specific content exists, state exactly: "Not specified".
 
### Comparison Table
- Side-by-side comparison of enforceable regulatory requirements.
- One row per requirement.
- Columns:
  - Reference Jurisdiction
  - <Country Name>
- Use precise regulatory wording.
- If missing, state exactly: "Not specified".
 
SECTION CONTENT RULES:
 
- Paragraphs are permitted ONLY in summary sections.
- Bullet points are permitted ONLY inside the Comparison Table.
- No introductory or concluding narrative outside defined sections.
- No duplication between summaries and table.
- Do NOT restate the same requirement using different wording.
 
PROHIBITED LANGUAGE (GLOBAL):
Do NOT use:
- document, roadmap, paper, file, text
- outlines, explains, discusses, provides
- this, it, they, the above
- critical, strategic, important, recommended
 
STRICT RULES:
- Do NOT add external regulatory knowledge.
- Do NOT infer intent.
- Do NOT generalize.
- Do NOT normalize or soften regulatory language.
 
VALIDATION:
- Output is INVALID if:
  - Section order is not followed exactly.
  - Any summary contains bullet points.
  - Any table content appears in summaries.
  - Any comparison jurisdiction lacks a summary and table.
  - Any prohibited language appears.
"""

# =========================
# BASELINE FILE CACHE
# =========================

BASELINE_FILE = None
TARGET_FILE_CACHE = {}

def get_baseline_file(client):
    global BASELINE_FILE
    if BASELINE_FILE is None:
        start = time.perf_counter()
        BASELINE_FILE = client.files.upload(
            file="data/United_Arab_Emirates_Banking_and_Financial_Services_Regulatory_Framework.pdf"
        )
        end = time.perf_counter()
        print(f"📄 Baseline file upload time: {end - start:.2f}s")
    return BASELINE_FILE


# =========================
# HELPERS
# =========================

def extract_target_countries(user_query: str):
    user_query = user_query.lower()
    seen_files = set()
    selected_countries = []

    for country, path in COUNTRY_FILE_MAP.items():
        if country in user_query and path not in seen_files:
            selected_countries.append(country)
            seen_files.add(path)

    return selected_countries


def upload_target_files(client, target_countries):
    uploaded_files = []

    for country in target_countries:
        if country in TARGET_FILE_CACHE:
            uploaded_files.append(TARGET_FILE_CACHE[country])
        else:
            start = time.perf_counter()
            file_path = COUNTRY_FILE_MAP[country]
            uploaded_file = client.files.upload(file=file_path)
            end = time.perf_counter()

            TARGET_FILE_CACHE[country] = uploaded_file
            uploaded_files.append(uploaded_file)

            print(f"📄 {country.upper()} upload time: {end - start:.2f}s")

    return uploaded_files


# =========================
# CORE ASYNC FUNCTIONS
# =========================

async def expansion_async(user_query: str):
    home_file = get_baseline_file(client)

    target_countries = extract_target_countries(user_query)
    if not target_countries:
        return "No target country identified."

    target_files = upload_target_files(client, target_countries)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[home_file, *target_files, PROMPT_EXPANSION]
    )
    return response.text.strip()

async def compare_async(user_query: str):
    reference_file = get_baseline_file(client)

    target_countries = extract_target_countries(user_query)
    if not target_countries:
        return "No comparison country identified."

    comparison_files = upload_target_files(client, target_countries)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[reference_file, *comparison_files, PROMPT_COMPARISON]
    )
    return response.text.strip()

async def run_all(user_query:str):
    #user_query = "I would like to expand my business from UAE to India."

    total_start = time.perf_counter()

    ## 1️⃣ Expansion
    #expansion_start = time.perf_counter()
    #expansion_result = await expansion_async(user_query)
    #expansion_end = time.perf_counter()
#
    ## 2️⃣ Comparison
    #comparison_start = time.perf_counter()
    #compare_result = await compare_async(user_query)
    #comparison_end = time.perf_counter()
#
    #total_end = time.perf_counter()
#


    # ⏱ Start total timer
    total_start = time.perf_counter()

    # Create tasks
    expansion_task = expansion_async(user_query)
    comparison_task = compare_async(user_query)

    # ⏱ Run both in parallel
    parallel_start = time.perf_counter()
    expansion_result, compare_result = await asyncio.gather(
        expansion_task,
        comparison_task
    )
    parallel_end = time.perf_counter()

    # ⏱ End total timer
    total_end = time.perf_counter()

    parallel_time = parallel_end - parallel_start
    total_time = total_end - total_start

    ## ⏱ Time calculations
    #expansion_time = expansion_end - expansion_start
    #comparison_time = comparison_end - comparison_start
    #total_time = total_end - total_start


    combined_txt = (
        "===== EXPANSION GAP ANALYSIS =====\n\n"
        + expansion_result
        + "\n\n===== REGULATORY COMPARISON =====\n\n"
        + compare_result
    )

    combined_md = (
        "### Expansion Gap Analysis\n\n"
        + expansion_result
        + "\n\n---\n\n"
        + "### Regulatory Comparison\n\n"
        + compare_result
    )

    #with open("combined_output_9.txt", "w", encoding="utf-8") as f:
    #    f.write(combined_txt)
    #
    #with open("combined_output_sg.md", "w", encoding="utf-8") as f:
    #   f.write(combined_md)

    print("✅ Expansion & Comparison completed (parallel).")
    print(f"⏱ Parallel execution time : {parallel_time:.2f}s")
    print(f"⏱ Total end-to-end time   : {total_time:.2f}s")

    return combined_md

def run_all_sync(user_query: str) -> str:
    return asyncio.run(run_all(user_query))


# Initialize RAG system
def initialize_rag():
    global EMBEDDING_MODEL, SUMMARY_VECTORDB, CONTENT_VECTORDB, FULL_DATA, LLM
    
    if EMBEDDING_MODEL is None:
        EMBEDDING_MODEL = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"}
        )
    
    if LLM is None:
        LLM = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=GOOGLE_API_KEY,
            temperature=0.4
        )
    
    # Load data
    with open(FULL_CONTENT_JSON, "r", encoding="utf-8") as f:
        FULL_DATA = json.load(f)
    
    summary_docs = []
    content_docs = []
    
    for idx, item in enumerate(FULL_DATA):
        summary_docs.append(Document(
            page_content=item.get("summary", ""),
            metadata={"index": idx, "country": item.get("country", "").lower(), "sector": item.get("sector", "").lower()}
        ))
        content_docs.append(Document(
            page_content=item.get("content", ""),
            metadata={"index": idx, "country": item.get("country", "").lower(), "sector": item.get("sector", "").lower()}
        ))
    
    # Load or build FAISS
# Load or build FAISS Summary Index
    if os.path.exists(os.path.join(SUMMARY_FAISS_PATH, "index.faiss")):
        SUMMARY_VECTORDB = FAISS.load_local(
            SUMMARY_FAISS_PATH,
            EMBEDDING_MODEL,
            allow_dangerous_deserialization=True
        )
    else:
        SUMMARY_VECTORDB = FAISS.from_documents(summary_docs, EMBEDDING_MODEL)
        SUMMARY_VECTORDB.save_local(SUMMARY_FAISS_PATH)

    # Load or build FAISS Content Index
    if os.path.exists(os.path.join(CONTENT_FAISS_PATH, "index.faiss")):
        CONTENT_VECTORDB = FAISS.load_local(
            CONTENT_FAISS_PATH,
            EMBEDDING_MODEL,
            allow_dangerous_deserialization=True
        )
    else:
        CONTENT_VECTORDB = FAISS.from_documents(content_docs, EMBEDDING_MODEL)
        CONTENT_VECTORDB.save_local(CONTENT_FAISS_PATH)
        print("✅ Loading merged_content.json from:", FULL_CONTENT_JSON)
        print("✅ Loading Summary index from:", SUMMARY_FAISS_PATH)
        print("✅ Loading Content index from:", CONTENT_FAISS_PATH)



# Initialize on module load
try:
    initialize_rag()
except Exception as e:
    traceback.print_exc()
# Utility functions
def clean_text(text: str) -> str:
    return ' '.join(text.split())

def get_language_code(language):
    lang_map = vtt_utils.load_languages(LANGUAGE_CSV)
    return lang_map.get(language, None)

def filter_content_by_summary_tfidf(top5_sum_docs, top5_cont_docs, top_n=5):
    if not top5_sum_docs or not top5_cont_docs:
        return []
    sum_texts = [d.page_content for d in top5_sum_docs]
    cont_texts = [d.page_content for d in top5_cont_docs]
    vect = TfidfVectorizer().fit(sum_texts + cont_texts)
    sum_tfidf = vect.transform(sum_texts)
    cont_tfidf = vect.transform(cont_texts)
    sim_matrix = cosine_similarity(sum_tfidf, cont_tfidf)
    cont_scores = sim_matrix.mean(axis=0)
    scored = list(zip(top5_cont_docs, cont_scores))
    scored.sort(key=lambda x: x[1], reverse=True)
    return [doc for doc, _ in scored[:top_n]]

def safe_llm_invoke(prompt_text):
    for _ in range(3):
        try:
            result = LLM.invoke(prompt_text)
            if result and result.content.strip():
                return result.content
        except Exception:
            time.sleep(uniform(1.0, 2.5))
    return "No detailed content found to answer your query."

def generate_followup_suggestions(question, answer, country, sector, language, lang_code):
    print(language)
    suggestion_prompt = f"""
IMPORTANT INSTRUCTION:
You MUST write ALL questions ONLY in {language}.
DO NOT use English unless {language} is English.
        
You just had this exchange with someone:

Their question: "{question}"

Your answer covered: {answer[:500]}...

Now suggest 2-3 natural follow-up questions they might ask next. These should:
- Feel like the next thing a curious person would ask
- Be short and conversational (5-8 words max)
- Dig deeper into what was just discussed
- Be specific to {country}'s {sector} sector
- Sound natural, not academic

Just list 2-3 questions, one per line. No numbers, bullets, or extra text."""

    try:
        result = LLM.invoke(suggestion_prompt)
        suggestions_text = result.content.strip()
        
        suggestions = []
        for line in suggestions_text.split('\n'):
            line = line.strip()
            line = re.sub(r'^[\d\.\-\*\•]+\s*', '', line)
            
            if line and 4 <= len(line.split()) <= 9:
                if not any(bad in line.lower() for bad in ["define", "what is", "explain", "tell me about", "can you"]):
                    suggestions.append(line)
        
        suggestions = suggestions[:3]
        if not suggestions:
            suggestions = ["What are the key requirements?", "How is this enforced?"]
        
        # Translate suggestions if needed
        if lang_code and lang_code != "en" and language.lower() != "english":
            try:
                translated_suggestions = []
                for sugg in suggestions:
                    translated = GoogleTranslator(source="en", target=lang_code).translate(sugg)
                    translated_suggestions.append(translated)
                suggestions = translated_suggestions
            except:
                pass
        print(language)
        return suggestions
    except Exception as e:
        print(f"Error generating suggestions: {e}")
        return []

# RAG Prompt
prompt_template = """
You are a professional Compliance Knowledge Assistant with expertise across India, the United States, the United Arab Emirates, and China.
You provide insights into compliance, regulations, legal frameworks, governance, and policy for the sectors: Banking, Finance, Healthcare, and Environment.

Your answer must be based ONLY on the provided Relevant Information (RAG Context).

### Response Guidelines:
1. **Core Domain Check:** Your primary focus is on the 'User's Selected Sector' ({sector}).
2. **Sector Mismatch Fallback:** If the question asks about a sector *other than* the selected sector, respond: "To maintain focus on your current workflow, please ask questions related to the **{sector}** sector. If you wish to change focus, kindly update your Sector setting."
3. **Country Flexibility:** If the question asks about a different country but stays within the selected sector, answer using the RAG Context.
4. **Data Constraint:** If answers are not available in the RAG Context, synthesize the most closely related information.
5. Opening Style:
Start with a natural compliance-focused sentence.
Mention the country and sector early, but do not force the exact phrase.

6. **Style & Structure:**
   * Write in a clear, confident tone.
   * Use structured paragraphs and/or bullet points.
   * Expand acronyms on first use.
   * Be factual, concise (20-25 lines), and engaging.
7. **Guardrails:**
   * Never mention "document," "context," or "source text."
   * Work only on the selected sector.
   

### User Context:
- **User's Selected Country:** {country}
- **User's Selected Sector:** {sector}
- **Current Question:** {question}
- **Relevant Information (RAG Context):**
{context}

**Answer:**
"""

prompt = PromptTemplate(
    input_variables=["context", "question", "country", "sector"],
    template=prompt_template
)

# Helper to get or create session
def get_or_create_session(request):
    session_id = request.session.get('session_id')
    user_email = request.session.get('user_email')
    
    if not session_id or not user_email:
        return None
    
    try:
        chat_session = ChatSession.objects.get(session_id=session_id, user_email=user_email)
    except ChatSession.DoesNotExist:
        chat_session = ChatSession.objects.create(
            user_email=user_email,
            session_id=session_id,
            chat_history=json.dumps([]),
            stm_context=json.dumps([]),
            title="New Chat"
        )
    
    return chat_session


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="email",
            type=str,
            location=OpenApiParameter.QUERY,
            required=False,
            description="User or guest email address"
        )
    ],
    responses={200: UserInfoResponseSerializer},
    description="""
    Fetch user information for both login and guest users.
    Priority:
    1. Query parameter email
    2. Session user_email
    3. Session guest_email
    """
)
@api_view(["GET"])
def get_user_info(request):
    try:
        # ===================================
        # ✅ Resolve Email (Priority Order)
        # ===================================
        query_email = request.query_params.get("email")
        session_email = request.session.get("user_email")
        guest_email = request.session.get("guest_email")

        user_email = query_email or session_email or guest_email

        # ===================================
        # ✅ No Email Case
        # ===================================
        if not user_email:
            return Response(
                {
                    "success": True,
                    "user_type": "none",
                    "email": None,
                    "name": None,
                    "user_country": None,
                    "sub_category": None,
                    "country": None,
                    "sector": None,
                    "language": None,
                },
                status=status.HTTP_200_OK
            )

        # ===================================
        # ✅ Detect User Type
        # ===================================
        name = user_country = sub_category = None
        
        try:
            # 🔹 Business User
            user = User.objects.get(email=user_email)
            user_type = "business"
            name = user.name
            user_country = user.user_country
            sub_category = user.sub_category

        except User.DoesNotExist:
            try:
                # 🔹 Regulator User
                reg_user = RegulatoryUser.objects.get(email=user_email)
                user_type = "regulator"
                name = reg_user.name
                user_country = reg_user.user_country
                sub_category = reg_user.sub_category

            except RegulatoryUser.DoesNotExist:
                # 🔹 Guest
                user_type = "guest"
                name = None
                user_country = None
                sub_category = None

        # ===================================
        # ✅ Load Settings Based on User Type
        # ===================================
        country = sector = language = None

        # Fix: Allow both Business and Regulator users to pull from UserSettings
        if user_type in ["business", "regulator"]:
            user_settings = UserSettings.objects.filter(
                user_email=user_email
            ).first()

            if user_settings:
                country = user_settings.country
                sector = user_settings.sector
                language = user_settings.language
        
        # Guest fallback
        elif user_type == "guest":
            guest_settings = GuestUserUserSettings.objects.filter(
                email=user_email
            ).first()

            if guest_settings:
                country = guest_settings.country
                sector = guest_settings.sector
                language = None

        # ===================================
        # ✅ Final Response
        # ===================================
        return Response(
            {
                "success": True,
                "user_type": user_type,
                "email": user_email,
                "name": name,
                "user_country": user_country,
                "sub_category": sub_category,
                "country": country,
                "sector": sector,
                "language": language  # Now returns for both business and regulator
            },
            status=status.HTTP_200_OK
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response(
            {
                "success": False,
                "message": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@extend_schema(
    request=RegisterRequestSerializer,
    responses={
        201: dict,
        400: dict
    }
)
@api_view(["POST"])
def register(request):
    """
    Register a new user (Business or Regulatory).

    POST /api/register/
    """

    # ✅ Validate Request Data
    serializer = RegisterRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # ✅ Extract Fields
    name = serializer.validated_data["name"]
    email = serializer.validated_data["email"]
    password = serializer.validated_data["password"]

    # ✅ Optional Phone Inputs
    country_code = serializer.validated_data.get("country_code")
    phone_number = serializer.validated_data.get("phone_number")

    # ✅ Optional Category Inputs
    country = serializer.validated_data.get("user_country")
    category = serializer.validated_data.get("sub_category")

    # ✅ NEW FIELD → User Type
    user_type = serializer.validated_data["user_type"]  # "business" or "regulator"

    # ======================================================
    # ✅ STEP 1: Email Uniqueness Check (Both Tables)
    # ======================================================
    if User.objects.filter(email=email).exists() or RegulatoryUser.objects.filter(email=email).exists():
        return Response(
            {
                "success": False,
                "message": "Email already registered"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # ======================================================
    # ✅ STEP 2: Create User Based on user_type
    # ======================================================

    if user_type == "business":
        # ✅ Business User Store
        user = User.objects.create(
            name=name,
            email=email,
            password=make_password(password),
            user_type=user_type,  # ✅ STORE
            user_country=country,
            sub_category=category,

            country_code=country_code,
            phone_number=phone_number
        )

    elif user_type == "regulator":
        # ✅ Regulatory User Store
        user = RegulatoryUser.objects.create(
            name=name,
            email=email,
            password=make_password(password),
            user_type=user_type,  # ✅ STORE
            user_country=country,
            sub_category=category,

            country_code=country_code,
            phone_number=phone_number
        )

    else:
        return Response(
            {
                "success": False,
                "message": "Invalid user_type. Must be 'login' or 'regulator'"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # ======================================================
    # ✅ STEP 3: Send Confirmation Email (Non-blocking)
    # ======================================================
    try:
        if settings.YAGMAIL_USER and settings.YAGMAIL_PASS:
            yag = yagmail.SMTP(settings.YAGMAIL_USER, settings.YAGMAIL_PASS)

            yag.send(
                to=email,
                subject="Fanam Guard Registration Successful",
                contents=f"""
Hello {name},

Your Fanam Guard account has been created successfully.

User Type: {user_type.upper()}

You can now log in and start using the platform.

Regards,
Fanam Guard Team
"""
            )

    except Exception as e:
        print(f"Email send failed: {e}")

    # ======================================================
    # ✅ STEP 4: Final Response
    # ======================================================
    return Response(
        {
            "success": True,
            "message": "Registration successful ✅",

            "user_type": user_type,
            "name": user.name,
            "email": user.email,

            # ✅ Return Stored Details
            "country_code": user.country_code,
            "phone_number": user.phone_number,

            "user_country": user.user_country,
            "sub_category": user.sub_category,
        },
        status=status.HTTP_201_CREATED
    )



@extend_schema(
    request=LoginRequestSerializer,
    responses={
        200: dict,
        400: dict,
        401: dict,
        500: dict
    }
)
@api_view(["POST"])
def login(request):
    """
    Unified Login API for:
    ✅ Business Users (User table)
    ✅ Regulatory Users (RegulatoryUser table)

    POST /api/login/
    """

    # ✅ Validate Input
    serializer = LoginRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data["email"]
    password = serializer.validated_data["password"]

    user = None
    user_type = None

    # ✅ Default values
    user_country = None
    sub_category = None

    # ======================================================
    # ✅ STEP 1: Check Business User Table
    # ======================================================
    try:
        user = User.objects.get(email=email)
        user_type = "business"


        user_country = user.user_country
        sub_category = user.sub_category

    except User.DoesNotExist:

        # ======================================================
        # ✅ STEP 2: Check Regulatory User Table
        # ======================================================
        try:
            user = RegulatoryUser.objects.get(email=email)
            user_type = "regulator"

            user_country = user.user_country
            sub_category = user.sub_category

        except RegulatoryUser.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "Invalid credentials"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

    # ======================================================
    # ✅ STEP 3: Password Check
    # ======================================================
    if not check_password(password, user.password):
        return Response(
            {
                "success": False,
                "message": "Invalid credentials"
            },
            status=status.HTTP_401_UNAUTHORIZED
        )

    # ======================================================
    # ✅ STEP 4: Create Session
    # ======================================================
    request.session["user_email"] = user.email
    request.session["user_name"] = user.name
    request.session["session_id"] = str(uuid.uuid4())
    request.session["user_type"] = user_type

    # ✅ Remove Guest Session if Exists
    request.session.pop("guest_email", None)

    # ======================================================
    # ✅ STEP 5: Load Settings Safely
    # ======================================================
    user_settings = {
        "country": None,
        "sector": None,
        "language": None
    }

    # ✅ Only Business Users Have UserSettings Table
    if user_type == "business":
        try:
            user_settings_obj = UserSettings.objects.get(user_email=user.email)

            user_settings = {
                "country": user_settings_obj.country,
                "sector": user_settings_obj.sector,
                "language": user_settings_obj.language
            }

        except UserSettings.DoesNotExist:
            pass

    # ======================================================
    # ✅ STEP 6: Final Response
    # ======================================================
    return Response(
        {
            "success": True,
            "message": f"Welcome {user.name} ✅",
            "user_type": user.user_type,

            # ✅ User Info
            "name": user.name,
            "email": user.email,

            # ✅ Phone Info
            "country_code": user.country_code,
            "phone_number": user.phone_number,

            # ✅ Registration Info
            "user_country": user_country,
            "sub_category": sub_category,

            # ✅ Settings Info
            "country": user_settings["country"],
            "sector": user_settings["sector"],
            "language": user_settings["language"],

            # ✅ Session Info
            "session_id": request.session["session_id"],
        },
        status=status.HTTP_200_OK
    )




@extend_schema(
    request=LogoutRequestSerializer,
    responses={200: LogoutResponseSerializer}
)

@api_view(["POST"])
def logout(request):
    session_email = request.session.get("user_email")
    body_email = request.data.get("email")

    # 🔐 Prevent logout spoofing
    #if body_email and body_email != session_email:
    if not body_email:
        return Response(
            {
                "success": False,
                "message": "Email does not match active session"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    request.session.flush()

    return Response(
        {
            "success": True,
            "message": "Logged out successfully"
        },
        status=status.HTTP_200_OK
    )



@extend_schema(
    request=ForgotPasswordRequestSerializer,
    responses={
        200: dict,
        400: dict,
        404: dict,
        500: dict,
    },
)
@api_view(["POST"])
def forgot_password(request):
    """
    Reset user password and send a temporary password via email.
    POST /api/forgot-password/
    """
    try:
        email = request.data.get("email")

        # 🔹 Validate input
        if not email:
            return Response(
                {"success": False, "email": email, "message": "Email is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 🔹 Fetch user
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"success": False, "email": email, "message": "Email not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # 🔹 Generate temporary password
        temp_password = str(uuid.uuid4())[:8]
        user.password = make_password(temp_password)
        user.save()

        # 🔹 Email configuration check
        if not settings.YAGMAIL_USER or not settings.YAGMAIL_PASS:
            return Response(
                {"success": False, "email": email, "message": "Email service not configured"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # 🔹 Send email
        try:
            yag = yagmail.SMTP(settings.YAGMAIL_USER, settings.YAGMAIL_PASS)
            yag.send(
                to=email,
                subject="Fanam Guard Password Reset",
                contents=f"""
Dear {user.name},

Your temporary password is: {temp_password}

Please log in and change your password immediately.

Regards,
Fanam Guard Team
"""
            )
        except Exception as e:
            return Response(
                {"success": False, "email": email, "message": f"Failed to send email: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {
                "success": True,
                "email": email,
                "message": "Temporary password sent to your email"
            },
            status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response(
            {"success": False,"email": email, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )



@extend_schema(
    request=ChangePasswordRequestSerializer,
    responses={
        200: dict,
        400: dict,
        401: dict,
        404: dict,
        500: dict,
    }
)
@api_view(["POST"])
def change_password(request):
    """
    Change the password of the authenticated user.
    POST /api/change-password/
    """
    try:
        #user_email = request.session.get("user_email")
        serializer = ChangePasswordRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_email = serializer.validated_data['email']

        old_password = serializer.validated_data["old_password"]
        new_password = serializer.validated_data["new_password"]
        if not user_email:
            return Response(
                {"success": False, "message": "Not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = ChangePasswordRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        old_password = serializer.validated_data["old_password"]
        new_password = serializer.validated_data["new_password"]

        # 🔹 Fetch user
        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            return Response(
                {"success": False, "message": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # 🔹 Verify old password
        if not check_password(old_password, user.password):
            return Response(
                {"success": False, "message": "Invalid old password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # 🔹 Update password
        user.password = make_password(new_password)
        user.save()

        return Response(
            {
                "success": True,
                "message": "Password changed successfully"
            },
            status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response(
            {"success": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@extend_schema(
    request=SaveSettingsRequestSerializer,
    responses={200: BusinessSaveSettingsResponseSerializer}
)
@api_view(["POST"])
def save_settings(request):
    try:
        #user_email = request.session.get("user_email")
        serializer = SaveSettingsRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_email = serializer.validated_data["email"]
        country = serializer.validated_data["country"]
        sector = serializer.validated_data["sector"]
        language = serializer.validated_data["language"]       
        if not user_email:
            return Response(
                {"success": False, "message": "Not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        #serializer = SaveSettingsRequestSerializer(data=request.data)
        #serializer.is_valid(raise_exception=True)
        #
        #country = serializer.validated_data["country"]
        #sector = serializer.validated_data["sector"]
        #language = serializer.validated_data["language"]

        if country not in ALLOWED_COUNTRIES or sector not in ALLOWED_SECTORS:
            return Response(
                {"success": False, "message": "Invalid country or sector"},
                status=status.HTTP_400_BAD_REQUEST
            )

        settings_obj, created = UserSettings.objects.update_or_create(
            user_email=user_email,
            defaults={
                "country": country,
                "sector": sector,
                "language": language
            }
        )

        return Response(
            {
                "success": True,
                "message": "Settings created" if created else "Settings updated",
                "email": user_email,
                "settings": {
                    "country": settings_obj.country,
                    "sector": settings_obj.sector,
                    "language": settings_obj.language
                }
            },
            status=status.HTTP_200_OK
        )

    except Exception as e:
        traceback.print_exc()
        return Response(
            {"success": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    
@extend_schema(
    parameters=[
        OpenApiParameter(
            name="email",
            type=str,
            location=OpenApiParameter.QUERY,
            required=False,
            description="User email address (optional, falls back to session)"
        )
    ],
    responses={200: GetSettingsResponseSerializer},
    summary="Get user settings",
    description="Fetch user preferences using query email or session email"
)
@api_view(["GET"])
def get_settings(request):
    """
    Get user preferences (country, sector, language).

    Priority:
    1. Query param email
    2. Session email
    """
    try:
        # 🔹 1. Read email from query param
        query_email = request.query_params.get("email")

        # 🔹 2. Read email from session (fallback)
        session_email = request.session.get("user_email")

        user_email = query_email or session_email

        if not user_email:
            return Response(
                {"success": False, "message": "Not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            settings_obj = UserSettings.objects.get(user_email=user_email)
            settings_data = {
                "country": settings_obj.country,
                "sector": settings_obj.sector,
                "language": settings_obj.language
            }
        except UserSettings.DoesNotExist:
            # 🔹 Fallback defaults
            settings_data = {
                "country": list(ALLOWED_COUNTRIES)[0],
                "sector": list(ALLOWED_SECTORS)[0],
                "language": "English"
            }

        return Response(
            {
                "success": True,
                "email": user_email,
                "settings": settings_data
            },
            status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response(
            {"success": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
@extend_schema(
    parameters=[
        OpenApiParameter(
            name="email",
            type=str,
            location=OpenApiParameter.QUERY,
            required=True,
            description="User email used to identify chat history"
        ),
    ],
    request=None,
    responses={
        201: NewChatResponseSerializer,
        401: dict,
        500: dict,
    },
    summary="Create a new chat session",
    description="Creates a new chat session for the authenticated user."
)

@api_view(["POST"])
def new_chat(request):
    """
    Create a new chat session for the authenticated user.
    """
    try:
        user_email = request.query_params.get("email")
        #user_email = email
        if not user_email:
            return Response(
                {"success": False, "message": "Not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # 🔹 Generate new session ID
        new_session_id = str(uuid.uuid4())

        # 🔹 Store session ID in Django session
        request.session["session_id"] = new_session_id

        # 🔹 Persist chat session
        ChatSession.objects.create(
            user_email=user_email,
            session_id=new_session_id,
            chat_history=json.dumps([]),
            stm_context=json.dumps([]),
            title="New Chat"
        )

        return Response(
            {
                "success": True,
                "email": user_email,
                "message": "New chat created",
                "session_id": new_session_id
            },
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return Response(
            {"success": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
'''@extend_schema(
    responses={
        200: ChatHistoryResponseSerializer,
        401: dict,
        500: dict,
    },
    summary="Get chat history",
    description="Retrieve chat history for the current session."
)

@api_view(["GET"])
def get_chat_history(request):
    """
    Get chat history for the current session.
    """
    try:
        user_email = request.session.get("user_email")
        session_id = request.session.get("session_id")

        if not user_email or not session_id:
            return Response(
                {"success": False, "message": "Not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            chat_session = ChatSession.objects.get(
                session_id=session_id,
                user_email=user_email
            )

            return Response(
                {
                    "success": True,
                    "email": user_email,
                    "chat_history": json.loads(chat_session.chat_history),
                    "stm_context": json.loads(chat_session.stm_context),
                    "title": chat_session.title
                },
                status=status.HTTP_200_OK
            )

        except ChatSession.DoesNotExist:
            # 🔹 Fallback for new / missing session
            return Response(
                {
                    "success": True,
                    "chat_history": [],
                    "stm_context": [],
                    "title": "New Chat"
                },
                status=status.HTTP_200_OK
            )

    except Exception as e:
        return Response(
            {"success": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
'''

@extend_schema(
    parameters=[
        OpenApiParameter(
            name="email",
            type=str,
            location=OpenApiParameter.QUERY,
            required=True,
            description="User email used to identify chat history"
        ),
        OpenApiParameter(
            name="session_id",
            type=str,
            location=OpenApiParameter.QUERY,
            required=True,
            description="Chat session identifier"
        ),
    ],
    responses={
        200: ChatHistoryResponseSerializer,
        400: dict,
        500: dict,
    },
    summary="Get chat history",
    description="Retrieve chat history using email and session_id without session authentication."
)
@api_view(["GET"])
def get_chat_history(request):
    try:
        user_email = request.query_params.get("email")
        session_id = request.query_params.get("session_id")

        if not user_email or not session_id:
            return Response(
                {
                    "success": False,
                    "message": "email and session_id are required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            chat_session = ChatSession.objects.get(
                session_id=session_id,
                user_email=user_email
            )

            raw_history = json.loads(chat_session.chat_history)
            formatted_history = []

            i = 0
            while i < len(raw_history):
                if raw_history[i]["role"] == "user":
                    user_msg = raw_history[i].get("content", "")
                    assistant_msg = ""
                    audio_path = None
                    sources = []
                    suggestions = []

                    # Check next message
                    if i + 1 < len(raw_history) and raw_history[i + 1]["role"] == "assistant":
                        assistant_data = raw_history[i + 1]
                        assistant_msg = assistant_data.get("content", "")
                        audio_path = assistant_data.get("audio_path")
                        sources = assistant_data.get("sources", [])
                        suggestions = assistant_data.get("suggestions", [])

                        i += 1  # skip assistant since it's paired

                    formatted_history.append({
                        "user": user_msg,
                        "assistant": assistant_msg,
                        "audio_path": audio_path,
                        "sources": sources,
                        "suggestions": suggestions
                    })

                i += 1

            return Response(
                {
                    "success": True,
                    "data": formatted_history
                },
                status=status.HTTP_200_OK
            )

        except ChatSession.DoesNotExist:
            return Response(
                {
                    "success": True,
                    "data": []
                },
                status=status.HTTP_200_OK
            )

    except Exception as e:
        return Response(
            {
                "success": False,
                "message": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


'''@extend_schema(
    responses={
        200: AllSessionsResponseSerializer,
        401: dict,
        500: dict,
    },
    summary="Get all chat sessions",
    description="Retrieve all chat sessions for the authenticated user."
)
@api_view(["GET"])
def get_all_sessions(request):
    """
    Get all chat sessions for the authenticated user.
    """
    try:
        user_email = request.session.get("user_email")
        if not user_email:
            return Response(
                {"success": False, "message": "Not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        sessions = (
            ChatSession.objects
            .filter(user_email=user_email)
            .order_by("-updated_at")
        )

        session_list = [
            {
                "session_id": session.session_id,
                "title": session.title,
                "created_at": session.created_at.isoformat(),
                "updated_at": session.updated_at.isoformat(),
            }
            for session in sessions
        ]

        return Response(
            {
                "email": user_email,
                "success": True,
                "sessions": session_list
            },
            status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response(
            {"success": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )'''


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="email",
            type=str,
            location=OpenApiParameter.QUERY,
            required=True,
            description="User email used to retrieve chat sessions"
        )
    ],
    responses={
        200: AllSessionsResponseSerializer,
        400: dict,
        500: dict,
    },
    summary="Get all chat sessions",
    description="Retrieve all chat sessions using email without session authentication."
)
@api_view(["GET"])
def get_all_sessions(request):
    try:
        # 🔹 Read email from query params
        user_email = request.query_params.get("email")

        if not user_email:
            return Response(
                {
                    "success": False,
                    "message": "email is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        sessions = (
            ChatSession.objects
            .filter(user_email=user_email)
            .order_by("-updated_at")
        )

        session_list = [
            {
                "session_id": session.session_id,
                "title": session.title,
                "created_at": session.created_at.isoformat(),
                "updated_at": session.updated_at.isoformat(),
            }
            for session in sessions
        ]

        return Response(
            {
                "email": user_email,
                "success": True,
                "sessions": session_list
            },
            status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response(
            {"success": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@extend_schema(
    request=LoadSessionRequestSerializer,
    responses={
        200: LoadSessionResponseSerializer,
        400: dict,
        401: dict,
        404: dict,
        500: dict,
    },
    summary="Load chat session",
    description="Loads an existing chat session and sets it as the active session."
)
@api_view(["POST"])
def load_session(request):
    """
    Load an existing chat session and make it active.
    POST /api/load-session/
    """
    try:
        serializer = LoadSessionRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_email = serializer.validated_data["email"]
        session_id = str(serializer.validated_data["session_id"])
        if not user_email:
            return Response(
                {"success": False, "message": "Not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            chat_session = ChatSession.objects.get(
                session_id=session_id,
                user_email=user_email
            )

            # 🔹 Set active session
            request.session["session_id"] = session_id

            return Response(
                {
                    "success": True,
                    "email": user_email,
                    "session_id": session_id,
                    "title": chat_session.title,
                    "chat_history": json.loads(chat_session.chat_history),
                    #"stm_context": json.loads(chat_session.stm_context),
                },
                status=status.HTTP_200_OK
            )

        except ChatSession.DoesNotExist:
            return Response(
                {"success": False, "message": "Session not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    except Exception as e:
        return Response(
            {"success": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

def run_rag_mode(question_en, country, sector, language, lang_code, stm_context):
    """
    Run standard RAG mode with internal knowledge base.
    
    Returns:
        tuple: (final_answer, english_answer)
    """
    if not SUMMARY_VECTORDB or not CONTENT_VECTORDB:
        english_answer = "Internal RAG Index not loaded."
        return english_answer, english_answer
    
    # Add country/sector context if not in question
    current_country = country.lower()
    current_sector = sector.lower()
    
    search_context = ""
    if (
        current_country not in question_en.lower()
        and current_sector not in question_en.lower()
    ):
        search_context = f" in {current_country} {current_sector} sector"
    
    enhanced_question = question_en + search_context
    
    # Retrieve from FAISS
    top5_sum_docs = SUMMARY_VECTORDB.as_retriever(
        search_kwargs={"k": 5}
    ).invoke(enhanced_question)
    
    top5_cont_docs = CONTENT_VECTORDB.as_retriever(
        search_kwargs={"k": 5}
    ).invoke(enhanced_question)
    
    # Filter and rank
    top_docs = filter_content_by_summary_tfidf(
        top5_sum_docs,
        top5_cont_docs,
        top_n=5
    )
    
    rag_context = (
        "\n\n".join(d.page_content for d in top_docs)
        if top_docs else "No RAG data."
    )
    
    # Build prompt with STM context
    conversation_context = stm_handler.get_conversation_summary(stm_context)
    
    full_prompt = stm_handler.create_contextualized_prompt(
        prompt,
        rag_context,
        question_en,
        country,
        sector,
        conversation_context
    )
    
    # Generate answer
    english_answer = safe_llm_invoke(full_prompt)
    final_answer = english_answer
    
    # Translate if needed
    if (
        lang_code
        and lang_code != "en"
        and language.lower() != "english"
        and not any(p in english_answer.lower() for p in fallback_phrases)
    ):
        try:
            final_answer = GoogleTranslator(
                source="en",
                target=lang_code
            ).translate(english_answer)
        except Exception:
            pass
    
    return final_answer, english_answer


def run_enhance_mode(question_en, country, sector, language, lang_code, stm_context):
    """
    Run enhanced mode with web search integration.
    
    Returns:
        tuple: (final_answer, english_answer)
    """
    if not SUMMARY_VECTORDB or not CONTENT_VECTORDB:
        english_answer = "Internal RAG Index not loaded."
        return english_answer, english_answer
    
    # Add country/sector context if not in question
    current_country = country.lower()
    current_sector = sector.lower()
    
    search_context = ""
    if (
        current_country not in question_en.lower()
        and current_sector not in question_en.lower()
    ):
        search_context = f" in {current_country} {current_sector} sector"
    
    enhanced_question = question_en + search_context
    
    # Retrieve from FAISS
    top5_sum_docs = SUMMARY_VECTORDB.as_retriever(
        search_kwargs={"k": 5}
    ).invoke(enhanced_question)
    
    top5_cont_docs = CONTENT_VECTORDB.as_retriever(
        search_kwargs={"k": 5}
    ).invoke(enhanced_question)
    
    # Filter and rank
    top_docs = filter_content_by_summary_tfidf(
        top5_sum_docs,
        top5_cont_docs,
        top_n=5
    )
    
    rag_context = (
        "\n\n".join(d.page_content for d in top_docs)
        if top_docs else "No RAG data."
    )
    
    # Build conversation context
    conversation_context = stm_handler.get_conversation_summary(stm_context)
    
    # Process with enhance module
    final_answer, english_answer = enhance.process_enhance_mode(
        LLM,
        question_en,
        rag_context,
        country,
        sector,
        language,
        lang_code,
        conversation_context
    )
    
    return final_answer, english_answer   

"""@extend_schema(
    request=ChatRequestSerializer,
    responses={
        200: ChatResponseSerializer,
        400: dict,
        401: dict,
        500: dict,
    },
    summary="Chat with AI",
    description="Main chat endpoint supporting normal, enhance, and deep research modes."
)"""




def is_fallback_response(answer_text):
    """
    Check if the response is a fallback/no-information response
    """
    fallback_indicators = [
        "sorry, no detailed content found",
        "sorry, no relevant information",
        "no relevant information is available",
        "no relevant information",
        "provided context does not contain",
        "i am sorry",
        "no relevant data found",
        "no detailed content found",
        "no information found",
        "context does not contain",
        "unable to find information",
        "information is not available",
        "no data available",
        "cannot find relevant",
        "does not have information"
    ]
    
    answer_lower = answer_text.lower().strip()
    
    # Check for fallback phrases
    if any(phrase in answer_lower for phrase in fallback_indicators):
        return True
    
    # Check if response is suspiciously short (less than 100 chars suggests no real answer)
    if len(answer_lower) < 100:
        return True
        
    return False


def run_rag_mode(question_en, country, sector, language, lang_code, stm_context):
    """
    Run standard RAG mode with internal knowledge base.
    Falls back to deep research if no relevant answer found.
    
    Returns:
        tuple: (final_answer, english_answer, urls_display, is_deep_research_used)
    """
    if not SUMMARY_VECTORDB or not CONTENT_VECTORDB:
        english_answer = "Internal RAG Index not loaded."
        return english_answer, english_answer, [], False
    
    # Add country/sector context if not in question
    current_country = country.lower()
    current_sector = sector.lower()
    
    search_context = ""
    if (
        current_country not in question_en.lower()
        and current_sector not in question_en.lower()
    ):
        search_context = f" in {current_country} {current_sector} sector"
    
    enhanced_question = question_en + search_context
    
    # Retrieve from FAISS
    top5_sum_docs = SUMMARY_VECTORDB.as_retriever(
        search_kwargs={"k": 5}
    ).invoke(enhanced_question)
    
    top5_cont_docs = CONTENT_VECTORDB.as_retriever(
        search_kwargs={"k": 5}
    ).invoke(enhanced_question)
    
    # Filter and rank
    top_docs = filter_content_by_summary_tfidf(
        top5_sum_docs,
        top5_cont_docs,
        top_n=5
    )
    
    rag_context = (
        "\n\n".join(d.page_content for d in top_docs)
        if top_docs else "No RAG data."
    )
    
    # Build prompt with STM context
    conversation_context = stm_handler.get_conversation_summary(stm_context)
    
    full_prompt = stm_handler.create_contextualized_prompt(
        prompt,
        rag_context,
        question_en,
        country,
        sector,
        conversation_context
    )
    
    # Generate answer
    english_answer = safe_llm_invoke(full_prompt)
    
    # Check if answer is a fallback response
    if is_fallback_response(english_answer):
        print(f"⚠️ RAG Mode: No relevant answer found. Falling back to Deep Research...")
        
        # Fall back to deep research
        agent = deep.DeepResearchAgent(SERPAPI_KEY)
        urls_display, final_answer, english_answer = asyncio.run(
            agent.process(
                LLM,
                country,
                sector,
                question_en,
                language,
                lang_code or "en",
                stm_context,
                mode="rag"  # Pass mode to maintain RAG prompt style
            )
        )
        
        return final_answer, english_answer, urls_display, True
    
    # Normal RAG response - translate if needed
    final_answer = english_answer
    
    if (
        lang_code
        and lang_code != "en"
        and language.lower() != "english"
        and not any(p in english_answer.lower() for p in fallback_phrases)
    ):
        try:
            final_answer = GoogleTranslator(
                source="en",
                target=lang_code
            ).translate(english_answer)
        except Exception:
            pass
    
    return final_answer, english_answer, [], False


def run_enhance_mode(question_en, country, sector, language, lang_code, stm_context):
    """
    Run enhanced mode with web search integration.
    Falls back to deep research if no relevant answer found.
    
    Returns:
        tuple: (final_answer, english_answer, urls_display, is_deep_research_used)
    """
    if not SUMMARY_VECTORDB or not CONTENT_VECTORDB:
        english_answer = "Internal RAG Index not loaded."
        return english_answer, english_answer, [], False
    
    # Add country/sector context if not in question
    current_country = country.lower()
    current_sector = sector.lower()
    
    search_context = ""
    if (
        current_country not in question_en.lower()
        and current_sector not in question_en.lower()
    ):
        search_context = f" in {current_country} {current_sector} sector"
    
    enhanced_question = question_en + search_context
    
    # Retrieve from FAISS
    top5_sum_docs = SUMMARY_VECTORDB.as_retriever(
        search_kwargs={"k": 5}
    ).invoke(enhanced_question)
    
    top5_cont_docs = CONTENT_VECTORDB.as_retriever(
        search_kwargs={"k": 5}
    ).invoke(enhanced_question)
    
    # Filter and rank
    top_docs = filter_content_by_summary_tfidf(
        top5_sum_docs,
        top5_cont_docs,
        top_n=5
    )
    
    rag_context = (
        "\n\n".join(d.page_content for d in top_docs)
        if top_docs else "No RAG data."
    )
    
    # Build conversation context
    conversation_context = stm_handler.get_conversation_summary(stm_context)
    
    # Process with enhance module
    final_answer, english_answer = enhance.process_enhance_mode(
        LLM,
        question_en,
        rag_context,
        country,
        sector,
        language,
        lang_code,
        conversation_context
    )
    
    # Check if answer is a fallback response
    if is_fallback_response(english_answer):
        print(f"⚠️ Enhance Mode: No relevant answer found. Falling back to Deep Research...")
        
        # Fall back to deep research
        agent = deep.DeepResearchAgent(SERPAPI_KEY)
        urls_display, final_answer, english_answer = asyncio.run(
            agent.process(
                LLM,
                country,
                sector,
                question_en,
                language,
                lang_code or "en",
                stm_context,
                mode="enhance"  # Pass mode to maintain Enhance prompt style
            )
        )
        
        return final_answer, english_answer, urls_display, True
    
    return final_answer, english_answer, [], False

uae_shariat_template = """
You are an AI-powered Compliance Assistant for the Central Bank of Bahrain (CBB). Your role is to help financial institutions, fintechs, and regulators quickly understand Bahrain’s regulatory requirements. Your answers are brief, on-point, and mostly rulebook-driven, but with a touch of human clarity and interpretation.

### **Response Style & Guidelines:**  
- Use **bullet points only**.  
- Keep it **brief, clear, and professional** — no long explanations.  
- **70% content should be directly from the CBB Rulebook**.  
- **30% can be natural/human-style interpretation or simplification**.  
- **Do NOT include citations within the bullet points.**  
- **Mention all relevant rulebook modules/sections at the end only.**  
- **No large paragraphs** — just compact, action-ready info.  
- Be clear when **CBB confirmation or review is required**.

---

### **User Context:**  
**Context:** {context}  
**History:** {history}  

---

### **User Query:**  
**User:** {question}  

---

### **Assistant Response:**  
[Respond with bullet points only, blending rulebook-based accuracy with crisp human-friendly wording.]

---

### **Citations:**  
[List the relevant rulebook parts and modules used, such as: Part 3 – Modules AU, CA, CG, etc.]

Source Links:  
cbb-rulebook: https://cbben.thomsonreuters.com/cbb-rulebook  
conventional bank part a: https://cbben.thomsonreuters.com/rulebook/part-1  
conventional bank part b: https://cbben.thomsonreuters.com/rulebook/part-b-1  
islamic bank part a: https://cbben.thomsonreuters.com/rulebook/part-2  
islamic bank part b: https://cbben.thomsonreuters.com/rulebook/part-b-2  
Insurance part a: https://cbben.thomsonreuters.com/rulebook/part-3  
Insurance part b: https://cbben.thomsonreuters.com/rulebook/part-b-3  
Investment Business part a: https://cbben.thomsonreuters.com/rulebook/part-4  
Investment Business part b: https://cbben.thomsonreuters.com/rulebook/part-b-4  
Capital Markets part a: https://cbben.thomsonreuters.com/rulebook/part-13  
Capital Markets part b: https://cbben.thomsonreuters.com/rulebook/part-b-6  
Collective Investment Undertakings part a: https://cbben.thomsonreuters.com/rulebook/part-15  
Collective Investment Undertakings part b: https://cbben.thomsonreuters.com/rulebook/part-b-8


"""

uae_shariat_prompt = PromptTemplate(
    input_variables=["history", "context", "question"],
    template=uae_shariat_template,
)


# Add this section after your existing imports and before the chat function

# =========================
# SHARIAT SECTOR HANDLING
# =========================

SHARIAT_PROMPT_TEMPLATE = """You are an AI-powered Compliance Assistant for the Central Bank of Bahrain (CBB). Your role is to help financial institutions, fintechs, and regulators quickly understand Bahrain's regulatory requirements. Your answers are brief, on-point, and mostly rulebook-driven, but with a touch of human clarity and interpretation.

### **Response Style & Guidelines:**  
- Use **bullet points only**.  
- Keep it **brief, clear, and professional** — no long explanations.  
- **70% content should be directly from the CBB Rulebook**.  
- **30% can be natural/human-style interpretation or simplification**.  
- **Do NOT include citations within the bullet points.**  
- **Mention all relevant rulebook modules/sections at the end only.**  
- **No large paragraphs** — just compact, action-ready info.  
- Be clear when **CBB confirmation or review is required**.

---

### **User Context:**  
**Context:** {context}  
**History:** {history}  

---

### **User Query:**  
**User:** {question}  in CBB and Shariat Governance

---

### **Assistant Response:**  
[Respond with bullet points only, blending rulebook-based accuracy with crisp human-friendly wording.]

---

### **Citations:**  
[List the relevant rulebook parts and modules used, such as: Part 3 – Modules AU, CA, CG, etc.]

Source Links:  
cbb-rulebook: https://cbben.thomsonreuters.com/cbb-rulebook  
conventional bank part a: https://cbben.thomsonreuters.com/rulebook/part-1  
conventional bank part b: https://cbben.thomsonreuters.com/rulebook/part-b-1  
islamic bank part a: https://cbben.thomsonreuters.com/rulebook/part-2  
islamic bank part b: https://cbben.thomsonreuters.com/rulebook/part-b-2  
Insurance part a: https://cbben.thomsonreuters.com/rulebook/part-3  
Insurance part b: https://cbben.thomsonreuters.com/rulebook/part-b-3  
Investment Business part a: https://cbben.thomsonreuters.com/rulebook/part-4  
Investment Business part b: https://cbben.thomsonreuters.com/rulebook/part-b-4  
Capital Markets part a: https://cbben.thomsonreuters.com/rulebook/part-13  
Capital Markets part b: https://cbben.thomsonreuters.com/rulebook/part-b-6  
Collective Investment Undertakings part a: https://cbben.thomsonreuters.com/rulebook/part-15  
Collective Investment Undertakings part b: https://cbben.thomsonreuters.com/rulebook/part-b-8
"""

SHARIAT_PROMPT = PromptTemplate(
    input_variables=["history", "context", "question"],
    template=SHARIAT_PROMPT_TEMPLATE,
)


def is_shariat_sector(country, sector):
    """Check only if country is UAE (sector ignored)"""
    return country.lower() in ["uae", "united arab emirates"]


async def run_shariat_mode_async(question_en, country, sector, language, lang_code, stm_context, mode):
    """
    Unified Shariat handler for UAE supporting Enhance (Direct Prompt) 
    and Deep (Web Search) modes.
    """
    
    # --- 1. DEEP SEARCH MODE (Web Search via SerpApi) ---
    if mode == "deep":
        # Uses DeepResearchAgent to find live CBB/UAE updates
        agent = deep.DeepResearchAgent(SERPAPI_KEY)
        urls_display, final_answer, english_answer = await agent.process(
            llm=LLM, 
            country=country, 
            sector=sector, 
            question=question_en, 
            language=language, 
            lang_code=lang_code or "en", 
            stm_context=stm_context,
            mode="shariat" # Triggers the CBB-specific summary prompt in deep.py
        )
        return final_answer, english_answer, urls_display, True

    # --- 2. ENHANCE MODE (Direct LLM Persona - No RAG/FAISS) ---
    elif mode == "enhance":
        # Build conversation context from memory
        conversation_context = stm_handler.get_conversation_summary(stm_context)
        
        # Expert persona prompt for detailed UAE regulatory analysis
        enhance_prompt = f"""You are an AI-powered Compliance Assistant for the Central Bank of Bahrain (CBB).
Your role is to help financial institutions, fintechs, and regulators clearly understand Bahrain's regulatory and Shariat governance requirements using current live information.

### **Response Style & Guidelines**
- Provide a **DETAILED and COMPREHENSIVE explanation**, not brief summaries.
- Use **structured bullet sections**, but expand each point with clear explanation.
- Each major requirement should include:
  - What the rule requires
  - Why it exists (regulatory purpose)
  - How institutions implement it in practice
  - Risks or penalties if not followed
- **70% content must reflect rulebook-based regulatory meaning** derived from researched content.
- **30% can be expert interpretation, clarification, and practical guidance.**
- Write in a **professional regulatory advisory tone**.
- Be clear when **CBB approval, reporting, or supervisory review is required**.
- Explain governance responsibilities (Board, Sharia Board, Compliance, Audit where relevant).
- Include **practical operational impact** on financial institutions.
- Provide **realistic compliance examples** when helpful.
- Do NOT insert citations inside explanations.
- At the end, list all relevant **CBB Rulebook modules and sections referenced**.
- After that, list **source links**.


---

### **User Query:** **User:** Current requirements in CBB and Shariat Governance regarding this topic.

---

### **Assistant Response Structure**

1. Regulatory Overview  
2. Core Shariat Governance Requirements  
3. Institutional Responsibilities  
4. Operational Implementation  
5. Compliance Risks and Supervisory Expectations  
6. Practical Example or Scenario  
7. Key Takeaways for Institutions  

Provide a **deep, structured, expert-level explanation**.

---

### **Citations:** [List the relevant rulebook parts and modules identified, such as: Part 2 – Modules HC, AU, etc.]


Source Links:  
cbb-rulebook: https://cbben.thomsonreuters.com/cbb-rulebook  
conventional bank part a: https://cbben.thomsonreuters.com/rulebook/part-1  
conventional bank part b: https://cbben.thomsonreuters.com/rulebook/part-b-1  
islamic bank part a: https://cbben.thomsonreuters.com/rulebook/part-2  
islamic bank part b: https://cbben.thomsonreuters.com/rulebook/part-b-2  
Insurance part a: https://cbben.thomsonreuters.com/rulebook/part-3  
Insurance part b: https://cbben.thomsonreuters.com/rulebook/part-b-3  
Investment Business part a: https://cbben.thomsonreuters.com/rulebook/part-4  
Investment Business part b: https://cbben.thomsonreuters.com/rulebook/part-b-4  
Capital Markets part a: https://cbben.thomsonreuters.com/rulebook/part-13  
Capital Markets part b: https://cbben.thomsonreuters.com/rulebook/part-b-6  
Collective Investment Undertakings part a: https://cbben.thomsonreuters.com/rulebook/part-15  
Collective Investment Undertakings part b: https://cbben.thomsonreuters.com/rulebook/part-b-8

        """
        
        english_answer = safe_llm_invoke(enhance_prompt)
        final_answer = english_answer
        
        # Translation logic for Enhance mode
        if lang_code and lang_code != "en" and language.lower() != "english":
            try:
                final_answer = GoogleTranslator(source="en", target=lang_code).translate(english_answer)
            except Exception:
                pass
                
        return final_answer, english_answer, [], False

    # --- 3. STANDARD RAG MODE (Existing Logic) ---
    else:
        # Fallback to existing FAISS retrieval and SHARIAT_PROMPT logic
        if not SUMMARY_VECTORDB or not CONTENT_VECTORDB:
            english_answer = "Internal RAG Index not loaded."
            return english_answer, english_answer, [], False

        search_context = f" under Central Bank of Bahrain regulations"
        enhanced_question = question_en + search_context
        
        top5_sum_docs = SUMMARY_VECTORDB.as_retriever(search_kwargs={"k": 5}).invoke(enhanced_question)
        top5_cont_docs = CONTENT_VECTORDB.as_retriever(search_kwargs={"k": 5}).invoke(enhanced_question)
        top_docs = filter_content_by_summary_tfidf(top5_sum_docs, top5_cont_docs, top_n=5)
        
        rag_context = "\n\n".join(d.page_content for d in top_docs) if top_docs else "No relevant data."
        conversation_context = stm_handler.get_conversation_summary(stm_context)
        
        full_prompt = SHARIAT_PROMPT.format(
            context=rag_context,
            history=conversation_context,
            question=question_en
        )
        
        english_answer = safe_llm_invoke(full_prompt)
        final_answer = english_answer
        
        if lang_code and lang_code != "en" and language.lower() != "english":
            try:
                final_answer = GoogleTranslator(source="en", target=lang_code).translate(english_answer)
            except Exception:
                pass
                
        return final_answer, english_answer, [], False

# Synchronous wrapper used by the Django view
def run_shariat_mode(question_en, country, sector, language, lang_code, stm_context, mode):
    return asyncio.run(run_shariat_mode_async(question_en, country, sector, language, lang_code, stm_context, mode))

# =========================
# UPDATE ALLOWED SECTORS
# =========================

# Update your ALLOWED_SECTORS constant
ALLOWED_SECTORS = {"Banking", "Finance", "Healthcare", "Environment", "Shariat", "Ancillary Service Providers","Banking and Fintech", "Cryptocurrency and Blockchain related Services", "Financial Advisory Services", "Fund Management & Custodian", "Insurtech", "Investment and wealth management platforms", "Lending platforms", "Payment service providers", "Regtech"}

# Update COUNTRY_SECTOR_MAP
COUNTRY_SECTOR_MAP = {
    "India": ["Banking", "Finance", "Healthcare", "Environment"],
    "US": ["Banking", "Finance", "Healthcare", "Environment"],
    "UAE": ["Ancillary Service Providers","Banking and Fintech", "Cryptocurrency and Blockchain related Services", "Financial Advisory Services", "Fund Management & Custodian", "Insurtech", "Investment and wealth management platforms", "Lending platforms", "Payment service providers", "Regtech", "Shariat"],
    "China": ["Banking", "Finance", "Healthcare", "Environment"]
}



def flatten_faqs(data):
    flat = []
    if isinstance(data, list):
        for x in data:
            flat.extend(flatten_faqs(x))
    elif isinstance(data, dict):
        flat.append(data)
    return flat


@extend_schema(
    request=ChatRequestSerializer,
    responses={
        200: ChatResponseSerializer,
        400: dict,
        401: dict,
        500: dict,
    },
    summary="Chat with AI",
    description="Main chat endpoint supporting normal, enhance, deep research modes, and Shariat compliance."
)
@api_view(["POST"])
def chat(request):
    try:
        serializer = ChatRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        session_id = serializer.validated_data["session_id"]
        question = serializer.validated_data["question"].strip()
        enhance_mode = serializer.validated_data["enhance_mode"]
        deep_research_mode = serializer.validated_data["deep_research_mode"]
        audio_path = None

        user_email = email

        if not email or not session_id:
            return Response(
                {"success": False, "message": "Not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not question:
            return Response(
                {"success": False, "message": "Question required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get user settings
        try:
            user_settings = UserSettings.objects.get(user_email=email)
            country = user_settings.country
            sector = user_settings.sector
            language = user_settings.language
        except UserSettings.DoesNotExist:
            country = list(ALLOWED_COUNTRIES)[0]
            sector = list(ALLOWED_SECTORS)[0]
            language = "English"
        
        # FAQ Check
        faqs_file_path = os.path.join(os.path.dirname(__file__), "FAQs.json")
        if os.path.exists(faqs_file_path):
            with open(faqs_file_path, "r", encoding="utf-8") as f:
                faqs_data = json.load(f)

            flat_faqs = flatten_faqs(faqs_data)
            for item in flat_faqs:
                if (
                    item.get("question","").strip().lower() == question.strip().lower()
                    and item.get("sector","").lower() == sector.lower()
                    and item.get("country","").lower() == country.lower()
                ):
                    return Response(
                        {
                            "success": True,
                            "answer": item.get("response"),
                            "is_faq": True,
                            "sources": [],
                            "suggestions": []
                        },
                        status=status.HTTP_200_OK
                    )

        # Load or create chat session
        chat_session, created = ChatSession.objects.get_or_create(
            session_id=session_id,
            defaults={
                "user_email": email,
                "chat_history": json.dumps([]),
                "stm_context": json.dumps([]),
                "title": question[:40],
            }
        )
        
        if not created and chat_session.user_email != email:
            return Response({"success": False, "message": "Session belongs to another user"}, status=403)
            
        chat_history = json.loads(chat_session.chat_history or "[]")
        stm_context = json.loads(chat_session.stm_context or "[]")

        lang_code = get_language_code(language)
        question_en = question

        # Translate incoming question to English for normalized processing
        if language.lower() != "english" and lang_code:
            try:
                question_en = GoogleTranslator(source="auto", target="en").translate(question)
            except Exception:
                pass
            
        # ✅ NEW: Capture the clean English question for the CACHE KEY before reframing
        cache_key_question = question_en

        # Identify if current sector is UAE/Shariat
        is_shariat = is_shariat_sector(country, sector)

        # ✅ Determine mode logic - DEFINE EARLY
        shariat_sub_mode = None
        if is_shariat:
            # Pass specific sub-mode for UAE Shariat handler
            shariat_sub_mode = "deep" if deep_research_mode else "enhance" if enhance_mode else "rag"
            mode = "shariat" 
        else:
            mode = "deep" if deep_research_mode else "enhance" if enhance_mode else "rag"

        # ==========================================
        # ✅ CACHE CHECK (Using clean cache_key_question)
        # ==========================================
        cache_lookup_mode = shariat_sub_mode if is_shariat else mode
        cached_data = get_cached_response(cache_key_question, country, sector, cache_lookup_mode)

        if cached_data:
            print(f"✅ Cache Hit for: {question} (mode: {cache_lookup_mode})")
            
            english_cached_answer = cached_data.get("answer")
            english_suggestions = cached_data.get("suggestions", [])
            final_cached_answer = english_cached_answer
            final_suggestions = english_suggestions

            # Translate if language is not English
            if language.lower() != "english" and lang_code:
                try:
                    # 1. Translate the Answer
                    translation_prompt = (
                        f"Translate to {language}. Return ONLY translation:\n\n{english_cached_answer}"
                    )
                    llm_response = LLM.invoke(translation_prompt)
                    final_cached_answer = llm_response.content.strip()

                    # 2. Translate the Suggestions
                    if english_suggestions:
                        final_suggestions = []
                        for sug in english_suggestions:
                            try:
                                translated_sug = GoogleTranslator(source="en", target=lang_code).translate(sug)
                                final_suggestions.append(translated_sug)
                            except Exception:
                                final_suggestions.append(sug) 
                    
                except Exception as e:
                    print(f"❌ Translation failed: {e}. Falling back to English.")
                    final_cached_answer = english_cached_answer
                    final_suggestions = english_suggestions

            # Save to STM and History
            stm_handler.add_to_stm(stm_context, question, final_cached_answer)

            chat_history.extend([
                {"role": "user", "content": question},
                {
                    "role": "assistant",
                    "content": final_cached_answer,
                    "sources": cached_data.get("sources", []),
                    "suggestions": final_suggestions,
                    "audio_path": cached_data.get("audio_path"),
                    "is_cached": True
                }
            ])

            chat_session.chat_history = json.dumps(chat_history)
            chat_session.stm_context = json.dumps(stm_context)
            chat_session.save()

            return Response({
                "success": True,
                "email": email,
                "session_id": session_id,
                "answer": final_cached_answer,
                "sources": cached_data.get("sources", []),
                "suggestions": final_suggestions,
                "audio_path": cached_data.get("audio_path"),
                "is_cached": True,
                "mode": cache_lookup_mode
            }, status=status.HTTP_200_OK)
        # ==========================================
# ✅ NEW: SHARIAT → FIRST CHECK GLOBAL EXPANSION CACHE
# ==========================================
        if is_shariat:
            cached_ge = get_cached_response(cache_key_question, None, None, "global_expansion")

            if cached_ge:
                print("✅ SHARIAT GLOBAL EXPANSION CACHE HIT")

                final_answer_ge = cached_ge["answer"]

                # translate if needed
                if language.lower() != "english" and lang_code:
                    try:
                        final_answer_ge = GoogleTranslator(
                            source="en", target=lang_code
                        ).translate(final_answer_ge)
                    except:
                        pass

                # save stm + history
                stm_handler.add_to_stm(stm_context, question, final_answer_ge)

                chat_history.extend([
                    {"role": "user", "content": question},
                    {
                        "role": "assistant",
                        "content": final_answer_ge,
                        "sources": [],
                        "suggestions": [],
                        "audio_path": None,
                        "is_cached": True,
                        "mode": "global_expansion"
                    }
                ])

                chat_session.chat_history = json.dumps(chat_history)
                chat_session.stm_context = json.dumps(stm_context)
                chat_session.save()

                return Response({
                    "success": True,
                    "email": email,
                    "session_id": session_id,
                    "answer": final_answer_ge,
                    "sources": [],
                    "suggestions": [],
                    "audio_path": None,
                    "is_cached": True,
                    "mode": "global_expansion"
                }, status=status.HTTP_200_OK)

            print("❌ SHARIAT GLOBAL EXPANSION CACHE MISS → continue Shariat flow")


        # ==========================================
        # ✅ INTENT DETECTION (Use clean English question)
        # ==========================================
        if not is_shariat:
            intent_result = intent.classify_intent(LLM, cache_key_question, country, sector)
            detected_intent = intent_result.get("intent", "compliance_requirements")
            print(f"Detected Intent: {detected_intent}")
        else:
            detected_intent = "shariat_compliance"
            print("Shariat Mode Activated")

        # ==========================================
        # ✅ GLOBAL EXPANSION INTENT
        # ==========================================
        if detected_intent == "business_global_expansion":
            cached_ge = get_cached_response(cache_key_question, None, None, "global_expansion")
            if cached_ge:
                print("✅ GLOBAL EXPANSION CACHE HIT")
                final_answer_1 = cached_ge["answer"]
            else:
                print("❌ GLOBAL EXPANSION CACHE MISS")
                final_answer_1 = run_all_sync(cache_key_question)
                save_to_cache(cache_key_question, final_answer_1, None, None, "global_expansion", [], [], None)

            if language.lower() != "english" and lang_code:
                try:
                    final_answer_1 = GoogleTranslator(source="en", target=lang_code).translate(final_answer_1)
                except: pass

            stm_handler.add_to_stm(stm_context, question, final_answer_1)
            chat_history.extend([
                {"role": "user", "content": question},
                {"role": "assistant", "content": final_answer_1, "sources": [], "suggestions": [], "audio_path": None}
            ])
            chat_session.chat_history = json.dumps(chat_history)
            chat_session.stm_context = json.dumps(stm_context)
            chat_session.save()

            return Response({
                "success": True, "email": user_email, "session_id": session_id,
                "answer": final_answer_1, "sources": [], "suggestions": [], "audio_path": None
            }, status=status.HTTP_200_OK)

        # ✅ REFRAME question with context for LLM processing (question_en is now "dirty" with context)
        if stm_context:
            question_en = stm_handler.reframe_question_with_context(LLM, question_en, stm_context, country, sector)

        urls_display = []
        final_answer = ""
        english_answer = ""
        suggestions = []
        deep_research_used = False

        # ==========================================
        # ✅ HANDLE SHARIAT MODE
        # ==========================================
        if is_shariat:
            final_answer, english_answer, urls_display, deep_research_used = run_shariat_mode(
                question_en, country, sector, language, lang_code, stm_context, shariat_sub_mode
            )
            if final_answer and not is_fallback_response(final_answer):
                suggestions = intent.generate_intent_suggestions(
                    llm=LLM, intent="shariat_compliance", question=question,
                    answer=english_answer, country=country, sector=sector, language=language
                )

        # ==========================================
        # ✅ HANDLE OTHER MODES
        # ==========================================
        else:
            mode_name = "deep_research_mode" if deep_research_mode else "enhance_mode" if enhance_mode else "rag_mode"
            intent_intro = intent.get_intent_intro(detected_intent, mode_name, country, sector)

            if detected_intent == "greeting":
                final_answer = intent_intro
                english_answer = intent_intro
            else:
                if deep_research_mode:
                    agent = deep.DeepResearchAgent(SERPAPI_KEY)
                    urls_display, final_answer, english_answer = asyncio.run(
                        agent.process(LLM, country, sector, question_en, language, lang_code or "en", stm_context, mode="deep")
                    )
                    deep_research_used = True
                elif enhance_mode:
                    final_answer, english_answer, urls_display, deep_research_used = run_enhance_mode(
                        question_en, country, sector, language, lang_code, stm_context
                    )
                else:
                    final_answer, english_answer, urls_display, deep_research_used = run_rag_mode(
                        question_en, country, sector, language, lang_code, stm_context
                    )

                if final_answer:
                    suggestions = intent.generate_intent_suggestions(
                        llm=LLM, intent=detected_intent, question=question,
                        answer=english_answer, country=country, sector=sector, language=language
                    )

        # ==========================================
        # ✅ SAVE TO CACHE (Using clean cache_key_question)
        # ==========================================
        if final_answer and not is_fallback_response(final_answer):
            final_cache_mode = shariat_sub_mode if is_shariat else mode
            save_to_cache(cache_key_question, english_answer, country, sector, final_cache_mode, suggestions, urls_display, audio_path)

        stm_handler.add_to_stm(stm_context, question, final_answer)
        chat_history.extend([
            {"role": "user", "content": question},
            {"role": "assistant", "content": final_answer, "sources": urls_display, "suggestions": suggestions, "audio_path": None}
        ])

        chat_session.chat_history = json.dumps(chat_history)
        chat_session.stm_context = json.dumps(stm_context)
        chat_session.save()

        return Response({
            "success": True, "email": user_email, "session_id": session_id,
            "answer": final_answer, "sources": urls_display, "suggestions": suggestions, "audio_path": None,
        }, status=status.HTTP_200_OK)

    except Exception as e:
        traceback.print_exc()
        return Response({"success": False, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@extend_schema(
    request=FeedbackSubmitRequestSerializer,
    responses={
        201: FeedbackSubmitResponseSerializer,
        400: dict,
        401: dict,
        500: dict,
    },
    summary="Submit feedback for AI response",
    description="Submit thumbs up/down feedback along with session_id and email."
)
@api_view(["POST"])
def feedback_submit(request):
    """
    Submit feedback for an AI response.

    POST /api/feedback/

    Request body:
    {
        "email": "user@gmail.com",
        "session_id": "1234-uuid-session",
        "question": "What are RBI regulations?",
        "answer": "RBI regulates banks through...",
        "feedback_type": "Up",
        "feedback_text": "Very helpful explanation"
    }
    """
    try:
        # ✅ Validate Input
        serializer = FeedbackSubmitRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        session_id = serializer.validated_data["session_id"]

        question = serializer.validated_data["question"]
        answer = serializer.validated_data["answer"]

        feedback_type = serializer.validated_data["feedback_type"]
        feedback_text = serializer.validated_data.get("feedback_text", "")

        # ✅ Save Feedback in DB
        Feedback.objects.create(
            user_email=email,
            session_id=session_id,   # ✅ NEW
            question=question,
            answer=answer,
            feedback_type=feedback_type,
            feedback_text=feedback_text
        )

        return Response(
            {
                "success": True,
                "email": email,
                "session_id": session_id,
                "message": "Feedback saved successfully"
            },
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        traceback.print_exc()
        return Response(
            {"success": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


"""@extend_schema(
    request=None,  # No request body
    responses={
        200: VoiceToTextResponseSerializer,
        401: dict,
        500: dict,
    },
    summary="Convert voice to text",
    description="Convert user voice input to text based on their preferred language setting. Uses the language from user settings."
)
@api_view(["POST"])
def voice_to_text(request):
    
    Convert user voice input to text based on user's language.

    POST /api/voice-to-text/
    
    No request body required - uses microphone input and user's language preference.
    
    try:
        # 🔐 Authentication check
        user_email = request.session.get("user_email")
        if not user_email:
            return Response(
                {"success": False, "message": "Not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # 🔹 Get user's preferred language
        try:
            user_settings = UserSettings.objects.get(user_email=user_email)
            language = user_settings.language
        except UserSettings.DoesNotExist:
            language = "English"

        # 🔹 Process voice-to-text
        translated_text = vtt_utils.start_vtt_pipeline(language)

        if translated_text:
            return Response(
                {
                    "success": True,
                    "text": translated_text
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                "success": False,
                "message": "Voice recognition failed"
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response(
            {"success": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )"""


@extend_schema(
    request=VoiceToTextRequestSerializer,
    responses={
        200: VoiceToTextResponseSerializer,
        400: dict,
        401: dict,
        500: dict,
    },
    summary="Convert voice to text",
    description="Upload an audio file to convert speech into text"
)
@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def voice_to_text(request):
    try:
        # 🔐 Auth
        user_email = request.session.get("user_email")
        if not user_email:
            return Response(
                {"success": False, "message": "Not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # 🎧 Audio file
        audio_file = request.FILES.get("audio")
        if not audio_file:
            return Response(
                {"success": False, "message": "Audio file is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ⚙️ User settings
        try:
            settings_obj = UserSettings.objects.get(user_email=user_email)
            language = settings_obj.language
            country = settings_obj.country
            sector = settings_obj.sector
        except UserSettings.DoesNotExist:
            language = "English"
            country = "India"
            sector = "Banking"

        # 🔊 Audio → Text
        text = vtt_utils.audio_file_to_text(audio_file, language)

        if not text:
            return Response(
                {"success": False, "message": "Voice recognition failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {
                "success": True,
                "email": user_email,
                "text": text,
                "language": language,
                "country": country,
                "sector": sector
            },
            status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response(
            {"success": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@extend_schema(
    request=TextToSpeechRequestSerializer,
    responses={
        200: TextToSpeechResponseSerializer,
        400: dict,
        401: dict,
        500: dict,
    },
    summary="Convert text to speech",
    description="Generate audio only when user clicks mic."
)
@api_view(["POST"])
def text_to_speech(request):
    try:
        serializer = TextToSpeechRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_email = serializer.validated_data["email"]
        text = serializer.validated_data["text"]

        if not user_email:
            return Response(
                {"success": False, "message": "Not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # ✅ User preferred language
        try:
            user_settings = UserSettings.objects.get(user_email=user_email)
            language = user_settings.language
        except UserSettings.DoesNotExist:
            language = "English"

        # ✅ Generate speech ONLY NOW
        audio_data = tts.generate_speech(text, language, LANGUAGE_CSV)

        if not audio_data:
            return Response(
                {"success": False, "message": "TTS failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # ✅ Save audio file
        file_name = f"{uuid.uuid4()}.mp3"
        file_path = os.path.join(settings.TTS_AUDIO_DIR, file_name)

        with open(file_path, "wb") as f:
            f.write(audio_data)

        # ✅ Return accessible URL
        audio_url = request.build_absolute_uri(
            f"{settings.MEDIA_URL}tts_audio/{file_name}"
        )

        return Response(
            {
                "success": True,
                "audio_path": audio_url
            },
            status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response(
            {"success": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@extend_schema(
    request=RewriteRequestSerializer,
    responses={200: ChatResponseSerializer},
    summary="Rewrite AI Response",
    description="Regenerates assistant response for the same user question."
)
@api_view(["POST"])
def rewrite_response(request):

    try:
        serializer = RewriteRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        session_id = serializer.validated_data["session_id"]
        question = serializer.validated_data["question"].strip()

        # ✅ SAFETY CHECK: Ensure RAG + LLM Loaded
        global LLM, SUMMARY_VECTORDB, CONTENT_VECTORDB
        if LLM is None or SUMMARY_VECTORDB is None or CONTENT_VECTORDB is None:
            print("⚠️ Rewrite: RAG not initialized. Reloading...")
            initialize_rag()

        # ✅ Load Session
        chat_session = ChatSession.objects.get(
            session_id=session_id,
            user_email=email
        )

        chat_history = json.loads(chat_session.chat_history)
        stm_context = json.loads(chat_session.stm_context)

        # ✅ Load User Settings
        try:
            user_settings = UserSettings.objects.get(user_email=email)
            country = user_settings.country
            sector = user_settings.sector
            language = user_settings.language
        except:
            country, sector, language = "India", "Banking", "English"

        lang_code = get_language_code(language)

        # ✅ Translate Question if Needed
        question_en = question
        if language.lower() != "english" and lang_code:
            try:
                question_en = GoogleTranslator(
                    source="auto", target="en"
                ).translate(question)
            except:
                pass

        # ✅ MODE MUST COME FROM FRONTEND
        mode = request.data.get("mode", "rag")

        urls_display = []
        deep_research_used = False

        # ✅ Generate New Answer Based on Mode
        if mode == "deep":
            agent = deep.DeepResearchAgent(SERPAPI_KEY)
            urls_display, new_answer, english_answer = asyncio.run(
                agent.process(
                    LLM,
                    country,
                    sector,
                    question_en,
                    language,
                    lang_code or "en",
                    stm_context
                )
            )

        elif mode == "enhance":
            new_answer, english_answer, urls_display, deep_research_used = run_enhance_mode(
                question_en,
                country,
                sector,
                language,
                lang_code,
                stm_context
            )

        else:
            new_answer, english_answer, urls_display, deep_research_used = run_rag_mode(
                question_en,
                country,
                sector,
                language,
                lang_code,
                stm_context
            )

        # ✅ Generate Suggestions Again (Simple)
        suggestions = intent.generate_intent_suggestions(
            llm=LLM,
            intent="rewrite",
            question=question,
            answer=english_answer,
            country=country,
            sector=sector,
            language=language
        )

        # ✅ TEXT → SPEECH New Audio
        audio_path = None
        try:
            if new_answer:
                audio_data = tts.generate_speech(
                    new_answer,
                    language,
                    LANGUAGE_CSV
                )

                if audio_data:
                    file_name = f"{uuid.uuid4()}.mp3"
                    file_path = os.path.join(settings.TTS_AUDIO_DIR, file_name)

                    with open(file_path, "wb") as f:
                        f.write(audio_data)

                    audio_path = request.build_absolute_uri(
                        f"{settings.MEDIA_URL}tts_audio/{file_name}"
                    )

        except Exception as e:
            print("Rewrite TTS error:", e)

        # ✅ Replace Last Assistant Answer Instead of Adding New One
        replaced = False
        for i in range(len(chat_history) - 1, 0, -1):

            if (
                chat_history[i]["role"] == "assistant"
                and chat_history[i - 1]["role"] == "user"
                and chat_history[i - 1]["content"] == question
            ):
                chat_history[i] = {
                    "role": "assistant",
                    "content": new_answer,
                    "sources": urls_display,
                    "suggestions": suggestions,
                    "audio_path": audio_path,
                    "rewritten": True
                }
                replaced = True
                break

        # ✅ If Not Found, Append (Failsafe)
        if not replaced:
            chat_history.extend([
                {"role": "user", "content": question},
                {
                    "role": "assistant",
                    "content": new_answer,
                    "sources": urls_display,
                    "suggestions": suggestions,
                    "audio_path": audio_path,
                    "rewritten": True
                }
            ])

        # ✅ Save Updated History
        chat_session.chat_history = json.dumps(chat_history)
        chat_session.save()

        # ✅ Return Rewrite Response
        return Response(
            {
                "success": True,
                "question": question,
                "answer": new_answer,
                "sources": urls_display,
                "suggestions": suggestions,
                "audio_path": audio_path,
                "rewritten": True,
                "mode_used": mode
            },
            status=200
        )

    except ChatSession.DoesNotExist:
        return Response(
            {"success": False, "message": "Chat session not found"},
            status=404
        )

    except Exception as e:
        traceback.print_exc()
        return Response(
            {"success": False, "message": str(e)},
            status=500
        )


    

@extend_schema(
    request=ClickSuggestionRequestSerializer,
    responses={
        200: ClickSuggestionResponseSerializer,
        400: dict,
        401: dict,
        500: dict,
    },
    summary="Handle suggestion click",
    description="Handles a user clicking a follow-up suggestion and prepares it to be processed as a new question."
)
@api_view(["POST"])
def click_suggestion(request):
    """
    Handle user clicking a follow-up suggestion.
    """
    try:
        serializer = ClickSuggestionRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_email = serializer.validated_data["email"]
        suggestion = serializer.validated_data["suggestion"]
        if not user_email:
            return Response(
                {"success": False, "message": "Not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED
            )



        return Response(
            {
                "success": True,
                "suggestion": suggestion,
                "message": "Process this as a new question",
            },
            status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response(
            {"success": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@extend_schema(
    responses={
        200: HealthCheckResponseSerializer
    },
    summary="Health check",
    description="Verify API and RAG system readiness."
)
@api_view(["GET"])
def health_check(request):
    """
    Health check endpoint to verify API and RAG readiness.
    """
    return Response(
        {
            "success": True,
            "status": "healthy",
            "rag_initialized": (
                SUMMARY_VECTORDB is not None
                and CONTENT_VECTORDB is not None
            )
        },
        status=status.HTTP_200_OK
    )
@extend_schema(
    responses={200: dict},
    summary="Get dropdown metadata",
    description="Returns supported languages, sectors, and countries"
)

@api_view(["GET"])
def get_metadata(request):
    return Response(
        {
            "success": True,
            "language": LANGUAGES,
            "sector": ["Banking", "Finance", "Healthcare", "Environment"],
            "country": ["India", "US", "UAE", "China"]
        },
        status=status.HTTP_200_OK
    )
@extend_schema(
    responses={200: dict},
    summary="Get dropdown metadata",
    description="Returns supported languages"
)

@api_view(["GET"])
def get_languages(request):
    return Response(
        {
            "success": True,
            "language": LANGUAGES
        },
        status=status.HTTP_200_OK
    )


COUNTRIES = ["UAE", "India", "US", "China"]
@extend_schema(
    summary="Get list of supported countries",
    description="Returns all available countries for selection.",
    responses={
        200: OpenApiTypes.OBJECT
    }
)
@api_view(["GET"])
def get_countries_list(request):
    return Response(
        {
            "success": True,
            "countries": COUNTRIES
        },
        status=status.HTTP_200_OK
    )

COUNTRY_SECTOR_MAP = {
    "India": ["Banking", "Finance", "Healthcare", "Environment"],
    "US": ["Banking", "Finance", "Healthcare", "Environment"],
    "UAE": ["Shariat", "Ancillary Service Providers", "Banking and Fintech", "Cryptocurrency and Blockchain related Services", "Financial Advisory Services", "Fund Management & Custodian", "Insurtech", "Investment and wealth management platforms", "Lending platforms", "Payment service providers", "Regtech"],
    "China": ["Banking", "Finance", "Healthcare", "Environment"]
}
@extend_schema(
    summary="Get sectors by country",
    description="Returns sector list based on provided country.",
    parameters=[
        OpenApiParameter(
            name="country",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=True,
            description="Country name (e.g., India, US)"
        )
    ],
    responses={
        200: OpenApiTypes.OBJECT,
        400: OpenApiTypes.OBJECT,
        404: OpenApiTypes.OBJECT,
    }
)
@api_view(["GET"])
def get_sectors_by_country(request):
    country = request.query_params.get("country")

    if not country:
        return Response(
            {"success": False, "error": "Country parameter required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    sectors = COUNTRY_SECTOR_MAP.get(country)

    if not sectors:
        return Response(
            {"success": False, "error": "Invalid country"},
            status=status.HTTP_404_NOT_FOUND
        )

    return Response(
        {
            "success": True,
            "country": country,
            "sectors": sectors
        },
        status=status.HTTP_200_OK
    )

# Ensure the 'data' directory exists
output_dir = "data"
os.makedirs(output_dir, exist_ok=True)  # Create 'data' directory if it doesn't exist

def upload_pdf_to_azure(file_path, blob_name, expiry_hours=1):
    try:
        # Create BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(container=AZURE_CONTAINER_NAME, blob=blob_name)

        # Upload file
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

        print(f"File '{file_path}' uploaded successfully as '{blob_name}'.")

        # Generate SAS Token
        """sas_token = generate_blob_sas(
            account_name=blob_service_client.account_name,
            container_name=AZURE_CONTAINER_NAME,
            blob_name=blob_name,
            account_key=blob_service_client.credential.account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.datetime.utcnow() + datetime.timedelta(hours=expiry_hours)
        )"""

        # Construct SAS URL
        #sas_url = f"{blob_client.url}?{sas_token}"
        sas_url = blob_client.url
        return sas_url

    except Exception as e:
        print(f"Azure Upload Error: {e}")
        return None


def upload_rule_pdf_to_azure(file_path, blob_name, expiry_hours=1):
    try:
        # Create BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(container=AZURE_CONTAINER_NAME_1, blob=blob_name)

        # Upload file
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

        print(f"File '{file_path}' uploaded successfully as '{blob_name}'.")

        # Generate SAS Token
        """sas_token = generate_blob_sas(
            account_name=blob_service_client.account_name,
            container_name=AZURE_CONTAINER_NAME,
            blob_name=blob_name,
            account_key=blob_service_client.credential.account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.datetime.utcnow() + datetime.timedelta(hours=expiry_hours)
        )"""

        # Construct SAS URL
        #sas_url = f"{blob_client.url}?{sas_token}"
        sas_url = blob_client.url
        return sas_url

    except Exception as e:
        print(f"Azure Upload Error: {e}")
        return None
    

"""@extend_schema(

    request=UploadPDFRequestSerializer,

    responses={

        200: dict,

        400: dict,

        401: dict,

        500: dict,

    },

    summary="Upload PDF file",

    description="Upload a PDF, store it locally, upload to Azure Blob Storage, and log details in CSV."

)

@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
#new pdf
def upload_pdf(request):

    try:

        # 🔐 Authentication check (same pattern as TTS)

        user_email = request.session.get("user_email")

        if not user_email:

            return Response(

                {"success": False, "message": "Not authenticated"},

                status=status.HTTP_401_UNAUTHORIZED

            )
 
        # 🔹 Validate request using serializer

        '''serializer = UploadPDFRequestSerializer(

            data=request.data,

            files=request.FILES

        )'''
        serializer = UploadPDFRequestSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
 
        sub_category = serializer.validated_data["sub_category"]

        country = serializer.validated_data["country"]   # ✅ NEW

        pdf_file = serializer.validated_data["pdf_file"]
 
        # 🔹 Save PDF locally

        upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")

        os.makedirs(upload_dir, exist_ok=True)
 
        file_path = os.path.join(upload_dir, pdf_file.name)
 
        with open(file_path, "wb+") as destination:

            for chunk in pdf_file.chunks():

                destination.write(chunk)
 
        # 🔹 Upload to Azure

        sas_url = upload_rule_pdf_to_azure(file_path, pdf_file.name)

        if not sas_url:

            return Response(

                {"success": False, "message": "Azure upload failed"},

                status=status.HTTP_500_INTERNAL_SERVER_ERROR

            )
 
        # 🔹 Timestamp

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
 
        # 🔹 CSV paths

        output_dir = settings.MEDIA_ROOT

        csv_master = os.path.join(output_dir, "uploads/stored_path.csv")
#
        csv_logs = os.path.join(output_dir, "uploads/stored_paths_logs.csv")
 
        os.makedirs(os.path.dirname(csv_master), exist_ok=True)
 
        # 🔹 Append logs CSV

        file_exists = os.path.isfile(csv_logs)

        next_id = 1
 
        if file_exists:

            with open(csv_logs, "r", newline="") as f:

                rows = list(csv.reader(f))

                if len(rows) > 1:

                    next_id = int(rows[-1][0]) + 1
 
        with open(csv_logs, "a", newline="") as f:

            writer = csv.writer(f)

            if not file_exists:

                #writer.writerow(["ID", "Timestamp", "sub_category", "Azure_SAS_URL"])
                writer.writerow(["ID", "Timestamp", "sub_category", "country", "Azure_SAS_URL"])


            #writer.writerow([next_id, timestamp, sub_category, sas_url])
            writer.writerow([next_id, timestamp, sub_category, country, sas_url])

 
        # 🔹 Initialize master CSV if missing

        if not os.path.isfile(csv_master):

            IDs = [1,2,3,4,5,6,7,8,9,10]

            sub_categories = [

                "Banking and Fintech",

                "Payment service providers",

                "Lending platforms",

                "Investment and wealth management platforms",

                "Insurtech",

                "Regtech",

                "Cryptocurrency and Blockchain related Services",

                "Ancillary Service Providers",

                "Financial Advisory Services",

                "Fund Management & Custodian"

            ]
 
            with open(csv_master, "w", newline="") as f:

                writer = csv.writer(f)

                #writer.writerow(["ID", "Timestamp", "sub_category", "Azure_SAS_URL"])
                writer.writerow(["ID", "Timestamp", "sub_category", "country", "Azure_SAS_URL"])


                for i, cat in zip(IDs, sub_categories):

                    writer.writerow([i, "", cat, "", ""])
 
        # 🔹 Update matching sub_category row

        rows = []

        with open(csv_master, "r", newline="", encoding="utf-8") as f:

            reader = csv.reader(f)

            header = next(reader)

            for row in reader:

                if row[2].strip().lower() == sub_category.strip().lower():


                    row[1] = timestamp

                    row[3] = country 

                    row[4] = sas_url

                rows.append(row)
 
        with open(csv_master, "w", newline="", encoding="utf-8") as f:

            writer = csv.writer(f)

            writer.writerow(header)

            writer.writerows(rows)
 
        return Response(

            {

                "success": True,

                "message": "PDF uploaded successfully",

                "file_name": pdf_file.name,

                "sub_category": sub_category,

                "country": country, 

                "file_path": sas_url,

                "uploaded_at": timestamp,

            },

            status=status.HTTP_200_OK

        )
 
    except Exception as e:

        import traceback

        traceback.print_exc()

        return Response(

            {"success": False, "message": str(e)},

            status=status.HTTP_500_INTERNAL_SERVER_ERROR

        )
"""

@extend_schema(
    request=UploadPDFRequestSerializer,
    responses={
        200: dict,
        400: dict,
        401: dict,
        500: dict,
    },
    summary="Upload PDF file",
    description="Upload a PDF, store it locally, upload to Azure Blob Storage, and log details in CSV."
)
@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def upload_pdf(request):

    try:
        # 🔐 Authentication check
        # 🔹 Validate request
        serializer = UploadPDFRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_email = serializer.validated_data["email"]
        sub_category = serializer.validated_data["sub_category"]
        country = serializer.validated_data["country"]
        pdf_file = serializer.validated_data["pdf_file"]
        if not user_email:
            return Response(
                {"success": False, "message": "Not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED
            )



        # 🔹 Save PDF locally
        upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
        os.makedirs(upload_dir, exist_ok=True)

        file_path = os.path.join(upload_dir, pdf_file.name)
        with open(file_path, "wb+") as destination:
            for chunk in pdf_file.chunks():
                destination.write(chunk)

        # 🔹 Upload to Azure
        sas_url = upload_rule_pdf_to_azure(file_path, pdf_file.name)
        if not sas_url:
            return Response(
                {"success": False, "message": "Azure upload failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # 🔹 Timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 🔹 CSV paths
        output_dir = settings.MEDIA_ROOT
        csv_master = os.path.join(output_dir, "uploads/stored_path.csv")
        csv_logs = os.path.join(output_dir, "uploads/stored_paths_logs.csv")

        os.makedirs(os.path.dirname(csv_master), exist_ok=True)

        # =====================================================
        # 🔹 LOG CSV (append-only) — WORKING AS-IS
        # =====================================================
        file_exists = os.path.isfile(csv_logs)
        next_id = 1

        if file_exists:
            with open(csv_logs, "r", newline="") as f:
                rows = list(csv.reader(f))
                if len(rows) > 1:
                    next_id = int(rows[-1][0]) + 1

        with open(csv_logs, "a", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["ID", "Timestamp", "sub_category", "country", "Azure_SAS_URL"])

            writer.writerow([next_id, timestamp, sub_category, country, sas_url])

        # =====================================================
        # 🔹 MASTER CSV — FIXED LOGIC
        # =====================================================
        if not os.path.isfile(csv_master):
            with open(csv_master, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Timestamp", "sub_category", "country", "Azure_SAS_URL"])

        rows = []
        found = False

        with open(csv_master, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)

            for row in reader:
                if (
                    row[2].strip().lower() == sub_category.strip().lower()
                    and row[3].strip().lower() == country.strip().lower()
                ):

                    row[1] = timestamp
                    row[3] = country
                    row[4] = sas_url
                    found = True
                rows.append(row)

        # ➕ Append if sub_category not found
        if not found:
            new_id = len(rows) + 1
            rows.append([new_id, timestamp, sub_category, country, sas_url])

        with open(csv_master, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(rows)

        return Response(
            {
                "success": True,
                "message": "PDF uploaded successfully",
                "file_name": pdf_file.name,
                "sub_category": sub_category,
                "country": country,
                "file_path": sas_url,
                "uploaded_at": timestamp,
            },
            status=status.HTTP_200_OK
        )

    except Exception as e:
        import traceback
        traceback.print_exc()

        return Response(
            {"success": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@extend_schema(

    request=DisplayRulesRequestSerializer,

    responses={

        200: dict,

        400: dict,

        401: dict,

        404: dict,

        500: dict,

    },

    summary="Display rules from regulation PDF",

    description="Fetch PDF from Azure using sub_category, send it to Gemini, and extract rules as structured JSON."

)
@api_view(["POST"])
def display_rules(request):
    try:
        # ✅ Validate request
        serializer = DisplayRulesRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_email = serializer.validated_data["email"]
        sub_category = serializer.validated_data["sub_category"]
        user_country = serializer.validated_data["user_country"]
        # ✅ Fetch user name
        user_obj = User.objects.filter(email=user_email).first()
        user_name = user_obj.name if user_obj else None


        if not user_email:
            return Response(
                {"success": False, "message": "Not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # ======================================================
        # ✅ STEP 0: CACHE SETUP
        # ======================================================

        cache_dir = os.path.join("data", "rules_cache")
        os.makedirs(cache_dir, exist_ok=True)

        cache_file = os.path.join(cache_dir, "rules_cache.json")

        # Load cache JSON
        if os.path.exists(cache_file):
            with open(cache_file, "r", encoding="utf-8") as f:
                cache_data = json.load(f)
        else:
            cache_data = {}

        cache_key = f"{sub_category.strip().lower()}_{user_country.strip().lower()}"

        # ======================================================
        # ✅ STEP 1: CACHE HIT
        # ======================================================

        if cache_key in cache_data:

            cached_rules = cache_data[cache_key]
            rules_dict = cached_rules.get("rules", {})

            # ✅ Insert cached rules into DB
            for rule_id, rule_text in rules_dict.items():
                ComplianceRuleStatus.objects.get_or_create(
                    user_email=user_email,
                    sub_category=sub_category,
                    user_country=user_country,
                    rule_id=rule_id,
                    defaults={
                        "name": user_name,
                        "rule_text": rule_text,
                        "completed": False
                    }
                )

            return Response(
                {
                    "success": True,
                    "cached": True,
                    "rules": cached_rules,
                    "message": "Rules loaded from cache ✅"
                },
                status=200
            )

        # ======================================================
        # ✅ STEP 2: CACHE MISS → CSV LOAD
        # ======================================================

        csv_path = os.path.join(
            settings.MEDIA_ROOT,
            "uploads",
            "stored_path.csv"
        )

        if not os.path.exists(csv_path):
            return Response(
                {"success": False, "message": "CSV mapping file not found"},
                status=500
            )

        df = pd.read_csv(csv_path)

        matched_row = df[
            (df["sub_category"].str.strip().str.lower() == sub_category.strip().lower()) &
            (df["country"].str.strip().str.lower() == user_country.strip().lower())
        ]

        if matched_row.empty:
            return Response(
                {"success": False, "message": "No PDF found for this sub_category + country"},
                status=404
            )

        pdf_url = matched_row.iloc[0]["Azure_SAS_URL"]

        # ======================================================
        # ✅ STEP 3: Download PDF From Azure
        # ======================================================

        azure_response = requests.get(pdf_url, timeout=30)
        azure_response.raise_for_status()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(azure_response.content)
            temp_pdf_path = tmp.name

        # ======================================================
        # ✅ STEP 4: Gemini Extraction
        # ======================================================

        try:
            uploaded_file = client.files.upload(file=temp_pdf_path)

            prompt = """
            You are a regulatory compliance analyst.
           
            Your task is to extract a structured Compliance Rule List from the given regulatory document.
           
            STRICT OUTPUT REQUIREMENTS:
            - Output must be valid JSON only.
            - Do NOT add explanations, summaries, or commentary.
            - Do NOT invent rules.
            - Do NOT merge unrelated obligations.
            - Each rule must represent a single enforceable regulatory obligation.
            - Preserve the regulatory intent and mandatory language ("must", "shall", "required", "prohibited").
           
            JSON STRUCTURE:
            {
              "success": true,
              "sub_category": "<Regulatory sub-category inferred from the document>",
              "rules": {
                "<RULE_ID>": "<Rule text>"
              }
            }
           
            RULE IDENTIFICATION RULES:
            - Generate deterministic rule IDs based on document structure.
            - Use the following pattern:
              <MODULE>-<SECTION>.<SUBSECTION>.<RULE_NUMBER>
           
            COUNTRY-BASED MODULE PREFIX (MANDATORY):
            - Determine the regulatory country from the document context.
            - Use the following prefixes strictly:
           
              - India → RBI-1.1.1
              - Australia → AU-1.1.1
              - United Kingdom (UK) → UK-1.1.1
              - United States (USA, US, America) → USA-1.1.1
              - United Arab Emirates (UAE) → UAE-1.1.1
              - Singapore → SG-1.1.1
           
            - The prefix must be used consistently for all extracted rules.
            - Increment SECTION, SUBSECTION, and RULE_NUMBER deterministically based on document structure.
           
            Examples:
            - RBI-7.1.1
            - AU-3.2.1
            - UK-5.4.2
            - USA-12.1.3
            - UAE-2.1.1
            - SG-4.3.1
           
            - If the document does not explicitly number rules:
              - Infer numbering from headings, tables, and bullet hierarchy.
              - Maintain consistent incremental numbering.
           
            RULE TEXT REQUIREMENTS:
            - Each rule must be:
              - Self-contained
              - Legally enforceable
              - Written as a complete obligation
            - Convert tabular requirements into sentence-based rules.
            - Retain thresholds, conditions, approvals, timelines, and authorities exactly as stated.
            - Expand shorthand references into readable regulatory sentences without altering meaning.
           
            SUB-CATEGORY RULES:
            - Infer "sub_category" from the document scope (e.g., "Banking & FinTech Compliance", "Digital Lending", "AML & KYC", "Payments Regulation").
            - Use a single clear sub-category, not a list.
           
            EXTRACTION SCOPE:
            - Include only regulatory obligations, prohibitions, approvals, and mandatory controls.
            - Exclude:
              - Overviews
              - Background explanations
              - Non-binding guidance
              - Marketing or descriptive text
           
            If a requirement is conditional, include the condition inside the rule text.
           
            Begin extraction now.
            """

            gemini_response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[uploaded_file, prompt]
            )

        finally:
            if os.path.exists(temp_pdf_path):
                os.remove(temp_pdf_path)

        # ======================================================
        # ✅ STEP 5: Parse Gemini Output
        # ======================================================

        text = gemini_response.text.strip()
        text = text.replace("```json", "").replace("```", "").strip()

        rules_data = json.loads(text)
        rules_dict = rules_data.get("rules", {})

        if not rules_dict:
            return Response(
                {"success": False, "message": "No rules extracted from Gemini"},
                status=500
            )

        # ======================================================
        # ✅ STEP 6: Save To Cache JSON
        # ======================================================

        cache_data[cache_key] = rules_data

        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(cache_data, f, indent=4, ensure_ascii=False)

        # ======================================================
        # ✅ STEP 7: Insert Rules Into DB
        # ======================================================

        inserted_count = 0

        for rule_id, rule_text in rules_dict.items():
            obj, created = ComplianceRuleStatus.objects.get_or_create(
                user_email=user_email,
                sub_category=sub_category,
                user_country=user_country,
                rule_id=rule_id,
                defaults={
                    "name": user_name,
                    "rule_text": rule_text,
                    "completed": False
                }
            )
            if created:
                inserted_count += 1

        print("✅ Rules inserted into DB =", inserted_count)

        # ======================================================
        # ✅ FINAL RESPONSE
        # ======================================================

        return Response(
            {
                "success": True,
                "cached": False,
                "inserted_rules": inserted_count,
                "rules": rules_data,
                "message": "Rules extracted + stored successfully ✅"
            },
            status=200
        )

    except json.JSONDecodeError:
        return Response(
            {"success": False, "message": "Gemini output is invalid JSON"},
            status=500
        )

    except Exception as e:
        traceback.print_exc()
        return Response(
            {"success": False, "message": str(e)},
            status=500
        )
        


@api_view(["GET"])
def resource_list(request):
    try:
        # ✅ CSV File Path
        csv_file = settings.MEDIA_ROOT + "/uploads/stored_paths_logs.csv"

        resources = []

        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                # ✅ Skip empty lines
                if not row["ID"].strip():
                    continue

                # ✅ Convert timestamp to ISO format
                created_on = None
                if row["Timestamp"]:
                    created_on = (
                        datetime.strptime(row["Timestamp"], "%Y-%m-%d %H:%M:%S")
                        .isoformat() + "Z"
                    )

                resources.append({
                    "id": int(row["ID"]),
                    "resource_name": row["sub_category"],
                    "sub_category_country": row["country"],
                    "resource_url": row["Azure_SAS_URL"],
                    "created_on": created_on
                })

        return Response({
            "status": "success",
            "data": resources
        })

    except Exception as e:
        return Response({
            "status": "error",
            "message": str(e)
        }, status=500)
    
'''@api_view(["POST"])
def store_compliance_json(request):
    try:
        # 🔐 Authentication check (same pattern as your other APIs)
        user_email = request.session.get("user_email")
        if not user_email:
            return Response(
                {"success": False, "message": "Not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # 🔹 Validate request
        serializer = ComplianceStoreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        sub_category = serializer.validated_data["sub_category"]
        country = serializer.validated_data["country"]
        compliance_completed = serializer.validated_data["compliance_completed"]

        # 🔹 JSON file path
        output_dir = os.path.join(settings.MEDIA_ROOT, "compliance")
        os.makedirs(output_dir, exist_ok=True)

        json_file_path = os.path.join(output_dir, "compliance_data.json")

        # 🔹 Load existing JSON
        if os.path.exists(json_file_path):
            with open(json_file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []

        # 🔹 New entry
        entry = {
            "id": len(data) + 1,
            "email": email,
            "sub_category": sub_category,
            "country": country,
            "compliance_completed": compliance_completed,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        data.append(entry)

        # 🔹 Save JSON
        with open(json_file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        return Response(
            {
                "success": True,
                "message": "Compliance stored successfully",
                "data": entry
            },
            status=status.HTTP_200_OK
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response(
            {"success": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
'''

@extend_schema(
    request=ComplianceStoreSerializer,
    responses={
        200: dict,
        400: dict,
        401: dict,
        500: dict,
    },
    summary="Store compliance status in JSON",
    description=(
        "Stores compliance completion details in a JSON file. "
        "Accepts email, sub-category, country, and a list of completed compliance items."
    )
)
@api_view(["POST"])
def store_compliance_json(request):
    try:
        # ✅ STEP 0: Validate Request
        serializer = ComplianceStoreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_email = serializer.validated_data["email"]
        sub_category = serializer.validated_data["sub_category"]
        user_country = serializer.validated_data["user_country"]
        compliance_completed = serializer.validated_data["compliance_completed"]

        if not user_email:
            return Response(
                {"success": False, "message": "Not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # ======================================================
        # ✅ STEP 1: Ensure Rules Exist in DB First
        # ======================================================

        all_rules_qs = ComplianceRuleStatus.objects.filter(
            user_email=user_email,
            sub_category=sub_category,
            user_country=user_country
        )

        if not all_rules_qs.exists():
            return Response(
                {
                    "success": False,
                    "message": (
                        "No compliance rules found in DB for this user. "
                        "Run display_rules API first before updating completion."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Debug Print: Show Existing Rule IDs
        existing_rule_ids = list(
            all_rules_qs.values_list("rule_id", flat=True)
        )

        print("✅ Rules Found in DB:", existing_rule_ids)

        # ======================================================
        # ✅ STEP 2: Mark Completed Rules
        # ======================================================

        updated_count = ComplianceRuleStatus.objects.filter(
            user_email=user_email,
            sub_category=sub_category,
            user_country=user_country,
            rule_id__in=compliance_completed
        ).update(completed=True)

        print("✅ Completed Rules Updated =", updated_count)

        # ======================================================
        # ✅ STEP 3: Mark Remaining Rules as Pending
        # ======================================================

        ComplianceRuleStatus.objects.filter(
            user_email=user_email,
            sub_category=sub_category,
            user_country=user_country
        ).exclude(
            rule_id__in=compliance_completed
        ).update(completed=False)

        # ======================================================
        # ✅ STEP 4: Fetch Pending Rules
        # ======================================================

        pending_rules = ComplianceRuleStatus.objects.filter(
            user_email=user_email,
            sub_category=sub_category,
            user_country=user_country,
            completed=False
        )

        pending_list = [
            {
                "rule_id": r.rule_id,
                "rule_text": r.rule_text
            }
            for r in pending_rules
        ]

        # ======================================================
        # ✅ STEP 5: Send Pending Rules Email (Optional)
        # ======================================================

        if pending_rules.exists():
            pending_text = "\n\n".join(
                [f"{r.rule_id}: {r.rule_text}" for r in pending_rules]
            )

            yag = yagmail.SMTP(
                settings.YAGMAIL_USER,
                settings.YAGMAIL_PASS
            )

            yag.send(
                to=user_email,
                subject="Pending Compliance Rules Reminder",
                contents=f"""
Hello,

You still have pending compliance rules:

{pending_text}

Please login and complete them.

Regards,
Compliance Team
"""
            )

        # ======================================================
        # ✅ STEP 6: Save Backup JSON (Optional)
        # ======================================================

        output_dir = os.path.join(settings.MEDIA_ROOT, "compliance")
        os.makedirs(output_dir, exist_ok=True)

        json_file_path = os.path.join(output_dir, "compliance_data.json")

        # Load existing JSON
        if os.path.exists(json_file_path):
            with open(json_file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []

        entry = {
            "id": len(data) + 1,
            "email": user_email,
            "sub_category": sub_category,
            "user_country": user_country,
            "completed_rules": compliance_completed,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        data.append(entry)

        with open(json_file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        # ======================================================
        # ✅ FINAL RESPONSE
        # ======================================================

        return Response(
            {
                "success": True,
                "message": "Compliance updated successfully ✅",
                "updated_rows": updated_count,
                "completed_rules": compliance_completed,
                "pending_rules": pending_list,
                "total_rules": len(existing_rule_ids)
            },
            status=status.HTTP_200_OK
        )

    except Exception as e:
        import traceback
        traceback.print_exc()

        return Response(
            {"success": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )



@extend_schema(
    parameters=[
        OpenApiParameter(
            name="subcategory",
            type=str,
            location=OpenApiParameter.QUERY,
            required=True,
            description="Example: Banking and Fintech"
        )
    ],
    responses=StatisticsResponseSerializer,
    summary="User Statistics API"
)
@api_view(["GET"])
def statistics_view(request):

    subcategory = request.GET.get("subcategory")

    # ==============================
    # Overall Stats
    # ==============================
    total_users = User.objects.count()

    selected_users = User.objects.filter(
        sub_category=subcategory
    ).count()

    other_users = total_users - selected_users

    other_percentage = round(
        (other_users / total_users) * 100, 2
    ) if total_users > 0 else 0

    # ==============================
    # Monthly Percentage Calculation
    # ==============================

    # Total users per month
    total_monthly = (
        User.objects
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Count("id"))
        .order_by("month")
    )

    # Selected users per month
    selected_monthly = (
        User.objects.filter(sub_category=subcategory)
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(selected=Count("id"))
    )

    # Map selected counts by month
    selected_map = {
        item["month"]: item["selected"]
        for item in selected_monthly
    }

    # Build final monthly percentage data
    monthly_counts = []

    for item in total_monthly:
        month = item["month"]
        total = item["total"]
        selected = selected_map.get(month, 0)

        #other = total - selected

        other_percentage_month = round(
            (selected / total) * 100, 2
        ) if total > 0 else 0

        monthly_counts.append({
            "month": month.strftime("%b"),
            "count": other_percentage_month
        })

    # ==============================
    # Response
    # ==============================
    response_data = {
        "subcategory": subcategory,
        "selected_users": selected_users,
        "other_users": other_users,
        "other_percentage": other_percentage,
        "monthly_counts": monthly_counts
    }

    serializer = StatisticsResponseSerializer(response_data)

    return Response(serializer.data)

"""FILE_PATH = os.path.join(
    os.path.dirname(__file__),
    "compliance_data",
    md_file
)"""



COUNTRY_MAP = {
    "India": "## Regulatory Comparison with India",

    "United States": "## Regulatory Comparison with United States",
    "USA": "## Regulatory Comparison with United States",

    "United Kingdom": "## Regulatory Comparison with United Kingdom",
    "UK": "## Regulatory Comparison with United Kingdom",

    "Australia": "## Regulatory Comparison with Australia",

    "Singapore": "## Regulatory Comparison with Singapore",
    "SG": "## Regulatory Comparison with Singapore",
}
CATEGORY_MAP = {
    "Banking and Fintech": "BankingAndFintech.md",
    "Payment service providers": "PaymentServiceProviders.md",
    "Lending platforms": "LendingPlatforms.md",
    "Investment and wealth management platforms": "InvestmentWealth.md",
    "Insurtech": "Insurtech.md",
    "Regtech": "Regtech.md",
    "Cryptocurrency and Blockchain related Services": "CryptoBlockchain.md",
    "Ancillary Service Providers": "AncillaryServices.md",
    "Financial Advisory Services": "FinancialAdvisory.md",
    "Fund Management & Custodian": "FundManagement.md",
    "Shariat": "Shariat.md"
}




def extract_country_section(country_name, file_path):

    if not os.path.exists(file_path):
        print("❌ File not found:", file_path)
        return None

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    heading = COUNTRY_MAP.get(country_name)
    if not heading:
        return None

    pattern = rf"^{re.escape(heading)}\s*(.*?)(?=^## Regulatory Comparison with|\Z)"

    match = re.search(pattern, content, re.DOTALL | re.MULTILINE)

    if match:
        return heading + "\n\n" + match.group(1).strip()

    return None


@extend_schema(
    request=ComplianceCompareRequestSerializer,
    responses={200: ComplianceCompareResponseSerializer},
    summary="Compliance Comparison API",
    description="Compare regulatory compliance rules between up to 3 selected countries"
)
@api_view(["POST"])
def compliance_compare(request):

    serializer = ComplianceCompareRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    category = serializer.validated_data["category"]

    country1 = serializer.validated_data["country1"]
    country2 = serializer.validated_data["country2"]
    country3 = serializer.validated_data.get("country3")

    selected = [c for c in [country1, country2, country3] if c]

    # ✅ Pick correct MD file based on category
    md_file = CATEGORY_MAP.get(category)

    if not md_file:
        return Response({"error": "Invalid category selected"}, status=400)

    FILE_PATH = os.path.join(
        os.path.dirname(__file__),
        "compliance_data",
        md_file
    )

    result = {}

    for country in selected:
        section = extract_country_section(country, FILE_PATH)

        if not section:
            result[country] = "No compliance data found"
        else:
            result[country] = section

    return Response({
        "selected_category": category,
        "selected_countries": selected,
        "comparison_result": result
    })

@extend_schema(
    responses={200: CountryListResponseSerializer},
    summary="Get available countries",
    description="Returns dropdown list of supported countries for compliance comparison"
)
@api_view(["GET"])
def get_countries(request):
    return Response({
        "countries": list(COUNTRY_MAP.keys()),
        "categories": list(CATEGORY_MAP.keys())
    })

    


from .serializers import FAQRequestSerializer, FAQResponseSerializer


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="country",
            type=str,
            location=OpenApiParameter.QUERY,
            required=True,
            description="Country name (India, US, UAE, China)",
            enum=["India", "US", "UAE", "China"]
        ),
        OpenApiParameter(
            name="sector",
            type=str,
            location=OpenApiParameter.QUERY,
            required=True,
            description="Sector name (Banking, Finance, Healthcare, Environment)",
            enum=["Banking", "Finance", "Healthcare", "Environment","Shariat", "Ancillary Service Providers","Banking and Fintech", "Cryptocurrency and Blockchain related Services", "Financial Advisory Services", "Fund Management & Custodian", "Insurtech", "Investment and wealth management platforms", "Lending platforms", "Payment service providers", "Regtech"]
        )
    ],
    responses={
        200: FAQResponseSerializer,
        400: dict,
        404: dict,
        500: dict,
    },
    summary="Get Compliance FAQs",
    description="""
    Retrieve frequently asked compliance questions for a specific country and sector.
    
    Usage:
    - Call this endpoint with country and sector parameters
    - Receive a list of common compliance questions
    - Click on any question to pass it to the chat endpoint for detailed answers
    
    Example: GET /api/faqs/?country=India&sector=Banking
    """
)



@api_view(["GET"])
def get_faqs(request):
    """
    Get FAQs for a specific country and sector combination.
    """

    try:
        # ✅ Extract query parameters
        country = request.query_params.get("country")
        sector = request.query_params.get("sector")

        # ✅ Validate using serializer
        serializer = FAQRequestSerializer(data={
            "country": country,
            "sector": sector
        })

        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "message": "Please select a country and sector in the settings",
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        validated_data = serializer.validated_data
        country = validated_data["country"]
        sector = validated_data["sector"]

        # ✅ Load FAQs.json file (List format)
        faqs_file_path = os.path.join(
            os.path.dirname(__file__),
            "FAQs.json"
        )

        if not os.path.exists(faqs_file_path):
            return Response(
                {
                    "success": False,
                    "message": "FAQs data file not found"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        with open(faqs_file_path, "r", encoding="utf-8") as f:
            faqs_data = json.load(f)

        # ✅ Filter FAQs from list structure
        flat_faqs = flatten_faqs(faqs_data)

        filtered_faqs = [
            item.get("question")
            for item in flat_faqs
            if item.get("sector") == sector
            and item.get("country") == country
        ]



        # ✅ If no FAQs found
        if not filtered_faqs:
            return Response(
                {
                    "success": False,
                    "message": f"No FAQs found for country: {country} and sector: {sector}"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # ✅ Success Response (Your Required Format)
        return Response(
    {
        "success": True,
        "country": country,
        "sector": sector,
        "total_questions": len(filtered_faqs),
        "questions": filtered_faqs
    },
    status=status.HTTP_200_OK
)


    except json.JSONDecodeError:
        return Response(
            {
                "success": False,
                "message": "Error parsing FAQs data file"
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response(
            {
                "success": False,
                "message": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
# Static country code list
COUNTRY_CODES = [
    "+1",   # USA/Canada
    "+7",   # Russia
    "+20",  # Egypt
    "+27",  # South Africa
    "+30",  # Greece
    "+31",  # Netherlands
    "+32",  # Belgium
    "+33",  # France
    "+34",  # Spain
    "+39",  # Italy
    "+44",  # UK
    "+49",  # Germany
    "+52",  # Mexico
    "+55",  # Brazil
    "+61",  # Australia
    "+62",  # Indonesia
    "+63",  # Philippines
    "+64",  # New Zealand
    "+65",  # Singapore
    "+66",  # Thailand
    "+81",  # Japan
    "+82",  # Korea
    "+86",  # China
    "+91",  # India ⭐
    "+92",  # Pakistan
    "+94",  # Sri Lanka
    "+971", # UAE
]

@extend_schema(
    responses=CountryCodesResponseSerializer
)
@api_view(["GET"])
def get_country_codes(request):
    """
    GET /api/country-codes/
    Returns list of phone country calling codes
    """

    return Response(
        {
            "success": True,
            "codes": COUNTRY_CODES
        },
        status=status.HTTP_200_OK
    )





async def get_language_data():
    """Load language codes from CSV"""
    df = pd.read_csv("language_code.csv")
    return df

async def translate_response(text, lang_code):
    """Translate text to target language"""
    if lang_code == "en":
        return text
    try:
        translator = GoogleTranslator(source="en", target=lang_code)
        return translator.translate(text)
    except:
        return text

@extend_schema(
    request=ComplianceBotRequestSerializer,
    responses={200: ComplianceBotResponseSerializer},
    summary="Compliance Bot Query",
    tags=["Compliance"]
)
@api_view(["POST"])

@csrf_exempt
def compliance_bot(request):

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            ques_prompt = data.get("question")

            # ==============================
            # Validate input
            # ==============================
            if not ques_prompt:
                return JsonResponse({"error": "Question not provided."}, status=400)

            # ==============================
            # SQL Prompt
            # ==============================
            q_prompt = f"""
Generate ONLY a valid PostgreSQL SQL query in a single line for the following user request:

User Request:
{ques_prompt}

Database Engine: PostgreSQL
Table Name: "compliance_rule_status"

Columns:
id, name, user_email, sub_category, user_country, rule_id, rule_text, completed, last_updated

Column Meanings:
- rule_text = compliance description
- sub_category = industry/category
- user_country = applicable country
- completed = BOOLEAN (TRUE = completed, FALSE = incomplete)

Rules & Instructions:

1️⃣ SQL SYNTAX
- Use PostgreSQL-compatible syntax only.
- Use STRING_AGG(column, ', ') instead of GROUP_CONCAT().
- Use double quotes for table name.
- Do NOT include explanations or markdown.
- Output ONLY SQL in ONE line.

2️⃣ BOOLEAN HANDLING
- If user says incomplete → use completed = FALSE
- If user says completed → use completed = TRUE

3️⃣ USER IDENTIFICATION (IMPORTANT)
- Always return BOTH name and user_email when individuals are requested.
- Use COALESCE(name, user_email) AS user_identity when presenting users.
- Group by BOTH name and user_email when aggregation is needed.
- Never group only by user_email unless explicitly requested.

4️⃣ QUERY TYPE SELECTION
- Use SELECT * only for full record retrieval.
- If summaries/statistics requested → use aggregation.
- If lists requested → use DISTINCT or STRING_AGG.

5️⃣ INDIVIDUAL VS OVERALL METRICS
- If individuals/users mentioned → compute metrics per person using:
  GROUP BY name, user_email
- If overall/system-wide metrics requested → compute across entire table.
- If completion percentage requested → include percentage per individual.

6️⃣ PERCENTAGE CALCULATION
Use this EXACT formula:

SUM(CASE WHEN completed THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS completion_percentage

7️⃣ OUTPUT CONTROL
- Avoid returning entire table when summary requested.
- Return only relevant columns.
- Use aliases for readability:
  COALESCE(name, user_email) AS user_identity

8️⃣ EXAMPLE STRUCTURE (FOLLOW THIS STYLE)

SELECT
COALESCE(name, user_email) AS user_identity,
name,
user_email,
SUM(CASE WHEN completed THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS completion_percentage
FROM "compliance_rule_status"
GROUP BY name, user_email;

Return ONLY the SQL query in a single line.
"""


            # ==============================
            # LLM INIT
            # ==============================
            model = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=GOOGLE_API_KEY,
                temperature=0.2,
            )

            # ==============================
            # Generate SQL
            # ==============================
            res = model.invoke(q_prompt)
            raw_query = res.content.replace("```sql", "").replace("```", "").strip()

            print("Generated SQL:", raw_query)

            # ==============================
            # Execute SQL
            # ==============================
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()

            cursor.execute(raw_query)
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            cursor.close()
            conn.close()

            raw_rows = [dict(zip(columns, row)) for row in results]

            # ==============================
            # Explanation Stage
            # ==============================
            explain_prompt = f"""
User Question:
{ques_prompt}

SQL Result:
{raw_rows}

Important:
- completion_percentage is ALREADY a percentage value (0 to 100).
- Do NOT multiply or scale the value.
- Example: 0.8 means 0.8%, NOT 80%.
- 0E-20 means 0%.

Task:
Explain the result clearly in simple human-readable text.
Do not show SQL.
Be concise and accurate with percentages.
"""

            explain_res = model.invoke(explain_prompt)
            llm_text = explain_res.content

            # ==============================
            # Final Response
            # ==============================
            return JsonResponse(
                {
                    "answer": llm_text
                },
                status=200
            )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

def run_compliance_query(question):

    q_prompt = f"""
Generate ONLY a valid PostgreSQL SELECT SQL query in a single line.

User Request:
{question}

Table: compliance_rule_status
Columns:
id, name, user_email, sub_category, user_country,
rule_id, rule_text, completed, last_updated

Return ONLY SQL.
"""

    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=GOOGLE_API_KEY,
        temperature=0.2,
    )

    res = model.invoke(q_prompt)
    raw_query = res.content.replace("```sql", "").replace("```", "").strip()

    # ==============================
    # SQL SAFETY GUARD
    # ==============================
    if not raw_query.lower().startswith("select"):
        raise Exception("Unsafe query blocked")

    # Optional limit enforcement
    #if "limit" not in raw_query.lower():
    #    raw_query += " LIMIT 100"

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute(raw_query)
    results = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    cursor.close()
    conn.close()

    rows = [dict(zip(columns, row)) for row in results]

    # ==============================
    # Explain Results
    # ==============================
    explain_prompt = f"""
User Question:
{question}

SQL Result:
{rows}

Explain clearly in simple human text.
"""

    explain_res = model.invoke(explain_prompt)
    return explain_res.content


@extend_schema(
    request=RegulatorChatRequestSerializer,
    responses={200: dict},
    summary="Regulator Chat Router",
    description="Routes request to Compliance SQL bot or Main Chat system"
)
@api_view(["POST"])
def regulator_chat(request):

    serializer = RegulatorChatRequestSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data
    factory = APIRequestFactory()

    # =====================================================
    # ✅ ROUTE → COMPLIANCE BOT
    # =====================================================
    if data.get("query_mode"):

        fake_request = factory.post(
            "/compliance-bot/",
            json.dumps({"question": data["question"]}),
            content_type="application/json"
        )

        return compliance_bot(fake_request)

    # =====================================================
    # ✅ ROUTE → MAIN CHAT
    # =====================================================
    fake_request = factory.post(
        "/chat/",
        json.dumps({
            "email": data["email"],
            "session_id": data["session_id"],
            "question": data["question"],
            "enhance_mode": data["enhance_mode"],
            "deep_research_mode": data["deep_research_mode"],
        }),
        content_type="application/json"
    )

    return chat(fake_request)
