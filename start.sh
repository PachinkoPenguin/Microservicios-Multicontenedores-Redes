#!/bin/bash

# Script to initialize and run the microservices application

echo "Initializing Microservices Equation Calculator..."

# Build and start all containers
docker compose up --build -d

# Check if all containers are running
echo "Checking container status..."
docker ps

echo ""
echo "Services are available at:"
echo "- Suma Service: http://localhost:8001/sumar"
echo "- Resta Service: http://localhost:8002/restar"
echo "- Ecuacion Service: http://localhost:8003/resolver"
echo "- Database API: http://localhost:8004/results"
echo ""
echo "Example API call:"
echo "curl -X POST -H \"Content-Type: application/json\" -d '{\"a\": 10, \"b\": 5, \"c\": 8, \"d\": 3}' http://localhost:8003/resolver"
echo ""
