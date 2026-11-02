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
    # model's arguments not automatically trusted
    # ob Datum im richtigen Format, ob es String ist und in ISO-Format YYYY-MM-DD konvertieren kann
    if not isinstance(day, str) or date.fromisoformat(day).isoformat() != day:
        raise ValueError("Das Datum muss YYYY-MM-DD entsprechen.")
    
    url = f"{base_url.rstrip('/')}/calendar/{day}.json"
    
    try:
        # A timeout prevents waiting forever. No model API key is sent here.
        with urlopen(url, timeout=15) as response:
            data = json.load(response)
    
    except HTTPError as error:
        error.close() # HTTPError ist Kontextmanager, der Verbindung offen hält, bis er geschlossen wird.
        if error.code == 404:
            return {"ok": True, "available": False, "date": day,
                    "message": "Keine Daten für dieses Datum verfügbar (HTTP 404)."}
        return {"ok": False, "date": day,
                "message": f"Kalenderdienst meldet HTTP {error.code}."} 
    
    except (OSError, ValueError):
        return { "ok": False, "date": day, "message": "Kalenderdaten konnten nicht geladen oder verarbeitet werden."}

    if not isinstance(data, dict) or not isinstance(data.get("events"), list):
        return {"ok": False, "date": day,
                "message": "Unerwartetes Kalenderformat: events muss eine Liste sein."}

    return {"ok": True, "available": True, "date": day, "data": data}