FROM python:3.11-slim

WORKDIR /app
COPY backend/ /app
RUN pip install --no-cache-dir fastapi uvicorn sqlmodel sqlalchemy psycopg2-binary authlib alembic python-multipart email_validator email_validator httpx itsdangerous

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
