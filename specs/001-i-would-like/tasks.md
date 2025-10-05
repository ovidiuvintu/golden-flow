```markdown
# Tasks: Data Streaming Simulator

**Input**: Design documents from C:\Development\golden-flow-oct-05\golden-flow\specs\001-i-would-like

## Phase 3.1: Setup
- [ ] T001 Initialize Next.js app routes and basic page at `src/app/streaming/page.tsx`
- [ ] T002 [P] Create `src/server/simulator.ts` (simulator engine skeleton)
- [ ] T003 [P] Configure linting and TypeScript in `src` if not present

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**
- [ ] T004 [P] Contract test: stream payload schema in `specs/001-i-would-like/contracts/stream-schema.test.ts`
- [ ] T005 [P] Unit test: simulator produces correct number of samples at configured cadence (`tests/unit/test_simulator.ts`)
- [ ] T006 [P] Integration test (Playwright): dashboard shows live samples when Start is pressed (`tests/integration/test_dashboard_start.spec.ts`)
- [ ] T007 [P] Integration test: Pause/Stop behavior (`tests/integration/test_dashboard_pause.spec.ts`)

## Phase 3.3: Core Implementation (ONLY after tests are failing)
- [ ] T008 [P] Implement SSE route handler at `src/app/api/stream/route.ts` that streams batches from `src/server/simulator.ts`
- [ ] T009 [P] Implement Start/Pause/Stop controls in `src/app/streaming` and wire to server actions or client commands
- [ ] T010 [P] Implement client-side localStorage persistence for control config (e.g., `src/lib/localStorage.ts`)
- [ ] T011 [P] Implement minimal charting (canvas-based or lightweight lib) with rendering throttle

## Phase 3.4: Observability & Integration
- [ ] T012 Add structured logging in `src/server/simulator.ts` for start/pause/stop and batch stats
- [ ] T013 Add lightweight metric reporting (samplesEmittedPerSec) to server logs

## Phase 3.5: Polish & Performance
- [ ] T014 [P] Performance test: validate 1000 samples/sec server emit with batching (smoke test)
- [ ] T015 [P] Accessibility checks: keyboard controls and ARIA labels on the dashboard
- [ ] T016 [P] Add export CSV client task

## Validation Checklist
- [ ] All contract tests written and failing
- [ ] All integration tests written and failing
- [ ] Observability tasks included
- [ ] Tasks reference exact file paths

```
