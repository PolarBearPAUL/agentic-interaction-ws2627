"""The tool description is for the model; the function performs the HTTP request.
    "transit": "transit/{from}/{to}/{date}.json",
"""

import json
import re
from datetime import date
from urllib.error import HTTPError
from urllib.request import urlopen


TRAIN_TOOL = {
    "type": "function",
    "function": {
        "name": "get_train_info",
        "description": (
            "Read the mock train connections for one day between two cities. "
            "Use this tool for questions about trains, departures or arrival times. "
            "Only the routes ulm -> muenchen and muenchen -> ulm exist. "
            "Convert the requested date to YYYY-MM-DD. "
            "If the result says available=false, there is no data: do not guess."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "The requested calendar date, formatted YYYY-MM-DD.",
                },
                "from": {
                    "type": "string",
                    "description": "Departure city as lowercase ASCII slug without umlauts, e.g. 'ulm' or 'muenchen'.",
                },
                "to": {
                    "type": "string",
                    "description": "Arrival city as lowercase ASCII slug without umlauts, e.g. 'ulm' or 'muenchen'.",
                }
            },
            "required": ["date", "from", "to"],
            "additionalProperties": False,
        },
    },
}

def get_train_info(base_url: str, day: str, from_station: str, to_station: str) -> dict:
    """Get the mock transit data for one connection on one day.""" 
    try:
        valid = date.fromisoformat(day).isoformat() == day
    except (ValueError, TypeError):
        valid = False
    if not valid:
        return {"ok": False, "date": day, "message": "Ungültiges Datum."}
    
    from_station = from_station.strip().lower() if isinstance(from_station, str) else "" # check whether the variable fits the spelling that is expected
    if not re.fullmatch(r"[a-z]+", from_station): 
        return {"ok": False, "date": day, "from": from_station, "to": to_station, 
                "message": "Invalid departure city. Expected: lowercase letters without umlauts, e.g. B. 'ulm' or 'muenchen'."}
    
    to_station = to_station.strip().lower() if isinstance(to_station, str) else "" # same: check whether the variable fits the spelling that is expected
    if not re.fullmatch(r"[a-z]+", to_station):
        return {"ok": False, "date": day, "from": from_station, "to": to_station,
                "message": "Invalid departure city. Expected: lowercase letters without umlauts, e.g. B. 'ulm' or 'muenchen'."}
    
    url = f"{base_url}/transit/{from_station}/{to_station}/{day}.json"
    
    try:
        with urlopen(url, timeout=15) as response:
            data = json.load(response)
    except HTTPError as e:
        if e.code == 404:
            return {"ok": True, "available": False, "date": day, "from": from_station, "to": to_station,
                    "message": "Keine Zugverbindungen für diese Strecke und diesen Tag verfügbar."}
        return {"ok": False, "available": False, "date": day, "from": from_station, "to": to_station,
                "message": f"HTTP-Fehler: {e.code} {e.reason}"}
    except (OSError, ValueError):
        return {"ok": False, "available": False, "date": day, "from": from_station, "to": to_station,
                "message": "Fehler beim Abrufen der Zugverbindungen."}

    if not isinstance(data, dict):
        return {"ok": False, "available": False, "date": day, "from": from_station, "to": to_station,
                "message": "Ungültige Datenstruktur."}
        
    return {"ok": True, "available": True, "date": day, "from": from_station, "to": to_station, "data": data, "message": "Daten erfolgreich abgerufen."}