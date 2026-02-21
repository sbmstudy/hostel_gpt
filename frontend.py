import streamlit as st
import backend 
import time

# DB Initialize
backend.init_db()

# Page Config
st.set_page_config(page_title="The 1% Mentor", page_icon="⛩️", layout="centered")


st.markdown("""
    <style>
    /* Gradient Background for header */
    .hero-text {
        background: -webkit-linear-gradient(45deg, #FF4B2B, #FF416C);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3em;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0px;
    }
    
    /* Motion Button Hack (Hover Effects) */
    div.stButton > button {
        transition: all 0.3s ease-in-out;
        border-radius: 8px;
        border: 2px solid #FF416C;
        color: white;
    }
    div.stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0px 8px 15px rgba(255, 65, 108, 0.4);
    }
    </style>
""", unsafe_allow_html=True)


@st.dialog("🔐 Enter The Dojo")
def login_modal():
    st.markdown("Bhai, is knowledge ko access karne ke liye apni identity verify kar.")
    access_code = st.text_input("Tera Room Number / ID:", placeholder="e.g., Room-204")
    
    if st.button("Unlock Knowledge 🚀"):
        if access_code:
            st.session_state.access_code = access_code
            st.session_state.logged_in = True
            st.rerun() 
        else:
            st.error("Bhai, khali chhodega toh kaise andar aane du?")


if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False


if "chat_session" not in st.session_state:
    st.session_state.chat_session = backend.start_new_chat()


if "messages" not in st.session_state:
    st.session_state.messages = []


if not st.session_state.logged_in:
    st.markdown("<div class='hero-text'>⛩️ The 1% Mentor built by SHREYAS_M</div>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: gray;'>First Principles. Friendly Guide.</h4>", unsafe_allow_html=True)
    st.divider()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Start Authentication Process", use_container_width=True):
            login_modal()

else:
    st.success(f"🔓 Access Granted: Welcome {st.session_state.access_code}")
    st.markdown("<div class='hero-text'>⛩️ The Dojo is Open use karo kuch bhii seekhne ke liye</div>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; color: gray;'>Tumara choota  bhai yahan hai. Puch kya samajhna hai.</h5>", unsafe_allow_html=True)
    st.divider()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Puch bhai, Arrays, Pointers, ya DSA ka koi bhi doubt...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        
        with st.chat_message("assistant"):
            with st.spinner("Choota bhai dimaag laga raha hai..."):
                ai_reply = backend.get_chat_response(st.session_state.chat_session, prompt)
                
                if "❌ ERROR" in ai_reply:
                    st.error(ai_reply)
                else:
                    st.markdown(ai_reply)
                    st.session_state.messages.append({"role": "assistant", "content": ai_reply})