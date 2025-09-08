#!/bin/bash

# Start backend from its own directory
(cd /app/backend && node server.js) &

# Start frontend from its own directory
(cd /app/frontend && node server.js) &

# Wait for both to exit
wait
