# Golden Flow — Web Application Constitution

This constitution defines the non-negotiable principles, constraints, and governance rules for Golden Flow's web application surface (frontend, public APIs, and any browser-executed code). The purpose is to keep user safety, privacy, accessibility, reliability, and developer velocity aligned across the project.

## Core Principles (Non-negotiable)

1. Security First — default-deny
   - All public-facing functionality must be implemented assuming hostile input and hostile networks.
   - Enforce HTTPS only (HSTS), secure cookie flags (HttpOnly, Secure, SameSite=strict where practical).
   - Apply Content Security Policy (CSP) with explicit sources; use Subresource Integrity (SRI) for critical third-party static assets.
   - Protect against XSS, CSRF, SQL/NoSQL injection, open redirects, and privilege escalation.

2. Privacy by Design
   - Minimize collection of PII. Treat any collected PII as sensitive: encrypt in transit and at rest, document retention policies, and provide deletion procedures.
   - Default telemetry must be anonymous and opt-in for detailed traces; maintain a privacy notice and data processing records.

3. Accessibility and Inclusivity
   - Meet WCAG 2.1 AA as a minimum for production UI components. Automated accessibility checks and at least one manual a11y review per release.
   - Keyboard navigability, semantic markup, and ARIA where appropriate.

4. Test-First Quality
   - Unit tests for business logic, integration tests for API contracts, end-to-end tests for critical user flows. Tests must be added alongside features.
   - Maintain a baseline test coverage target (e.g., 80% unit+integration for critical modules) and focus on meaningful tests over raw coverage numbers.

5. Observability and Error Budgeting
   - Structured logging, distributed tracing and metrics for key business flows; define SLOs/SLA and error budget policies before major releases.
   - Runtime feature flags and health checks for rapid rollback and graceful degradation.

6. Performance and Resilience
   - Establish performance budgets (bundle size, TTFB, Time to Interactive). Optimize for first meaningful paint and accessibility.
   - Implement progressive enhancement and graceful degradation for poor networks; use caching, CDNs, and SSR/edge rendering where beneficial.

7. Simplicity and Maintainability
   - Prefer small, well-documented modules with clear public contracts. Avoid premature optimization and unnecessary abstractions.
   - Use typed interfaces (TypeScript or equivalent) for public components and APIs.

## Constraints and Standards

- Technology: The web application should use the approved stack documented in `TECH_STACK.md` (frontend framework, testing libs, build tooling). Any deviation requires an RFC and approval.
- Dependency policy: Third-party dependencies must be vetted for security, license compatibility, and maintenance. Major security or EOL issues require a remediation plan within 72 hours.
- Secrets: Do not store secrets in the repo. Use secret management (e.g., cloud KMS, Vault) and rotated credentials.
- Authentication & Authorization: Use standard, auditable protocols (OAuth2/OIDC or equivalent). Principle of least privilege for service-to-service auth.
- Data handling: All PII must be labelled in the schema and access-controlled. Use field-level encryption where required.
- API Contracts: Public API schemas must be versioned and backwards compatible where possible; breaking changes require a migration window and communication plan.

## Development Workflow & Quality Gates

- Branching: Small focused PRs; a single feature should map to one PR where possible. Large/long-lived work requires regular rebase and integration checkpoints.
- Reviews: All PRs require at least one code review and a security checklist sign-off for changes touching auth, input handling, or data storage.
- CI/CD: Every PR must pass automated checks — linting, type-check, unit tests, integration tests, accessibility scans (automated), and a smoke E2E test before merge.
- Releases: Use semantic versioning for public APIs. Production releases must go through staged rollout (canary → gradual → full) with automated rollback on SLO breaches.
- Infrastructure as Code: All infra changes go through the same review and CI pipeline; stateful infra changes need a migration plan and backups.

## Observability, Monitoring & Incidents

- Define key metrics (availability, latency, error rate, throughput) and create dashboards and alerts for SLO breaches.
- Retain logs and traces for the period mandated by privacy and compliance policies; have runbooks for common incidents and a post-incident review process.

## Accessibility & UX Policy

- Include accessibility criteria in the definition of done for every UI story.
- Run automated a11y scans in CI; include representative manual checks for keyboard navigation and screen-reader compatibility in release QA.

## Performance Budgets

- Set and enforce budgets for bundle size, critical render path, and server response times. CI must warn (and fail optionally) when budgets are exceeded.

## Security Checklist (must be satisfied for any public release)

- Threat model updated for new public features.
- Dependency scan (SCA) report reviewed; critical findings remediated or mitigated.
- CSP and secure headers configured; automated tests for missing headers.
- Secrets and credentials not present in repo or logs.
- Input validation and server-side authorization checks in place.

## Governance and Amendments

- The constitution is the single source of high-level policy for the web application surface. Amendments require:
  1. A documented rationale and proposed text change (PR). 
  2. Approval by the maintainers team (2 approvals required) and security lead for security/privacy changes.
  3. A migration or compliance plan for infra, docs, and dependent components when applicable.

## Non-compliance

- Non-compliant changes must be flagged in PRs and accompanied by an explicit risk acceptance statement and mitigation plan. Critical non-compliance (security or privacy) blocks merge.

## Notes & Helpful Links

- Update `CONTRIBUTING.md` and `TECH_STACK.md` when the constitution introduces new tooling or standards.
- Use the `.specify/memory` path for living governance documents; cross-reference `CONSTITUTION.md` where other templates require it.

**Version**: 1.0.0 | **Ratified**: 2025-09-14 | **Last Amended**: 2025-09-14