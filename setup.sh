#!/bin/bash
docker compose up -d --build

echo "Waiting for database..."
until docker exec cards_db pg_isready -U postgres; do
  sleep 1
done

docker exec cards_api alembic upgrade head

echo "Done. Open http://localhost:8000/docs"