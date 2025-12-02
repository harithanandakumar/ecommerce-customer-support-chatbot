# Multi-stage build for optimized image size
FROM python:3.9-slim as builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Create virtual environment and install dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.9-slim

# Set metadata
LABEL maintainer="harithanandakumar"
LABEL description="Rule-based NLP e-commerce customer support chatbot"
LABEL version="1.0.0"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH" \
    LOG_LEVEL=INFO

# Create app user for security
RUN useradd -m -u 1000 chatbot && \
    mkdir -p /app/logs && \
    chown -R chatbot:chatbot /app

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Copy application code
COPY --chown=chatbot:chatbot chatbot/ ./chatbot/
COPY --chown=chatbot:chatbot data/ ./data/
COPY --chown=chatbot:chatbot config.json .
COPY --chown=chatbot:chatbot main.py .
COPY --chown=chatbot:chatbot requirements.txt .

# Switch to non-root user
USER chatbot

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "from chatbot.dialogue_system import DialogueSystem; chatbot = DialogueSystem(); print('healthy')" || exit 1

# Expose port for API
EXPOSE 5000

# Run the chatbot
CMD ["python", "main.py"]
