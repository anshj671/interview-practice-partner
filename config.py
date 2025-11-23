"""
Configuration settings for the Interview Practice Partner
"""
import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Interview Settings
DEFAULT_ROLES = ["software engineer", "sales representative", "retail associate", "data scientist", "product manager"]
MAX_FOLLOW_UPS = 3
INTERVIEW_DURATION_MINUTES = 15

# Voice Settings
VOICE_ENABLED = True
VOICE_LANGUAGE = "en-US"
VOICE_RATE = 150  # Words per minute

# Conversation Settings
MAX_OFF_TOPIC_REDIRECTS = 2
CONFIDENCE_THRESHOLD = 0.7

