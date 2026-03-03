FROM python:3.14-slim
WORKDIR /app
COPY pyproject.toml README.md /app/
COPY src /app/src
RUN pip install --no-cache-dir .
CMD ["python", "-m", "thunderbird_bot.main"]
