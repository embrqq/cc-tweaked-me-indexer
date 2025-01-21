FROM python:3.12-alpine AS installer

WORKDIR /api

RUN python -m venv /venv

# Make sure we use the virtualenv:
# build a virtualenv with all requirements
ENV PATH="/venv/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1

COPY ./requirements.txt ./

RUN python -m pip install -r requirements.txt

COPY ./main.py ./
COPY ./db_setup.py ./
COPY ./src ./src
