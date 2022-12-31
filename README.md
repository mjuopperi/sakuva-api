# SA-Kuva API

APIs for http://sa-kuva.fi/ modernisation project.

## Setup:

1. Install python 3.11+, poetry, docker and docker-compose
2. Copy `app/.env.template` to `app/.env` and make any changes you may need
3. Install dependencies with `poetry install`
4. Start services with `docker-compose up -d`
5. Run `app/main.py` or run `uvicorn app.main:app --reload` in terminal
