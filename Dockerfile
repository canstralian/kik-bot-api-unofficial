FROM python:3.11-slim

LABEL name="kik-bot-api-unofficial"
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY . /app/
RUN python -m pip install --no-cache-dir . && \
    python -m pip check && \
    useradd --create-home --uid 10001 bot && \
    chown -R bot:bot /app
USER bot
CMD ["python", "examples/simple_echo_bot.py"]
