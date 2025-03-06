import os
from dotenv import load_dotenv

load_dotenv()

APPLICATION_WIDTH = 85
THEME = "DarkGray12"

OUTPUT_FILE_NAME = "record.wav"
SAMPLE_RATE = 48000

MODELS = ["qwen2.5-coder:3b", "qwen2.5-coder:latest", "deepseek-coder-v2:latest", "gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"]
DEFAULT_MODEL = MODELS[0]

DEFAULT_CHARACTER = "a Python Specialist"

WHISPER_API_URL = os.getenv('WHISPER_API_URL')
WHISPER_API_KEY = os.getenv('WHISPER_API_KEY')

SCREENSHOT_CAPTURE_HOTKEY = "p"

TESSERACT_EXE_PATH = os.getenv('TESSERACT_EXE_PATH', None) #For Windows users
