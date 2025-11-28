IMG ?= ghcr.io/agentic-layer/agent-template-adk:test

ifneq (,$(wildcard ./.env))
    include .env
    export
endif

.PHONY: all
all: build

.PHONY: build
build:
	uv sync

.PHONY: docker-build
docker-build:
	docker build -t $(IMG) .

.PHONY: check
check: build
	uv run mypy .
	uv run ruff check


.PHONY: check-fix
check-fix: build
	uv run ruff format
	uv run ruff check --fix