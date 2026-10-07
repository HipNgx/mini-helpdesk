import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")

@dataclass(frozen=True)
class Settings:
    ollama_host: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "gemma4:31b")
    ollama_quiz_model: str = os.getenv("OLLAMA_QUIZ_MODEL", os.getenv("OLLAMA_MODEL", "gemma4:31b"))
    ollama_api_key: str = os.getenv("OLLAMA_API_KEY", "")

settings = Settings()
