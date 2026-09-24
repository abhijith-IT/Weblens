import streamlit as st
from llm.agent import run_agent

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="WebLens | GECBH",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# SVG Icons (Lucide-style monochrome outline icons)
ICON_GLOBE = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>'
ICON_BUILDING = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/><path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2"/><path d="M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2"/><path d="M10 6h4"/><path d="M10 10h4"/><path d="M10 14h4"/><path d="M10 18h4"/></svg>'
ICON_LAYERS = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65"/><path d="m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65"/></svg>'
ICON_LANDMARK = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" x2="21" y1="22" y2="22"/><line x1="6" x2="6" y1="18" y2="11"/><line x1="10" x2="10" y1="18" y2="11"/><line x1="14" x2="14" y1="18" y2="11"/><line x1="18" x2="18" y1="18" y2="11"/><polygon points="12 2 20 7 4 7"/></svg>'
ICON_BRIEFCASE = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="14" x="2" y="7" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>'
ICON_MONITOR = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="14" x="2" y="3" rx="2"/><line x1="8" x2="16" y1="21" y2="21"/><line x1="12" x2="12" y1="17" y2="21"/></svg>'
ICON_NETWORK = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="16" y="16" width="6" height="6" rx="1"/><rect x="2" y="16" width="6" height="6" rx="1"/><rect x="9" y="2" width="6" height="6" rx="1"/><path d="M5 16v-3a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v3"/><path d="M12 12V8"/></svg>'

# Source mapping for sidebar and metadata formatting
TRUSTED_SOURCES = [
    ("GECBH Official", "https://www.gecbh.ac.in/", ICON_BUILDING),
    ("Departments", "https://www.gecbh.ac.in/departments.php", ICON_LAYERS),
    ("Facilities", "https://www.gecbh.ac.in/facilities.php", ICON_LANDMARK),
    ("Placement & Career", "https://www.gecbh.ac.in/placement.php", ICON_BRIEFCASE),
    ("GECBH CSI", "https://www.gecbh.ac.in/csi.php", ICON_MONITOR),
    ("CSI Student Branch (Limited Access)", "https://csigecbh.in/", ICON_NETWORK),
]

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown(
    """
<style>
/* Root variables */
:root {
    --bg-main: #0F1115;
    --bg-secondary: #16181D;
    --border-color: #262931;
    --text-primary: #ECECF1;
    --text-secondary: #8E95A3;
    --accent: #387BFF;
}

/* Global reset */
.stApp {
    background-color: var(--bg-main) !important;
    color: var(--text-primary) !important;
}

.main .block-container {
    max-width: 850px;
    padding-top: 2rem;
    padding-bottom: 8rem;
}

/* Hide defaults */
header { background: transparent !important; }
#MainMenu, footer { visibility: hidden; display: none; }
.stDeployButton { display: none; }

/* Landing Page Elements */
.landing-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    margin-top: 5vh;
    margin-bottom: 2rem;
    animation: fadeIn 0.5s ease-out;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.brand-mark {
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 60px;
    height: 60px;
    background-color: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 14px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.2);
    color: var(--accent);
}
.brand-title {
    font-size: 2rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: var(--text-primary);
    letter-spacing: -0.02em;
}
.brand-subtitle {
    font-size: 0.95rem;
    color: var(--text-secondary);
    max-width: 480px;
    line-height: 1.5;
}

/* Suggested questions */
div.stButton > button {
    background-color: var(--bg-main) !important;
    border: 1px solid var(--border-color) !important;
    color: var(--text-secondary) !important;
    border-radius: 10px !important;
    padding: 0.8rem 1rem !important;
    font-size: 0.9rem !important;
    text-align: left !important;
    min-height: 54px !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
}
div.stButton > button p {
    margin: 0 !important;
    font-size: 0.9rem !important;
    display: flex;
    align-items: center;
}
div.stButton > button:hover {
    background-color: var(--bg-secondary) !important;
    border-color: #38404E !important;
    color: var(--text-primary) !important;
}

/* Add generic search SVG icon to suggestion buttons */
div.stButton > button p::before {
    content: "";
    display: inline-block;
    width: 16px;
    height: 16px;
    margin-right: 8px;
    background-color: currentColor;
    mask: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>') no-repeat center / contain;
    -webkit-mask: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>') no-repeat center / contain;
}

/* Override the icon for the clear conversation button in sidebar */
section[data-testid="stSidebar"] div.stButton > button p::before {
    mask: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/><line x1="10" x2="10" y1="11" y2="17"/><line x1="14" x2="14" y1="11" y2="17"/></svg>') no-repeat center / contain;
    -webkit-mask: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/><line x1="10" x2="10" y1="11" y2="17"/><line x1="14" x2="14" y1="11" y2="17"/></svg>') no-repeat center / contain;
}

/* Subtle grounding statement */
.grounding-statement {
    text-align: center;
    font-size: 0.75rem;
    color: var(--text-secondary);
    margin-top: 2.5rem;
    letter-spacing: 0.02em;
}

/* Chat Input Area */
div[data-testid="stChatInput"] {
    background-color: var(--bg-main) !important;
    padding-bottom: 2rem !important;
}
div[data-testid="stChatInput"] > div {
    background-color: var(--bg-secondary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 12px !important;
    padding: 0.1rem 0.5rem !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3) !important;
}
div[data-testid="stChatInput"] textarea {
    color: var(--text-primary) !important;
    font-size: 0.95rem !important;
}
div[data-testid="stChatInput"] textarea::placeholder {
    color: var(--text-secondary) !important;
}
div[data-testid="stChatInput"] button {
    background-color: var(--accent) !important;
    color: #fff !important;
    border-radius: 8px !important;
    transition: opacity 0.2s !important;
}
div[data-testid="stChatInput"] button:hover {
    opacity: 0.9 !important;
}
div[data-testid="stChatInput"] button svg {
    fill: #fff !important;
}

/* Chat Messages */
div[data-testid="stChatMessage"] {
    background-color: transparent !important;
    border: none !important;
    padding: 1.5rem 0 !important;
    gap: 1rem !important;
}
div[data-testid="stChatMessageAvatar"] {
    background-color: var(--bg-secondary) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 6px !important;
    width: 28px !important;
    height: 28px !important;
}
div[data-testid="stChatMessageContent"] {
    color: var(--text-primary) !important;
    font-size: 0.95rem !important;
    line-height: 1.6 !important;
}

/* Tool & Source Output in Chat */
.tool-badge-container {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background-color: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 6px;
    padding: 0.25rem 0.6rem;
    font-size: 0.7rem;
    color: var(--text-secondary);
    margin-top: 0.8rem;
    margin-bottom: 0.5rem;
}
.tool-badge-container span {
    color: var(--text-primary);
    font-weight: 500;
}
.source-card-chat {
    background-color: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 6px;
    padding: 0.6rem 0.8rem;
    margin-top: 0.5rem;
    display: inline-block;
    max-width: 100%;
}
.source-card-header {
    font-size: 0.65rem;
    text-transform: uppercase;
    color: var(--text-secondary);
    letter-spacing: 0.05em;
    margin-bottom: 0.3rem;
}
.source-card-title {
    font-size: 0.8rem;
    color: var(--text-primary);
    font-weight: 500;
    margin-bottom: 0.2rem;
}
.source-card-link {
    font-size: 0.75rem;
    color: var(--text-secondary) !important;
    text-decoration: none !important;
    word-break: break-all;
    display: block;
}
.source-card-link:hover {
    color: var(--accent) !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: var(--bg-main) !important;
    border-right: 1px solid var(--border-color) !important;
}
.sidebar-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 2rem;
    color: var(--text-primary);
}
.sidebar-header svg {
    color: var(--accent);
}
.sidebar-section {
    font-size: 0.7rem;
    text-transform: uppercase;
    color: var(--text-secondary);
    letter-spacing: 0.05em;
    margin-bottom: 0.8rem;
}
.sidebar-link {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.5rem 0.8rem;
    border-radius: 6px;
    color: var(--text-secondary) !important;
    text-decoration: none !important;
    font-size: 0.85rem;
    margin-bottom: 0.2rem;
    transition: all 0.2s;
}
.sidebar-link:hover {
    background-color: var(--bg-secondary);
    color: var(--text-primary) !important;
}
.sidebar-link svg {
    color: var(--text-secondary);
    transition: color 0.2s;
}
.sidebar-link:hover svg {
    color: var(--text-primary);
}
</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_query" not in st.session_state:
    st.session_state.pending_query = None


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown(
        f"""<div class="sidebar-header">
{ICON_GLOBE} WebLens
</div>
<div class="sidebar-section">Trusted Sources</div>
""",
        unsafe_allow_html=True,
    )
    
    for name, url, icon in TRUSTED_SOURCES:
        st.markdown(
            f'<a href="{url}" target="_blank" class="sidebar-link">{icon} {name}</a>',
            unsafe_allow_html=True
        )
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_query = None
        st.rerun()


# =========================================================
# HERO & SUGGESTIONS
# =========================================================

if not st.session_state.messages:
    
    st.markdown(
        f"""<div class="landing-container">
<div class="brand-mark">{ICON_GLOBE}</div>
<div class="brand-title">WebLens</div>
<div class="brand-subtitle">Domain-scoped AI web agent for GECBH. Answers using trusted sources.</div>
</div>""",
        unsafe_allow_html=True,
    )

    examples = [
        "What is the vision of GECBH?",
        "What departments are available at GECBH?",
        "What facilities are available at GECBH?",
        "What information is available about placements at GECBH?",
    ]

    def set_pending_query(q):
        st.session_state.pending_query = q

    col1, col2 = st.columns(2)
    for index, question in enumerate(examples):
        with (col1 if index % 2 == 0 else col2):
            st.button(
                question, 
                key=f"example_{index}", 
                use_container_width=True,
                on_click=set_pending_query,
                args=(question,)
            )

    st.markdown(
        """<div class="grounding-statement">
Answers grounded in trusted GECBH sources
</div>""",
        unsafe_allow_html=True,
    )


# =========================================================
# CHAT HISTORY
# =========================================================

def get_source_metadata(url):
    for name, source_url, _ in TRUSTED_SOURCES:
        if source_url in url or url in source_url:
            return name
    return "Web Source"

for message in st.session_state.messages:
    
    # We use built-in Streamlit generic avatars ("user"/"assistant") which automatically render as professional icons instead of emojis.
    avatar = "assistant" if message["role"] == "assistant" else "user"
    
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

        if message["role"] == "assistant":
            tool_name = message.get("tool_name")
            source_url = message.get("source_url")

            if tool_name:
                st.markdown(
                    f"""<div class="tool-badge-container">
<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.77 3.77z"></path></svg>
Used tool: <span>{tool_name}</span>
</div>""",
                    unsafe_allow_html=True,
                )

            if source_url:
                for url in source_url.split(", "):
                    source_name = get_source_metadata(url)
                    st.markdown(
                        f"""<div class="source-card-chat">
<div class="source-card-header">Source</div>
<div class="source-card-title">{source_name}</div>
<a href="{url}" target="_blank" class="source-card-link">{url}</a>
</div>""",
                        unsafe_allow_html=True,
                    )


# =========================================================
# CHAT INPUT
# =========================================================

query = st.chat_input("Ask anything about GECBH...")


# =========================================================
# PROCESS QUERY
# =========================================================

if st.session_state.pending_query:
    query = st.session_state.pending_query
    st.session_state.pending_query = None

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user", avatar="user"):
        st.markdown(query)

    with st.chat_message("assistant", avatar="assistant"):
        with st.spinner("Finding the right trusted source..."):
            try:
                result = run_agent(query)
                answer = result.get("answer", "No answer was returned.")
                tool_name = result.get("tool_name")
                source_url = result.get("source_url")

                st.markdown(answer)

                if tool_name:
                    st.markdown(
                        f"""<div class="tool-badge-container">
<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.77 3.77z"></path></svg>
Used tool: <span>{tool_name}</span>
</div>""",
                        unsafe_allow_html=True,
                    )

                if source_url:
                    for url in source_url.split(", "):
                        source_name = get_source_metadata(url)
                        st.markdown(
                            f"""<div class="source-card-chat">
<div class="source-card-header">Source</div>
<div class="source-card-title">{source_name}</div>
<a href="{url}" target="_blank" class="source-card-link">{url}</a>
</div>""",
                            unsafe_allow_html=True,
                        )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "tool_name": tool_name,
                        "source_url": source_url,
                    }
                )

            except Exception as exc:
                error_text = str(exc).lower()

                if "429" in error_text or "resource_exhausted" in error_text or "quota" in error_text:
                    message = "⚠️ **Gemini API quota reached.**\n\nPlease try again after the quota resets."
                elif "503" in error_text or "unavailable" in error_text or "high demand" in error_text:
                    message = "⚠️ **Gemini is temporarily unavailable.**\n\nPlease try again later."
                elif "401" in error_text or "403" in error_text or "api key" in error_text or "permission" in error_text:
                    message = "⚠️ **Gemini API authentication error.**\n\nPlease check your API key."
                elif "timeout" in error_text or "connection" in error_text or "failed to fetch" in error_text:
                    message = "⚠️ **Unable to access the web source.**\n\nPlease try again later."
                else:
                    message = "⚠️ **WebLens encountered an error.**\n\nThe request could not be completed."

                st.error(message)

                with st.expander("Technical details"):
                    st.code(str(exc))

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": message,
                    }
                )