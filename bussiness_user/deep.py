"""
Deep Research Module
Performs live web searches and provides detailed responses with source URLs.
Now includes Shariat-specific formatting for CBB compliance.
"""

import asyncio
import httpx
import re
import time
from bs4 import BeautifulSoup
from serpapi.google_search import GoogleSearch
from deep_translator import GoogleTranslator
from random import uniform

class DeepResearchAgent:
    """Agent for conducting deep research using live web search"""
    
    def __init__(self, serpapi_key):
        self.serpapi_key = serpapi_key
    
    def extract_urls(self, text: str) -> list:
        """Extract URLs from text"""
        pattern = re.compile(r"http[s]?://[^\s'\"]+")
        return list(set(pattern.findall(text)))
    
    def search_google(self, query: str) -> list:
        """Search Google and return top 5 URLs"""
        if not self.serpapi_key:
            print("Deep Research Mode Failed: SERPAPI_KEY is missing.")
            return []
        
        try:
            search = GoogleSearch({
                "q": query,
                "api_key": self.serpapi_key,
                "num": 5
            })
            results = search.get_dict()
            urls = [r["link"] for r in results.get("organic_results", [])[:5]]
            return urls
        except Exception as e:
            print(f"Deep Research Search Error: {e}")
            return []

    async def scrape_urls(self, urls: list) -> str:
        """Scrape content from multiple URLs asynchronously"""
        headers = {"User-Agent": "Mozilla/5.0"}
        async with httpx.AsyncClient(timeout=20.0, follow_redirects=True) as client:
            tasks = [self._fetch_and_parse(client, url, headers) for url in urls]
            results = await asyncio.gather(*tasks)
            text_dump = "\n\n".join([r for r in results if r])
        return text_dump

    async def _fetch_and_parse(self, client, url, headers):
        try:
            r = await client.get(url, headers=headers)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "html.parser")
                for tag in soup(["script", "style", "nav", "footer", "iframe"]):
                    tag.decompose()
                text = soup.get_text(" ", strip=True)
                if len(text) > 500:
                    return f"\n--- SOURCE: {url} ---\n{text[:20000]}"
        except Exception as e:
            print(f"Error fetching {url}: {e}")
        return ""

    def translate_large_text(self, text, target_lang):
        """Helper to translate long research summaries in chunks"""
        try:
            translator = GoogleTranslator(source="en", target=target_lang)
            chunks = [text[i:i+4000] for i in range(0, len(text), 4000)]
            translated_chunks = [translator.translate(chunk) for chunk in chunks]
            return "\n".join(translated_chunks)
        except Exception as e:
            print(f"Translation chunk error: {e}")
            return text

    async def reframe_question(self, llm, country: str, sector: str, question: str) -> str:
        """Reframe user question for optimal web search"""
        prompt = f"""You need to create a focused search query for finding current, authoritative information.
Original question: "{question}"
Context: Looking for {country} {sector} sector information
Create a concise search query (3-8 words) that will find the most relevant, current compliance information.
Just return the search query, nothing else."""
        return safe_llm_invoke(llm, prompt)

    async def summarize(self, llm, raw_text_chunks: list, country: str, sector: str, urls: list, mode: str = "deep", stm_context: list = None) -> str:
        """
        Generate comprehensive research summary with natural flow.
        Adapts style based on mode (rag/enhance/deep/shariat).
        """
        url_list = "\n".join([f"{i+1}. {url}" for i, url in enumerate(urls[:5])])
        combined_summaries = "\n---\n".join(raw_text_chunks)
        history_snippet = str(stm_context[-2:]) if stm_context else "No previous history."
        
        # 1. SHARIAT MODE (CBB Formatting)
        if mode == "shariat":
            prompt = f"""You are an AI-powered Compliance Assistant for the Central Bank of Bahrain (CBB).
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

### **Researched Information (Context):** {combined_summaries}

---

### **History Snapshot:**
{history_snippet}

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
{url_list}"""

        # 2. RAG STYLE
        elif mode == "rag":
            prompt = f"""You are a professional Compliance Knowledge Assistant with expertise in {country}'s {sector} sector.

You've researched current information from these sources:
{combined_summaries}

Provide a clear, professional response following these guidelines:
1. **Introduction:** Start by explicitly mentioning the country and sector (e.g., "In {country}'s {sector} Sector...")
2. **Core Content:** Present the information in structured paragraphs with clear flow
3. **Compliance Focus:** Highlight regulations, requirements, frameworks, and governance
4. **Practical Details:** Include key requirements, deadlines, penalties where relevant
5. **Factual & Concise:** Write 5-10 lines that are informative and actionable
6. **Professional Tone:** Clear, confident, and compliance-oriented

Never mention "document," "context," or "source text."

---
### 🌐 Sources Referenced:
{url_list}

Your professional compliance response:"""

        # 3. ENHANCE STYLE
        elif mode == "enhance":
            prompt = f"""You are a knowledgeable compliance advisor having a natural conversation with a professional colleague working in {country}'s {sector} sector.

You've researched the latest information from these sources:
{combined_summaries}

Provide a detailed, conversational response (30+ lines) as if explaining over coffee:

How you should respond:
- Talk naturally, like you're explaining this to a colleague
- Start with a brief, direct answer
- Then expand with important details they need to know
- Use real examples and scenarios when possible
- Break down complex regulations into digestible parts
- Explain WHY regulations exist, not just WHAT they are
- Include practical implications for their daily work
- Mention compliance requirements, key deadlines, or common pitfalls
- Discuss different interpretations or recent changes
- Connect related concepts for better understanding

Structure naturally (30+ lines):
1. Clear, direct answer (2-3 sentences)
2. Essential background and context
3. Specific regulations, requirements, frameworks
4. Practical implementation and real-world application
5. Compliance obligations, penalties, or best practices
6. Actionable insights or recommendations

Write with natural flow - conversational paragraphs that build on each other, not rigid sections.

---
### 🌐 Sources Referenced:
{url_list}

Your detailed, conversational response:"""

        # 4. DEEP STYLE (Default)
        else:
            prompt = f"""You're a compliance research expert who just finished researching current information about {country}'s {sector} sector.

You found information from these reliable sources:
{combined_summaries}

Now, synthesize this into a comprehensive, naturally flowing response:

1. **Key Finding:** What's the most important takeaway?
2. **Context:** Why does this matter now?
3. **Details:** What are the specific regulations, requirements, or developments?
4. **Implications:** How does this affect organizations in this sector?
5. **Expert Perspective:** What insights can you provide?
6. **Actionable Insights:** What should professionals know or do?

Write with depth and clarity, making complex compliance information accessible.

---
### 🌐 Sources Referenced:
{url_list}

Your comprehensive research summary:"""
        
        return safe_llm_invoke(llm, prompt)

    async def process(self, llm, country: str, sector: str, question: str, language: str, lang_code: str, stm_context: list, mode: str = "deep"):
        """
        Main processing pipeline for deep research.
        Determines the prompt style based on the mode argument.
        """
        
        # Step 1: Reframe question for search
        reframed = await self.reframe_question(llm, country, sector, question)
        
        # Step 2: Search web
        urls = self.search_google(reframed)
        if not urls:
            return [], "I wasn't able to find current information on this topic.", ""
        
        # Step 3: Scrape content
        scraped_text = await self.scrape_urls(urls)
        if not scraped_text or len(scraped_text) < 500:
            return urls, "I found sources but couldn't extract enough detail.", ""
        
        # Step 4: Chunk and summarize based on mode
        chunks = [scraped_text[i:i+20000] for i in range(0, len(scraped_text), 20000)]
        english_summary = await self.summarize(llm, chunks, country, sector, urls, mode, stm_context)
        
        # Step 5: Translate if needed
        final_answer = english_summary
        if lang_code and lang_code != "en" and language.lower() != "english":
            try:
                # Handle translation while preserving source links if they are tagged
                if "### 🌐 Sources Referenced:" in english_summary:
                    parts = english_summary.split("### 🌐 Sources Referenced:")
                    main_content = parts[0]
                    sources_section = "### 🌐 Sources Referenced:" + parts[1]
                    translated_content = self.translate_large_text(main_content, lang_code)
                    final_answer = translated_content + "\n\n" + sources_section
                else:
                    final_answer = self.translate_large_text(english_summary, lang_code)
            except Exception as e:
                print(f"Deep Research translation error: {e}")
        
        return urls, final_answer, english_summary


def safe_llm_invoke(llm, prompt_text, retries=3):
    """Safe LLM invocation with retry logic"""
    for attempt in range(retries):
        try:
            result = llm.invoke(prompt_text)
            if result and hasattr(result, 'content') and result.content.strip():
                return result.content
        except Exception:
            if attempt < retries - 1:
                time.sleep(uniform(1.0, 2.5))
    return "Unable to generate a response."