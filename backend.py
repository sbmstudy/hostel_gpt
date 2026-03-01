import os
import sqlite3
from datetime import date
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash') 

def init_db():
    conn = sqlite3.connect("mentor_app.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (access_code TEXT PRIMARY KEY, queries_used INTEGER, last_active TEXT)''')
    conn.commit()
    conn.close()

def get_chat_response(chat_session, user_message):
    
    print("⏳ Mentor dimaag laga raha hai...")
    try:

        master_prompt = f"""

        
        """
        
        response = model.generate_content(master_prompt)
        ai_reply = response.text
        
        return ai_reply

    except Exception as e:
        return f"❌ ERROR: Mentor ka server down hai. Details: {e}"

def start_new_chat():
    return model.start_chat(history=[])


if __name__ == "__main__":
    init_db()
