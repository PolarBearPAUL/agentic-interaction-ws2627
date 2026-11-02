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
python -m agent "Your task"
```

Run it from the repository root with the virtual environment active.

## Usage

Initial calendar example, once implemented:

```bash
python -m agent "Was steht am 29.10.2026 im Kalender?"
```

A successful calendar run prints the answer to standard output and exits with code `0`. Diagnostics should use standard error. Additional commands and any interaction-mode selection will be documented when implemented; no unimplemented command-line flags are specified here.

## Mock data and tools

The course provides fictional service data through HTTP endpoints:

[Course mock data repository](https://github.com/jhbelz/agentic-interaction-data)

The initial dataset covers **26 October through 8 November 2026**. Tools should fetch data rather than copy the hosted dataset into this repository.

For the initial calendar tool:

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
    └── __main__.py
```

Local files and generated folders may include `.env`, `.venv/`, and `logs/`; they are not tracked.

Each invocation must create its own JSONL log file inside the repository directory `logs/`. JSONL stores one complete JSON object per line. All records belonging to one run share a run identifier.

Logs provide a trace of the application's execution. They are stored locally and are **not tracked by Git** under the initial exercise requirements.

## Licenses

This project was created for academic purposes. No license has been selected yet.