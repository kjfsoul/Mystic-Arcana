#!/bin/bash
python app.py &  # Start Flask backend on port 5000
npm start &      # Start Node.js frontend on port 3000
wait