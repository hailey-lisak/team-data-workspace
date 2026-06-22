FROM python:3.14-slim
WORKDIR /app

# Install Python deps first for better layer caching
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application source after installing deps
COPY . /app

EXPOSE 8000

# Adjust the module path if your ASGI app is in a different location
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
