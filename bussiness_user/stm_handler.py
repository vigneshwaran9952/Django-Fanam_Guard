"""
STM Handler - Short Term Memory Management
Manages conversation context within a session for natural, continuous chat flow
"""

def add_to_stm(stm_context, user_question, assistant_answer, max_turns=5):
    """
    Adds a Q&A turn to the STM context.
    Maintains only the last `max_turns` conversation pairs.
    
    Args:
        stm_context: List of conversation turns
        user_question: The user's question
        assistant_answer: The assistant's response
        max_turns: Maximum number of turns to keep in memory (default: 5)
    """
    stm_context.append({
        "question": user_question,
        "answer": assistant_answer[:1000]  # Truncate long answers to save memory
    })
    
    # Keep only the last max_turns
    if len(stm_context) > max_turns:
        stm_context.pop(0)


def get_conversation_summary(stm_context):
    """
    Creates a summary of recent conversation for context.
    
    Args:
        stm_context: List of conversation turns
    
    Returns:
        String summary of the conversation
    """
    if not stm_context:
        return ""
    
    summary_parts = []
    for i, turn in enumerate(stm_context, 1):
        summary_parts.append(f"Turn {i}:")
        summary_parts.append(f"User asked: {turn['question']}")
        summary_parts.append(f"Assistant responded about: {turn['answer'][:200]}...")
        summary_parts.append("")
    
    return "\n".join(summary_parts)


def reframe_question_with_context(llm, current_question, stm_context, country, sector):
    """
    Reframes the current question using conversation history for natural continuity.
    This makes follow-up questions feel natural and contextual.
    
    Args:
        llm: Language model instance
        current_question: The user's current question
        stm_context: List of previous conversation turns
        country: User's selected country
        sector: User's selected sector
    
    Returns:
        Reframed question with full context
    """
    if not stm_context:
        return current_question
    
    # Build conversation history
    conversation_history = []
    for turn in stm_context[-3:]:  # Use last 3 turns for context
        conversation_history.append(f"User: {turn['question']}")
        conversation_history.append(f"Assistant: {turn['answer'][:300]}...")
    
    history_text = "\n".join(conversation_history)
    
    reframe_prompt = f"""You are helping maintain conversational continuity. Given the recent conversation history and a new user question, reframe the question to include necessary context for standalone understanding.

Recent Conversation:
{history_text}

Current User Question: "{current_question}"

Context: {country}'s {sector} sector

Task: If the current question refers to previous conversation (uses words like "that", "this", "it", "them", "how about", etc.), rewrite it as a standalone question that includes the referenced context. If it's already standalone, return it as-is.

Examples:
- "What about the penalties?" → "What are the penalties for non-compliance with [specific regulation mentioned earlier]?"
- "How does this affect small businesses?" → "How does [specific regulation/topic from previous answer] affect small businesses in {country}'s {sector} sector?"
- "Any recent changes?" → "Have there been any recent changes to [specific topic discussed]?"

Reframed Question:"""

    try:
        result = llm.invoke(reframe_prompt)
        reframed = result.content.strip()
        
        # Clean up any extra formatting
        reframed = reframed.replace("Reframed Question:", "").strip()
        reframed = reframed.strip('"').strip("'").strip()
        
        # If reframing failed or returned empty, use original
        if not reframed or len(reframed) < 5:
            return current_question
            
        return reframed
    except Exception as e:
        print(f"Error reframing question: {e}")
        return current_question


def create_contextualized_prompt(base_prompt, rag_context, question, country, sector, conversation_context):
    """
    Creates a prompt that includes both RAG context and conversation history.
    Balances 60% RAG data with 40% conversation continuity.
    
    Args:
        base_prompt: The base prompt template
        rag_context: Retrieved RAG context
        question: Current question (possibly reframed)
        country: User's country
        sector: User's sector
        conversation_context: Summary of recent conversation
    
    Returns:
        Complete prompt string
    """
    # If no conversation context, use standard prompt
    if not conversation_context:
        return base_prompt.format(
            context=rag_context,
            question=question,
            country=country,
            sector=sector
        )
    
    # Enhanced prompt with conversation awareness
    enhanced_template = f"""You are a professional Compliance Knowledge Assistant with expertise across India, the United States, the United Arab Emirates, and China.
You provide insights into compliance, regulations, legal frameworks, governance, and policy for the sectors: Banking, Finance, Healthcare, and Environment.

### Recent Conversation Context:
{conversation_context}

### Current Question Context:
The user is now asking: "{question}"

This question may be a follow-up to the previous conversation. Use both the RAG Context (primary source - 90% weight) and the conversation history (continuity - 10% weight) to provide a natural, contextual response.

### Response Guidelines:
1. Answer the current question directly without recap or filler.
Only reference earlier points if explicitly required.
2. **Primary Source:** Base your answer primarily (90%) on the RAG Context below
3. **Conversation Integration:** Use conversation history (10%) to maintain natural flow and reference previous points when relevant
4. **Core Domain Check:** Focus on the user's selected sector ({sector})
5. **Sector Mismatch Fallback:** If asking about a different sector, respond: "To maintain focus on your current workflow, please ask questions related to the **{sector}** sector."
6. **Country Flexibility:** Answer questions about different countries within the selected sector
8. **Style & Structure:**
   * Write in a clear, confident, conversational tone
   * Use structured paragraphs and/or bullet points
   * Expand acronyms on first use
   * Be factual, concise (30 plus lines), and engaging
9. **Guardrails:**
   * Never mention "document," "context," or "source text", or "while starting dont start with country and sector name example (In UAE's Banking sector))
   * Work only on the selected sector
   * Maintain natural conversation flow
### STRICT RESPONSE OPENING RULE

- Start immediately with the compliance answer.
- Do NOT use filler introductions such as:
  "Continuing our discussion..."
  "As mentioned earlier..."
  "In India's banking sector..."
- The first sentence must directly address the user's question.
- Follow-up context must be integrated silently, without narration.

## Make sure while response dont start with Eg: Continuing our discussion on critical compliance measures in India's banking sector  , Start with Natural way of response   
### User Context:
- **User's Selected Country:** {country}
- **User's Selected Sector:** {sector}

### RAG Context (Primary Source - 60%):
{rag_context}

**Answer:**"""

    return enhanced_template


def update_stm_context(stm_context, removed_index):
    """
    Updates STM context when a conversation turn is removed (e.g., rewrite).
    
    Args:
        stm_context: List of conversation turns
        removed_index: Index of the removed turn
    """
    # Calculate which STM entry corresponds to the removed chat
    # Each chat pair (user + assistant) = 1 STM entry
    stm_index = removed_index // 2
    
    if 0 <= stm_index < len(stm_context):
        stm_context.pop(stm_index)


def clear_stm(stm_context):
    """
    Clears the entire STM context (used when starting a new session).
    
    Args:
        stm_context: List of conversation turns
    """
    stm_context.clear()


def get_stm_size(stm_context):
    """
    Returns the number of conversation turns in STM.
    
    Args:
        stm_context: List of conversation turns
    
    Returns:
        Integer count of turns
    """
    return len(stm_context)


def get_last_turn(stm_context):
    """
    Gets the last conversation turn from STM.
    Useful for suggestion generation and context.
    
    Args:
        stm_context: List of conversation turns
    
    Returns:
        Dictionary with 'question' and 'answer', or None if empty
    """
    if not stm_context:
        return None
    return stm_context[-1]