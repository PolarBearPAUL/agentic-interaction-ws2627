"""The tool description is for the model; the function performs the HTTP request.
  "weather": "weather/{city}/{date}.json", 
"""

import json
import re
from datetime import date
from urllib.error import HTTPError
from urllib.request import urlopen

WEATHER_TOOL = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": (
            "Read the mock weather data for one city on one day. "
            "Use this tool for questions about weather, rain or umbrellas. "
            "Convert the requested date to YYYY-MM-DD. "
            "The city name should be a string without special characters. "
            "If the result says available=false, there is no forecast: do not guess. "
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "The requested calendar date, formatted YYYY-MM-DD.",
                },
                "city": {
                    "type": "string",
                    "description": "City as lowercase ASCII slug without umlauts, e.g. 'ulm' or 'muenchen'.",
                }
            },
            "required": ["date", "city"],
            "additionalProperties": False,
        },
    },
}

def get_weather(base_url: str, day: str, city: str) -> dict:
    """Get the mock weather data for one day in a specific city.""" 
    try:
        valid = date.fromisoformat(day).isoformat() == day
    except (ValueError, TypeError):
        valid = False
    if not valid:
        return {"ok": False, "date": day, "message": "Ungültiges Datum."}
    
    city = city.strip().lower() if isinstance(city, str) else ""
    if not re.fullmatch(r"[a-z]+", city):
        return {"ok": False, "date": day, "city": city, "message": "Ungültiger Stadtname."}

    url = f"{base_url}/weather/{city}/{day}.json" # build url then call
    
    try:
        with urlopen(url, timeout=15) as response:
            data = json.load(response)
    except HTTPError as e:
        if e.code == 404:
            return {"ok": True, "available": False, "date": day, "city": city, "message": "Keine Wetterdaten für diesen Tag verfügbar."}
        else:
            return {"ok": False, "available": False, "date": day, "message": f"HTTP-Fehler: {e.code} {e.reason}"}
    except (OSError, ValueError) as e: # OSError: Netzwerkfehler, ValueError: JSON-Decode-Fehler
        return {"ok": False, "available": False, "date": day, "message": "Fehler beim Abrufen der Wetterdaten."}
        
    if not isinstance(data, dict):
        return {"ok": False, "available": False, "date": day, "city": city, "message": "Ungültige Datenstruktur."}

    return {"ok": True, "available": True, "date": day, "city": city, "data": data, "message": "Daten erfolgreich abgerufen."}