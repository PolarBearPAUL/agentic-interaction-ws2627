"""Approval step for irreversible tools. 
    like a bouncer who asks if the function/tool ​​that the model is supposed to execute is dangerous 
    and whether the preview or direct option is running."""

import sys
from .tools.appointment_tool import APPOINTMENT_TOOL

# The one place that defines which tools are irreversible. 
IRREVERSIBLE_TOOLS = {"create_appointment"}


def _plan_lines(tool_name: str, args: dict) -> list[str]:
    """Turn a tool call into readable lines for the user."""
    if tool_name == APPOINTMENT_TOOL["function"]["name"]:
        if args.get("all_day") is True:
            when = "ganztägig"
        else:
            when = f"{args.get('start')} - {args.get('end')}"
        lines = [
            "Aktion: Termin anlegen (kann nicht rückgängig gemacht werden)",
            f"Datum:  {args.get('date')}",
            f"Zeit:   {when}",
            f"Titel:  {args.get('title')}",
        ]
        if args.get("location"):
            lines.append(f"Ort:    {args['location']}")
        return lines

    # fallback for tools added later: show the tool name and all arguments
    return [f"Aktion: {tool_name}"] + [f"{key}: {value}" for key, value in args.items()]


# just asks user for approval, No check to see if the tool is dangerous…
def ask_approval(tool_name: str, args: dict, auto_approve: bool) -> bool:
    """Show the plan on stderr and ask the user. True = approved, False = not approved."""
    print("\nPlan:", file=sys.stderr) # Standardfehlerausgabe, stdout (Standardausgabe)
    for line in _plan_lines(tool_name, args):
        print(f"  {line}", file=sys.stderr)

    if auto_approve:
        print("Automatisch genehmigt (AUTO_APPROVE=1).", file=sys.stderr)
        return True

    # print() to stderr instead of input(), because input() writes its prompt to stdout
    print("Genehmigen? [j/N] ", end="", file=sys.stderr, flush=True)
    answer = sys.stdin.readline()   # returns "" if there is no input, no crash

    if not answer:
        print(file=sys.stderr)      # line break, so the next output starts on a new line

    # only a clear yes counts, everything else (including empty) is a no
    return answer.strip().lower() in {"j", "ja", "y", "yes"}