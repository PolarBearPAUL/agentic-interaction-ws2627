"""The tool description is for the model; the function performs the HTTP request."""

import json
from datetime import date
from urllib.error import HTTPError
from urllib.request import urlopen


TRAIN_TOOL = {
    "type": "function",
    "function": {
        "name": "get_train_info",
        "description": (
            "Read the mock train information for one day. "
            "Use this tool to answer questions about train schedules. "
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

def get_train_info(base_url: str, day: str) -> dict:
    
    return {"ok": True, "available": True, "date": day, "data": data, "message": "Daten erfolgreich abgerufen."}