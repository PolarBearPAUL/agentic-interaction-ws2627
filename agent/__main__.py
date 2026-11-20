"""Start from the repository root: python -m agent \"Your calendar question\"."""

import json
import sys
from time import perf_counter
from datetime import date
from openai import OpenAI, OpenAIError

from .calendar_tool import CALENDAR_TOOL, get_calendar_day
from .weather_tool import get_weather, WEATHER_TOOL
from .train_tool import get_train_info, TRAIN_TOOL
from .config import ROOT, load_config
from .run_log import RunLog
from .prompts import build_system_prompt

MAX_STEPS = 8  # maximale Anzahl der Tool-Aufrufe, um Endlosschleifen zu vermeiden

def answer_question(client, config, task, log):
    messages = [
        {"role": "system", "content": build_system_prompt()},
        {"role": "user", "content": task},
    ]
    all_ok = True
    
    # äußere schleife, um mehrere Tool-Aufrufe zu ermöglichen, jede runde = ein Tool-Aufruf
    for step in range(MAX_STEPS): 
    
        response = client.chat.completions.create(
            model=config.model,
            messages=messages,
            tools=[CALENDAR_TOOL, WEATHER_TOOL, TRAIN_TOOL], 
            tool_choice="auto", # Tool oder antwort
        )
            
        # Modellantwort holen und an Messages hängen
        assistant_message = response.choices[0].message 
        messages.append(assistant_message.model_dump(exclude_none=True))
    
        # Keine Tool-Calls = das Modell ist fertig, das ist die Endantwort
        if not assistant_message.tool_calls:
            answer = assistant_message.content
            if not answer or not answer.strip():
                raise RuntimeError("Das Modell hat keine Antwort geliefert.") 
            return answer, all_ok
        
        # Innere Schleife: alle Tool-Calls DIESER Antwort abarbeiten
        for call in assistant_message.tool_calls:
            started = perf_counter()
            name = call.function.name
            # tool call
            try:
                arguments = json.loads(call.function.arguments)
            except json.JSONDecodeError:
                arguments = None
            if not isinstance(arguments, dict):
                arguments = None
    
            log.write("tool_call", tool=name, args=arguments)  
            
            args = arguments or {}
            if name == CALENDAR_TOOL["function"]["name"]:
                result = get_calendar_day(config.data_base_url, args.get("date"))
            elif name == TRAIN_TOOL["function"]["name"]:
                result = get_train_info(config.data_base_url, args.get("date"), args.get("from"),args.get("to"))
            elif name == WEATHER_TOOL["function"]["name"]:
                result = get_weather(config.data_base_url, args.get("date"), args.get("city"))
            else: result = {"ok": False, "message": f"Unbekanntes Tool: {name}"}    
                 
            elapsed = round((perf_counter() - started) * 1000, 3)
            log.write("tool_result", ok=result["ok"], tool=name, args=arguments, duration_ms=elapsed)    # NACH dem Ausführen

            all_ok = all_ok and result["ok"]
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": json.dumps(result, ensure_ascii=False), 
            })
        
    raise RuntimeError(f"Maximale Anzahl von {MAX_STEPS} Tool-Aufrufen erreicht. Mögliche Endlosschleife.") # wird abgefangen in main 


def main() -> int:
    started = perf_counter()
    log = RunLog(ROOT)
    
    if len(sys.argv) < 2:
        print('Usage: python -m agent "Your calendar question"', file=sys.stderr)
        log.write("error", ok=False,
                  duration_ms=round((perf_counter() - started) * 1000, 3))
        return 1
    
    task = " ".join(sys.argv[1:])  # Join all arguments into a single string
    
    try:
        config = load_config()
        log.model = config.model 
        log.write("user_task")
        
        # API Client erstellen, mit 'with' wird Client automatisch geschlossen, wenn Block verlassen wird
        with OpenAI(base_url=config.base_url, api_key=config.api_key,
                    timeout=30, max_retries=0) as client:
            answer, ok = answer_question(client, config, task, log)
        
    except (ValueError, RuntimeError, OpenAIError) as error:
        print(error, file=sys.stderr)
        log.write("error", ok=False, duration_ms=round((perf_counter() - started) * 1000, 3))
        return 1
    
    log.write("final", ok=ok, duration_ms=round((perf_counter() - started) * 1000, 3))
    print(answer)
    return 0 

if __name__ == "__main__":
    sys.exit(main())