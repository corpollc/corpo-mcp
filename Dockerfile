FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
COPY corpo_mcp.py .
COPY __init__.py .
COPY __main__.py .

RUN pip install --no-cache-dir mcp httpx

ENV CORPO_API_URL=https://api.corpo.llc

ENTRYPOINT ["python", "-m", "corpo_mcp"]
