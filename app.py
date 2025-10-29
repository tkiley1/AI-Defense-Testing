import os
from flask import Flask, render_template, request, session, redirect, url_for
from typing import Tuple
from dotenv import load_dotenv
from validation import *

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

# Load environment variables from .env if present
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-change-me")


def get_openai_client() -> "OpenAI":
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Define it in your environment or .env file.")
    if OpenAI is None:
        raise RuntimeError(
            "The 'openai' package is not installed. Please install dependencies from requirements.txt.")
    return OpenAI(api_key=api_key)


def get_history() -> list:
    history = session.get("history")
    if history is None:
        history = []
        session["history"] = history
    return history


def append_history(role: str, content: str) -> None:
    history = get_history()
    history.append({"role": role, "content": content})
    session["history"] = history


def validate_user_input(user_text: str) -> Tuple[bool, str]:
    if user_text is None:
        return False, "No input provided."
    text = user_text.strip()
    if not text:
        return False, "Please enter a message."
    if len(text) > 2000:
        return False, "Your message is too long (limit is 2000 characters)."
    is_safe, classifications = valiation(user_text)
    if not is_safe:
        return False, classifications
    return True, "OK"


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", response_text=None, error_text=None, user_text="", history=get_history())


@app.route("/clear", methods=["POST"])
def clear_history():
    session["history"] = []
    return redirect(url_for("index"))


@app.route("/chat", methods=["POST"])
def chat():
    user_text = request.form.get("prompt", "")
    is_valid, validation_message = validate_user_input(user_text)
    if not is_valid:
        return render_template(
            "index.html",
            response_text=None,
            error_text=validation_message,
            user_text=user_text,
            history=get_history(),
        )

    try:
        append_history("user", user_text)

        messages = [
            {"role": "system", "content": "You are a helpful assistant."}]
        messages.extend(get_history())

        client = get_openai_client()
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
        )
        assistant_text = completion.choices[
            0].message.content if completion.choices else "(No response)"

        append_history("assistant", assistant_text)

        return render_template("index.html", response_text=None, error_text=None, user_text="", history=get_history())
    except Exception as e:
        return render_template("index.html", response_text=None, error_text=str(e), user_text=user_text, history=get_history())


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
