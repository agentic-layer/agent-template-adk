VERSION ?= $(shell git describe --tags --always | sed 's/^v//')
IMAGE_TAG_BASE ?= ghcr.io/agentic-layer/agent-template-adk
IMG ?= $(IMAGE_TAG_BASE):$(VERSION)
PLATFORMS ?= linux/arm64,linux/amd64

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
	docker build -t $(IMAGE_TAG_BASE) .

.PHONY: docker-push
docker-push:
	- docker buildx create --name agent-builder
	docker buildx use agent-builder
	docker buildx build --push --platform=$(PLATFORMS) --tag $(IMG) --tag latest .
