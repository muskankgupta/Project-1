# MetricMind — Production Polish TODOs

> All completed work in prior phases (backend readiness, live-data integration, chat wiring) is preserved.
> These TODO items cover the 12 production-polish phases. Databricks hostname/path restoration is PAUSED pending user-provided exact values (do NOT guess).

## Environment / Credentials
- [x] Add `GEMINI_API_KEY` to local `env` (user-provided; full value intact) — active LLM provider is Gemini
- [x] Removed `OPENAI_API_KEY` from `env` — Gemini is now the sole configured LLM provider (verified: provider=gemini, model `gemini-flash-latest`)
- [ ] Restore exact `DATABRICKS_SERVER_HOSTNAME` + `DATABRICKS_HTTP_PATH` (PAUSED — awaiting user values, do not fabricate). Current values present in `env` but hostname does NOT resolve via DNS (`gaierror [Errno 11001]` — network-level block, not a code/credential issue; `www.databricks.com` and `google.com` resolve fine from this machine)
- [ ] Re-verify live Databricks + LLM after DNS/network access to `cloud.databricks.com` is available (blocked on above)
- [x] Backend fail-fast on unreachable Databricks (`databricks_connection.py`): DNS pre-check + configurable connect/socket timeouts so `/query` & dashboard endpoints return a clean error in ~3s instead of hanging 90s+ (committed `522f05f`)

## Phase 1 — Dynamic Chatbot
- [x] Backend robustness: no-metric queries return clean 200 error message (orchestrator.py + api_router.py)
- [x] ChatPanel renders answer, SQL (expand/collapse), insights, chart metadata, explanation
- [x] Render actual chart inside chat from chart spec (not just "Recommended visual") — new `chat-chart.tsx` renders KPI/Line/Bar/Pie/Table from `response.data` via recharts
- [x] Typing animation + better loading + robust error handling
- [x] Never hardcode responses; always call `/query`

## Phase 2 — AI Insights Quality (executive level)
- [x] Frontend executive number-formatting helpers (`lib/format-indian.ts`: ₹ Lakhs/Crores)
- [x] Backend `insight_agent.py` executive narrative (₹ Cr/L compact formatting, top-contributor share)
- [x] Use LLM when configured (Gemini active via `GEMINI_API_KEY`) else deterministic templates (`llm_service.py` verified provider=gemini)
- [x] Format as business narrative (₹ Cr, top contributor share, etc.) — `_executive_summary`/`_synth_answer_headline` verified

## Phase 3 — Login System
- [x] `/login` page (professional UI)
- [x] Logout
- [x] Protected dashboard (redirect unauthenticated via `route-guard.tsx`)
- [x] Session persistence + "remember user"
- [x] Local auth only, no DB

## Phase 4 — Dark/Light/System Mode
- [x] Theme toggle (dark / light / system) via `theme-toggle.tsx`
- [x] Persist preference (`theme-provider.tsx`, localStorage + init script)
- [x] Smooth transitions (`globals.css` theme-aware variables)

## Phase 5 — Sidebar Navigation
- [x] Pages: Dashboard, Revenue, Sales, Customers, Forecast, Reports, Settings (`app-layout.tsx`)
- [x] Reusable `AppLayout` component shell + meaningful BI content per page

## Phase 6 — UI/UX Polish
- [x] Glassmorphism, spacing, hover/transition polish via shared `AppLayout` + theme CSS
- [ ] Responsive refinements for logical pages (incremental)


## Phase 7 — Dashboard Improvements
- [x] Date range filter, state filter, category filter (FilterBar component, client-side)
- [x] Search, refresh button
- [x] Refresh button (dashboard-section.tsx toolbar, wired to useDashboardData().refresh)
- [x] Export CSV (dashboard-section.tsx toolbar → shared client-side export util)
- [x] Export PDF (jsPDF professional multi-section report via lib/export.ts)
- [ ] Connect filters to backend APIs where possible

## Phase 8 — Chart Improvements
- [x] Tooltips, legends, responsive resize present in chart sections (recharts)
- [x] Animations — chat charts (KPI/Line/Bar/Pie/Table) now animate on mount via `chat-chart.tsx` (recharts `isAnimationActive`)
- [ ] Drill-down (where supported)

## Phase 9 — Settings Page
- [x] Theme, profile, API status, Databricks status, semantic layer status, LLM status, version, about

## Phase 10 — API Status Indicator
- [x] Backend / Semantic Layer / Databricks / LLM status read from backend `/health`

## Phase 11 — LLM
- [x] Confirm `GEMINI_API_KEY` provided & stored in `env` — verify backend loads it
- [x] Verify provider switches to gemini (not fallback): confirmed `LLMService().provider == "gemini"` with env loaded (model `gemini-flash-latest`)
- [x] `llm_service.py` refactored to Gemini-first: `GeminiClient` (std-lib REST, no hardcoded secrets) + `gemini` provider in `_detect_provider`/`generate`. Activates when `GEMINI_API_KEY` present; falls back to deterministic executive summary on any failure. Verified: provider=gemini with key, provider=fallback + deterministic ₹ narrative without key.
- [ ] (Blocked) Re-verify live Databricks + Gemini once Databricks hostname/path restored — warehouse at configured path was unreachable/timeout during probe (external infra, not code)

## Phase 12 — Final Verification
- [x] `npm run build` — compiled successfully, all 12 routes generated, lint + type check passed (chat-chart / chat-panel / use-chat changes verified)
- [x] `npx tsc --noEmit` — no type errors
- [ ] Run backend + frontend together (needs Databricks live creds)
- [ ] Verify login, theme, sidebar, dashboard, chat, APIs, dynamic questions, charts, filters
- [ ] Fix only actual issues

### Output
- [x] Files modified/created: `bi-dashboard/src/components/chat/chat-chart.tsx` (new), `bi-dashboard/src/hooks/use-chat.ts`, `bi-dashboard/src/components/chat-panel.tsx`, `llm_service.py` (Gemini-first refactor + fixed indentation), `TODO.md`
- [x] Commands run: `npm run lint` (passed), `npm run build` (compiled, all 12 routes, lint+types passed), Python provider verification (gemini + fallback)
- [ ] Blockers: Databricks hostname/path not yet restored (awaiting user values)
- [ ] Production-ready status: pending live Databricks verification


