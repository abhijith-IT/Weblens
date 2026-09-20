# WebLens — Domain-Scoped AI Web Agent for GECBH

WebLens is a domain-scoped AI web agent designed to answer college-related questions using trusted and predefined web sources.

The system uses Gemini native function calling to select the most relevant registered source, fetches live content from that source, and generates a grounded answer based only on the retrieved information.

---

## Features

- Natural-language question answering
- Domain-scoped to GECBH
- Gemini native function/tool calling
- Dynamic source selection
- Live web content fetching
- Multiple trusted sources
- Grounded answers
- Anti-hallucination fallback
- Source URL attribution
- Tool invocation display
- Streamlit chat interface
- Error handling for API and network failures
- Automated tests

---

## Trusted Sources

WebLens currently uses the following registered sources.

### 1. GECBH Official Website

URL:

https://www.gecbh.ac.in/

Description:

Official Government Engineering College Barton Hill website containing college information, departments, faculty, notices, and general institutional information.

---

### 2. GECBH CSI

URL:

https://www.gecbh.ac.in/csi.php

Description:

Official GECBH CSI page containing information about the CSI Student Branch, staff advisor, executive committee, activities, workshops, competitions, project guidance, and related CSI information.

---

### 3. CSI Student Branch GECBH

URL:

https://csigecbh.in/

Description:

CSI Student Branch GECBH website containing information about student-branch activities, events, announcements, achievements, and related student activities.

---

## Architecture

```text
                    User Query
                        |
                        v
                +---------------+
                |   Streamlit   |
                |      UI       |
                +---------------+
                        |
                        v
                +---------------+
                | Gemini Agent  |
                +---------------+
                        |
                        v
             Gemini Function Calling
                        |
          +-------------+-------------+
          |             |             |
          v             v             v
     GECBH Official  GECBH CSI   CSI Student
       Website                    Branch
          |             |             |
          +-------------+-------------+
                        |
                        v
                  Web Fetcher
                        |
                        v
                Readable Web Text
                        |
                        v
                 Gemini Grounding
                        |
                        v
                  Final Answer
                        |
              +---------+---------+
              |                   |
              v                   v
         Tool Invoked          Source URL
        
Project Structure

WebLens/
│
├── app.py
├── config.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── README.md
│
├── web/
│   ├── __init__.py
│   ├── registry.py
│   └── fetcher.py
│
├── llm/
│   ├── __init__.py
│   ├── agent.py
│   ├── tools.py
│   └── prompts.py
│
└── tests/
    ├── test_agent.py
    ├── test_fetcher.py
    └── test_registry.py

Technology Stack
Python
Streamlit
Google Gemini API
Google GenAI SDK
Requests
Trafilatura
BeautifulSoup4
python-dotenv
Pytest
How It Works
1. User enters a question

Example:

Who is the staff advisor listed on the GECBH CSI page?
2. Gemini selects a registered tool

Gemini analyzes the available tool descriptions and selects the relevant source.

For the example above, the GECBH CSI source is selected.

3. WebLens fetches the source

The web fetcher retrieves the current page content.

4. Content is provided to Gemini

The fetched website content is supplied to Gemini as the function response.

5. Gemini generates the answer

The final response is generated using the retrieved content.

WebLens is instructed not to invent information when the retrieved content does not contain the requested information.

6. Source information is displayed

The UI displays:

Tool invoked
Source URL

along with the answer.

Installation

Clone the repository:

git clone <YOUR_GITHUB_REPOSITORY_URL>
cd WebLens

Create a virtual environment:

python -m venv .venv

Activate it on Windows:

.venv\Scripts\Activate.ps1

Install dependencies:

python -m pip install -r requirements.txt
Environment Configuration

Create a .env file:

GEMINI_API_KEY=your_gemini_api_key_here

Do not commit the .env file.

It is already included in .gitignore.

Run WebLens

Start the Streamlit application:

streamlit run app.py

The application will open in the browser.

Running Tests

Run the complete test suite:

python -m pytest tests -v

Current test status:

8 passed

The tests cover:

API key validation
Gemini response handling
Empty response handling
Web fetching
Source registry validation
HTTPS URL validation
Example Queries
College information
What is the vision of GECBH?
CSI information
What activities are associated with CSI at GECBH?
Staff advisor
Who is the staff advisor listed on the GECBH CSI page?
Unknown information
What is my current GPA?

For information that cannot be found in the registered sources, WebLens should clearly indicate that the information could not be found rather than inventing an answer.

Error Handling

WebLens handles:

Missing Gemini API key
Gemini API quota exhaustion
Gemini service unavailability
API authentication errors
Website connection failures
Website timeouts
Empty web responses
Unreadable web pages
Empty Gemini responses
Testing

WebLens uses pytest for automated testing.

The test suite currently contains 8 tests covering the registry, web fetcher, and agent behavior.

All tests pass successfully.

Limitations
WebLens only uses sources registered in the source registry.
The quality of answers depends on the content available on those sources.
Some websites may block automated requests.
Gemini API availability and quota can affect live question answering.
JavaScript-heavy websites may require additional browser-based fetching support.
Future Improvements

Possible future enhancements include:

Multi-source synthesis
Session caching
Playwright support for JavaScript-heavy websites
Confidence indicators
Detailed tool invocation logs
Additional trusted college sources
Improved source-content extraction
Deployment as a hosted web application
Project Goal

WebLens demonstrates how a domain-scoped AI agent can combine:

Natural Language
       +
LLM Reasoning
       +
Function Calling
       +
Trusted Web Sources
       +
Live Retrieval
       +
Grounded Generation

to provide useful and traceable answers within a restricted college domain.