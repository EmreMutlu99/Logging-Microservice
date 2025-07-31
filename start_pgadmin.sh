#!/bin/bash

echo "🌐 Checking internet connection..."
if ping -q -c 1 -W 2 google.com >/dev/null; then
  echo "✅ Internet connection is active."
else
  # sudo dhclient
  echo "❌ No internet connection! Please check your network."
  exit 1
fi

echo ""
echo "🔍 Checking PostgreSQL 16 service status..."
PG_STATUS=$(systemctl is-active postgresql@16-main)

if [ "$PG_STATUS" = "active" ]; then
  echo "✅ PostgreSQL 16 is already running."
else
  echo "🚀 Starting PostgreSQL 16..."
  sudo systemctl start postgresql@16-main
  if [ $? -eq 0 ]; then
    echo "✅ PostgreSQL 16 started successfully."
  else
    echo "❌ Failed to start PostgreSQL 16!"
    exit 1
  fi
fi

echo ""
echo "🔍 Checking pgAdmin status..."

if pgrep -f "pgadmin4" > /dev/null; then
  echo "✅ pgAdmin is already running."
else
  echo "🚀 Starting pgAdmin..."
  pgadmin4 &>/dev/null &
  if [ $? -eq 0 ]; then
    echo "✅ pgAdmin started in the background. Open your browser and visit http://127.0.0.1:5050"
  else
    echo "❌ Failed to start pgAdmin!"
    exit 1
  fi
fi
