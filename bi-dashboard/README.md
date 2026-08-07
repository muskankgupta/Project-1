# MetricMind – AI Business Intelligence Dashboard

## Project Overview

MetricMind is an enterprise business intelligence dashboard built with Next.js, TypeScript, Tailwind CSS, shadcn/ui-style components, and Recharts. It provides a dark glassmorphism visual system over a live analytics backend.

The dashboard connects to the **MetricMind FastAPI backend** (see the repository root) which exposes:

- `POST /query` — Natural-language → SQL answer with insights, chart suggestion, and explanation
- `POST /dashboard/kpis` — Core KPIs (revenue, orders, units, AOV)
- `POST /dashboard/trends` — Revenue/Order + AOV monthly trends
- `POST /dashboard/top-states` — Top states by revenue
- `POST /dashboard/rankings` — Best/worst performing categories
- `POST /dashboard/impact` — Order-status impact analysis
- `GET /health` — Backend health check

## Features

- Dark enterprise-grade theme with layered glassmorphism surfaces
- Reusable dashboard shell with left sidebar, top navigation, and analytics canvas
- **Live backend integration** — all dashboard sections fetch from the MetricMind API in parallel
- **Graceful mock fallback** — when the backend is unreachable, bundled sample data is shown with a "Sample data" badge
- **AI Insights strip** — surfaces `insights` and `explanation` returned by the live API
- **AI Chat panel** — floating assistant that calls `POST /query` for natural-language questions (with SQL + chart suggestion + insights)
- **INR formatting** — currency helpers default to `en-IN` / `INR` (dataset is Amazon.in)
- KPI cards, revenue/order trend chart, AOV trend, top states, category rankings, and order-status impact sections
- Responsive layout from large desktop screens down to mobile widths

## Tech Stack

- Next.js 15 (App Router)
- React 19
- TypeScript
- Tailwind CSS v4
- Recharts
- lucide-react
- Radix UI primitives (shadcn/ui style)

## Folder Structure

```text
bi-dashboard/
├─ src/
│  ├─ app/
│  │  ├─ globals.css
│  │  ├─ layout.tsx
│  │  └─ page.tsx
│  ├─ components/
│  │  ├─ dashboard-shell.tsx      # Layout + data source badge + AI insights + chat FAB
│  │  ├─ chat-panel.tsx           # Floating AI chat UI
│  │  ├─ dashboard/               # Section components (KPIs, trends, states, rankings, impact, AOV)
│  │  └─ ui/                      # shadcn-style UI primitives
│  ├─ hooks/
│  │  ├─ use-dashboard-data.ts    # Dashboard data loading hook
│  │  └─ use-chat.ts              # Chat message state/flow
│  ├─ lib/
│  │  ├─ api-config.ts            # API base URL + endpoint constants
│  │  ├─ api-client.ts            # Typed fetch helper
│  │  ├─ dashboard-format.ts      # INR/percentage formatters
│  │  └─ utils.ts
│  ├─ services/
│  │  ├─ dashboard-data.service.ts # Parallel API calls + mock fallback
│  │  └─ query.service.ts         # POST /query for the chat assistant
│  ├─ types/
│  │  ├─ dashboard.ts             # Dashboard data types
│  │  └─ query.ts                 # QueryResponse types (mirrors backend)
│  └─ mock-data/                  # Bundled fallback datasets
├─ public/
├─ .env.local                     # NEXT_PUBLIC_API_BASE_URL
├─ package.json
└─ README.md
```

## Setup Instructions

1. Install dependencies:

```bash
npm install
```

2. Configure the backend URL:

Create `.env.local` in the dashboard folder:

```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

> The value defaults to `http://localhost:8000` when unset.

3. Start the MetricMind backend (from the repository root):

```bash
uvicorn main:app --reload --port 8000
```

4. Run the development server:

```bash
npm run dev
```

5. Open the app:

```text
http://localhost:3000
```

6. Create a production build:

```bash
npm run build
```

## Data Source Behavior

The dashboard prefers live data from the backend:

- When all five dashboard endpoints respond successfully, the UI shows a **"Live data"** badge and renders AI-generated insights/explanation.
- If the backend is unreachable or any section errors, the service falls back to bundled mock JSON and shows a **"Sample data"** badge.

The chat panel always calls the live `POST /query` endpoint. If the backend is offline it displays a structured offline error message.

## Future Roadmap

- Make the theme toggle fully interactive
- Add collapsible mobile sidebar behavior
- Add filtering, drill-downs, and date range controls to chart sections
- Expand reporting views and export actions
- Add per-question chart rendering in the chat panel based on the chart suggestion

