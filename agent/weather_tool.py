"""The tool description is for the model; the function performs the HTTP request."""

import json
from datetime import date
from urllib.error import HTTPError
from urllib.request import urlopen


WEATHER_TOOL = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": (
            "Read the mock weather data for one day. "
            "Use this tool to answer questions about weather. "
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

def get_weather(base_url: str, day: str) -> dict:
    
    return {"ok": True, "available": True, "date": day, "data": data, "message": "Daten erfolgreich abgerufen."}