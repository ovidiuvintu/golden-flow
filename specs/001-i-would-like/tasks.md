```markdown
# Tasks: Data Streaming Simulator

**Input**: Design docs from C:\Development\golden-flow-oct-05\golden-flow\specs\001-i-would-like

Note: Tasks are ordered for TDD. Do not implement core behavior until the tests in Phase 3.2 are created and failing.

### IDs: T001..T030 (this feature uses T001-T016)

## Phase 3.1: Setup

- [x] T001 Initialize streaming UI page (blocking)
	- Path: `src/app/streaming/page.tsx`
	- Create a stub Next.js app router page that renders a placeholder UI with Start, Pause, Stop buttons and a chart container.
	- Acceptance: Page loads at `/streaming` and shows the three buttons and an empty chart area.

- [x] T002 [P] Add server simulator skeleton (parallel)
	- Path: `src/server/simulator.ts`
	- Create an exported class `Simulator` with methods: `start(config)`, `pause()`, `stop()`, `onBatch(callback)` and in-memory config storage. No emission logic yet—just skeleton and typed interfaces.
	- Acceptance: Module builds and exports the named API; unit tests can import the class.

- [ ] T003 [P] Ensure TypeScript & linting configured for `src` (parallel)
	- Paths: `src/tsconfig.json` (if needed), update root `package.json` scripts under `src` (if applicable)
	- Acceptance: `npm --prefix src run build` (typecheck) should succeed locally after configuration; eslint config present.

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation

- [ ] T004 [P] Contract test: stream payload schema (parallel)
	- Path: `specs/001-i-would-like/contracts/stream-schema.test.ts`
	- Create a test that imports a function (to be implemented) that returns a sample payload and asserts `sessionId` exists, `batchSize === samples.length`, and each sample has `timestamp`, `metricName`, `value` (number), `unit` (string).
	- Acceptance: Test file exists and fails (because function is not implemented yet).

- [ ] T005 [P] Unit test: simulator cadence and batch size (parallel)
	- Path: `tests/unit/test_simulator.ts`
	- Create a test that constructs `Simulator` (from `src/server/simulator.ts`), calls `start({cadence: 10, metrics: [...]})` and expects `onBatch` to be called at least once within a short timeout with `samples.length > 0`.
	- Acceptance: Test exists and fails (simulator logic not implemented).

- [ ] T006 [P] Integration test (Playwright): dashboard start shows samples (parallel)
	- Path: `tests/integration/test_dashboard_start.spec.ts`
	- Create a Playwright test that loads `/streaming`, clicks Start, waits for the chart's data container to show an updated numeric sample, and asserts presence of numeric text.
	- Acceptance: Test exists and fails (dashboard and stream not implemented yet).

- [ ] T007 [P] Integration test: Pause/Stop behavior (parallel)
	- Path: `tests/integration/test_dashboard_pause.spec.ts`
	- Create a Playwright test that clicks Start, then Pause, and asserts no new samples arrive after pause (use short time window), then Stop clears the buffer.
	- Acceptance: Test exists and fails.

## Phase 3.3: Core Implementation (ONLY after tests are failing)

- [ ] T008 [P] Implement SSE route handler (parallel)
	- Path: `src/app/api/stream/route.ts`
	- Implement a Next.js Route Handler that accepts a GET and responds with `text/event-stream`. It should hook into `src/server/simulator.ts` to forward batches as SSE messages. Include correct headers.
	- Acceptance: Route exists; a simple curl to `/api/stream` returns event-stream framing (can be smoke-tested).

- [ ] T009 [P] Implement simulator emission logic (parallel)
	- Path: `src/server/simulator.ts` (extend T002)
	- Implement start/pause/stop with an internal timer respecting `cadence` and producing `MetricSample` objects. Batch samples when cadence > 10/s.
	- Acceptance: Unit tests from T005 pass (after implementation) and `onBatch` delivers arrays matching contract.

- [ ] T010 [P] Wire UI controls to server actions (parallel)
	- Paths: `src/app/streaming/page.tsx`, `src/app/streaming/components/controls.tsx`
	- Implement client Start/Pause/Stop handlers that call route actions or open SSE and send control commands (server-side control optional; initial client-only control acceptable, but document in quickstart).
	- Acceptance: Clicking Start opens stream and UI begins receiving updates (manual smoke test).

- [ ] T011 [P] Client localStorage persistence for config (parallel)
	- Path: `src/lib/localStorage.ts` and usage in `src/app/streaming/page.tsx`
	- Persist user control settings (cadence, selected metrics, noise) and restore on load.
	- Acceptance: Settings persist across page reloads.

- [ ] T012 [P] Minimal chart rendering with throttle (parallel)
	- Path: `src/app/streaming/components/chart.tsx`
	- Implement a simple chart (e.g., canvas or lightweight lib) that can accept batch updates and applies a rendering throttle (default 10 fps). Document how to increase rendering cadence.
	- Acceptance: Chart updates visually and respects rendering throttle.

## Phase 3.4: Observability & Integration

- [ ] T013 Add structured logging in simulator (sequential after T009)
	- Path: `src/server/simulator.ts`
	- Emit structured logs (JSON) for start/pause/stop and each batch: { event, sessionId, batchSize, timestamp }
	- Acceptance: Logs are output to server console or Node logger in JSON format.

- [ ] T014 Add samplesEmittedPerSec metric (sequential after T009)
	- Path: `src/server/metrics.ts` (or append to simulator)
	- Emit metric periodically to logs for performance observation.
	- Acceptance: Metric appears in logs and can be asserted in performance tests.

## Phase 3.5: Polish & Performance

- [ ] T015 [P] Performance smoke test: validate 1000 samples/sec emit with batching (parallel)
	- Path: tests/perf/test_1000_samples_smoke.ts
	- Run a smoke test that starts simulator at high cadence and verifies server can emit batches without unbounded memory growth for a short duration.
	- Acceptance: Smoke test passes locally within machine constraints.

- [ ] T016 [P] Accessibility & ARIA checks (parallel)
	- Path: `src/app/streaming/components/controls.tsx` and `src/app/streaming/page.tsx`
	- Add ARIA labels to buttons, ensure keyboard operability, and include a short automated axe-core test in `tests/integration/test_accessibility.spec.ts`.
	- Acceptance: axe run reports no critical a11y violations.

- [ ] T017 [P] Add CSV export UI (parallel)
	- Path: `src/app/streaming/components/export.tsx`
	- Implement client-side CSV export of recent samples present in memory (download link creation).
	- Acceptance: Clicking Export downloads a CSV with header and recent samples.

## Dependencies & Ordering Notes
- Setup: T001-T003 must complete first (T002 skeleton needed by T005 test import but tests can be created earlier).  
- Testing before implementation: T004-T007 MUST be created and failing before T008-T012 are implemented.  
- Simulator implementation T009 must complete before observability tasks T013-T014 and before performance test T015.  

## Parallel Execution Examples

- Launch these independent tasks together (they do not modify the same files):
	- Group 1 (parallel): T002, T003, T004, T005
	- Group 2 (parallel): T006, T007

## Task agent command examples (what to run for each task)
- T002 example instruction for an LLM: "Create `src/server/simulator.ts` exporting a `Simulator` class with typed methods `start(config)`, `pause()`, `stop()`, `onBatch(cb)`. Include JSDoc and TypeScript types."
- T004 example instruction for an LLM: "Create `specs/001-i-would-like/contracts/stream-schema.test.ts` with a failing test that asserts the stream payload contract as specified in `contracts/stream-schema.md`."

## Validation checklist
- [ ] Each test file in Phase 3.2 exists and initially fails
- [ ] Implementation tasks reference the exact file paths above
- [ ] Observability & performance tasks included

```
