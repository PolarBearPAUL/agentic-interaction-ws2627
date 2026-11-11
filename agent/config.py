"""Load settings without hard-coding a provider or model."""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# agent/ is inside the repository, so its parent is the project root.
ROOT = Path(__file__).resolve().parent.parent 

@dataclass(frozen=True) # frozen=True dataclass immutable, fields cannot be changed after initialization
class Config:
    base_url: str
    model: str
    api_key: str
    data_base_url: str

def load_config() -> Config:
    """Load settings from .env file and environment variables."""
    load_dotenv(ROOT / ".env", override=False) # Load environment variables from .env file in the project root
   
    names = ["OPENAI_BASE_URL", "MODEL", "OPENAI_API_KEY", "DATA_BASE_URL"]
    missing = [n for n in names if not os.environ.get(n, "").strip()] # Check for missing environment variables
    if missing:
        raise ValueError(f"Missing configuration variables: {', '.join(missing)}")
    
    return Config(
        base_url=os.environ["OPENAI_BASE_URL"].strip(),
        model=os.environ["MODEL"].strip(),
        api_key=os.environ["OPENAI_API_KEY"].strip(),
        data_base_url=os.environ["DATA_BASE_URL"].strip().rstrip("/"),  # Remove trailing slash if present
    )