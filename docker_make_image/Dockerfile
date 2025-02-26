# Use the official Python image
FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install PostgreSQL client tools
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy dependency files first for better caching
COPY pyproject.toml poetry.lock ./

# Install Poetry and dependencies
RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Copy the entire project into the container
COPY src /app/src

# Set the working directory inside the source directory
WORKDIR /app/src

# Expose port 8000 for Django
EXPOSE 8000

# Run the application (replace wait-for-db.sh)
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
