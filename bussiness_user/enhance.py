"""
Enhance Mode Module
Provides comprehensive, detailed responses (30+ lines) with in-depth analysis
"""

from langchain_core.prompts import PromptTemplate
from deep_translator import GoogleTranslator
from random import uniform
import time

# Enhanced Mode Prompt Template (Detailed, 30+ lines)
# Note: Added {conversation_history} to the prompt for better continuity
enhance_prompt_template = """
You are a knowledgeable compliance advisor having a natural conversation with a professional colleague. 
You understand {country}'s {sector} sector deeply and can explain complex regulations in a clear, engaging way.

The person asking you is working in {sector} and needs detailed, practical guidance. They've asked: "{question}"

Previous conversation context for continuity:
{conversation_history}

Here's what you know from your expertise:
{context}

How you should respond:
- Maintain a professional advisory tone (banking/compliance style)
- Do NOT start with overly casual greetings like "Hey there"
- Start with a clear professional opener such as:
  "Certainly.", "That’s an important regulatory question.", or
  "To answer your question directly..."
- Talk naturally, like an experienced compliance colleague
- Talk naturally, like you're explaining this over coffee to a colleague
- Start with a brief, direct answer to their specific question
- Then expand with important details they need to know
- Use real examples and scenarios when possible
- Break down complex regulations into digestible parts
- Explain WHY regulations exist, not just WHAT they are
- Include practical implications - what does this mean for their daily work?
- Mention compliance requirements, key deadlines, or common pitfalls
- If there are different interpretations or recent changes, discuss them
- Connect related concepts that might help them understand better

Structure your response like a natural conversation:
1. Start with a clear, direct answer (2-3 sentences)
2. Provide essential background and context (explaining the bigger picture)
3. Detail the specific regulations, requirements, or frameworks
4. Discuss practical implementation and real-world application
5. Mention compliance obligations, penalties, or best practices
6. End with actionable insights or recommendations

Write 30+ lines with natural flow - not rigid sections, but conversational paragraphs that build on each other.

Your response should feel like helpful advice from an experienced colleague, not a textbook or legal document.

Remember: Only use information from your expertise above. If something isn't covered there, acknowledge what you can share and what you can't.

Your detailed, conversational response:
"""

# Added 'conversation_history' to input_variables
enhance_prompt = PromptTemplate(
    input_variables=["context", "question", "country", "sector", "conversation_history"],
    template=enhance_prompt_template
)

def translate_large_text(text, target_lang):
    """
    Splits text into chunks of 4000 characters to prevent Google Translate API 
    from failing on long 'Enhance Mode' responses.
    """
    try:
        translator = GoogleTranslator(source="en", target=target_lang)
        chunks = [text[i:i+4000] for i in range(0, len(text), 4000)]
        translated_chunks = []
        for chunk in chunks:
            translated_chunks.append(translator.translate(chunk))
        return "\n".join(translated_chunks)
    except Exception as e:
        print(f"Chunked translation error: {e}")
        return text

# FIXED: Added conversation_context as the 8th parameter
def process_enhance_mode(llm, question_en, rag_context, country, sector, language, lang_code, conversation_context):
    """
    Process question in Enhanced Mode - returns detailed 30+ line response
    """
    
    # Passing the new conversation_context to the prompt
    full_prompt = enhance_prompt.format(
        context=rag_context,
        question=question_en,
        country=country,
        sector=sector,
        conversation_history=conversation_context
    )
    
    english_answer = safe_llm_invoke(llm, full_prompt)
    
    final_answer = english_answer
    if lang_code and lang_code != "en" and language.lower() != "english":
        try:
            fallback_phrases = [
                "sorry, no detailed content found",
                "no relevant information",
                "no detailed content found"
            ]
            if not any(phrase in english_answer.lower() for phrase in fallback_phrases):
                final_answer = translate_large_text(english_answer, lang_code)
        except Exception as e:
            print(f"Translation error in enhance mode: {e}")
            final_answer = english_answer
    
    return final_answer, english_answer

def safe_llm_invoke(llm, prompt_text, retries=3):
    """Safe LLM invocation with retry logic"""
    for attempt in range(retries):
        try:
            result = llm.invoke(prompt_text)
            if result and hasattr(result, 'content') and result.content.strip():
                return result.content
        except Exception as e:
            print(f"LLM invocation error (attempt {attempt + 1}): {e}")
            if attempt < retries - 1:
                time.sleep(uniform(1.0, 2.5))
    return "Unable to generate a detailed response. Please try again."