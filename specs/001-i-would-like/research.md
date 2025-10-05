```markdown
# Phase 0 Research: Data Streaming Simulator

Decisions and rationale:

- Protocol choice: Server-Sent Events (SSE) for initial implementation.
  - Rationale: SSE is simple to implement as a Next.js route handler, supports
    unidirectional streaming from server to browser, and is easier to reason about
    for early prototypes. If bi-directional low-latency control is later required,
    we can migrate to WebSockets.

- Simulator pattern: Single in-memory SimulationSession per active dashboard instance.
  - Rationale: avoids persistence complexity; meets ephemeral simulation requirement.
  - Implementation: `src/server/simulator.ts` exposes start/stop/pause and emits
    batches of MetricSample objects to SSE clients.

- Performance approach:
  - Emit at requested cadence but batch samples into small arrays for network
    efficiency when cadence > 10/s.
  - Provide per-sample timestamps and batch metadata (batchStart, batchSize).
  - Implement server backpressure: when outgoing queue exceeds threshold, apply
    sampling or drop policy documented in research.

- Client rendering:
  - Default rendering throttle: 10 updates/sec for charts; UI provides option
    to increase if user accepts reduced responsiveness or uses downsampling.
  - Use an efficient charting library or manual canvas rendering for higher
    cadences.

- Observability:
  - Emit structured logs for actions: start/pause/stop, errors, and sample batch
    statistics (size, min/max timestamps).
  - Expose an internal metric: samplesEmittedPerSec for monitoring in dev.

Open questions left for planning (not blocking):
- Export/persistence: implement CSV export on client on demand (preferred) vs
  server-side export (requires storage). Default: client-side export only.

```
