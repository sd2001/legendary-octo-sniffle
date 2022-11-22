FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/backend

COPY . .

EXPOSE 8000

RUN pip install poetry

RUN poetry install

CMD [ "bash", "run.sh" ]