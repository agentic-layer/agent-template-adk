FROM python:3.13-trixie AS build_python
WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.8 /uv /uvx /bin/
COPY ./pyproject.toml ./uv.lock ./
RUN uv sync --frozen --no-default-groups


FROM python:3.13-slim-trixie AS final
WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000

COPY --from=build_python /app/.venv ./.venv
COPY . ./

ENTRYPOINT ["uvicorn", "main:app", "--host=0.0.0.0"]
