```markdown
# Stream Contract: MetricSample Batch Schema

Each SSE message emits a JSON payload with the following structure (application/json):

```json
{
  "sessionId": "<uuid>",
  "batchStart": "2025-10-05T12:00:00.000Z",
  "batchSize": 10,
  "samples": [
    { "timestamp": "2025-10-05T12:00:00.000Z", "metricName": "volume", "value": 12.34, "unit": "L" }
  ]
}
```

Contract tests MUST validate:
- `sessionId` present and UUID-like
- `batchSize` equals `samples.length`
- Each sample has `timestamp`, `metricName`, `value` (number), and `unit` (string)

Versioning: If this contract changes, update the stream endpoint path to contain
versioning (e.g., `/api/v1/stream`) and include a migration note in the contract.

```
