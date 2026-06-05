FROM node:22-alpine AS base
RUN corepack enable pnpm

FROM base AS deps
WORKDIR /app
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
COPY apps/api/package.json apps/api/
COPY libs/shared/package.json libs/shared/
COPY libs/db/package.json libs/db/
RUN pnpm install --frozen-lockfile --prod

FROM base AS build
WORKDIR /app
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
COPY apps/ apps/
COPY libs/ libs/
COPY tsconfig*.json nx.json ./
RUN pnpm install --frozen-lockfile
RUN pnpm build

FROM base AS api
WORKDIR /app
COPY --from=deps /app/node_modules node_modules
COPY --from=build /app/dist/apps/api dist/
USER node
EXPOSE 4000
CMD ["node", "dist/main.js"]
