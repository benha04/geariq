# Local Development

# copy env

cp .env.example .env

# start services

docker compose up --build

# visit frontend

open http://localhost:3000

# check API

curl http://localhost:8000/health
curl "http://localhost:8000/v1/search?q=MIPS%20bike%20helmet&budget=150"
