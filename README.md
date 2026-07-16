# MetricMind – AI Business Intelligence Dashboard

## Project Overview

MetricMind is a modern enterprise business intelligence dashboard built with Next.js, TypeScript, Tailwind CSS, shadcn/ui-style components, and Recharts. The current foundation focuses on a dark glassmorphism visual system, a reusable dashboard shell, and responsive layout regions for analytics and future AI insights.

## Features Implemented So Far

- Dark enterprise-grade theme with layered glassmorphism surfaces
- Reusable dashboard shell with left sidebar, top navigation, analytics canvas, and right AI insights reserve panel
- Search, notifications, theme toggle, and user profile entry points in the top bar
- KPI cards, revenue trend chart, sales channel chart, and operational summary blocks
- Responsive layout designed to scale from large desktop screens down to mobile widths

## Tech Stack

- Next.js
- TypeScript
- Tailwind CSS
- Recharts
- shadcn/ui

## Folder Structure

```text
bi-dashboard/
├─ src/
│  ├─ app/
│  │  ├─ globals.css
│  │  ├─ layout.tsx
│  │  └─ page.tsx
│  ├─ components/
│  │  ├─ dashboard-shell.tsx
│  │  └─ ui/
│  │     ├─ avatar.tsx
│  │     ├─ badge.tsx
│  │     ├─ button.tsx
│  │     ├─ card.tsx
│  │     └─ input.tsx
│  └─ lib/
│     └─ utils.ts
├─ public/
├─ package.json
└─ README.md
```

## Setup Instructions

1. Install dependencies:

```bash
npm install
```

2. Run the development server:

```bash
npm run dev
```

3. Open the app in your browser:

```text
http://localhost:3000
```

4. Create a production build:

```bash
npm run build
```

## Future Roadmap

- Make the theme toggle fully interactive
- Add collapsible mobile sidebar behavior
- Wire the AI insights panel to live model outputs
- Add filtering, drill-downs, and date range controls
- Expand reporting views and export actions
- Connect the dashboard to a live analytics backend
