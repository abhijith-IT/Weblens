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




rs within a restricted college domain.
