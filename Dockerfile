# --- Build stage: compile the C++ calculator with Bazel -----------------
FROM debian:bookworm-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        git \
        python3 \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install bazelisk (reads .bazelversion to fetch the matching Bazel release).
RUN curl -fsSL -o /usr/local/bin/bazel \
        https://github.com/bazelbuild/bazelisk/releases/latest/download/bazelisk-linux-amd64 \
    && chmod +x /usr/local/bin/bazel

WORKDIR /workspace
COPY . .

RUN bazel build -c opt //:main \
    && cp -L bazel-bin/main /workspace/main_bin

# --- Runtime stage: Flask app + compiled binary --------------------------
FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        libstdc++6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY webapp/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY webapp/ ./
COPY --from=builder /workspace/main_bin /app/bin/main

# Tell the Flask app where to find the compiled calculator binary.
ENV MACROS_BINARY=/app/bin/main
ENV FLASK_DEBUG=0

# Render sets $PORT at runtime; gunicorn binds to it.
EXPOSE 8080
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-8080} app:app"]
