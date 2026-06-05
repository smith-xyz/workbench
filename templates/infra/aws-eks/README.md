# AWS EKS application template (`yourservice`)

Kubernetes manifests to run a containerized API on Amazon EKS behind an Application Load Balancer, with autoscaling, IRSA, and a restrictive NetworkPolicy.

## What’s included

| File | Purpose |
|------|---------|
| `kustomization.yaml` | Binds resources; sets namespace `yourproject` and common labels |
| `namespace.yaml` | Namespace `yourproject` |
| `deployment.yaml` | API workload: probes (`/health`, `/ready`), requests/limits, ConfigMap + Secret env, security context (non-root, read-only root FS, `/tmp` emptyDir), pod anti-affinity, zone spread |
| `service.yaml` | `ClusterIP` service (port 80 → container 8080) |
| `ingress.yaml` | Internet-facing ALB, TLS (ACM), `target-type: ip`, health checks on `/ready` |
| `configmap.yaml` | Non-sensitive config |
| `secret.yaml` | Sensitive placeholders (`stringData`) |
| `hpa.yaml` | HorizontalPodAutoscaler (CPU/memory) |
| `pdb.yaml` | PodDisruptionBudget for voluntary disruptions |
| `serviceaccount.yaml` | IRSA annotation for the pod IAM role |
| `deny-all.yaml` | Default-deny ingress and egress for app pods; explicit allows in `networkpolicy.yaml` |
| `networkpolicy.yaml` | Ingress on `8080` from a VPC CIDR placeholder; egress DNS (`kube-system` / CoreDNS), HTTPS `443`, PostgreSQL `5432` — replace CIDRs and ports with your ALB and backends |
| `internal-tls.yaml` | cert-manager self-signed Issuer + Certificate for pod-to-pod TLS |

## Prerequisites

- **AWS Load Balancer Controller** installed in the cluster, with an **IngressClass** named `alb` (default in the [installation guide](https://kubernetes-sigs.github.io/aws-load-balancer-controller)).
- **Metrics Server** for the HPA (`kubectl get apiservices v1beta1.metrics.k8s.io`).
- **IAM**: OIDC provider on the cluster and an IAM role trusted by `yourproject/yourservice` ServiceAccount; set the role ARN in `serviceaccount.yaml`.
- **ACM**: Certificate in the same region as the ALB (typically the cluster region); set ARN in `ingress.yaml`.
- **DNS** (optional): **external-dns** or manual record for `yourservice.example.com` → ALB DNS name.
- **Container**: image listens on **8080** and implements **GET `/health`** and **GET `/ready`** (or change probes and ports in `deployment.yaml` / `service.yaml`).
- **NetworkPolicy**: CNI must enforce policies (e.g. VPC CNI with network policy support). Replace the `ipBlock` CIDR in `networkpolicy.yaml` with the range that actually reaches your pods from the ALB (often your VPC or node subnet CIDRs—validate in your environment).

## Quick deploy

From this directory:

```bash
kubectl apply -k .
```

Ensure secrets are not committed: for production prefer [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets) or [External Secrets Operator](https://external-secrets.io/), or `kubectl create secret`, instead of applying `secret.yaml` from git.

## Customize

| Goal | Where |
|------|--------|
| Namespace | `namespace.yaml`, `kustomization.yaml` (`namespace:`) |
| Image / tag | `deployment.yaml` → `containers[].image` |
| App name / labels | Replace `yourservice`; update `kustomization.yaml` `labels` pairs and selectors if you rename |
| ACM certificate | `ingress.yaml` → `alb.ingress.kubernetes.io/certificate-arn` |
| IAM role (IRSA) | `serviceaccount.yaml` → `eks.amazonaws.com/role-arn` |
| Hostname | `ingress.yaml` → `spec.rules[].host` |
| ALB scheme / internal | `ingress.yaml` → `alb.ingress.kubernetes.io/scheme` |
| Resources, replicas, probes | `deployment.yaml`; HPA `minReplicas` / `maxReplicas` in `hpa.yaml` |
| Network ingress / egress | `networkpolicy.yaml` — ingress CIDR; egress DNS, `443`, `5432` — narrow to your ALB and backends |

## Common operations

```bash
# Watch rollout
kubectl -n yourproject rollout status deployment/yourservice

# Logs
kubectl -n yourproject logs -l app.kubernetes.io/name=yourservice -f

# Shell (if image has a shell)
kubectl -n yourproject exec -it deploy/yourservice -- sh

# HPA status
kubectl -n yourproject get hpa yourservice

# Ingress / ALB address
kubectl -n yourproject get ingress yourservice

# Diff before apply
kubectl diff -k .
```

Replace placeholders (`123456789012`, certificate ID, IAM role name, host, secrets, and NetworkPolicy CIDR) before production use.
