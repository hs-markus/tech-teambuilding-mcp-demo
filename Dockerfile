FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir fastmcp

COPY server_http.py .
COPY snippets/ ./snippets/

EXPOSE 3001

CMD ["fastmcp", "run", "server_http.py", "--transport", "streamable-http"]
