# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Upgrade pip & install dependencies
RUN python3 -m pip install --upgrade pip setuptools wheel
RUN python3 -m pip install -r requirements.txt

# Install Playwright browsers
RUN python3 -m playwright install

# Set environment variables (optional defaults)
ENV HEADLESS=true
ENV RESTART_HOURS=5

# Start bot
CMD ["python3", "bot.py"]
