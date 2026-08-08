"use client";

import Sidebar from "../components/chat/Sidebar";
import ChatWindow from "../components/chat/ChatWindow";

export default function Home() {
  return (
    <main className="h-screen bg-slate-950 text-white flex">

      {/* Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <div className="flex-1 flex flex-col">

        {/* Header */}
        <header className="sticky top-0 z-50 border-b border-blue-700 bg-blue-600 backdrop-blur-md">
  <div className="flex items-center justify-between px-8 py-2">

    <div>
      <p className="text-xs uppercase tracking-[0.3em] text-slate-500">
        Enterprise Command Center
      </p>

      <h1 className="mt-1 text-3xl font-bold text-white">
        BI Dashboard Overview
      </h1>
    </div>

    <div className="flex items-center gap-4">

      <input
        placeholder="Search revenue, accounts, reports..."
        className="w-80 rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 text-white outline-none focus:border-cyan-500"
      />

      <button className="rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 text-slate-300 hover:border-cyan-500">
        🔔
      </button>

      <button className="rounded-xl bg-slate-900 px-4 py-3 text-white">
        🌙 Dark Mode
      </button>

      <div className="flex items-center gap-3 rounded-xl bg-slate-900 px-4 py-2">
        <div className="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-bold">
          V
        </div>

        <div>
          <p className="text-sm font-semibold text-white">
            Vaishnavi
          </p>
          <p className="text-xs text-slate-400">
            BI Developer
          </p>
        </div>
      </div>

    </div>

  </div>
</header>

        {/* Chat */}
        <div className="flex-1 overflow-hidden">
          <ChatWindow />
        </div>

      </div>

    </main>
  );
}