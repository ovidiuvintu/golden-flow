```markdown
# Data Model

## Entities

- SimulationSession
  - id: string (UUID)
  - status: enum {running, paused, stopped}
  - config: object {
    cadence: number (samples/sec),
    metrics: { name: string, mean: number, noiseStd: number, unit: string }[],
    batchSize?: number
  }
  - startedAt?: ISO timestamp
  - stoppedAt?: ISO timestamp

- MetricSample
  - timestamp: ISO timestamp
  - metricName: string
  - value: number
  - unit: string

- ControlCommand
  - command: string (start|pause|stop|update-config)
  - parameters?: object
  - issuedAt: ISO timestamp

## Data Flows
- Simulator produces MetricSample objects and sends them via SSE batches to the
  client. Each SSE message may contain an array of MetricSample objects plus
  metadata (sessionId, batchStart, batchSize).

## Identity & Uniqueness
- SimulationSession.id is a UUID. MetricSample entries are not persisted server-side
  by default; uniqueness is not enforced beyond timestamp+metricName in a batch.

```
