#!/bin/sh
# Entrypoint script for the Investment App Docker container.
#
# This script manages the application startup, including different modes of operation:
# - Test mode: Starts FastAPI, runs tests, and shuts down the server.
# - Production mode: Starts FastAPI in production mode with hot reload disabled.
#
# Created on Thu Nov 28 15:16:38 2024
# Author: Derson

# Check the execution mode
if [ "$EXECUTION_MODE" = "test" ]; then
  echo "Test mode activated. Starting FastAPI and running pytest."

  # Start FastAPI in the background
  uvicorn app.main:app --host 0.0.0.0 --port 8000 &
  FASTAPI_PID=$!

  # Wait for FastAPI to initialize
  echo "Waiting for FastAPI to start..."
  until nc -z localhost 8000; do
    sleep 1
  done

  echo "FastAPI is running. Starting tests..."

  # Run tests
  pytest tests/unit/
  pytest tests/integration/
  pytest tests/functional/

  # Shut down FastAPI after tests
  kill $FASTAPI_PID
else
  # Default mode (Production)
  echo "Production mode activated. Starting FastAPI."
  uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
fi
