#!/bin/bash

# Function to print help message
print_help() {
  echo ""
  echo "Usage: ./start.sh [OPTIONS]"
  echo ""
  echo "This script builds and starts the logging-service Docker container."
  echo ""
  echo "Options:"
  echo "  --build        Rebuild the Docker image before running"
  echo "  --help         Show this help message"
  echo ""
}

# Load .env file
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
else
  echo ".env file not found."
  exit 1
fi

# Option handling
BUILD=false

for arg in "$@"
do
  case $arg in
    --build)
      BUILD=true
      shift
      ;;
    --help)
      print_help
      exit 0
      ;;
    *)
      echo "Unknown option: $arg"
      print_help
      exit 1
      ;;
  esac
done

# Optional build step
if [ "$BUILD" = true ]; then
  echo "Building Docker image..."
  docker build -t logging-service .
  echo "Build completed."
fi

# Run Docker container (without volume)
echo "Starting Docker container..."

docker run --rm \
  -e SERVER_TYPE=$SERVER_TYPE \
  -e PYTHONPATH=src \
  -p 3005:3005 \
  --network host \
  logging-service

# Ask user if unused Docker objects should be pruned
read -p "Do you want to remove all unused Docker objects (images, containers, volumes)? (y/N): " answer
if [[ "$answer" == "y" || "$answer" == "Y" ]]; then
    docker system prune
fi
