
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

DEFAULT_ROLES = ["software engineer", "sales representative", "retail associate", "data scientist", "product manager"]
MAX_FOLLOW_UPS = 3
INTERVIEW_DURATION_MINUTES = 15

VOICE_ENABLED = True
VOICE_LANGUAGE = "en-US"
VOICE_RATE = 150

MAX_OFF_TOPIC_REDIRECTS = 2
CONFIDENCE_THRESHOLD = 0.7

