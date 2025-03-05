#!/bin/bash

# Kill any process running on port 3000
echo "Checking for processes on port 3000..."
npx kill-port 3000 || true

# Start the React application
echo "Starting React app..."
PORT=3000 npm start
