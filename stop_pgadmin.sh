#!/bin/bash

echo "🛑 Shutting down pgAdmin..."

# Terminate all running pgAdmin4 processes
PGADMIN_PIDS=$(pgrep -f "pgadmin4")

if [ -z "$PGADMIN_PIDS" ]; then
  echo "ℹ️ pgAdmin is already stopped."
else
  kill $PGADMIN_PIDS
  echo "✅ pgAdmin has been stopped."
fi

# If --with-postgresql parameter is provided, stop PostgreSQL 16 as well
if [[ "$1" == "--with-postgresql" ]]; then
  echo ""
  echo "🛑 Stopping PostgreSQL 16 service..."
  sudo systemctl stop postgresql@16-main
  if [ $? -eq 0 ]; then
    echo "✅ PostgreSQL 16 was successfully stopped."
  else
    echo "❌ Failed to stop PostgreSQL 16!"
    exit 1
  fi
fi
