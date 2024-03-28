FROM python:3.11.1

ENV ENV DEV
ENV DATABASE_URL postgresql+psycopg2://postgres:1234@database:5432/test

WORKDIR /app

COPY /src /app

COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]