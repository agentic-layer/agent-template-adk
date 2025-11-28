IMG ?= ghcr.io/agentic-layer/agent-template-adk:test

ifneq (,$(wildcard ./.env))
    include .env
    export
endif

.PHONY: all
all: docker-build

.PHONY: build
build:
	uv sync

.PHONY: docker-build
docker-build:
	docker build -t $(IMG) .

.PHONY: run
run: build
	UVICORN_PORT=8001 uv run uvicorn main:app

.PHONY: docker-run
docker-run: docker-build
	docker run --rm -it -p 8001:8001 --env-file .env -e UVICORN_PORT=8001 $(IMG)

.PHONY: check
check: build
	uv run mypy .
	uv run ruff check


.PHONY: check-fix
check-fix: build
	uv run ruff format
	uv run ruff check --fix