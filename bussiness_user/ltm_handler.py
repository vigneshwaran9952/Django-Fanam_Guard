"""
LTM Handler - Long Term Memory Management
Manages persistent storage and retrieval of chat sessions (history)
Enables users to continue conversations from where they left off
"""

import json
import os
from datetime import datetime


def save_to_ltm(filepath, chat_history, username):
    """
    Saves the current session to LTM (persistent storage).
    Stores both the chat history and STM context for session resumption.
    
    Args:
        filepath: Path to save the session file
        chat_history: List of chat messages
        username: Username of the current user
    """
    if not chat_history or not filepath:
        return
    
    history_folder = os.path.dirname(filepath)
    if not os.path.exists(history_folder):
        os.makedirs(history_folder)
    
    # Extract STM context from chat history
    stm_context = extract_stm_from_history(chat_history)
    
    # Generate session title
    title = generate_session_title(chat_history)
    
    # Prepare data structure
    session_data = {
        "title": title,
        "username": username,
        "timestamp": datetime.now().isoformat(),
        "last_updated": datetime.now().isoformat(),
        "chat_history": chat_history,
        "stm_context": stm_context,
        "version": "1.0"
    }
    
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(session_data, f, indent=4, ensure_ascii=False)
        print(f"✅ Session saved to LTM: {os.path.basename(filepath)}")
    except Exception as e:
        print(f"❌ Error saving session to LTM: {e}")


def load_from_ltm(filepath):
    """
    Loads a session from LTM (persistent storage).
    Restores both chat history and STM context for natural continuation.
    
    Args:
        filepath: Path to the session file
    
    Returns:
        Tuple of (chat_history, stm_context)
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            session_data = json.load(f)
        
        chat_history = session_data.get("chat_history", [])
        stm_context = session_data.get("stm_context", [])
        
        # If old format without STM, extract it
        if not stm_context and chat_history:
            stm_context = extract_stm_from_history(chat_history)
        
        print(f"✅ Session loaded from LTM: {os.path.basename(filepath)}")
        print(f"   Restored {len(chat_history)} messages and {len(stm_context)} STM turns")
        
        return chat_history, stm_context
        
    except Exception as e:
        print(f"❌ Error loading session from LTM: {e}")
        return [], []


def extract_stm_from_history(chat_history, max_turns=5):
    """
    Extracts STM context from chat history.
    Used when loading old sessions or creating new STM from history.
    
    Args:
        chat_history: List of chat messages
        max_turns: Maximum number of turns to extract
    
    Returns:
        List of STM context turns
    """
    stm_context = []
    
    # Process chat history in pairs (user + assistant)
    i = 0
    while i < len(chat_history) - 1:
        user_msg = chat_history[i]
        assistant_msg = chat_history[i + 1]
        
        # Extract content based on message format
        if isinstance(user_msg, dict):
            user_content = user_msg.get("content", "")
        else:
            user_content = user_msg[1] if isinstance(user_msg, tuple) else str(user_msg)
        
        if isinstance(assistant_msg, dict):
            assistant_content = assistant_msg.get("content", "")
        else:
            assistant_content = assistant_msg[1] if isinstance(assistant_msg, tuple) else str(assistant_msg)
        
        stm_context.append({
            "question": user_content,
            "answer": assistant_content[:1000]  # Truncate to save space
        })
        
        i += 2
    
    # Keep only the last max_turns
    if len(stm_context) > max_turns:
        stm_context = stm_context[-max_turns:]
    
    return stm_context


def generate_session_title(chat_history):
    """
    Generates a title for the session based on the first user message.
    
    Args:
        chat_history: List of chat messages
    
    Returns:
        String title for the session
    """
    if not chat_history:
        return "New Chat"
    
    for msg in chat_history:
        if isinstance(msg, dict):
            role = msg.get("role", "")
            content = msg.get("content", "")
        elif isinstance(msg, tuple):
            role = msg[0]
            content = msg[1]
        else:
            continue
        
        if role == "user" and content.strip():
            title = content.strip().replace("\n", " ")
            if len(title) > 50:
                title = title[:50] + "..."
            return title
    
    return "Untitled Session"


def get_user_sessions(username, history_folder):
    """
    Retrieves all LTM sessions for a specific user.
    Returns sessions sorted by most recent first.
    
    Args:
        username: Username to filter sessions
        history_folder: Folder containing session files
    
    Returns:
        List of session dictionaries with metadata
    """
    if not os.path.exists(history_folder):
        return []
    
    sessions = []
    prefix = f"{username}_"
    
    for filename in os.listdir(history_folder):
        if filename.startswith(prefix) and filename.endswith(".json"):
            filepath = os.path.join(history_folder, filename)
            
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    session_data = json.load(f)
                
                sessions.append({
                    "filename": filename,
                    "filepath": filepath,
                    "title": session_data.get("title", filename),
                    "timestamp": session_data.get("timestamp", datetime.min.isoformat()),
                    "last_updated": session_data.get("last_updated", session_data.get("timestamp", datetime.min.isoformat())),
                    "message_count": len(session_data.get("chat_history", []))
                })
            except Exception as e:
                print(f"⚠️  Skipping corrupted session file: {filename} - {e}")
                continue
    
    # Sort by last_updated (most recent first)
    sessions.sort(key=lambda x: x["last_updated"], reverse=True)
    
    return sessions


def delete_session(filepath):
    """
    Deletes a session file from LTM.
    
    Args:
        filepath: Path to the session file to delete
    
    Returns:
        Boolean indicating success
    """
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"✅ Session deleted: {os.path.basename(filepath)}")
            return True
        return False
    except Exception as e:
        print(f"❌ Error deleting session: {e}")
        return False


def get_session_summary(filepath):
    """
    Gets a summary of a session without loading full content.
    Useful for displaying session previews.
    
    Args:
        filepath: Path to the session file
    
    Returns:
        Dictionary with session summary information
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            session_data = json.load(f)
        
        chat_history = session_data.get("chat_history", [])
        
        # Count messages
        user_messages = sum(1 for msg in chat_history if 
                          (isinstance(msg, dict) and msg.get("role") == "user") or
                          (isinstance(msg, tuple) and msg[0] == "user"))
        
        return {
            "title": session_data.get("title", "Untitled"),
            "timestamp": session_data.get("timestamp", ""),
            "last_updated": session_data.get("last_updated", session_data.get("timestamp", "")),
            "total_messages": len(chat_history),
            "user_messages": user_messages,
            "has_stm": "stm_context" in session_data
        }
    except Exception as e:
        print(f"❌ Error getting session summary: {e}")
        return None


def update_session_timestamp(filepath):
    """
    Updates the last_updated timestamp for a session.
    Called when a user continues an old conversation.
    
    Args:
        filepath: Path to the session file
    """
    try:
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                session_data = json.load(f)
            
            session_data["last_updated"] = datetime.now().isoformat()
            
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(session_data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"⚠️  Could not update session timestamp: {e}")


def merge_sessions(filepath1, filepath2, output_filepath):
    """
    Merges two sessions into one.
    Useful for combining related conversations.
    
    Args:
        filepath1: First session file
        filepath2: Second session file
        output_filepath: Path for merged session
    
    Returns:
        Boolean indicating success
    """
    try:
        # Load both sessions
        with open(filepath1, "r", encoding="utf-8") as f:
            session1 = json.load(f)
        with open(filepath2, "r", encoding="utf-8") as f:
            session2 = json.load(f)
        
        # Merge chat histories
        merged_history = session1.get("chat_history", []) + session2.get("chat_history", [])
        
        # Create merged session
        merged_session = {
            "title": f"{session1.get('title', 'Session 1')} + {session2.get('title', 'Session 2')}",
            "username": session1.get("username", ""),
            "timestamp": session1.get("timestamp", datetime.now().isoformat()),
            "last_updated": datetime.now().isoformat(),
            "chat_history": merged_history,
            "stm_context": extract_stm_from_history(merged_history),
            "version": "1.0",
            "merged_from": [filepath1, filepath2]
        }
        
        # Save merged session
        with open(output_filepath, "w", encoding="utf-8") as f:
            json.dump(merged_session, f, indent=4, ensure_ascii=False)
        
        print(f"✅ Sessions merged successfully: {os.path.basename(output_filepath)}")
        return True
        
    except Exception as e:
        print(f"❌ Error merging sessions: {e}")
        return False


def export_session_to_text(filepath, output_format="txt"):
    """
    Exports a session to a human-readable text format.
    
    Args:
        filepath: Path to the session file
        output_format: Format for export ("txt" or "md")
    
    Returns:
        String with formatted session content
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            session_data = json.load(f)
        
        title = session_data.get("title", "Untitled Session")
        timestamp = session_data.get("timestamp", "Unknown")
        chat_history = session_data.get("chat_history", [])
        
        if output_format == "md":
            output = f"# {title}\n\n"
            output += f"**Date:** {timestamp}\n\n"
            output += "---\n\n"
        else:
            output = f"{'='*60}\n"
            output += f"{title}\n"
            output += f"Date: {timestamp}\n"
            output += f"{'='*60}\n\n"
        
        # Format messages
        for i, msg in enumerate(chat_history):
            if isinstance(msg, dict):
                role = msg.get("role", "unknown")
                content = msg.get("content", "")
            elif isinstance(msg, tuple):
                role = msg[0]
                content = msg[1]
            else:
                continue
            
            if output_format == "md":
                if role == "user":
                    output += f"### 👤 User:\n{content}\n\n"
                else:
                    output += f"### 🤖 Assistant:\n{content}\n\n"
                output += "---\n\n"
            else:
                output += f"[{role.upper()}]:\n{content}\n\n"
                output += f"{'-'*60}\n\n"
        
        return output
        
    except Exception as e:
        print(f"❌ Error exporting session: {e}")
        return None