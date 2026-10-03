import os

from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
	try:
		import streamlit as st

		GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY")
	except (ImportError, FileNotFoundError, KeyError, TypeError):
		GEMINI_API_KEY = None

GEMINI_MODEL = "gemini-3.1-flash-lite"