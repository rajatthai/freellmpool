# freellmpool — OpenAI-compatible gateway over free LLM tiers.
#
#   docker run -p 8080:8080 ghcr.io/0xzr/freellmpool
#
# Works out of the box with no keys (keyless providers). Add provider keys as
# env vars to unlock more, e.g. `-e GROQ_API_KEY=...`. When exposing the proxy
# beyond localhost, set FREELLMPOOL_PROXY_KEY to require a Bearer token.
FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir .

EXPOSE 8080
ENTRYPOINT ["freellmpool"]
CMD ["proxy", "--host", "0.0.0.0", "--port", "8080"]
