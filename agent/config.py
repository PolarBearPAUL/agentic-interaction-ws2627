"""Load settings without hard-coding a provider or model."""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# agent/ is inside the repository, so its parent is the project root.
ROOT = Path(__file__).resolve().parent.parent 
# Path(__file__) -> Pfad der aktuellen Datei 
# resolve() -> absoluten Pfad, mit allen symbolischen Links auflösen
# parent.parent -> zwei Ebenen nach oben

# frozen dataclass: immutable, cannot be changed after creation.
# Konfiguration in strukturierten Form speichern
@dataclass(frozen=True)
class Config:
    base_url: str
    model: str
    api_key: str
    data_base_url: str

def load_config() -> Config:
    # Settings already present in the environment take precedence over .env file values.
    load_dotenv(ROOT / ".env", override=False) # not overrride existing variables
    names = ("OPENAI_BASE_URL", "MODEL", "OPENAI_API_KEY", "DATA_BASE_URL")
    missing = [name for name in names if not os.environ.get(name, "").strip()] 
    # strip whitespace, wenn Variablen in der env-Datei nicht gesetzt sind, dann hat missing eine Länge > 0 und es wird eine ValueError ausgelöst.
    # mit os kann man auf die Umgebungsvariablen zugreifen, die in der .env-Datei gesetzt sind. 
    # Wenn eine Variable fehlt oder leer ist, wird sie in der Liste "missing" gesammelt.
    # get(string, default)
    if missing:
        raise ValueError("Fehlende Konfiguration: " + ", ".join(missing))
    
    return Config(
        base_url=os.environ["OPENAI_BASE_URL"].strip(),
        model=os.environ["MODEL"].strip(),
        api_key=os.environ["OPENAI_API_KEY"].strip(),
        data_base_url=os.environ["DATA_BASE_URL"].strip().rstrip("/"), 
        # rstrip("/") entfernt abschließende "/", damit URL konsistent und keine doppelten Schrägstriche, wenn später in Pfaden verwenden
    )