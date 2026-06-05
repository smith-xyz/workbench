# syntax=docker/dockerfile:1

FROM rust:1-bookworm AS builder
WORKDIR /app
COPY Cargo.toml Cargo.lock ./
COPY src ./src
RUN cargo build --release

FROM debian:bookworm-slim
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --system --home-dir /app --shell /usr/sbin/nologin app
WORKDIR /app
COPY --from=builder /app/target/release/daemon-template /usr/local/bin/daemon-template
COPY --chown=app:app config.example.toml /app/config.toml
USER app
ENV DAEMON_CONFIG=/app/config.toml
ENV RUST_LOG=info
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD test -f /app/var/health.json || exit 1
CMD ["daemon-template"]
