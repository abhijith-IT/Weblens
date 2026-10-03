# WebLens — Domain-Scoped AI Web Agent for GECBH

WebLens is a Streamlit-based AI assistant for Government Engineering College Barton Hill (GECBH).  
It answers questions using only trusted, registered college sources with Gemini function calling and grounded response generation.

---

## Recent Updates

- Added modular LLM layer (`llm/agent.py`, `llm/tools.py`, `llm/prompts.py`)
- Expanded trusted source registry (`web/registry.py`)
- Added local web indexing support (`web/indexer.py`)
- Added local relevance search over indexed pages (`web/site_search.py`)
- Updated Gemini model configuration in `config.py`

---

## Features

- Domain-scoped question answering for GECBH
- Gemini native function/tool calling for source selection
- Live trusted-source web fetching (`web/fetcher.py`)
- Grounded final-answer generation from fetched content only
- Source attribution (tool and URL)
- Streamlit chat UI with source cards
- Local index builder for GECBH pages
- Local page relevance ranking utilities
- Automated test coverage for key modules

---

## Trusted Sources

WebLens currently registers the following trusted sources:

1. **GECBH Official Website**  
   https://www.gecbh.ac.in/
2. **GECBH Departments**  
   https://www.gecbh.ac.in/departments.php
3. **GECBH Campus Facilities**  
   https://www.gecbh.ac.in/campus-facilities.php
4. **GECBH Placement & Career**  
   https://www.gecbh.ac.in/placement.php
5. **GECBH CSI**  
   https://www.gecbh.ac.in/csi.php
6. **CSI Student Branch GECBH**  
   https://csigecbh.in/

---

## Project Structure

```text
Weblens/
├── app.py
├── config.py
├── llm/
│   ├── agent.py
│   ├── prompts.py
│   └── tools.py
├── web/
│   ├── fetcher.py
│   ├── registry.py
│   ├── indexer.py
│   └── site_search.py
├── data/
│   └── gecbh_index.json
└── tests/
```

---

## Runtime Flow

```text
User Query
   ↓
Streamlit UI (app.py)
   ↓
Gemini source selection (function calling)
   ↓
Trusted source fetch (web/fetcher.py)
   ↓
Grounded final-answer generation (llm/agent.py)
   ↓
Answer + source metadata
```

---

## Setup

Create and activate a virtual environment, then install the application and
test dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Configure environment variables:

```bash
cp .env.example .env
```

Set `GEMINI_API_KEY` in `.env`.

---

## Run the App

```bash
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Push this repository to GitHub.
2. Open [share.streamlit.io](https://share.streamlit.io/) and sign in with GitHub.
3. Select the `abhijith-IT/Weblens` repository, branch `main`, and file `app.py`.
4. In **Advanced settings**, add this secret:

```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
```

5. Deploy the app. Never commit `.env` or the API key to GitHub.

---

## Build Local Index (Optional)

```bash
python -m web.indexer
```

This generates `data/gecbh_index.json`.

---

## Run Tests

```bash
python3 -m pytest -v
```
