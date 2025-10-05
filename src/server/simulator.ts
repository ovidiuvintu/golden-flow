export type MetricConfig = {
  name: string
  mean: number
  noiseStd: number
  unit: string
}

export type SimulatorConfig = {
  cadence: number // samples per second
  metrics: MetricConfig[]
  batchSize?: number
}

export type MetricSample = {
  timestamp: string
  metricName: string
  value: number
  unit: string
}

export type Batch = {
  sessionId: string
  batchStart: string
  batchSize: number
  samples: MetricSample[]
}

export class Simulator {
  private config?: SimulatorConfig
  private running = false
  private paused = false
  private callbacks: ((b: Batch) => void)[] = []

  start(config: SimulatorConfig) {
    this.config = config
    this.running = true
    this.paused = false
    // emission loop to be implemented in T009
  }

  pause() {
    if (!this.running) return
    this.paused = true
  }

  stop() {
    this.running = false
    this.paused = false
  }

  onBatch(cb: (b: Batch) => void) {
    this.callbacks.push(cb)
  }

  // helper to invoke callbacks when batches are ready
  protected _emitBatch(batch: Batch) {
    for (const cb of this.callbacks) cb(batch)
  }
}

export default Simulator
