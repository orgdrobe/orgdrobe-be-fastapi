[old redme for `/app`](README-app.md)

# OrgDrobe - Backend - FastAPI

## setup

```bash
# create .env
# TODO? add template in readme.md or as a file

# python
pip install uv
uv sync

# docker
cd infra
docker-compose -p orgdrope up -d --build
cd ..

# migration
uv run alembic upgrade head

# seeding
uv run manage.py seed all

# run
uv run fastapi dev src/main.py

```
