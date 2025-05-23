FROM python:3.11-slim

WORKDIR /tg-bot

COPY . .

RUN pip install -r requirements.txt --no-cache-dir

CMD ["python", "bot.py"]
