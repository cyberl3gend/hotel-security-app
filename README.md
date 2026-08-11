# Hotel Security App — 16-Week DevSecOps Portfolio Sprint

A deliberately vulnerable hotel booking application built and progressively secured over 16 weeks, demonstrating end-to-end DevSecOps practices from secure coding to automated CI/CD security pipelines.

## What This Project Demonstrates

This isn't a tutorial follow-along. Every vulnerability was built, exploited, and fixed hands-on — then documented with real screenshots, working code, and blog writeups explaining the why behind every decision.

## The Stack

**Application:** Python, Flask, SQLite, bcrypt  
**Infrastructure:** AWS (VPC, EC2, Security Groups, Network ACLs, WAF, S3)  
**IaC:** Terraform  
**Containers:** Docker, Alpine base image  
**CI/CD:** GitHub Actions  
**Security Scanning:** Semgrep, TruffleHog, Trivy, OWASP ZAP  
**Observability:** Prometheus, Grafana, Alertmanager  
**SBOM:** Syft (CycloneDX format)  

## Security Controls Implemented

### Application Layer
- Parameterized queries preventing SQL injection
- bcrypt password hashing with automatic salting
- Server-side session management with HttpOnly + SameSite cookie flags
- Rate limiting and account lockout against credential stuffing
- IDOR prevention with ownership verification on every API endpoint

### UI Layer
- Clickjacking prevention via X-Frame-Options and CSP headers
- CSS attribute exfiltration prevention via Content Security Policy
- Subresource Integrity (SRI) for third-party script verification

### Container Layer
- Alpine minimal base image (175MB vs 689MB Ubuntu — 75% attack surface reduction)
- Non-root user (hoteluser) with least privilege
- .dockerignore preventing secrets from entering image
- Trivy scanning blocking CRITICAL CVEs before deployment

### Infrastructure Layer
- AWS VPC with public/private subnet segmentation
- Security Groups with default deny, explicit allow
- Network ACLs at subnet boundary (stateless, defense in depth)
- AWS WAF with Core Rule Set and SQL injection rules
- Zero-Trust Architecture applied at every layer

### Pipeline Layer
- 7-stage automated security pipeline on every push to main
- TruffleHog → Semgrep → Docker/Trivy → OWASP ZAP → SBOM → S3 → Deploy
- Branch protection requiring PR review before merge to main
- SBOM and scan artifacts stored in S3 by commit hash for compliance audit trail

### Observability Layer
- Prometheus scraping application metrics every 15 seconds
- Grafana dashboard with HTTP request rate, error rate, rate-limited requests
- Alertmanager routing alerts to Slack — AppDown, HighErrorRate, HighLoginFailures

## The CI/CD Pipeline

## Weekly Blog Posts

Each week has a detailed writeup covering the attack, the defense, the lab, and the lessons:

| Week | Topic | Key Concept |
|------|-------|-------------|
| 1 | HTML Security & Input Validation | XSS prevention, innerHTML vs textContent |
| 2 | UI Layer Attacks | Clickjacking, CSS exfiltration, SRI |
| 3 | Broken Authentication | bcrypt, sessions, credential stuffing |
| 4 | Secure API Design | IDOR, authorization vs authentication |
| 5 | Git Security | Branch protection, secret management |
| 6 | SAST with Semgrep | Automated code scanning, custom rules |
| 7 | Secrets Management | TruffleHog, Git history scanning, .env |
| 8 | Containerization | Docker, Alpine, Trivy, non-root user |
| 9 | Cloud Infrastructure | AWS VPC, Zero-Trust Architecture |
| 10 | Firewall Management | Network ACLs, WAF, defense in depth |
| 11 | Infrastructure as Code | Terraform, GitOps for infrastructure |
| 13 | CI/CD Security Pipeline | GitHub Actions, SBOM, S3 compliance |
| 14 | Continuous Deployment | GitOps, automated deployment |
| 15 | Observability | Prometheus, Grafana, Alertmanager |

## Resume Keywords

`DevSecOps` `Shift-Left Security` `SAST` `DAST` `Secret Detection` `Container Hardening` `Infrastructure as Code` `CI/CD` `Zero-Trust Architecture` `SBOM` `Threat Modeling` `AWS` `Terraform` `Docker` `GitHub Actions` `Python` `Flask` `Prometheus` `Grafana`
