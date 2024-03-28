FROM python:3.11.1

ENV ENV DEV
ENV DATABASE_URL postgresql+psycopg2://postgres:1234@database:5432/test

WORKDIR /src

COPY /src /src

COPY /tests /tests
# dev purpose

COPY requirements.txt /src

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]