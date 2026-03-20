import os
import streamlit as st
from datetime import datetime
import google.generativeai as genai
from supabase import create_client, Client

try:
    SUPABASE_URL   = st.secrets["supabase"]["url"]
    SUPABASE_KEY   = st.secrets["supabase"]["key"]
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    # Local ke liye .env fallback
    from dotenv import load_dotenv
    load_dotenv()
    SUPABASE_URL   = os.getenv("SUPABASE_URL")
    SUPABASE_KEY   = os.getenv("SUPABASE_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# ── Clients ──
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
genai.configure(api_key=GOOGLE_API_KEY)
genai.configure(api_key=GOOGLE_API_KEY)

MASTER_PROMPT = """
You are Arjun — a witty, helpful, slightly chaotic Indian guy who lives on WhatsApp and somehow ended up inside an AI. You are NOT a robot. You are NOT an assistant. You are NOT "here to help" in that boring corporate way. You're just... Arjun. Bas.

🗣️ TONE & LANGUAGE RULES:
1. Always reply in Hinglish — Hindi + English mix, just like we actually talk in India.
   - ✅ "Bhai yaar, yeh toh simple hai, sun"
   - ❌ "Certainly! I'd be happy to assist you with that."

2. Use casual WhatsApp-style formatting:
   - Short sentences. Fragments even.
   - Use "..." for dramatic pause
   - Use "CAPS" for emphasis kabhi kabhi
   - Emojis but not OTT — 1-2 max per message
   - Never use bullet points like a PowerPoint presentation.

3. Humour is MANDATORY but natural.

🧠 PERSONALITY RULES:
- You have opinions. Share them.
- You give straight answers. No fluff.
- You remember context within the conversation.

🚫 THINGS YOU NEVER DO:
- NEVER say "Certainly!", "Of course!", "Absolutely!"
- NEVER use "As an AI language model..."
- NEVER be overly formal
"""

model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    system_instruction=MASTER_PROMPT
)

# ── Auth Functions ────────────────────────────────────

def is_room_allowed(room_number: str) -> bool:
    """Check karo ki room number allowed hai ya nahi"""
    try:
        result = supabase.table("allowed_rooms")\
            .select("room_number")\
            .eq("room_number", room_number)\
            .execute()
        return len(result.data) > 0
    except Exception as e:
        print(f"Auth error: {e}")
        return False

def upsert_user(room_number: str):
    try:
        existing = supabase.table("users")\
            .select("*")\
            .eq("room_number", room_number)\
            .execute()

        if existing.data:
            current = existing.data[0]["queries_used"] or 0
            supabase.table("users")\
                .update({
                    "queries_used": current + 1,
                    "last_active": datetime.now().isoformat()
                })\
                .eq("room_number", room_number)\
                .execute()
        else:
            supabase.table("users")\
                .insert({
                    "room_number": room_number,
                    "queries_used": 1,
                    "last_active": datetime.now().isoformat()
                })\
                .execute()
    except Exception as e:
        print(f"Upsert error: {e}")

# ── Chat Functions ────────────────────────────────────

def save_message(room_number: str, role: str, message: str):
    try:
        supabase.table("chats").insert({
            "room_number": room_number,
            "role": role,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }).execute()
    except Exception as e:
        print(f"Save message error: {e}")

def get_chat_response(chat_session, user_message: str, room_number: str) -> str:
    print("⏳ Arjun dimaag laga raha hai...")
    try:
        save_message(room_number, "user", user_message)
        response = chat_session.send_message(user_message)
        ai_reply = response.text
        
        save_message(room_number, "assistant", ai_reply)

        upsert_user(room_number)

        return ai_reply

    except Exception as e:
        return f"❌ ERROR: Arjun ka server down hai. Details: {e}"

def start_new_chat():
    return model.start_chat(history=[])
