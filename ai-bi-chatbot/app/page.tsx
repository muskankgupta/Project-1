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
        <header className="sticky top-0 z-50 border-b border-slate-800 bg-slate-950/80 backdrop-blur-xl">

          <div className="flex items-center justify-between px-8 py-5">

            <div>
              <h1 className="text-3xl font-bold text-cyan-400">
                AI Business Intelligence
              </h1>

              <p className="text-slate-400 mt-1">
                Enterprise Analytics Assistant
              </p>
            </div>

            <div className="flex items-center gap-3">
              <div className="h-3 w-3 rounded-full bg-green-500 animate-pulse"></div>

              <span className="text-slate-300 font-medium">
                AI Online
              </span>
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