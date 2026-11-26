"""The tool wirtes to var/calendar.jsonl and Mock data remains unchanged
"""

import json
import re
from datetime import date
from pathlib import Path
from uuid import uuid4

# exactly HH:MM, 24 hours, leading zeros (00:00 - 23:59)
TIME_PATTERN = re.compile(r"([01]\d|2[0-3]):[0-5]\d")

APPOINTMENT_TOOL = {
    "type": "function",
    "function": {
        "name": "create_appointment",
        "description": (
            "Create a new appointment in the user's calendar. "
            "This action cannot be undone. "
            "Use it only when the user explicitly asks to create, add or block an appointment. "
            "Convert the date to YYYY-MM-DD and the times to HH:MM (24-hour clock). "
            "The new appointment is stored separately and does not appear in "
            "get_calendar_day results, so do not look for it there."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "description": "Optional unique ID of the appointment. Leave it out; the system generates one.",
                },
                "date": {
                    "type": "string",
                    "description": "The calendar date of the appointment, formatted YYYY-MM-DD.",
                },
                "start": {
                    "type": "string",
                    "description": "Start time, formatted HH:MM (24-hour). Must be before the end. For all-day appointments use '00:00'; it is ignored.",
                },                  
                "end": {
                    "type": "string",
                    "description": "End time, formatted HH:MM (24-hour). Must be after the start. For all-day appointments use '23:59'; it is ignored.",
                },
                "all_day": {
                    "type": "boolean",
                    "description": "True only for an all-day appointment. Defaults to false.",
                },
                "title": {
                    "type": "string",
                    "description": "Short title of the appointment. Must not be empty.",
                },
                "location": {
                    "type": "string",
                    "description": "Optional location of the appointment.",
                },
            },
            "required": ["date", "start", "end", "title"],
            "additionalProperties": False,
        },
    },
}

def create_appointment(root: Path, day: str, start: str, end: str, title: str,
                       appointment_id=None, all_day=None, location=None) -> dict:
    """Append one appointment as a JSON line to var/calendar.jsonl."""
    # 1. date
    try:
        valid = date.fromisoformat(day).isoformat() == day
    except (ValueError, TypeError):
        valid = False
    if not valid:
        return {"ok": False, "date": day, "message": "Ungültiges Datum. Erwartet: YYYY-MM-DD."}

    # 4. title must be a non-empty string
    if not isinstance(title, str) or not title.strip():
        return {"ok": False, "date": day, "message": "Der Titel darf nicht leer sein."}

    # all_day: optional boolean, default False
    if all_day is None:
        all_day = False
    if not isinstance(all_day, bool):
        return {"ok": False, "date": day, "message": "all_day muss true oder false sein."}

    if all_day:
        start, end = None, None
    else:
        for value in (start, end):
            if not isinstance(value, str) or not TIME_PATTERN.fullmatch(value):
                return {"ok": False, "date": day,
                        "message": "Ungültige Uhrzeit. Erwartet: HH:MM (24 Stunden), z. B. '17:00'."}
        if end <= start:
            return {"ok": False, "date": day, "message": "Das Ende muss nach dem Beginn liegen."}
        
    # id: use the given one, otherwise generate one
    if isinstance(appointment_id, str) and appointment_id.strip():
        appointment_id = appointment_id.strip()
    else:
        appointment_id = f"user-{uuid4().hex[:8]}"

    # location: optional
    location = location.strip() if isinstance(location, str) and location.strip() else None

    # 5. build the appointment 
    appointment = {
        "id": appointment_id,
        "date": day,
        "start": start,
        "end": end,
        "all_day": all_day,
        "title": title.strip(),
        "location": location,
    }
    
    # 6. append exactly one line 
    try:
        folder = root / "var"
        folder.mkdir(exist_ok=True) 
        with (folder / "calendar.jsonl").open("a", encoding="utf-8") as file:
            file.write(json.dumps(appointment, ensure_ascii=False) + "\n")
    except OSError:
        return {"ok": False, "date": day, "message": "Der Termin konnte nicht gespeichert werden."}

    return {"ok": True, "created": True, "appointment": appointment,
            "message": "Termin wurde angelegt."}