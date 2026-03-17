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
    page_title="HostelMind — Your Study Companion",
    page_icon="🏮",
    layout="centered"
)

# ── Global CSS ────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f !important;
    color: #e8e0d0 !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(196,145,70,0.13) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(120,80,200,0.07) 0%, transparent 50%),
        #0a0a0f !important;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none !important; }

/* ── Hide Streamlit default elements ── */
#MainMenu, footer, .stDeployButton { display: none !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb { background: rgba(196,145,70,0.3); border-radius: 2px; }

/* ── Hero Section ── */
.hm-hero {
    text-align: center;
    padding: 3.5rem 1rem 2rem;
    position: relative;
}

.hm-badge {
    display: inline-block;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #c49146;
    border: 1px solid rgba(196,145,70,0.35);
    padding: 0.3rem 1rem;
    border-radius: 999px;
    margin-bottom: 1.4rem;
    background: rgba(196,145,70,0.06);
}

.hm-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.4rem, 7vw, 3.8rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #f5dfa0 0%, #c49146 45%, #a0673a 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.6rem;
}

.hm-subtitle {
    font-family: 'DM Sans', sans-serif;
    font-size: 1rem;
    font-weight: 300;
    color: rgba(232,224,208,0.55);
    letter-spacing: 0.01em;
    margin-bottom: 2.5rem;
    line-height: 1.6;
}

/* ── Feature Pills ── */
.hm-pills {
    display: flex;
    justify-content: center;
    gap: 0.6rem;
    flex-wrap: wrap;
    margin-bottom: 2.5rem;
}

.hm-pill {
    font-size: 0.78rem;
    color: rgba(232,224,208,0.65);
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 0.35rem 0.9rem;
    border-radius: 999px;
    font-family: 'DM Sans', sans-serif;
}

/* ── Divider ── */
.hm-divider {
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(196,145,70,0.25), transparent);
    margin: 1.5rem 0;
}

/* ── Login Card ── */
.hm-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(196,145,70,0.18);
    border-radius: 16px;
    padding: 2rem 1.8rem;
    margin: 0 auto 2rem;
    max-width: 440px;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 40px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05);
}

.hm-card-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #f5dfa0;
    margin-bottom: 0.35rem;
}

.hm-card-sub {
    font-size: 0.82rem;
    color: rgba(232,224,208,0.45);
    margin-bottom: 1.4rem;
    line-height: 1.5;
}

/* ── Input fields ── */
[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(196,145,70,0.25) !important;
    border-radius: 10px !important;
    color: #e8e0d0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 1rem !important;
    transition: border-color 0.2s ease !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: rgba(196,145,70,0.6) !important;
    box-shadow: 0 0 0 3px rgba(196,145,70,0.1) !important;
}
[data-testid="stTextInput"] input::placeholder { color: rgba(232,224,208,0.3) !important; }
[data-testid="stTextInput"] label {
    color: rgba(232,224,208,0.6) !important;
    font-size: 0.8rem !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Buttons ── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #c49146, #a0673a) !important;
    color: #0a0a0f !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.04em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem 1.5rem !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 15px rgba(196,145,70,0.25) !important;
}
[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(196,145,70,0.4) !important;
    filter: brightness(1.08) !important;
}
[data-testid="stButton"] > button:active {
    transform: translateY(0px) !important;
}

/* ── Secondary button (New Chat) ── */
.secondary-btn [data-testid="stButton"] > button {
    background: rgba(255,255,255,0.05) !important;
    color: rgba(232,224,208,0.7) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    box-shadow: none !important;
    font-size: 0.8rem !important;
    padding: 0.45rem 1rem !important;
}
.secondary-btn [data-testid="stButton"] > button:hover {
    background: rgba(255,255,255,0.08) !important;
    border-color: rgba(196,145,70,0.3) !important;
    box-shadow: none !important;
}

/* ── Welcome Bar ── */
.hm-welcome {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(196,145,70,0.08);
    border: 1px solid rgba(196,145,70,0.2);
    border-radius: 12px;
    padding: 0.8rem 1.2rem;
    margin-bottom: 1.5rem;
}
.hm-welcome-left { display: flex; align-items: center; gap: 0.8rem; }
.hm-welcome-dot {
    width: 8px; height: 8px; border-radius: 50%;
    background: #4ade80;
    box-shadow: 0 0 8px rgba(74,222,128,0.6);
    flex-shrink: 0;
}
.hm-welcome-name {
    font-family: 'Syne', sans-serif;
    font-size: 0.9rem;
    font-weight: 700;
    color: #f5dfa0;
}
.hm-welcome-sub {
    font-size: 0.75rem;
    color: rgba(232,224,208,0.45);
    margin-top: 0.1rem;
}

/* ── Chat Messages ── */
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 14px !important;
    padding: 1rem 1.2rem !important;
    margin-bottom: 0.8rem !important;
}
[data-testid="stChatMessage"][data-testid*="user"] {
    border-color: rgba(196,145,70,0.2) !important;
    background: rgba(196,145,70,0.05) !important;
}

/* ── Chat Input ── */
[data-testid="stChatInput"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(196,145,70,0.25) !important;
    border-radius: 14px !important;
}
[data-testid="stChatInput"] textarea {
    color: #e8e0d0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    background: transparent !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: rgba(232,224,208,0.3) !important; }

/* ── Selectbox (language toggle) ── */
[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #e8e0d0 !important;
    font-size: 0.82rem !important;
}

/* ── Success / Error ── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.85rem !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] p {
    color: rgba(232,224,208,0.5) !important;
    font-size: 0.82rem !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Streamlit dialog ── */
[data-testid="stModal"] {
    background: #111118 !important;
    border: 1px solid rgba(196,145,70,0.2) !important;
    border-radius: 18px !important;
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
@st.dialog("🔐 Access Your Study Space")
def login_modal():
    st.markdown("""
        <p style='font-size:0.85rem; color:rgba(232,224,208,0.55); margin-bottom:1.2rem; font-family:DM Sans,sans-serif;'>
        Enter your room number to unlock your personal AI study companion.
        </p>
    """, unsafe_allow_html=True)

    room_input = st.text_input(
        "Room Number",
        placeholder="e.g., Room-204",
        label_visibility="visible"
    )

    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("Unlock Access 🚀", use_container_width=True):
            if not room_input.strip():
                st.error("Room number empty hai bhai!")
            elif not backend.is_room_allowed(room_input.strip()):
                st.error("❌ Yeh room number registered nahi hai.")
            else:
                st.session_state.access_code  = room_input.strip()
                st.session_state.logged_in    = True
                st.session_state.chat_session = backend.start_new_chat()
                st.session_state.messages     = []
                st.rerun()


# ════════════════════════════════════════════════════
# LOGGED OUT — Landing Page
# ════════════════════════════════════════════════════
if not st.session_state.logged_in:

    st.markdown("""
    <div class='hm-hero'>
        <div class='hm-badge'>🏮 Hostel Study AI</div>
        <div class='hm-title'>HostelMind</div>
        <div class='hm-subtitle'>
            Koi bhi topic — seedha, simple, apni bhasha mein.<br>
            Your personal AI mentor, always in the room.
        </div>
        <div class='hm-pills'>
            <span class='hm-pill'>⚡ Instant Explanations</span>
            <span class='hm-pill'>🧠 Hinglish + English</span>
            <span class='hm-pill'>💬 Real Conversations</span>
            <span class='hm-pill'>🔒 Room-Based Access</span>
        </div>
    </div>
    <div class='hm-divider'></div>
    """, unsafe_allow_html=True)

    # Login card
    st.markdown("""
    <div class='hm-card'>
        <div class='hm-card-title'>Begin Your Session</div>
        <div class='hm-card-sub'>
            Room number verify hone ke baad tumhara personal AI study space unlock ho jaayega.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Enter Your Room →", use_container_width=True):
            login_modal()

    # Footer
    st.markdown("""
    <div style='text-align:center; margin-top:3rem; padding-top:1.5rem;
         border-top: 1px solid rgba(255,255,255,0.05);'>
        <p style='font-size:0.72rem; color:rgba(232,224,208,0.2);
           font-family:DM Sans,sans-serif; letter-spacing:0.08em;'>
            BUILT FOR HOSTEL RESIDENTS &nbsp;·&nbsp; POWERED BY GEMINI AI
        </p>
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════
# LOGGED IN — Chat Interface
# ════════════════════════════════════════════════════
else:
    # Safety check
    if st.session_state.chat_session is None:
        st.session_state.chat_session = backend.start_new_chat()
        st.session_state.messages     = []

    # ── Top Bar ──
    st.markdown(f"""
    <div class='hm-welcome'>
        <div class='hm-welcome-left'>
            <div class='hm-welcome-dot'></div>
            <div>
                <div class='hm-welcome-name'>🏮 {st.session_state.access_code}</div>
                <div class='hm-welcome-sub'>Study session active</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Controls Row ──
    col_lang, col_gap, col_new = st.columns([2, 3, 2])

    with col_lang:
        lang = st.selectbox(
            "Language",
            ["Hinglish", "English"],
            index=0 if st.session_state.language == "Hinglish" else 1,
            label_visibility="collapsed"
        )
        st.session_state.language = lang

    with col_new:
        st.markdown("<div class='secondary-btn'>", unsafe_allow_html=True)
        if st.button("🔄 New Chat", use_container_width=True):
            st.session_state.chat_session = backend.start_new_chat()
            st.session_state.messages     = []
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='hm-divider'></div>", unsafe_allow_html=True)

    # ── Chat History ──
    if not st.session_state.messages:
        st.markdown(f"""
        <div style='text-align:center; padding: 2.5rem 1rem; opacity:0.5;'>
            <div style='font-size:2rem; margin-bottom:0.8rem;'>🧠</div>
            <div style='font-family:Syne,sans-serif; font-size:1rem;
                 font-weight:600; color:#f5dfa0; margin-bottom:0.4rem;'>
                Kya samajhna hai aaj?
            </div>
            <div style='font-size:0.8rem; color:rgba(232,224,208,0.4);
                 font-family:DM Sans,sans-serif;'>
                Arrays, DSA, OS, DBMS — kuch bhi puch. Arjun yahan hai.
            </div>
        </div>
        """, unsafe_allow_html=True)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # ── Chat Input ──
    placeholder = (
        "Kuch bhi puch — Hinglish mein baat karte hain..."
        if st.session_state.language == "Hinglish"
        else "Ask anything — let's figure it out together..."
    )

    prompt = st.chat_input(placeholder)

    if prompt:
        # Language instruction add karo prompt mein
        lang_prefix = (
            "[Respond in Hinglish — casual Hindi+English mix]\n"
            if st.session_state.language == "Hinglish"
            else "[Respond in clear, friendly English]\n"
        )
        full_prompt = lang_prefix + prompt

        # User message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI Response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
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
