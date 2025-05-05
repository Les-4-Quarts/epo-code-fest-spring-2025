# epo-code-fest-spring-2025

[toc]: # (TOC)

## Prod

## Dev

### Setup

#### Install Poetry

Make sure to install Poetry and Python 3.13+.

1. Install Poetry :
```bash
curl -sSL https://install.python-poetry.org | python3 -
echo 'export PATH=$HOME/.local/bin:$PATH' >> ~/.bashrc # or ~/.zshrc
source ~/.bashrc # or ~/.zshrc
```

If it works, you should be able to run:
```bash
poetry --version
```

2. Install dependencies:
```bash
cd backend
poetry install
```

#### Feed the database

Create the database with Docker:
```bash
docker compose up postgres -d
```

Create `config.yaml` file copy from `config-example.yaml` and fill in the values.
```bash
cd backend
cp src/backend/config/config-example.yaml src/backend/config/config.yaml
```

:warning: This will drop all existing data in the database. :warning:
```bash
poetry run python3 -m src.backend.init_db
```

Download the `db.sql` file. Then run the `psql` command to import the data into the database:
```bash
docker exec -i postgres psql -U user -d cep < {path-to-your-file}/db.sql
```
