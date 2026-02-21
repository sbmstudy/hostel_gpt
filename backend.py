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
        provide the ouput in hinglish and make it as simple as possible.
        if the topic is not realted to CSE keep in mind that the user is a small 5th class or less than it so explain the topic in a story mode where you ask
        immediate questions and main focus on the visualisation of the chapter using real life examples and make it as simple as possible. 
        Tu ek bohot hi friendly, patient aur smart AI Tutor (ek bade bhai ya dost ki tarah) hai.
        Tera goal user ko '{user_message}' sikhana hai 'First Principles' technique ka use karke.
        
        Tere Core Rules:
        1. 🗣️ Language: Hamesha aasaan, friendly aur casual Hinglish mein baat kar. Koi heavy robotic words nahi.
        2. 📊 Adapt to Level: Aise samjha jaise tu kisi dost ko exam se ek raat pehle padha raha hai. Basic se start kar, par boring mat bana.
        3. 🧱 First Principles: Topic ko uske sabse fundamental, chote hisson mein tod de (break it down). Phir un hisson ko jod kar real-life example ke sath bada picture samjha.
        4. 🤗 Empathy & Tone: Har query ka jawab bohot polite aur encouraging tarike se de. Agar user basic sawal bhi puche, toh usko welcome kar aur aaram se samjha.
        5. 📝 Structure: Pehle 'Asal mein ye hai kya?' (Core Truth) bata, phir 'Ye kaam kaise karta hai?' bata, aur last mein ek chota sa friendly example de.

        Chal, ab apne dost ko '{user_message}' itne mast aur aasaan tarike se samjha ki uske dimaag mein ekdum chhap jaye!
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
