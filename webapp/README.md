# Family dashboard web application

## Setup

    python3 -m venv .venv
    . .venv/bin/activate
    pip install -r requirements.txt
    sudo apt install wkhtmltopdf xvfb

## Development mode

    python main.py
    firefox http://127.0.0.1:8000/

## Run with uvicorn

    .venv/bin/uvicorn --host 0.0.0.0 --port 8000 main:app

Example usage with custom prefix and port on a public server:

    PATHPREFIX=/Rae2wiechuuth8ixie6tah7l .venv/bin/uvicorn --host 0.0.0.0 --port 8000 main:app
