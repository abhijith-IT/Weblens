import streamlit as st

from llm.agent import run_agent

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="WebLens | GECBH",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed",
)


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
    margin-top: 10vh;
    margin-bottom: 2rem;
    animation: fadeIn 0.5s ease-out;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.brand-mark {
    font-size: 2.2rem;
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
}
.brand-title {
    font-size: 2rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: var(--text-primary);
    letter-spacing: -0.02em;
}
.brand-subtitle {
    font-size: 1rem;
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
}
div.stButton > button:hover {
    background-color: var(--bg-secondary) !important;
    border-color: #38404E !important;
    color: var(--text-primary) !important;
}

/* Trusted Sources */
.sources-container {
    display: flex;
    justify-content: center;
    gap: 0.8rem;
    flex-wrap: wrap;
    margin-top: 2rem;
}
.source-tag {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.3rem 0.8rem;
    border-radius: 6px;
    background-color: var(--bg-secondary);
    border: 1px solid var(--border-color);
    font-size: 0.75rem;
    color: var(--text-secondary);
}
.source-tag a {
    color: var(--text-secondary) !important;
    text-decoration: none !important;
    transition: color 0.2s;
}
.source-tag a:hover {
    color: var(--text-primary) !important;
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
    font-size: 0.75rem;
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
.source-card-link {
    font-size: 0.8rem;
    color: var(--accent) !important;
    text-decoration: none !important;
    word-break: break-all;
    display: block;
}
.source-card-link:hover {
    text-decoration: underline !important;
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
    gap: 0.5rem;
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
        """<div class="sidebar-header">
<span>🌐</span> WebLens
</div>
<div class="sidebar-section">Trusted Sources</div>
<a href="https://www.gecbh.ac.in/" target="_blank" class="sidebar-link">🏫 GECBH Official</a>
<a href="https://www.gecbh.ac.in/csi.php" target="_blank" class="sidebar-link">💻 GECBH CSI</a>
<a href="https://csigecbh.in/" target="_blank" class="sidebar-link">🌐 CSI Student Branch</a>
<br>""",
        unsafe_allow_html=True,
    )
    
    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_query = None
        st.rerun()


# =========================================================
# HERO & SUGGESTIONS
# =========================================================

if not st.session_state.messages:
    
    st.markdown(
        """<div class="landing-container">
<div class="brand-mark">🌐</div>
<div class="brand-title">WebLens</div>
<div class="brand-subtitle">Domain-scoped AI web agent for GECBH. Answers using trusted sources.</div>
</div>""",
        unsafe_allow_html=True,
    )

    examples = [
        ("🏫", "What is the vision of GECBH?"),
        ("💻", "What activities are associated with CSI at GECBH?"),
        ("👤", "Who is the staff advisor listed on the GECBH CSI page?"),
        ("🌐", "What is the CSI Student Branch at GECBH?"),
    ]

    col1, col2 = st.columns(2)
    for index, (icon, question) in enumerate(examples):
        with (col1 if index % 2 == 0 else col2):
            if st.button(f"{icon}  {question}", key=f"example_{index}", use_container_width=True):
                st.session_state.pending_query = question
                st.rerun()

    st.markdown(
        """<div class="sources-container">
<div class="source-tag">🏫 <a href="https://www.gecbh.ac.in/" target="_blank">GECBH Official</a></div>
<div class="source-tag">💻 <a href="https://www.gecbh.ac.in/csi.php" target="_blank">GECBH CSI</a></div>
<div class="source-tag">🌐 <a href="https://csigecbh.in/" target="_blank">CSI Student Branch</a></div>
</div>""",
        unsafe_allow_html=True,
    )


# =========================================================
# CHAT HISTORY
# =========================================================

for message in st.session_state.messages:
    
    avatar = "🌐" if message["role"] == "assistant" else "👤"
    
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

        if message["role"] == "assistant":
            tool_name = message.get("tool_name")
            source_url = message.get("source_url")

            if tool_name:
                st.markdown(
                    f"""<div class="tool-badge-container">
<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.77 3.77z"></path></svg>
Used tool: <span>{tool_name}</span>
</div>""",
                    unsafe_allow_html=True,
                )

            if source_url:
                for url in source_url.split(", "):
                    st.markdown(
                        f"""<div class="source-card-chat">
<div class="source-card-header">Source</div>
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
    with st.chat_message("user", avatar="👤"):
        st.markdown(query)

    with st.chat_message("assistant", avatar="🌐"):
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
<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.77 3.77z"></path></svg>
Used tool: <span>{tool_name}</span>
</div>""",
                        unsafe_allow_html=True,
                    )

                if source_url:
                    for url in source_url.split(", "):
                        st.markdown(
                            f"""<div class="source-card-chat">
<div class="source-card-header">Source</div>
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