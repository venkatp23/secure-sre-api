# STAGE 1: Build stage
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
# Install dependencies into a local folder
RUN pip install --user --no-cache-dir -r requirements.txt

# STAGE 2: Production stage
FROM python:3.12-slim AS runner
WORKDIR /app

# SRE Best Practice: Run as a non-root user for security
RUN useradd -m sreuser
USER sreuser

# Copy only the installed packages and code from the builder
COPY --from=builder /root/.local /home/sreuser/.local
COPY . .

# Ensure the local bin is in the PATH
ENV PATH=/home/sreuser/.local/bin:$PATH

# SRE: Use Gunicorn for reliability and Uvicorn for speed
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "-b", "0.0.0.0:8000", "--workers", "4"]