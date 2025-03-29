FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure script has correct permissions and format
RUN apt-get update
RUN chmod +x /app/start

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Use bash to run the start script
CMD ["bash", "/app/start"]
