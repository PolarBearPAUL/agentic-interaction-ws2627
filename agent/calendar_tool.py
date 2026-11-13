"""The tool description is for the model; the function performs the HTTP request."""

import json
from datetime import date
from urllib.error import HTTPError
from urllib.request import urlopen


TOOL = {
    "type": "function",
    "function": {
        "name": "get_calendar_day",
        "description": (
            "Read the mock calendar appointments for one day. "
            "Use this tool to answer questions about appointments. "
            "Convert the requested date to YYYY-MM-DD."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "The requested calendar date, formatted YYYY-MM-DD.",
                }
            },
            "required": ["date"],
            "additionalProperties": False,
        },
    },
}

def get_calendar_day(base_url: str, day: str) -> dict:
    """Get the mock calendar appointments for one day."""
    try:
        valid = date.fromisoformat(day).isoformat() == day
    except (ValueError, TypeError):
        valid = False
    if not valid:
        return {"ok": False, "date": day}
    
    url = f"{base_url}/calendar/{day}.json"
    
    try:
        with urlopen(url, timeout=15) as response: # Timeout von 15 Sekunden für die HTTP-Anfrage
            data = json.load(response)
    except HTTPError as e:
        if e.code == 404:
            return {"ok": True, "available": False, "date": day, "message": "Keine Termine für diesen Tag verfügbar."}  # 404 Not Found bedeutet, dass keine Termine für diesen Tag vorhanden sind
        else:
            return {"ok": False, "available": False, "date": day, "message": f"HTTP-Fehler: {e.code} {e.reason}"}
    
    except (OSError, ValueError) as e: # OSError: Netzwerkfehler, ValueError: JSON-Decode-Fehler
        return {"ok": False, "available": False, "date": day, "message": "Fehler beim Abrufen der Kalenderdaten."}
     
    if not isinstance(data, dict) or not isinstance(data.get("events"), list):
        return {"ok": False, "available": False, "date": day, "message": "Ungültige Datenstruktur."}
    
    return {"ok": True, "available": True, "date": day, "data": data, "message": "Daten erfolgreich abgerufen."}