FROM python:3.14-slim

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy project
COPY . /app

# Install dependencies from pyproject/uv lock
# (uv gère l'environnement dans l'image)
RUN uv sync

EXPOSE 8000

# Lance uvicorn via uv (pour utiliser les deps installées par uv)
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
