```markdown
# Quickstart

1. Clone the repository and install dependencies in the project root (use the `src` package if applicable):

   npm install --prefix src

2. Start the Next.js dev server (from repo root):

   npm --prefix src run dev

3. Open http://localhost:3000/streaming (example route) to view the simulator
   dashboard. Use the Start / Pause / Stop controls to operate the simulation.

4. To run tests:

   - Unit tests: run test runner configured in `src` (e.g., `npm --prefix src run test`)
   - Integration tests (Playwright): `npx playwright test`

Notes:
- Simulation data is ephemeral by default. Use the dashboard Export button to
  download recent samples as CSV if you need persistence.

```
