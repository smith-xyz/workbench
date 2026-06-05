FROM golang:1.24 AS builder
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /api ./cmd/api
RUN CGO_ENABLED=0 go build -o /migrate ./cmd/migrate

FROM gcr.io/distroless/static-debian12
COPY --from=builder /api /api
COPY --from=builder /migrate /migrate
ENTRYPOINT ["/api"]
