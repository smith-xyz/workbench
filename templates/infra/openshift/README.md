# OpenShift API service template (`yourservice`)

Production-oriented manifests for a containerized HTTP API on OpenShift (OCP): Deployment with probes and hardening, ClusterIP Service, edge-terminated Route, ConfigMap/Secret wiring, HPA, dedicated ServiceAccount, default-deny NetworkPolicy plus explicit allow (ingress from cluster router; egress DNS, HTTPS, PostgreSQL — adjust to your backends).

## What is included

| File | Purpose |
|------|---------|
| `serviceaccount.yaml` | Dedicated ServiceAccount for the workload |
| `configmap.yaml` | Non-secret configuration (`envFrom`) |
| `secret.yaml` | Example Secret; **replace placeholders** before real use |
| `deployment.yaml` | Two replicas, requests/limits, `/health` and `/ready`, security context, pod anti-affinity |
| `service.yaml` | ClusterIP Service on port 80 → container `http` (8080) |
| `route.yaml` | Route with TLS **edge** termination and redirect for plain HTTP |
| `hpa.yaml` | CPU and memory utilization targets |
| `deny-all.yaml` | Default-deny ingress and egress for app pods; explicit allows added by `networkpolicy.yaml` |
| `networkpolicy.yaml` | Ingress from `network.openshift.io/policy-group: ingress`; egress DNS (kube-system + `openshift-dns`), HTTPS (443), PostgreSQL (5432) — tighten `ipBlock`/`ports` to your backends |
| `pdb.yaml` | PodDisruptionBudget (`minAvailable: 1`) |
| `internal-tls.yaml` | Service with auto-minted TLS cert (OCP service CA) + CA bundle ConfigMap |
| `kustomization.yaml` | Namespace `yourproject`, common labels, image reference |

## Quick deploy

From this directory (after editing placeholders):

```bash
oc apply -k .
```

Or apply resources individually in a sensible order (ServiceAccount and Config/Secret before Deployment):

```bash
oc apply -f serviceaccount.yaml -f configmap.yaml -f secret.yaml -n yourproject
oc apply -f deployment.yaml -f service.yaml -f route.yaml -f hpa.yaml -f deny-all.yaml -f networkpolicy.yaml -n yourproject
```

Ensure the project/namespace exists:

```bash
oc new-project yourproject
# or: oc create namespace yourproject
```

Build or import an image matching:

`image-registry.openshift-image-registry.svc:5000/yourproject/yourservice:latest`

`kustomization.yaml` lists that image so you can change tag via Kustomize `images` or by editing the Deployment.

## Customize

- **Namespace**: Change `namespace:` in `kustomization.yaml` (and optionally `oc apply -k . --namespace ...` if you patch locally).
- **Image**: Update the image in `deployment.yaml` or the `images` entry in `kustomization.yaml`. Push to the internal registry or reference your external registry (may need `imagePullSecrets`).
- **Environment**: Edit keys under `configmap.yaml` / `secret.yaml`, or switch to specific `env` entries instead of `envFrom` if you do not want full map injection.
- **Resources and scaling**: Adjust `resources` in `deployment.yaml` and `minReplicas` / `maxReplicas` / metrics in `hpa.yaml`.
- **Probes**: Paths and ports must match your application (`/health`, `/ready`, port `8080` and name `http`).
- **TLS / hostname**: Set `spec.host` on the Route to your real hostname (often `<app>-<project>.apps.<cluster-base>`). For **re-encrypt** or **passthrough**, change `spec.tls` per [OpenShift Route documentation](https://docs.openshift.com/container-platform/latest/networking/routes/secured-routes.html).
- **Read-only root**: The Deployment mounts an `emptyDir` at `/tmp`; add more volumes if the app needs other writable paths.
- **NetworkPolicy**: If you use a custom ingress namespace or mesh, adjust ingress `namespaceSelector` and container port **8080** to match the Service. Restrict egress `ipBlock` and `ports` in `networkpolicy.yaml` to your real dependencies (APIs, database hosts).

## Common operations

```bash
# Scale (HPA may change replica count again)
oc scale deployment/yourservice --replicas=3 -n yourproject

# Rollout and history
oc rollout status deployment/yourservice -n yourproject
oc rollout history deployment/yourservice -n yourproject
oc rollout undo deployment/yourservice -n yourproject

# Logs
oc logs -f deployment/yourservice -n yourproject

# Route URL
oc get route yourservice -n yourproject -o jsonpath={.spec.host}
```

For production secrets, prefer [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets) or [External Secrets Operator](https://external-secrets.io/) instead of committing `secret.yaml`. Review `secret.yaml` and substitute real values through your preferred flow; avoid committing live credentials.
