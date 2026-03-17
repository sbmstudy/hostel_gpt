import streamlit as st
import os
import backend

# ── Secrets Setup ─────────────────────────────────────
try:
    os.environ["SUPABASE_URL"]   = st.secrets["supabase"]["url"]
    os.environ["SUPABASE_KEY"]   = st.secrets["supabase"]["key"]
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
except:
    pass

# ── Page Config ───────────────────────────────────────
st.set_page_config(
    page_title="HostelMind",
    page_icon="🌿",
    layout="centered"
)

# ── CSS ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

* { font-family: 'Plus Jakarta Sans', sans-serif !important; }

/* Background */
[data-testid="stAppViewContainer"] {
    background: #f0faf4 !important;
}
[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer, [data-testid="stToolbar"] { display: none !important; }

/* Buttons */
[data-testid="stButton"] > button {
    background: #22c55e !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 1.4rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 8px rgba(34,197,94,0.3) !important;
}
[data-testid="stButton"] > button:hover {
    background: #16a34a !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(34,197,94,0.4) !important;
}

/* Input */
[data-testid="stTextInput"] input {
    border: 1.5px solid #bbf7d0 !important;
    border-radius: 10px !important;
    background: white !important;
    font-size: 0.9rem !important;
    color: #1a1a1a !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #22c55e !important;
    box-shadow: 0 0 0 3px rgba(34,197,94,0.15) !important;
}

/* Chat input */
[data-testid="stChatInput"] {
    border: 1.5px solid #bbf7d0 !important;
    border-radius: 12px !important;
    background: white !important;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background: white !important;
    border: 1px solid #dcfce7 !important;
    border-radius: 12px !important;
    margin-bottom: 0.6rem !important;
}

/* Selectbox */
[data-testid="stSelectbox"] > div > div {
    background: white !important;
    border: 1.5px solid #bbf7d0 !important;
    border-radius: 10px !important;
    font-size: 0.85rem !important;
}
</style>
""", unsafe_allow_html=True)


# ── Session State ─────────────────────────────────────
def init_session():
    defaults = {
        "logged_in":    False,
        "access_code":  None,
        "chat_session": None,
        "messages":     [],
        "language":     "Hinglish"
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()


# ── Login Modal ───────────────────────────────────────
@st.dialog("🔐 Enter Your Room Number")
def login_modal():
    st.markdown("Apna room number dalo — sirf registered rooms ko access milega.")
    room_input = st.text_input("Room Number", placeholder="e.g., Room-204")

    if st.button("Unlock 🚀", use_container_width=True):
        if not room_input.strip():
            st.error("Room number khali hai!")
        elif not backend.is_room_allowed(room_input.strip()):
            st.error("❌ Yeh room number registered nahi hai.")
        else:
            st.session_state.access_code  = room_input.strip()
            st.session_state.logged_in    = True
            st.session_state.chat_session = backend.start_new_chat()
            st.session_state.messages     = []
            st.rerun()


# ════════════════════════════════════════════════════
# LOGGED OUT
# ════════════════════════════════════════════════════
if not st.session_state.logged_in:

    # Header
    st.markdown("""
    <div style='text-align:center; padding: 3rem 1rem 1.5rem;'>
        <div style='font-size:3rem; margin-bottom:0.5rem;'>🌿</div>
        <h1 style='font-size:2.2rem; font-weight:700; color:#15803d; margin-bottom:0.4rem;'>
            HostelMind
        </h1>
        <p style='color:#6b7280; font-size:1rem; margin-bottom:0.3rem;'>
            Koi bhi topic — seedha, simple, apni bhasha mein.
        </p>
        <p style='color:#9ca3af; font-size:0.85rem;'>
            Your personal AI study companion 🧠
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Feature cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style='background:white; border:1px solid #dcfce7; border-radius:12px;
             padding:1rem; text-align:center;'>
            <div style='font-size:1.5rem;'>⚡</div>
            <div style='font-size:0.78rem; color:#374151; font-weight:600; margin-top:0.3rem;'>
                Instant Help
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style='background:white; border:1px solid #dcfce7; border-radius:12px;
             padding:1rem; text-align:center;'>
            <div style='font-size:1.5rem;'>🗣️</div>
            <div style='font-size:0.78rem; color:#374151; font-weight:600; margin-top:0.3rem;'>
                Hinglish Mode
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style='background:white; border:1px solid #dcfce7; border-radius:12px;
             padding:1rem; text-align:center;'>
            <div style='font-size:1.5rem;'>🔒</div>
            <div style='font-size:0.78rem; color:#374151; font-weight:600; margin-top:0.3rem;'>
                Room Access
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Login button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚪 Enter Your Room", use_container_width=True):
            login_modal()

    # Credits
    st.markdown("""
    <div style='text-align:center; margin-top:3rem; padding-top:1.5rem;
         border-top:1px solid #dcfce7;'>
        <p style='font-size:0.78rem; color:#9ca3af;'>
            Built with ❤️ by <strong style='color:#15803d;'>Shreyas</strong>
            &nbsp;·&nbsp; Powered by Gemini AI
        </p>
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════
# LOGGED IN
# ════════════════════════════════════════════════════
else:
    if st.session_state.chat_session is None:
        st.session_state.chat_session = backend.start_new_chat()
        st.session_state.messages     = []

    # Top bar
    st.markdown(f"""
    <div style='background:white; border:1px solid #dcfce7; border-radius:12px;
         padding:0.8rem 1.2rem; margin-bottom:1rem;
         display:flex; align-items:center; justify-content:space-between;'>
        <div style='display:flex; align-items:center; gap:0.6rem;'>
            <span style='font-size:1.2rem;'>🌿</span>
            <div>
                <div style='font-weight:700; color:#15803d; font-size:0.95rem;'>
                    HostelMind
                </div>
                <div style='font-size:0.72rem; color:#9ca3af;'>
                    {st.session_state.access_code} · Session Active
                </div>
            </div>
        </div>
        <div style='font-size:0.72rem; color:#9ca3af;'>
            Built by <strong style='color:#15803d;'>Shreyas</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Controls
    col_lang, col_gap, col_new = st.columns([2, 3, 2])
    with col_lang:
        lang = st.selectbox(
            "Lang",
            ["Hinglish", "English"],
            index=0 if st.session_state.language == "Hinglish" else 1,
            label_visibility="collapsed"
        )
        st.session_state.language = lang

    with col_new:
        if st.button("🔄 New Chat", use_container_width=True):
            st.session_state.chat_session = backend.start_new_chat()
            st.session_state.messages     = []
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Empty state
    if not st.session_state.messages:
        st.markdown("""
        <div style='text-align:center; padding:2.5rem 1rem; color:#9ca3af;'>
            <div style='font-size:2.5rem; margin-bottom:0.8rem;'>🧠</div>
            <div style='font-weight:600; color:#374151; font-size:1rem;'>
                Kya samajhna hai aaj?
            </div>
            <div style='font-size:0.82rem; margin-top:0.4rem;'>
                Arrays, DSA, OS, DBMS — kuch bhi puch!
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Chat history
    for message in st.session_state.messages:
        avatar = "🧑‍💻" if message["role"] == "user" else "🤖"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # Chat input
    placeholder = (
        "Kuch bhi puch — Hinglish mein baat karte hain..."
        if st.session_state.language == "Hinglish"
        else "Ask anything — let's figure it out together..."
    )

    prompt = st.chat_input(placeholder)

    if prompt:
        lang_prefix = (
            "[Respond in Hinglish — casual Hindi+English mix]\n"
            if st.session_state.language == "Hinglish"
            else "[Respond in clear, friendly English]\n"
        )
        full_prompt = lang_prefix + prompt

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Arjun soch raha hai... 🤔"):
                ai_reply = backend.get_chat_response(
                    st.session_state.chat_session,
                    full_prompt,
                    st.session_state.access_code
                )
                if "❌ ERROR" in ai_reply:
                    st.error(ai_reply)
                else:
                    st.markdown(ai_reply)

        st.session_state.messages.append({
            "role": "assistant",
            "content": ai_reply
        })
