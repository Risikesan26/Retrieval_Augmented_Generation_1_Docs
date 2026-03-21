import streamlit as st
import requests

# =========================
# CONFIG
# =========================
API_BASE = "http://127.0.0.1:8000"

# =========================
# PAGE SETUP
# =========================
st.set_page_config(
    page_title="DocChat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# DARK THEME CSS
# =========================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    * { font-family: 'Inter', sans-serif; box-sizing: border-box; }

    /* App background */
    .stApp { background-color: #0e0e10; color: #e2e2e5; }
    .stApp > header { background: transparent; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #16161a !important;
        border-right: 1px solid #2a2a2e;
    }
    [data-testid="stSidebar"] * { color: #e2e2e5 !important; }

    /* Main content */
    .main .block-container { padding: 2rem 2.5rem 6rem 2.5rem; max-width: 860px; margin: auto; }

    /* Page title */
    .page-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.4px;
        margin-bottom: 0.2rem;
    }
    .page-sub {
        font-size: 0.85rem;
        color: #555;
        margin-bottom: 1.8rem;
    }

    /* Chat bubbles */
    .bubble-wrap { display: flex; margin: 0.6rem 0; align-items: flex-start; }
    .bubble-wrap.user  { justify-content: flex-end; }
    .bubble-wrap.bot   { justify-content: flex-start; }

    .bubble {
        max-width: 75%;
        padding: 0.8rem 1.1rem;
        border-radius: 18px;
        font-size: 0.92rem;
        line-height: 1.65;
        word-break: break-word;
    }
    .bubble.user {
        background: #5865f2;
        color: #ffffff;
        border-bottom-right-radius: 4px;
    }
    .bubble.bot {
        background: #1e1e24;
        color: #dcdcdc;
        border: 1px solid #2a2a32;
        border-bottom-left-radius: 4px;
    }

    /* Avatar */
    .avatar {
        width: 30px; height: 30px;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 0.72rem; font-weight: 700;
        flex-shrink: 0;
        margin-top: 2px;
    }
    .avatar.user { background: #5865f2; color: #fff; margin-left: 8px; }
    .avatar.bot  { background: #2a2a32; color: #aaa; margin-right: 8px; }

    /* Context chunks */
    .context-chunk {
        background: #121216;
        border-left: 3px solid #5865f2;
        padding: 0.7rem 1rem;
        border-radius: 0 8px 8px 0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: #888;
        line-height: 1.6;
        margin-bottom: 0.6rem;
    }
    .chunk-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.7rem;
        font-weight: 600;
        color: #5865f2;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 0.3rem;
    }

    /* Upload zone */
    [data-testid="stFileUploader"] {
        background: #1a1a20 !important;
        border: 1.5px dashed #3a3a44 !important;
        border-radius: 10px !important;
    }
    [data-testid="stFileUploader"] * { color: #aaa !important; }

    /* File pills */
    .file-pill {
        background: #1e1e26;
        border: 1px solid #2e2e38;
        border-radius: 8px;
        padding: 0.45rem 0.8rem;
        margin-bottom: 0.35rem;
        font-size: 0.82rem;
        color: #bbb;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .file-pill .dot { width:7px; height:7px; background:#22c55e; border-radius:50%; flex-shrink:0; }

    /* Badges */
    .badge-ok   { display:inline-flex; align-items:center; gap:6px; background:#14532d; color:#86efac; padding:5px 12px; border-radius:999px; font-size:0.8rem; font-weight:500; margin-top:6px; }
    .badge-err  { display:inline-flex; align-items:center; gap:6px; background:#450a0a; color:#fca5a5; padding:5px 12px; border-radius:999px; font-size:0.8rem; font-weight:500; margin-top:6px; }
    .badge-info { display:inline-flex; align-items:center; gap:6px; background:#1e3a5f; color:#93c5fd; padding:5px 12px; border-radius:999px; font-size:0.8rem; font-weight:500; margin-top:6px; }

    /* Buttons */
    .stButton > button {
        background: #1e1e26 !important;
        color: #ccc !important;
        border: 1px solid #2e2e38 !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        width: 100% !important;
        transition: all 0.2s !important;
    }
    .stButton > button:hover {
        background: #2a2a36 !important;
        color: #fff !important;
        border-color: #5865f2 !important;
    }

    /* Toggle */
    [data-testid="stToggle"] label { color: #aaa !important; font-size: 0.85rem !important; }

    /* Chat input */
    [data-testid="stChatInput"] textarea {
        background: #1a1a22 !important;
        border: 1.5px solid #2e2e3a !important;
        border-radius: 14px !important;
        color: #e2e2e5 !important;
        font-size: 0.92rem !important;
    }
    [data-testid="stChatInput"] textarea::placeholder { color: #444 !important; }
    [data-testid="stChatInput"] button { background: #5865f2 !important; border-radius: 10px !important; }

    /* Expander */
    [data-testid="stExpander"] {
        background: #13131a !important;
        border: 1px solid #2a2a32 !important;
        border-radius: 10px !important;
        margin-top: 0.4rem !important;
        margin-left: 38px !important;
    }
    [data-testid="stExpander"] summary { color: #555 !important; font-size: 0.8rem !important; }

    /* Divider */
    hr { border-color: #222 !important; margin: 1rem 0 !important; }

    /* Spinner */
    .stSpinner > div { border-top-color: #5865f2 !important; }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: #0e0e10; }
    ::-webkit-scrollbar-thumb { background: #2a2a32; border-radius: 4px; }

    /* Empty state */
    .empty-state { text-align: center; padding: 5rem 2rem; }
    .empty-state .icon { font-size: 3rem; margin-bottom: 1rem; }
    .empty-state .title { font-size: 1rem; color: #444; font-weight: 500; }
    .empty-state .sub   { font-size: 0.85rem; color: #333; margin-top: 0.4rem; }

    /* Brand */
    .brand { font-size: 1.3rem; font-weight: 700; color: #ffffff !important; letter-spacing: -0.3px; }
    .brand span { color: #5865f2 !important; }

    /* Section label */
    .sec-label {
        font-size: 0.72rem;
        font-weight: 600;
        color: #555;
        text-transform: uppercase;
        letter-spacing: 0.9px;
        margin-bottom: 0.5rem;
        margin-top: 0.2rem;
    }

    /* Warning */
    [data-testid="stAlert"] {
        background: #1a1a10 !important;
        border: 1px solid #3a3a20 !important;
        color: #d4d4a0 !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "indexed_files" not in st.session_state:
    st.session_state.indexed_files = set()
if "show_context" not in st.session_state:
    st.session_state.show_context = True

# =========================
# HELPERS
# =========================
def auto_index(file) -> tuple[bool, str]:
    try:
        files = {"file": (file.name, file.getvalue(), "application/pdf")}
        r = requests.post(f"{API_BASE}/upload", files=files, timeout=60)
        if r.status_code == 200:
            return True, r.json().get("message", "Indexed successfully")
        return False, r.json().get("detail", "Upload failed")
    except requests.exceptions.ConnectionError:
        return False, "Cannot reach API — is the server running?"

def ask_api(question: str) -> tuple[str, list]:
    try:
        r = requests.post(f"{API_BASE}/ask", params={"question": question}, timeout=30)
        if r.status_code == 200:
            data = r.json()
            return data.get("answer", "No answer."), data.get("context_used", [])
        return f"Error: {r.json().get('detail', 'Unknown error')}", []
    except requests.exceptions.ConnectionError:
        return "⚠️ Cannot reach the API server. Make sure it is running on port 8000.", []

def render_message(msg):
    role = msg["role"]
    content = msg["content"]
    if role == "user":
        st.markdown(f"""
        <div class="bubble-wrap user">
            <div class="bubble user">{content}</div>
            <div class="avatar user">You</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="bubble-wrap bot">
            <div class="avatar bot">AI</div>
            <div class="bubble bot">{content}</div>
        </div>""", unsafe_allow_html=True)
        if st.session_state.show_context and msg.get("context"):
            with st.expander("📎 View source context", expanded=False):
                for i, chunk in enumerate(msg["context"], 1):
                    st.markdown(f"""
                    <div class="chunk-label">Source {i}</div>
                    <div class="context-chunk">{chunk}</div>
                    """, unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("<p class='brand'>Doc<span>Chat</span></p>", unsafe_allow_html=True)
    st.markdown("<p style='color:#333; font-size:0.78rem; margin-top:-0.4rem; margin-bottom:1.2rem;'>RAG-powered document Q&A</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Upload — auto index on drop
    st.markdown("<p class='sec-label'>Upload PDF</p>", unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Drop a PDF here",
        type=["pdf"],
        label_visibility="collapsed",
        key="pdf_uploader"
    )

    if uploaded:
        if uploaded.name not in st.session_state.indexed_files:
            with st.spinner(f"Auto-indexing {uploaded.name}..."):
                ok, msg = auto_index(uploaded)
            if ok:
                st.session_state.indexed_files.add(uploaded.name)
                st.markdown(f"<div class='badge-ok'>✓ {msg}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='badge-err'>✗ {msg}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='badge-info'>ℹ Already indexed</div>", unsafe_allow_html=True)

    # Indexed files list
    if st.session_state.indexed_files:
        st.markdown("---")
        st.markdown("<p class='sec-label'>Indexed Documents</p>", unsafe_allow_html=True)
        for fname in sorted(st.session_state.indexed_files):
            short = fname if len(fname) <= 26 else fname[:23] + "..."
            st.markdown(f"<div class='file-pill'><span class='dot'></span>{short}</div>", unsafe_allow_html=True)

    st.markdown("---")

    # Settings
    st.markdown("<p class='sec-label'>Settings</p>", unsafe_allow_html=True)
    st.session_state.show_context = st.toggle("Show source context", value=st.session_state.show_context)
    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)

    if st.button("🗑  Clear conversation"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("<p style='color:#2a2a2a; font-size:0.72rem;'>Groq · Cohere · ChromaDB</p>", unsafe_allow_html=True)

# =========================
# MAIN
# =========================
st.markdown("<p class='page-title'>Ask your documents</p>", unsafe_allow_html=True)

if st.session_state.indexed_files:
    names = ", ".join(sorted(st.session_state.indexed_files)[:2])
    extra = f" +{len(st.session_state.indexed_files)-2} more" if len(st.session_state.indexed_files) > 2 else ""
    st.markdown(f"<p class='page-sub'>Chatting with: <span style='color:#5865f2; font-weight:500'>{names}{extra}</span></p>", unsafe_allow_html=True)
else:
    st.markdown("<p class='page-sub'>Upload a PDF in the sidebar — it will be indexed automatically.</p>", unsafe_allow_html=True)

# Render history
if st.session_state.messages:
    for msg in st.session_state.messages:
        render_message(msg)
else:
    st.markdown("""
    <div class="empty-state">
        <div class="icon">💬</div>
        <div class="title">No messages yet</div>
        <div class="sub">Drop a PDF on the left, then ask anything</div>
    </div>
    """, unsafe_allow_html=True)

# Chat input
if question := st.chat_input("Ask anything about your document..."):
    if not st.session_state.indexed_files:
        st.warning("Upload a PDF first — it will be indexed automatically.")
    else:
        user_msg = {"role": "user", "content": question}
        st.session_state.messages.append(user_msg)
        render_message(user_msg)

        with st.spinner(""):
            answer, context = ask_api(question)

        bot_msg = {"role": "assistant", "content": answer, "context": context}
        st.session_state.messages.append(bot_msg)
        render_message(bot_msg)
        st.rerun()