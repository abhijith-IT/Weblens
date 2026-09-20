import streamlit as st

from llm.agent import run_agent


st.set_page_config(
    page_title="WebLens",
    page_icon="🌐",
    layout="wide",
)


# ---------------------------------------------------------
# Page styling
# ---------------------------------------------------------

st.markdown(
    """
    <style>
        .main {
            max-width: 1000px;
            margin: auto;
        }

        .weblens-title {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }

        .weblens-subtitle {
            color: #888;
            font-size: 1.05rem;
            margin-bottom: 1.5rem;
        }

        .source-card {
            padding: 12px 16px;
            border-radius: 10px;
            border: 1px solid #444;
            margin-top: 8px;
        }

        .metadata {
            color: #aaa;
            font-size: 0.9rem;
        }

        .example-box {
            padding: 12px;
            border-radius: 10px;
            border: 1px solid #444;
            margin-bottom: 8px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.markdown(
    '<div class="weblens-title">🌐 WebLens</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="weblens-subtitle">'
    "A domain-scoped AI web agent for GECBH"
    "</div>",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:

    st.header("About WebLens")

    st.write(
        "WebLens answers college-related questions using "
        "trusted registered web sources."
    )

    st.divider()

    st.subheader("Trusted Sources")

    st.markdown(
    "🏫 [GECBH Official Website](https://www.gecbh.ac.in/)"
    )

    st.markdown(
    "💻 [GECBH CSI](https://www.gecbh.ac.in/csi.php)"
    )

    st.markdown(
    "🌐 [CSI Student Branch GECBH](https://csigecbh.in/)"
    )

    st.divider()

    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ---------------------------------------------------------
# Session state
# ---------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------------------------------------------------
# Example questions
# ---------------------------------------------------------

if not st.session_state.messages:

    st.markdown("### Try asking")

    examples = [
        "What is the vision of GECBH?",
        "What activities are associated with CSI at GECBH?",
        "Who is the staff advisor listed on the GECBH CSI page?",
        "What is the CSI Student Branch at GECBH?",
    ]

    for i, example in enumerate(examples):

        if st.button(
            f"💬 {example}",
            key=f"example_{i}",
            use_container_width=True,
        ):
            st.session_state.pending_query = example
            st.rerun()


# ---------------------------------------------------------
# Display previous messages
# ---------------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant":

            if message.get("tool_name"):
                st.markdown(
                    f"**🔧 Tool(s) invoked:** "
                    f"{message['tool_name']}"
                )

            if message.get("source_url"):
                st.markdown("**🔗 Source(s):**")

                urls = message["source_url"].split(", ")

                for url in urls:
                    st.markdown(
                        f"- [{url}]({url})"
                    )


# ---------------------------------------------------------
# Chat input
# ---------------------------------------------------------

query = st.chat_input(
    "Ask something about GECBH..."
)

# Check whether an example question was selected.
if "pending_query" in st.session_state:

    query = st.session_state.pending_query
    del st.session_state.pending_query


if query:

    # -----------------------------------------------------
    # User message
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query,
        }
    )

    with st.chat_message("user"):
        st.markdown(query)

    # -----------------------------------------------------
    # Agent response
    # -----------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "WebLens is selecting trusted sources..."
        ):

            try:

                result = run_agent(query)

                answer = result.get(
                    "answer",
                    "No answer was returned.",
                )

                tool_name = result.get("tool_name")
                source_url = result.get("source_url")

                st.markdown(answer)

                if tool_name:
                    st.markdown(
                        f"**🔧 Tool(s) invoked:** {tool_name}"
                    )

                if source_url:

                    st.markdown("**🔗 Source(s):**")

                    urls = source_url.split(", ")

                    for url in urls:
                        st.markdown(
                            f"- [{url}]({url})"
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

                if (
                    "429" in error_text
                    or "resource_exhausted" in error_text
                    or "quota" in error_text
                ):

                    message = (
                        "⚠️ **Gemini API quota reached.**\n\n"
                        "The WebLens agent has temporarily reached "
                        "the available Gemini API request limit."
                    )

                elif (
                    "503" in error_text
                    or "unavailable" in error_text
                    or "high demand" in error_text
                ):

                    message = (
                        "⚠️ **Gemini is temporarily unavailable.**\n\n"
                        "Please try again later."
                    )

                elif (
                    "401" in error_text
                    or "403" in error_text
                    or "api key" in error_text
                    or "permission" in error_text
                ):

                    message = (
                        "⚠️ **Gemini API authentication error.**\n\n"
                        "Please check the GEMINI_API_KEY configuration."
                    )

                elif (
                    "timeout" in error_text
                    or "connection" in error_text
                    or "failed to fetch" in error_text
                ):

                    message = (
                        "⚠️ **Unable to access the web source.**\n\n"
                        "The trusted website could not be reached."
                    )

                else:

                    message = (
                        "⚠️ **WebLens encountered an error.**\n\n"
                        "The request could not be completed."
                    )

                st.error(message)

                with st.expander("Technical details"):
                    st.code(str(exc))

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": message,
                    }
                )