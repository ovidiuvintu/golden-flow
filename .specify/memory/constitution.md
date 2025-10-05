# golden-flow Constitution
<!-- Sync Impact Report - generated 2025-10-05
Version change: 2.1.1 -> 2.2.0
Modified principles: Modularity & Encapsulation; Test-First (TDD, NON-NEGOTIABLE); Observability & Structured Logging; Performance & Accessibility; Versioning & Stability
Added sections: Constraints & Standards; Development Workflow
Removed sections: none
Templates updated: .specify/templates/plan-template.md ✅ (updated to include explicit constitution gates)
.specify/templates/spec-template.md ✅ (aligned - no change required)
.specify/templates/tasks-template.md ✅ (already aligned with TDD requirements)
.specify/templates/agent-file-template.md ⚠ pending manual review (placeholder dates and manual sections)
Follow-up TODOs: RATIFICATION_DATE (deferred - needs historical adoption date)
-->

## Core Principles

### Modularity & Encapsulation
Every new feature SHOULD be developed as a well-scoped, modular unit (component, package,
or library) with a clearly documented public contract. Modules MUST be independently
testable and importable; internal helpers MUST remain private to the module. This reduces
cross-cutting coupling, speeds reviews, and makes automated contract tests practical.

Rationale: Modular code is easier to reason about, test, and evolve with minimal
blast-radius for changes.

### Test-First (TDD) (NON-NEGOTIABLE)
Tests MUST be written before implementation: feature specs and automated tests (unit,
contract, or integration as appropriate) MUST exist and FAIL before any implementation is
committed. Follow the Red→Green→Refactor cycle. PRs that add or change behavior MUST
include tests that demonstrate the intended change and cover edge cases.

Rationale: Test-first development prevents regressions, clarifies requirements, and
ensures implementation meets observable criteria.

### Observability & Structured Logging
All services, APIs, and important UI flows MUST emit structured logs and errors with
contextual metadata (request id, user id where applicable, environment). Quickstarts
and new features MUST include guidance for how to observe behavior (logs, tracing,
and relevant metrics). Logging MUST be structured (JSON or equivalent) so it can be
consumed by downstream observability tools.

Rationale: Observability is required to triage incidents, validate behavior in CI, and
measure feature health in production-like environments.

### Performance & Accessibility
Frontend and API changes MUST include performance and accessibility considerations.
New pages or components MUST document performance budgets (e.g., p95, LCP targets)
and accessibility acceptance criteria (keyboard navigation, ARIA, semantic DOM). When
trade-offs are made, the plan MUST document the rationale and mitigation steps.

Rationale: Web quality includes speed and inclusivity. Defining targets early avoids
late regressions and technical debt.

### Versioning & Stability
The project MUST use semantic versioning for public APIs and published packages.
Breaking changes MUST be announced, documented, and accompanied by a migration plan.
Internal experiments may use feature flags, but any change that impacts external
contracts (APIs, published packages, stable GraphQL schemas) requires a minor/major
versioning decision and review.

Rationale: Clear rules for versioning reduce unexpected consumer breakage and create
an auditable change history.

## Constraints & Standards

Technology stack: Next.js 15 (React 19), TypeScript, TailwindCSS (where used), and
Node.js toolchains as documented in repository manifests. Linting and formatting MUST be
configured and enforced in CI (ESLint + project rules; Prettier optional but recommended).

Security & compliance: Sensitive data MUST be treated according to company policy; no
secrets in source. Dependencies with known critical CVEs MUST be remediated or
documented with a mitigation. Authentication and authorization decisions MUST be
documented in specs where applicable.

Testing & quality: Unit, contract, and integration tests MUST be present per the test-first
principle. CI pipelines MUST run the full test suite on feature branches before merge.

Accessibility & performance: Frontend features MUST include accessibility checks and
performance budgets as part of the quickstart/PR checklist.

## Development Workflow

1. Author creates a feature spec (`/specs/<feature>/spec.md`) or updates an existing one.
2. Create failing tests per TDD (unit/contract/integration) in the feature branch.
3. Implement changes with small, focused commits and update `data-model.md` / contracts as
	necessary.
4. Open a PR that references the spec and includes a passing CI build that:
	- Runs linting and type checks
	- Runs the test suite (unit, contract, integration)
	- Runs constitution checks (see Governance below)
5. At least one reviewer must approve; high-impact or breaking changes MUST include
	an explicit migration plan and at least two reviewers.

Quality gates: PRs without tests, without lint/type checks passing, or that violate core
principles (TDD, observability, semantic versioning for public contract changes) MUST
be blocked until remediated.

## Governance

The constitution is the authoritative source for project norms. Changes to the
constitution MUST be proposed via a PR that includes: the amended document, a short
change rationale, and a list of templates/files impacted by the change. Amendments
are accepted with a majority review (1 maintainer + 1 reviewer) and MUST include a
Last Amended date. Major governance changes (adding or removing a core principle)
require a public discussion and at least two maintainers' approval.

Compliance: Automated checks SHOULD validate that new plans and PRs reference the
constitution and verify principle alignment during the /plan step. Failures in
automated constitution checks MUST be documented as complexity items and addressed
before merge.

Guidance files: Use `.specify/templates/agent-file-template.md` and project quickstarts
for runtime developer guidance; update them when adding new tooling or flows.

**Version**: 2.2.0 | **Ratified**: TODO(RATIFICATION_DATE): historical adoption date needed | **Last Amended**: 2025-10-05