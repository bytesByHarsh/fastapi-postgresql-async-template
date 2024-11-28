## FastAPI + PostgreSQL Async Template


## Installation

```bash
sudo snap install ruff
pip install -r requirements.txt
pip install -r requirements_test.txt

```

## Start Application

> Note: Make sure you have created `.env` file and update relevant information

```bash
alembic upgrade head

python main.py
```

## Alembic

### Update to head
```bash
alembic upgrade head
```

### New Database Migration Version
```bash
alembic revision --autogenerate -m "Init Migration"
```