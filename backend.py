import os
import sqlite3
from datetime import date
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# ✅ System prompt model ke andar daal - yahi sahi jagah hai
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

💬 RESPONSE LENGTH GUIDE:
- Simple sawaal → 1-3 lines max.
- Medium sawaal → 4-8 lines. Conversational.
- Complex topic → paragraph style, list nahi.
"""

model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    system_instruction=MASTER_PROMPT  # ✅ Yahan daal system prompt
)

def init_db():
    conn = sqlite3.connect("mentor_app.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (access_code TEXT PRIMARY KEY, queries_used INTEGER, last_active TEXT)''')
    conn.commit()
    conn.close()

def get_chat_response(chat_session, user_message):
    print("⏳ Arjun dimaag laga raha hai...")
    try:
        # ✅ chat_session.send_message() use kar - yahi history maintain karta hai
        response = chat_session.send_message(user_message)
        return response.text

    except Exception as e:
        return f"❌ ERROR: Arjun ka server down hai. Details: {e}"

def start_new_chat():
    # ✅ Yeh sahi hai - naya chat session banata hai fresh history ke saath
    return model.start_chat(history=[])

if __name__ == "__main__":
    init_db()