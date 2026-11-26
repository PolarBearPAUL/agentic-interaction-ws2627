# Agentic Human AI Interaction

Semester project for **Agentic Human-AI Interaction**, winter term 2026/27, Ulm University.

This project explores how an AI assistant can help people plan their day and travel while keeping its actions understandable and controllable. It is developed incrementally throughout the semester in the public repository `agentic-interaction-ws2627`.

## Description

The goal is a Python-based assistant that combines a simulated calendar, train timetable, weather service, and notes to support natural-language planning tasks.

An illustrative target scenario from the course is:

> Get me to my 14:00 meeting in Stuttgart on Thursday by train, and remind me to take an umbrella if it rains.

The assistant will use tools to gather information, combine results, identify constraints, and communicate a plan. All service data is fictional. The project does not require access to real personal accounts, real bookings, or personal calendar data. 

This scenario describes the semester goal, not a claim that all features are already available or that every destination exists in the current mock dataset.

## Development status

The project is under development.  The features below describe the planned scope and are not a list of completed functionality. The initial user interface is a command-line application. A graphical or chat-based user interface will be added later.

## Planned Features

- **Natural-language interaction:** Accept questions and planning requests expressed in everyday language.
- **Calendar queries:** Retrieve appointments for a selected day from the simulated calendar.
- **Travel planning:** Look up simulated train connections and relate them to appointment times.
- **Weather-aware planning:** Include relevant weather information in travel suggestions and reminders.
- **Notes and reminders:** Use simulated notes to provide additional information and support reminders, following the relevant exercise requirements.
- **Context-aware assistance:** Use provided context to identify when a suggestion or reminder may be relevant.
- **Transparent results:** Explain which information supports a recommendation and communicate missing data or failed steps.
- **Execution logging:** Record tasks, tool calls, results, and errors in structured logs.

Two interaction conditions are planned:

| Condition | Behavior |
| --- | --- |
| **Direct execution** | The assistant carries out its plan within the supported simulated environment and then presents the result. |
| **Plan preview with approval** | The assistant shows its plan first. The user can approve, change, or stop it before the planned actions are carried out. |

The two conditions will be compared in a small peer user study later in the semester. Their exact behavior and supported actions follow the course specifications.

## Technical approach

The application is being developed in **Python**. It coordinates the language model, tool execution, interaction flow, and logging. The language model interprets a request and can ask the application to call a tool. The Python application validates the requested tool and its arguments, fetches the relevant data, and returns the result to the model. The model then uses that information to formulate an answer or continue planning.

The default backend is Groq, and the endpoint, model, key, and data URL are configured through environment variables. 

No frontend framework has been selected. The command-line interface remains the initial entry point; aadditional interfaces will be documented as needed.

## Requirements

- Python **3.11 or newer**
- Git
- A credential for the configured model service
- Network access to the model endpoint and mock data service
- Python dependencies declared in `requirements.txt`

## Quickstart

If the repository is already cloned, open its existing root folder. Otherwise, clone your copy from GitHub and open that folder.

Check that your Python version is at least 3.11:

```bash
python3 --version
```

If `.venv` does not already exist:

```bash
python3 -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies from the repository root:

```bash
python -m pip install -r requirements.txt
```

Create a local `.env` file in the repository root:

```dotenv
OPENAI_BASE_URL=your_base_url (e.g. https://api.groq.com/openai/v1)
MODEL=your_model (e.g. openai/gpt-oss-20b)
OPENAI_API_KEY=your_api_key
DATA_BASE_URL=your_data_base_url (e.g. https://jhbelz.github.io/agentic-interaction-data/v1)
```

Then run the repository with
    
```bash
CONDITION=[direct/preview] python -m agent "Your task."
```

Run it from the repository root with the virtual environment active.

## Usage

The environment variable `CONDITION` is required. Without it (or with any value other
than `preview` or `direct`) the agent stops with an error message and exit code 1.
It can be set on the command line or in `.env`.

```bash
CONDITION=preview python -m agent "Block one hour of buffer for me on 29 Oct 2026 at 17:00."
CONDITION=direct  python -m agent "Block one hour of buffer for me on 29 Oct 2026 at 17:00."
```

Read-only questions work in both conditions, for example:

```bash
CONDITION=direct python -m agent "How do I get to Munich on 29 Oct 2026, and do I need an umbrella?"
```

The answer is printed to standard output. Plan, approval question and report go to
standard error. A successful run exits with code `0`.

## Interaction conditions

| Condition | Behavior |
| --- | --- |
| `preview` | Before every irreversible action the agent shows the plan on stderr and asks `Genehmigen? [j/N]`, one action at a time. Only a clear yes (`j`, `ja`, `y`, `yes`) executes it. |
| `direct` | The agent executes the action without asking and reports on stderr afterwards. |

- **Denial:** Any other answer, including no input, counts as "not approved". The model
  receives this as the tool result and keeps planning; nothing is written and the run
  ends normally.
- **`AUTO_APPROVE=1`** approves in `preview` without asking (the plan is still shown).
- **Irreversible tools** are defined in one place, `IRREVERSIBLE_TOOLS` in
  `agent/approval.py`. Read-only tools never trigger the approval step.
- **Same system prompt, tools and model:** The condition is not part of the system
  prompt, so the model never learns which condition it runs in. Only the approval step
  differs.
- **Log:** Every log line carries the field `condition`. In `preview` the events
  `approval_request` and then `approval_granted` or `approval_denied` are added.

## Approval dialog and the Amershi guidelines

The approval dialog violates "Make clear why the system did what it did", because it
shows what will be created but not why the agent chose this date, time or title.
It also violates "Support efficient correction", because the user can only answer yes
or no and cannot change the planned values, so fixing a wrong time means denying and
asking again.

## Mock data and tools

The course provides fictional service data through HTTP endpoints:

[Course mock data repository](https://github.com/jhbelz/agentic-interaction-data)

The initial dataset covers **26 October through 8 November 2026**. Tools should fetch data rather than copy the hosted dataset into this repository.

For example the initial calendar tool:

```text
GET {DATA_BASE_URL}/calendar/{YYYY-MM-DD}.json
```

An empty events list means that the calendar day has no appointments. HTTP `404` means no data is available and must be handled as a tool result rather than an unhandled crash. Missing data must not be presented as a confirmed free day.

## Repository structure

```text
agentic-interaction-ws2627/
├── README.md
├── requirements.txt
├── .gitignore
└── agent/
    ├── __main__.py       # agent loop, tool dispatch, entry point
    ├── approval.py       # irreversible tools and approval dialog
    ├── config.py         # settings from environment / .env
    ├── prompts.py        # system prompt (identical in both conditions)
    ├── run_log.py        # JSONL run log
    └── tools/
        ├── calendar_tool.py
        ├── weather_tool.py
        ├── train_tool.py
        └── appointment_tool.py
```

Local files and generated folders may include `.env`, `.venv/`, `logs/` and `var/`; they are not tracked.

## Licenses

This project was created for academic purposes. No license has been selected yet.
