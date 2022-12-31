FROM python:3.11

ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_NO_INTERACTION=1
ENV PYSETUP_PATH=/opt/pysetup
ENV VENV_PATH=/opt/pysetup/.venv

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

RUN python3 -m venv $POETRY_HOME
RUN $POETRY_HOME/bin/pip install poetry

WORKDIR $PYSETUP_PATH
COPY pyproject.toml poetry.lock ./
RUN $POETRY_HOME/bin/poetry install --only main --no-root

COPY ./app /code/app
COPY docker-entrypoint.sh /docker-entrypoint.sh

WORKDIR /code
ENTRYPOINT /docker-entrypoint.sh $0 $@
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
