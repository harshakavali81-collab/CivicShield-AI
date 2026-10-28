FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml README.md alembic.ini ./
COPY src ./src
COPY backend ./backend
RUN pip install --no-cache-dir '.[migrations]' && test -f /app/alembic.ini
EXPOSE 8000
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
