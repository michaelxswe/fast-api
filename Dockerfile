FROM python:3.11.1

ENV ENV PROD
ENV DATABASE_URL REAL_DATABASE_URL

WORKDIR /src

COPY /src /src

COPY requirements.txt /src

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]