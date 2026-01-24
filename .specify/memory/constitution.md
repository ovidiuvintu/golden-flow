<!--
Sync Impact Report

- Version change: template -> 1.0.0
- Modified principles: added language & tooling, modularity, API Blueprint pattern, testing & CI, observability & versioning
- Added sections: Technology constraints, Development workflow
- Removed sections: template placeholders replaced with concrete policy
- Templates updated: .specify/templates/plan-template.md ✅, .specify/templates/tasks-template.md ✅
- Templates pending manual review: .specify/templates/spec-template.md ⚠ pending review
- Templates pending manual review: none
- Follow-up TODOs: TODO(RATIFICATION_DATE): confirm original adoption date if known
-->

# Golden Flow Constitution

## Core Principles

### I. Language & Tooling (NON-NEGOTIABLE)
All code in this repository MUST target Python 3.12 or newer. All source files MUST include type hints for public functions and classes where types can be reasonably inferred. Code formatting MUST follow Black's default configuration and be enforced via pre-commit / CI checks. Projects MUST include static type checking (mypy or equivalent) in CI pipelines.

Rationale: Modern Python features and static typing reduce runtime errors and improve maintainability across contributors.

### II. Modularity & Library-First
Design for modularity: features MUST be implemented as small, well-scoped packages or modules that expose a clear public surface. Modules MUST be independently testable, have minimal cross-module coupling, and include concise documentation and examples for public APIs.

Rationale: Encourages reuse, easier testing, and safer refactors.

### III. API Routing: Blueprint Pattern
Web API routes MUST follow the Blueprint pattern: group related endpoints into logical routers (Flask `Blueprint` or FastAPI `APIRouter`) and register them at application composition time. Each router module MUST be small, focused, and importable without side effects.

Rationale: Blueprint/Router patterns provide clear separation of concerns, enable testing of route groups, and keep application composition explicit.

### IV. Testing & CI (NON-NEGOTIABLE)
Testing is mandatory: unit tests MUST exist for all new library-level code; integration and contract tests are REQUIRED for public APIs and inter-service boundaries. The project MUST adopt a test-first or test-driven approach where practical: tests for new behavior SHOULD be added before implementation. CI pipelines MUST run formatting, linting, type checks, and the test suite on every PR.

Rationale: Ensures correctness, prevents regressions, and keeps the codebase healthy as it grows.

### V. Observability, Versioning & Releases
Code MUST produce structured logs (JSON or similarly parseable records) for significant events/errors. Metrics and error reporting integrations SHOULD be present for services that run in production. Semantic versioning (MAJOR.MINOR.PATCH) MUST be used for published packages and services; changes that break public contracts MUST increment MAJOR.

Rationale: Observability aids operations and diagnosis; semantic versioning communicates compatibility guarantees.

## Technology Constraints

- Python runtime: 3.12+ (MUST)
- Formatting: Black (MUST) — pre-commit + CI enforcement
- Type hints: public APIs MUST be annotated (MUST). Internal helpers SHOULD be typed when practical.
- API grouping: Use Blueprint/Router pattern (Flask `Blueprint` or FastAPI `APIRouter`) for all route modules (MUST)
- Packaging & distribution: Use reproducible, pinned dependency manifests (`requirements.txt` or `pyproject.toml`) for releases (SHOULD)

## Development Workflow

- Pull Requests: Every PR MUST include a description of the change, linked issue/spec, and a passing CI run that includes Black, mypy/type checks, and tests.
- Pre-commit: Repos MUST include pre-commit hooks for Black and basic linters to avoid style churn.
- Code Review: Changes to public APIs or major architectural decisions MUST include a design note and at least one reviewer familiar with the affected area.
- Commits: Use short, imperative commit messages and include issue references when applicable.

## Governance

- Amendment: Amendments to this constitution require a documented proposal, a majority approval from core maintainers, and an incremental update plan when changes affect the codebase or CI.
- Versioning: This constitution uses semantic versioning. Non-backwards-compatible governance changes require a MAJOR bump. Additive or clarifying changes without policy removals are MINOR or PATCH based on scale.
- Compliance: All PRs that touch source code MUST validate against the constitution gates (language version, formatting, typing, Blueprint pattern for routes, tests for new behavior).

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE): confirm original adoption date | **Last Amended**: 2026-01-24
<!-- End of file -->
