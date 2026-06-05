# Templates

Project templates and starter kits across languages.

## Quick Start

```bash
cp templates/config.example ~/.config/workbench/config  # one-time setup
scaffold                                                 # interactive (fzf)
```

Templates use `__TOKEN__` placeholders (`__ORG__`, `__SERVICE__`, `__NAMESPACE__`, etc). The scaffold script reads `~/.config/workbench/config`, copies the template, and replaces all tokens. `__SERVICE__` comes from the project name prompt; everything else from the config file.

## Scaffolds (quick, minimal, extend immediately)

| Template | Stack | Description |
|----------|-------|-------------|
| `go/api-service-template` | Chi + GORM | Production-shaped API with migrations, domain slices, health checks |
| `go/cli-template` | Cobra + Viper | CLI with subcommands, config (file + env + flags), version injection |
| `go/daemon-template` | stdlib | Long-running process with tick loop, health file, cross-platform deploy |
| `typescript/bun-cli-template` | Bun + parseArgs | CLI with config-file-first, CLI overrides, single-binary build |
| `typescript/bun-api-template` | Bun + Hono | JSON API with CORS, logging, in-memory store |
| `typescript/node-cli-template` | Node + parseArgs | CLI with config-file-first, CLI overrides, zero deps |
| `typescript/node-api-template` | Node + Fastify | JSON API with CORS, health probes, typed routes |
| `rust/api-service-template` | Axum | JSON API with CORS, tracing, in-memory store |
| `rust/daemon-template` | Tokio | Async daemon with signal handling and tracing |
| `python/daemon-template` | stdlib | Unix double-fork daemon with PID management |

## Infrastructure (deploy manifests, ready to `apply -k`)

| Template | Platform | Description |
|----------|----------|-------------|
| `infra/openshift` | OCP | Deployment, Service, Route, HPA, NetworkPolicy, Kustomize |
| `infra/aws-eks` | EKS + ALB | Deployment, Service, ALB Ingress, IRSA, HPA, NetworkPolicy, Kustomize |
| `infra/digitalocean` | DOKS + nginx | Deployment, Service, nginx Ingress, cert-manager TLS, HPA, Kustomize |

## Starter Kits (opinionated, batteries-included)

| Template | Stack | Description |
|----------|-------|-------------|
| `typescript/nx-monorepo` | Nx + pnpm + Vite + TypeORM | Full-stack monorepo (React web + Express API + shared libs) |
| `python/full-stack-monorepo` | FastAPI + React + SQLAlchemy + UV | Full-stack monorepo with migrations, frontend build, tooling |
| `python/ml-template` | PyTorch + HF + MLflow + Optuna | ML platform with training, evaluation, serving, experiment tracking |
