"use client"

import React, { useState } from 'react'
import styles from './styles.module.css'

export default function StreamingPage() {
  const [status, setStatus] = useState<'stopped'|'running'|'paused'>('stopped')

  return (
    <main className={styles.root}>
      <h1>Data Streaming Simulator</h1>

      <section aria-label="controls" className={styles.controls}>
        <button
          aria-label="Start simulation"
          onClick={() => setStatus('running')}
          className={styles.button}
        >
          Start
        </button>
        <button
          aria-label="Pause simulation"
          onClick={() => setStatus('paused')}
          className={styles.button}
        >
          Pause
        </button>
        <button
          aria-label="Stop simulation"
          onClick={() => setStatus('stopped')}
          className={styles.button}
        >
          Stop
        </button>
        <span className={styles.status}>Status: <strong>{status}</strong></span>
      </section>

      <section aria-label="chart" className={styles.chart}>
        <div id="chart-container" className={styles.chartContainer}>
          {/* Empty chart area — chart will be rendered here in later tasks */}
        </div>
        <div className={styles.hint}>No data yet. Start the simulation to stream values.</div>
      </section>
    </main>
  )
}
