#!/bin/bash

# --- Command Detection ---
if docker compose version >/dev/null 2>&1; then
    DOCKER_CMD="docker compose"
elif docker-compose version >/dev/null 2>&1; then
    DOCKER_CMD="docker-compose"
else
    echo "Error: Neither 'docker compose' nor 'docker-compose' was found."
    exit 1
fi

COMPOSE_FILE="backend/docker-compose.yml"

case "$1" in
  db)
    echo "Starting DB service..."
    $DOCKER_CMD -f $COMPOSE_FILE up -d db
    ;;
  backend)
    echo "Starting DB + API..."
    $DOCKER_CMD -f $COMPOSE_FILE up -d api
    ;;
  all)
    echo "Starting all services..."
    $DOCKER_CMD -f $COMPOSE_FILE up -d
    ;;
  rebuild)
    echo "Rebuilding images (no-cache)..."
    $DOCKER_CMD -f $COMPOSE_FILE build --no-cache
    echo "Restarting services..."
    $DOCKER_CMD -f $COMPOSE_FILE up -d
    ;;
  stop)
    echo "Stopping all services..."
    $DOCKER_CMD -f $COMPOSE_FILE down
    ;;
  logs)
    $DOCKER_CMD -f $COMPOSE_FILE logs -f
    ;;
  *)
    echo "Usage: $0 {db|backend|all|rebuild|stop|logs}"
    exit 1
esac