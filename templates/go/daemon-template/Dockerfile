FROM golang:1.24 AS builder
WORKDIR /src
COPY go.mod ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /__SERVICE__ .

FROM gcr.io/distroless/static-debian12
COPY --from=builder /__SERVICE__ /__SERVICE__
ENV DAEMON_LOG_JSON=true
ENV DAEMON_HEALTH_FILE=/var/health.json
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
    CMD ["/__SERVICE__", "-health-check"]
ENTRYPOINT ["/__SERVICE__"]
