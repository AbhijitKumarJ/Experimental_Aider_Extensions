#!/bin/bash

# Run the Python script to add lesson list
python addlessonlist.py

# Open the default browser with the URL
# Using xdg-open for Linux systems
xdg-open http://localhost:8888/index.html &

# Start Python HTTP server
python -m http.server 8888
