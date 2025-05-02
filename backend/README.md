# Backend

## Setup

Make sure to install Poetry and Python 3.13+.

1. Install Poetry :
```bash
curl -sSL https://install.python-poetry.org | python3 -
export PATH=$HOME/.local/bin:$PATH
```

If it works, you should be able to run:
```bash
poetry --version
```

2. Install dependencies:
```bash
poetry install
```

3. Init the database:

:warning: This will drop all existing data in the database. :warning:
```bash
poetry run python3 -m src.backend.init_db
```

1. Run the application:
```bash
poetry run start # For production
poetry run dev   # For development
```