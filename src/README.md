# Product Source Code Directory (`src/`)

This directory contains the primary product application source code for the active project.

## Structure & Architecture
- `index.ts`: Production HTTP baseline microservice featuring health check probes (`/health`, `/api/health`, `/api/info`) and a built-in security shield against path traversal attacks.
- Domain modules, controllers, business logic services, and models should be organized cleanly under `src/`.

## Running the Service
```bash
npm start
```
By default, the service starts on port `3000` (or `PORT` environment variable).
