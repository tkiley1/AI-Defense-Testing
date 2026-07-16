# Simple ChatGPT Flask App

A minimal Flask app that validates user input with Cisco AI Defense and chats with OpenAI. Conversations persist per browser session. Styled with a modern, responsive UI.  OpenAI API Key and Cisco AI Defense subscription required.

## Setup

1. Create an environment file:
   - Copy `ENV.EXAMPLE` to `.env` and fill in values.
   - Required variables:
     - `OPENAI_API_KEY` – your OpenAI API key
     - `CISCO_AI_DEFENSE_API_KEY` – your Cisco AI Defense key
     - `FLASK_SECRET_KEY` – any random string for Flask sessions

2. Install dependencies:

```bash
pip3 install -r requirements.txt
```

## Run locally

```bash
python3 app.py
```

Open `http://localhost:8080/`.

## Docker

Build the image:

```bash
docker build -t simple-chatgpt-flask .
```

Run with your environment file (recommended):

```bash
docker run --rm -p 8080:8080 --env-file .env simple-chatgpt-flask
```

Or pass variables explicitly:

```bash
docker run --rm -p 8080:8080 \
  -e OPENAI_API_KEY=... \
  -e CISCO_AI_DEFENSE_API_KEY=... \
  -e FLASK_SECRET_KEY=... \
  simple-chatgpt-flask
```

## Astroscale

The repository follows Astroscale's default deployment contract:

- The root `Dockerfile` builds the application.
- The container defaults to port `8080` and serves a 2xx response at `/`.
- Set `OPENAI_API_KEY`, `CISCO_AI_DEFENSE_API_KEY`, and `FLASK_SECRET_KEY` in the
  Astroscale runtime environment editor before using chat.

## Notes

- Secrets are no longer read from text files; use `.env` or env vars.
- The chat history is stored in the Flask session cookie and persists per browser session. Use the Clear conversation button to reset.
- To change the model or UI theme, edit `app.py` (model name) and `templates/index.html` (CSS variables).


