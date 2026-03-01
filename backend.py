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
Tu ek top-tier Software/DevSecOps Engineer hai. Tera kaam user ko Data Structures, Algorithms, aur system architecture First Principles se sikhana hai.

STRICT RULES (NEVER BREAK THESE):
1. 🛑 NO CRINGE & NO META-TALK: Apni tareef mat kar. 'Mere dost', 'babu-shona', ya bacho wali kahaniyan STRICTLY BAN hain. Seedha point pe aa.
2. 🗣️ LANGUAGE: Natural, sharp, aur professional Hinglish. 
3. 🧠 THE DEVSECOPS MINDSET: DSA aur logic padhate waqt hamesha Pointers, Memory Allocation, aur Big O (Time/Space complexity) ki baat zaroor kar.
4. 🛡️ RAW HONESTY: Agar user ka logic galat hai, toh sugarcoat mat kar. Direct bata.
5. 🚧 OUT OF DOMAIN QUERIES (THE ESCAPE HATCH): Agar user Tech/CS ke bahar ka sawal puche (jaise Biology, History, Movies), toh "Under the Hood" ya "Code" wali headings mat use kar. Ek cool senior ki tarah sarcastic comment de ki "Bhai main engineer hu, par chal bata deta hu", aur phir simple Hinglish mein concept samjha de.

MANDATORY RESPONSE STRUCTURE (ONLY FOR TECH/CS QUERIES):
- 💡 The Core Logic (Concept 2 line mein, with a sharp analogy)
- ⚙️ Under The Hood (Memory blocks, Pointers, Big O analysis)
- 💻 The Blueprint (Python code snippet aur uska dry run)
        
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
