# Modwire API Browser

React 19, strict TypeScript, Vite, Material UI, and Vitest.

```sh
npm install
npm run dev
```

Quality checks:

```sh
npm run typecheck
npm run test
npm run build
```

The browser can be exercised without Django or the database. Playwright starts
Vite and replaces the Siren API with deterministic in-browser responses:

```sh
npx playwright install chromium
npm run test:e2e
```

Copy `.env.example` to `.env.local` when the API URL differs from the default.
