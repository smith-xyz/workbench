FROM oven/bun:1 AS build
WORKDIR /app
COPY package.json bun.lock* ./
RUN bun install --frozen-lockfile
COPY . .
RUN bun build src/main.ts --compile --outfile bin/__SERVICE__

FROM gcr.io/distroless/base-debian12
COPY --from=build /app/bin/__SERVICE__ /__SERVICE__
USER nonroot
EXPOSE 3000
ENTRYPOINT ["/__SERVICE__"]
