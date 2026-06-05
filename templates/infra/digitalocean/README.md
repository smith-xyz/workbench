# DigitalOcean Kubernetes (DOKS) — `yourservice` template

## What’s included

A Kustomize bundle that deploys containerized API `yourservice` into namespace `yourproject`: Deployment (probes, resources, hardening, HA anti-affinity), ServiceAccount, ConfigMap, Secret, ClusterIP Service (port 80 → 8080), Ingress (NGINX + cert-manager TLS), HPA (2–10 replicas, CPU and memory), PodDisruptionBudget, default-deny plus allow `NetworkPolicy` (ingress from `ingress-nginx`; egress DNS, HTTPS, PostgreSQL — tighten to your backends), and internal TLS via cert-manager for pod-to-pod encryption.

## Prerequisites

- A running DOKS cluster.
- **NGINX Ingress Controller** — DigitalOcean 1-Click App or Helm; pods must live in a namespace labeled `kubernetes.io/metadata.name: ingress-nginx` (adjust `networkpolicy.yaml` if your install uses another namespace).
- **cert-manager** with a `ClusterIssuer` named `letsencrypt-prod` (or change the Ingress annotation and TLS setup).
- **DNS** — an `A` or `CNAME` record for `yourservice.example.com` pointing at the load balancer provisioned for the ingress controller (see below).
- If you use DigitalOcean Container Registry, ensure the cluster can pull `registry.digitalocean.com/yourregistry/yourservice:latest` (registry integration or image pull secret).

## Quick deploy

From this directory:

```bash
kubectl apply -k .
```

Edit placeholders in the manifests (or use Kustomize patches/overlays) before applying in production. For secrets, prefer [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets) or [External Secrets Operator](https://external-secrets.io/) instead of committing `secret.yaml` with real values.

## Customize

| Area | What to change |
|------|----------------|
| Namespace | `namespace.yaml` metadata `name`, and `namespace:` in `kustomization.yaml` |
| App labels / HPA target | `app.kubernetes.io/name` and resource `name` fields if you rename the app |
| Image | `deployment.yaml` → `image:` |
| Hostname & TLS secret | `ingress.yaml` → `rules[].host`, `tls[].hosts`, `tls[].secretName` |
| Issuer | `ingress.yaml` annotation `cert-manager.io/cluster-issuer` |
| Secrets | `secret.yaml` — placeholders only; use Sealed Secrets / External Secrets or manage Secret out-of-band |
| Ingress namespace | `networkpolicy.yaml` `namespaceSelector` if NGINX runs elsewhere |
| Network egress | `networkpolicy.yaml` — restrict `ipBlock` and `ports` to your APIs and database |

## Common operations

```bash
kubectl -n yourproject get pods,svc,ingress
kubectl -n yourproject logs deploy/yourservice -f
kubectl -n yourproject describe certificate yourservice-tls
kubectl -n yourproject rollout restart deploy/yourservice
```

## Load balancer

DigitalOcean provisions a **managed load balancer** when the NGINX Ingress Controller’s Service is type `LoadBalancer`. Point your DNS at that load balancer’s IP or hostname; you do not add a separate LoadBalancer Service for this application—the Ingress controller fronts traffic to the ClusterIP Service.
