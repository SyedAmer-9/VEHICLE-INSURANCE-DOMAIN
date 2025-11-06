FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
COPY pyproject.toml .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5001

CMD ["python","app.py"]

