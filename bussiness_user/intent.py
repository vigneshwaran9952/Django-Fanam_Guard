

import json
import re
from typing import Dict, List

# ==============================
# SECTOR-SPECIFIC INTENT DEFINITIONS
# ==============================

INTENT_DEFINITIONS = {
    # ==========================================
    # GENERAL INTENTS (All Sectors & Countries)
    # ==========================================
    "greeting": {
        "description": "User greets or starts a conversation",
        "sectors": ["Banking", "Finance", "Healthcare", "Environment"],
        "examples": ["hi", "hello", "hey", "good morning", "good evening", "how are you"]
    },

    "compliance_requirements": {
    "description": "General regulatory or compliance-related question",
    "sectors": ["Banking", "Finance", "Healthcare", "Environment"],
    "examples": [
        "What are the compliance requirements?",
        "Which regulations apply?",
        "What laws should be followed?",
        "Regulatory obligations",
        "Applicable compliance rules"
    ]
},


    # ==========================================
    # CROSS-SECTOR / STRATEGIC BUSINESS INTENTS
    # ==========================================
    "business_global_expansion": {
        "description": "User intends to expand business operations internationally or globally",
        "sectors": ["Banking", "Finance", "Healthcare", "Environment"],
        "examples": [
            # Direct intent
            "I want to expand my business across the globe",
            "I wish to take my business global",
            "I plan to expand my business internationally",
            "I want my company to operate worldwide",
            "I am looking to expand my business globally",

            # Organizational phrasing
            "Our organization plans to establish an international presence",
            "We aim to scale our operations globally",
            "The company seeks international market expansion",
            "We are planning worldwide business growth",

            # Strategy & planning
            "How can I expand my business globally?",
            "What are the steps to take my business international?",
            "What should I consider before global expansion?",
            "How do companies expand across multiple countries?",

            # Vision & goals
            "I aspire to build a global business",
            "My long-term goal is to operate internationally",
            "I want my business to have a global footprint",

            # Operational expansion
            "I want to register my business in multiple countries",
            "I am planning to open international branches",
            "I plan to establish overseas subsidiaries",
            "I want to start operations in foreign markets",

            # Startup & scaling
            "I want to scale my startup globally",
            "We aim to attract global investors through expansion",
            "Our business is targeting international markets for growth",

            # Compliance-driven expansion
            "I want to expand my business into multiple jurisdictions",
            "I need to comply with international regulations for expansion",
            "I am planning cross-border operations for my business",
            "I am exploring international licensing requirements"
        ]
    },

    # ==========================================
    # BANKING SECTOR INTENTS
    # ==========================================
    "aml_cft": {
        "description": "Anti-Money Laundering and Counter-Terrorism Financing",
        "sectors": ["Banking"],
        "examples": [
            "AML requirements", "KYC norms", "suspicious transaction reporting",
            "customer due diligence", "beneficial ownership", "PEP screening",
            "transaction monitoring", "STR filing", "CTF compliance", "CDD process"
        ]
    },
    "capital_adequacy": {
        "description": "Capital requirements and adequacy ratios",
        "sectors": ["Banking"],
        "examples": [
            "capital adequacy ratio", "Basel norms", "CRAR requirements",
            "Tier 1 capital", "risk-weighted assets", "capital buffers",
            "leverage ratio", "capital conservation", "minimum capital"
        ]
    },
    "lending_regulations": {
        "description": "Lending norms and credit policies",
        "sectors": ["Banking"],
        "examples": [
            "lending guidelines", "loan disbursement", "credit policy",
            "priority sector lending", "NPA classification", "loan recovery",
            "restructuring norms", "lending limits", "exposure norms"
        ]
    },
    "payment_systems": {
        "description": "Payment and settlement systems compliance",
        "sectors": ["Banking"],
        "examples": [
            "RTGS guidelines", "NEFT rules", "UPI compliance",
            "payment gateway", "digital payments", "settlement systems",
            "card payment rules", "mobile banking norms", "e-wallet regulations"
        ]
    },
    "deposit_insurance": {
        "description": "Deposit protection and insurance schemes",
        "sectors": ["Banking"],
        "examples": [
            "deposit insurance", "DICGC coverage", "depositor protection",
            "insurance limits", "claim process", "covered deposits",
            "insurance premium", "deposit guarantee"
        ]
    },
    "branch_licensing": {
        "description": "Branch authorization and licensing",
        "sectors": ["Banking"],
        "examples": [
            "branch license", "new branch approval", "branch opening norms",
            "banking license", "branch authorization", "expansion guidelines",
            "branch closure", "location approval"
        ]
    },
    "foreign_exchange": {
        "description": "Foreign exchange and FEMA compliance",
        "sectors": ["Banking"],
        "examples": [
            "FEMA compliance", "forex transactions", "cross-border payments",
            "remittance rules", "foreign currency", "external commercial borrowing",
            "LRS limits", "forex trading", "foreign investment"
        ]
    },
    "corporate_governance_bank": {
        "description": "Banking sector governance requirements",
        "sectors": ["Banking"],
        "examples": [
            "board composition", "fit and proper criteria", "related party transactions",
            "governance norms", "board committees", "independent directors",
            "ownership norms", "significant shareholding"
        ]
    },
    "risk_management_bank": {
        "description": "Risk management framework for banks",
        "sectors": ["Banking"],
        "examples": [
            "credit risk", "operational risk", "market risk",
            "liquidity risk", "IRRBB", "stress testing",
            "risk appetite", "risk governance", "ICAAP"
        ]
    },
    "cyber_security_bank": {
        "description": "Cybersecurity and IT governance for banks",
        "sectors": ["Banking"],
        "examples": [
            "cyber security framework", "IT security", "data breach",
            "incident reporting", "business continuity", "disaster recovery",
            "outsourcing guidelines", "cloud adoption", "API security"
        ]
    },

    # ==========================================
    # FINANCE SECTOR INTENTS
    # ==========================================
    "securities_regulations": {
        "description": "Securities market regulations and compliance",
        "sectors": ["Finance"],
        "examples": [
            "SEBI regulations", "IPO norms", "listing requirements",
            "insider trading", "market manipulation", "disclosure norms",
            "prospectus requirements", "stock exchange rules", "delisting"
        ]
    },
    "mutual_funds": {
        "description": "Mutual fund regulations and schemes",
        "sectors": ["Finance"],
        "examples": [
            "mutual fund regulations", "AMC compliance", "NAV calculation",
            "fund categorization", "expense ratio", "exit load",
            "scheme information", "portfolio disclosure", "fund governance"
        ]
    },
    "insurance_regulations": {
        "description": "Insurance sector compliance",
        "sectors": ["Finance"],
        "examples": [
            "insurance regulations", "IRDAI norms", "solvency requirements",
            "policy terms", "claim settlement", "premium regulations",
            "insurance brokers", "reinsurance", "actuarial requirements"
        ]
    },
    "nbfc_compliance": {
        "description": "Non-Banking Financial Company regulations",
        "sectors": ["Finance"],
        "examples": [
            "NBFC regulations", "systemically important", "registration requirements",
            "prudential norms", "asset classification", "lending guidelines",
            "deposit acceptance", "fair practices code", "NBFC-MFI"
        ]
    },
    "tax_compliance": {
        "description": "Tax regulations and compliance",
        "sectors": ["Finance"],
        "examples": [
            "tax compliance", "GST regulations", "income tax",
            "TDS requirements", "tax filing", "transfer pricing",
            "withholding tax", "tax audit", "advance tax"
        ]
    },
    "credit_rating": {
        "description": "Credit rating agency regulations",
        "sectors": ["Finance"],
        "examples": [
            "credit rating", "rating methodology", "rating surveillance",
            "default recognition", "rating disclosure", "conflicts of interest",
            "rating criteria", "rating migration"
        ]
    },
    "commodity_trading": {
        "description": "Commodity derivatives and trading",
        "sectors": ["Finance"],
        "examples": [
            "commodity derivatives", "commodity exchange", "warehouse receipts",
            "position limits", "commodity options", "delivery norms",
            "trading members", "commodity hedging"
        ]
    },
    "pension_regulations": {
        "description": "Pension and retirement fund regulations",
        "sectors": ["Finance"],
        "examples": [
            "pension regulations", "NPS compliance", "retirement funds",
            "pension fund management", "withdrawal norms", "annuity requirements",
            "subscriber protection", "PFRDA guidelines"
        ]
    },
    "fintech_regulations": {
        "description": "Financial technology and digital finance",
        "sectors": ["Finance"],
        "examples": [
            "fintech regulations", "digital lending", "peer-to-peer lending",
            "payment aggregators", "account aggregators", "regulatory sandbox",
            "robo-advisory", "crypto regulations", "digital wallets"
        ]
    },
    "corporate_governance_finance": {
        "description": "Corporate governance for financial institutions",
        "sectors": ["Finance"],
        "examples": [
            "corporate governance", "board responsibilities", "shareholder rights",
            "related party transactions", "audit committee", "nomination committee",
            "independent directors", "governance reporting"
        ]
    },

    # ==========================================
    # HEALTHCARE SECTOR INTENTS
    # ==========================================
    "medical_licensing": {
        "description": "Medical professional licensing and registration",
        "sectors": ["Healthcare"],
        "examples": [
            "medical license", "doctor registration", "medical council",
            "practice permit", "continuing education", "license renewal",
            "specialty certification", "foreign medical graduates", "MCI registration"
        ]
    },
    "hospital_accreditation": {
        "description": "Hospital and healthcare facility standards",
        "sectors": ["Healthcare"],
        "examples": [
            "hospital accreditation", "NABH standards", "JCI accreditation",
            "quality standards", "facility certification", "clinical establishment act",
            "hospital registration", "minimum standards", "accreditation process"
        ]
    },
    "drug_regulations": {
        "description": "Pharmaceutical and drug regulations",
        "sectors": ["Healthcare"],
        "examples": [
            "drug licensing", "pharmaceutical regulations", "drug approval",
            "clinical trials", "new drug application", "drug manufacturing",
            "drug import", "pharmacovigilance", "price control"
        ]
    },
    "medical_devices": {
        "description": "Medical device regulations and compliance",
        "sectors": ["Healthcare"],
        "examples": [
            "medical device regulations", "device classification", "device registration",
            "CE marking", "FDA approval", "device quality", "clinical investigation",
            "device labeling", "post-market surveillance"
        ]
    },
    "patient_safety": {
        "description": "Patient safety and quality of care",
        "sectors": ["Healthcare"],
        "examples": [
            "patient safety", "adverse events", "medication errors",
            "infection control", "patient rights", "informed consent",
            "medical negligence", "patient complaints", "quality improvement"
        ]
    },
    "health_insurance": {
        "description": "Health insurance and medical coverage",
        "sectors": ["Healthcare"],
        "examples": [
            "health insurance", "medical insurance", "coverage requirements",
            "claim reimbursement", "cashless treatment", "pre-authorization",
            "insurance portability", "waiting period", "exclusions"
        ]
    },
    "telemedicine": {
        "description": "Telemedicine and digital health regulations",
        "sectors": ["Healthcare"],
        "examples": [
            "telemedicine guidelines", "teleconsultation", "remote diagnosis",
            "digital health", "e-prescription", "online consultation",
            "tele-pharmacy", "remote monitoring", "virtual care"
        ]
    },
    "clinical_research": {
        "description": "Clinical trials and research ethics",
        "sectors": ["Healthcare"],
        "examples": [
            "clinical trials", "research ethics", "IRB approval",
            "informed consent", "patient compensation", "trial registration",
            "good clinical practice", "subject protection", "data safety"
        ]
    },
    "biomedical_waste": {
        "description": "Biomedical waste management",
        "sectors": ["Healthcare"],
        "examples": [
            "biomedical waste", "waste segregation", "waste disposal",
            "hazardous waste", "waste treatment", "infection waste",
            "sharps disposal", "waste management rules", "incinerator"
        ]
    },
    "health_data_privacy": {
        "description": "Healthcare data protection and privacy",
        "sectors": ["Healthcare"],
        "examples": [
            "patient data privacy", "medical records", "health information",
            "HIPAA compliance", "electronic health records", "data security",
            "patient confidentiality", "health data breach", "consent management"
        ]
    },

    # ==========================================
    # ENVIRONMENT SECTOR INTENTS
    # ==========================================
    "environmental_clearance": {
        "description": "Environmental impact assessment and clearances",
        "sectors": ["Environment"],
        "examples": [
            "environmental clearance", "EIA report", "EC approval",
            "project clearance", "environmental assessment", "public hearing",
            "ToR preparation", "clearance process", "forest clearance"
        ]
    },
    "pollution_control": {
        "description": "Air, water, and soil pollution regulations",
        "sectors": ["Environment"],
        "examples": [
            "air pollution", "water pollution", "emission standards",
            "effluent treatment", "pollution monitoring", "stack emissions",
            "wastewater discharge", "ambient air quality", "pollution control board"
        ]
    },
    "waste_management": {
        "description": "Solid and hazardous waste management",
        "sectors": ["Environment"],
        "examples": [
            "waste management", "hazardous waste", "e-waste disposal",
            "plastic waste", "solid waste rules", "waste segregation",
            "landfill regulations", "waste recycling", "waste authorization"
        ]
    },
    "water_resources": {
        "description": "Water usage and conservation regulations",
        "sectors": ["Environment"],
        "examples": [
            "water usage", "water conservation", "groundwater extraction",
            "water rights", "rainwater harvesting", "water pollution",
            "water quality", "effluent standards", "water permit"
        ]
    },
    "forest_wildlife": {
        "description": "Forest conservation and wildlife protection",
        "sectors": ["Environment"],
        "examples": [
            "forest clearance", "tree cutting", "wildlife protection",
            "compensatory afforestation", "forest conservation", "wildlife act",
            "protected areas", "biodiversity", "forest land diversion"
        ]
    },
    "climate_change": {
        "description": "Climate change and carbon emissions",
        "sectors": ["Environment"],
        "examples": [
            "climate change", "carbon emissions", "GHG reporting",
            "carbon footprint", "emission trading", "renewable energy",
            "carbon credits", "climate action", "net zero"
        ]
    },
    "renewable_energy": {
        "description": "Renewable energy regulations and incentives",
        "sectors": ["Environment"],
        "examples": [
            "renewable energy", "solar power", "wind energy",
            "green energy", "RPO compliance", "renewable certificates",
            "feed-in tariff", "renewable subsidies", "clean energy"
        ]
    },
    "environmental_audit": {
        "description": "Environmental audits and compliance",
        "sectors": ["Environment"],
        "examples": [
            "environmental audit", "compliance audit", "green audit",
            "environmental monitoring", "audit report", "audit frequency",
            "environmental performance", "audit checklist"
        ]
    },
    "coastal_regulations": {
        "description": "Coastal zone and marine regulations",
        "sectors": ["Environment"],
        "examples": [
            "coastal regulation zone", "CRZ clearance", "marine pollution",
            "coastal protection", "beach regulation", "ocean dumping",
            "coastal development", "maritime zone", "island protection"
        ]
    },
    "green_building": {
        "description": "Green building and sustainable construction",
        "sectors": ["Environment"],
        "examples": [
            "green building", "LEED certification", "sustainable construction",
            "energy efficiency", "green rating", "building standards",
            "eco-friendly materials", "sustainable design", "green certification"
        ]
    }
}

# ==============================
# INTENT INTRO TEMPLATES
# ==============================

def get_intent_intro(intent: str, mode: str, country: str, sector: str) -> str:
    """
    Return an intent-specific introduction based on mode and intent.
    """
    
    # Greeting intent - special handling
    if intent == "greeting":
        return f"Hello! I'm your compliance assistant for {country}'s {sector} sector. How can I help you today?"
    
    # Mode-specific base templates
    mode_templates = {
        "rag_mode": "In {country}'s {sector} sector, ",
        "enhance_mode": "Based on comprehensive analysis of {country}'s {sector} sector, ",
        "deep_research_mode": "After thorough research of {country}'s {sector} sector regulations, "
    }
    
    # Intent-specific continuations
    intent_continuations = {
        
        # Cross-sector / Strategic
        "business_global_expansion": (
            "here is an overview of the regulatory, compliance, and strategic "
            "considerations for expanding business operations globally:"
        ),

        # Banking
        "aml_cft": "here are the AML/CFT compliance requirements:",
        "capital_adequacy": "here's what you need to know about capital adequacy:",
        "lending_regulations": "here are the lending regulations and norms:",
        "payment_systems": "here's the payment systems compliance information:",
        "deposit_insurance": "here's what you need to know about deposit insurance:",
        "branch_licensing": "here's the branch licensing information:",
        "foreign_exchange": "here are the foreign exchange regulations:",
        "corporate_governance_bank": "here are the corporate governance requirements:",
        "risk_management_bank": "here's the risk management framework:",
        "cyber_security_bank": "here are the cybersecurity requirements:",
        
        # Finance
        "securities_regulations": "here are the securities regulations:",
        "mutual_funds": "here's the mutual fund compliance information:",
        "insurance_regulations": "here are the insurance regulations:",
        "nbfc_compliance": "here's the NBFC compliance framework:",
        "tax_compliance": "here are the tax compliance requirements:",
        "credit_rating": "here's the credit rating regulatory framework:",
        "commodity_trading": "here are the commodity trading regulations:",
        "pension_regulations": "here's the pension regulatory framework:",
        "fintech_regulations": "here are the fintech regulations:",
        "corporate_governance_finance": "here are the corporate governance norms:",
        
        # Healthcare
        "medical_licensing": "here's the medical licensing information:",
        "hospital_accreditation": "here are the hospital accreditation requirements:",
        "drug_regulations": "here are the pharmaceutical regulations:",
        "medical_devices": "here's the medical device regulatory framework:",
        "patient_safety": "here are the patient safety requirements:",
        "health_insurance": "here's the health insurance regulatory framework:",
        "telemedicine": "here are the telemedicine guidelines:",
        "clinical_research": "here's the clinical research regulatory framework:",
        "biomedical_waste": "here are the biomedical waste management requirements:",
        "health_data_privacy": "here are the health data privacy requirements:",
        
        # Environment
        "environmental_clearance": "here's the environmental clearance process:",
        "pollution_control": "here are the pollution control regulations:",
        "waste_management": "here's the waste management framework:",
        "water_resources": "here are the water resource regulations:",
        "forest_wildlife": "here's the forest and wildlife protection framework:",
        "climate_change": "here are the climate change regulations:",
        "renewable_energy": "here's the renewable energy regulatory framework:",
        "environmental_audit": "here are the environmental audit requirements:",
        "coastal_regulations": "here are the coastal zone regulations:",
        "green_building": "here's the green building regulatory framework:"

        
    }
    
    base = mode_templates.get(mode, mode_templates["rag_mode"])
    continuation = intent_continuations.get(intent, "here's the relevant compliance information:")
    
    return base.format(country=country, sector=sector) + continuation

# ==============================
# INTENT CLASSIFICATION
# ==============================

def classify_intent(llm, question: str, country: str, sector: str) -> Dict:
    """
    Classify user intent using LLM with sector-specific filtering
    """
    # Filter intents by sector
    sector = sector.strip().title()

    sector_intents = {
    k: v for k, v in INTENT_DEFINITIONS.items()
    if k == "greeting" or sector in v["sectors"]
}

    
    intent_desc = "\n".join(
        f"- {k}: {v['description']} (Examples: {', '.join(v['examples'][:3])})"
        for k, v in sector_intents.items()
    )

    prompt = f"""
You are an intent classification expert for compliance queries.

Context:
Country: {country}
Sector: {sector}
Question: "{question}"

Available Intents for {sector} Sector:
{intent_desc}

Classification Rules:
1. Match the question to the MOST SPECIFIC intent available
2. For greetings → "greeting"
3. For sector-specific queries → use sector-specific intents (e.g., aml_cft, medical_licensing)
4. For general compliance → use general intents (e.g., compliance_requirements)
5. Consider keywords, context, and domain terminology

Return ONLY valid JSON:
{{
  "intent": "intent_name",
  "confidence": 0.90,
  "reasoning": "short explanation"
}}
"""

    try:
        response = llm.invoke(prompt).content
        response = response.replace("```json", "").replace("```", "").strip()
        result = json.loads(response)

        # Validate intent exists for this sector
        if result.get("intent") not in INTENT_DEFINITIONS:
            result["intent"] = "compliance_requirements"
            result["confidence"] = 0.5
            result["reasoning"] = "Fallback to general compliance"

        return result

    except Exception as e:
        print(f"Intent classification error: {e}")
        return {
            "intent": "compliance_requirements",
            "confidence": 0.5,
            "reasoning": "Fallback due to parsing error"
        }

# ==============================
# RESPONSE PROMPTS
# ==============================

RESPONSE_PROMPTS = {
    "rag_mode": """
You are a compliance assistant.

Respond in a natural, professional, and regulatory tone.

Context:
- Country: {country}
- Sector: {sector}




Response Requirements:
- Strict only with {language} as content language.
- Length must be between 5-10 lines
- Do NOT use introductory phrases such as:
  • "here are the requirements"
  • "here's the regulatory framework"
  • "here is the compliance information"
  • "in {country}'s {sector}"
- Begin the response directly with a heading (no opening sentence)

Structure & Formatting:
- Use clear headings and sub-headings
- Use bullet points for obligations and controls
- Avoid narrative or conversational lead-ins
- Do not repeat the user’s question



Content Rules:
- Explain only regulations applicable to the specified country and sector
- Clearly state obligations, thresholds, or compliance actions using directive language (e.g., "must", "is required to")
- Do NOT assume laws or requirements apply universally
- Avoid vague summaries; focus on actionable compliance duties
- If regulatory scope varies by entity size or activity, state the condition explicitly

Style Constraints:
- Use plain, practical language
- No marketing, advisory disclaimers, or generic explanations
- No examples unless legally required for clarity

User Question:
"{question}"

""",

    "enhance_mode": """
You are a senior compliance expert.

Respond in a clear, detailed, and advisory regulatory tone.

Context:
- Country: {country}
- Sector: {sector}

Response Requirements:
- Strict only with {language} as content language.
- Minimum length: 35 lines
- Begin directly with a section heading (no introductory sentences)
- Do NOT use phrases such as:
  • "here are the requirements"
  • "here is the regulatory framework"
  • "this section covers"
  • "in {country}'s {sector}"
- Do not restate the user’s question

Structure & Formatting:
- Use clear section headings with logical sequencing
- Break content into topics and sub-topics
- Use bullet points and numbered lists where appropriate
- Structure must adapt to the nature of the question (no fixed template)

Content Expectations:
- Identify applicable laws, regulations, or supervisory guidance relevant to the specified country and sector
- Explain key compliance obligations using directive language (e.g., "must", "is required to", "is prohibited from")
- Describe operational implications for regulated entities
- Highlight recognized best practices used by compliant organizations
- Call out common compliance failures or regulatory pitfalls
- Clarify scope limitations or conditional applicability (e.g., entity size, license type, activity)

Style Constraints:
- Use practical, plain language suitable for compliance teams
- Avoid generic summaries or high-level theory
- No marketing language, disclaimers, or legal advice caveats
- No examples unless necessary to explain a regulatory requirement

User Question:
"{question}"

""",

    "deep_research_mode": """
You are an advanced compliance research assistant.

Respond with a deep, research-oriented and authoritative regulatory tone.

Context:
- Country: {country}
- Sector: {sector}

Response Requirements:
- Strict only with {language} as content language.
- Provide a highly detailed and comprehensive response
- Begin directly with a section heading (no opening or transitional sentences)
- Do NOT use phrases such as:
  • "here are the requirements"
  • "here is the regulatory framework"
  • "this response explains"
  • "in {country}'s {sector}"
- Do not restate or paraphrase the user’s question
- Do not follow a fixed structure across responses

Structural Guidance (use selectively, not mandatorily):
- Executive summary (only when the topic is broad or multi-regulatory)
- Thematic or risk-based sections
- Regulatory and legal breakdown by obligation type
- Use bullet points, numbered lists, or tables where they improve clarity

Content Expectations:
- Cite specific applicable laws, regulations, directives, standards, or regulatory guidance
- Identify relevant regulatory or supervisory authorities
- Explain compliance expectations and regulated entity responsibilities
- Describe enforcement approach, supervisory focus, or penalty mechanisms where relevant
- Clearly distinguish mandatory requirements from guidance or best practice
- Explicitly note conditional applicability (e.g., entity type, size, licensing, activity scope)
- Avoid assumptions of cross-border or universal legal equivalence

Sources & References:
- Conclude with a dedicated section listing official source URLs only
  • Government portals
  • Regulatory or supervisory authority websites
  • Statutory or official legal repositories
- Do not embed URLs inline within the analysis

Style Constraints:
- Use precise, technical, and practical language
- Avoid generic summaries, commentary, or advisory disclaimers
- No conversational phrasing or instructional narration
- No examples unless required to interpret a regulatory provision

User Question:
"{question}"

"""
}

# ==============================
# BUILD RESPONSE PROMPT
# ==============================

def build_response_prompt(
    mode: str,
    question: str,
    country: str,
    sector: str
) -> str:
    """
    Build the response prompt for RAG / Enhance / Deep Research
    """
    base_prompt = RESPONSE_PROMPTS.get(mode)
    return base_prompt.format(
        question=question,
        country=country,
        sector=sector
    )

# ==============================
# FOLLOW-UP SUGGESTIONS
# ==============================

def generate_intent_suggestions(
    llm,
    intent: str,
    question: str,
    answer: str,
    country: str,
    sector: str,
    language: str,
    lang_code: str = "en"
) -> List[str]:
    """
    Generate natural follow-up questions based on intent
    """
    intent_info = INTENT_DEFINITIONS.get(intent, {})
    intent_desc = intent_info.get("description", "")
    examples = intent_info.get("examples", [])[:3]

    prompt = f"""
Generate natural follow-up questions for a {sector} compliance conversation.

Context:
Intent: {intent} ({intent_desc})
Country: {country}
Sector: {sector}
Language: {language}
User Question: "{question}"
Answer Summary: "{answer[:400]}"

Example topics for {intent}: {', '.join(examples)}

Rules:
- Questions must be relevant to {intent} in {sector} sector
- Natural and professional
- Generate questions in {language}
- No numbering or bullets
- 2-4 questions maximum
- Similar in style to how professionals ask

Output:
One question per line
"""

    try:
        response = llm.invoke(prompt).content.strip()
        questions = []

        for line in response.split("\n"):
            line = re.sub(r'^[\d\.\-\*•]+\s*', '', line).strip()
            if len(line.split()) >= 4:
                questions.append(line)

        return questions[:4]

    except Exception:
        # Fallback suggestions based on intent
        fallback_map = {
            "aml_cft": ["What are the KYC requirements?", "How to report suspicious transactions?"],
            "medical_licensing": ["What are the renewal requirements?", "How long does approval take?"],
            "environmental_clearance": ["What documents are needed?", "How long is the process?"],
            "securities_regulations": ["What are the disclosure requirements?", "How often to report?"]
        }
        return fallback_map.get(intent, ["Are there any exemptions?", "What are the penalties?"])
    

"""def dummy():
    data = {
        "intents": [
            {
                "intent": "BUSINESS_GLOBAL_EXPANSION",
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
        ]
    }
    return data
"""