FROM python:3.12-slim

WORKDIR /app

# Install dependencies first for better layer caching.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy the application source.
COPY . .

EXPOSE 3000

# Run with gunicorn in production; app.py exposes the `app` object.
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-3000} app:app"]
