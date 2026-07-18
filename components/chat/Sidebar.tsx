"use client";

import { useMemo, useState } from "react";

type Chat = {
  id: number;
  title: string;
  group: "Today" | "Yesterday";
};

const initialChats: Chat[] = [
  { id: 1, title: "Revenue Report", group: "Today" },
  { id: 2, title: "Sales Analysis", group: "Today" },
  { id: 3, title: "Customer Insights", group: "Today" },
  { id: 4, title: "KPI Review", group: "Yesterday" },
  { id: 5, title: "Monthly Forecast", group: "Yesterday" },
];

export default function Sidebar() {
  const [search, setSearch] = useState("");
  const [activeChat, setActiveChat] = useState(1);
  const [chats, setChats] = useState(initialChats);

  const filteredChats = useMemo(() => {
    return chats.filter((chat) =>
      chat.title.toLowerCase().includes(search.toLowerCase())
    );
  }, [search, chats]);

  const createChat = () => {
    const newChat: Chat = {
      id: Date.now(),
      title: "New Conversation",
      group: "Today",
    };

    setChats([newChat, ...chats]);
    setActiveChat(newChat.id);
  };

  const deleteChat = (id: number) => {
    setChats((prev) => prev.filter((chat) => chat.id !== id));

    if (activeChat === id && chats.length > 1) {
      const next = chats.find((c) => c.id !== id);
      if (next) setActiveChat(next.id);
    }
  };

  return (
    <aside className="w-80 border-r border-slate-800 bg-slate-950 flex flex-col">

      {/* Logo */}

      <div className="border-b border-slate-800 p-6">

        <h1 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
          AI BI Assistant
        </h1>

        <p className="text-slate-500 text-sm mt-1">
          Enterprise Intelligence
        </p>

      </div>

      {/* New Chat */}

      <div className="p-5">

        <button
          onClick={createChat}
          className="w-full rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 py-3 text-white font-semibold shadow-lg hover:scale-[1.02] transition"
        >
          ✨ New Chat
        </button>

      </div>

      {/* Search */}

      <div className="px-5">

        <input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="🔍 Search chats..."
          className="w-full rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 text-white outline-none focus:border-cyan-500"
        />

      </div>

      {/* Chat History */}

      <div className="flex-1 overflow-y-auto px-5 py-6">

        <p className="text-xs uppercase tracking-widest text-slate-500 mb-4">
          Conversations
        </p>

        <div className="space-y-3">

          {filteredChats.map((chat) => (

            <div
              key={chat.id}
              onClick={() => setActiveChat(chat.id)}
              className={`group cursor-pointer rounded-2xl border p-4 transition-all duration-300 ${
                activeChat === chat.id
                  ? "border-cyan-500 bg-cyan-500/10"
                  : "border-slate-800 bg-slate-900 hover:bg-slate-800"
              }`}
            >

              <div className="flex justify-between items-start">

                <div>

                  <p className="font-medium text-white">
                    💬 {chat.title}
                  </p>

                  <p className="mt-2 text-xs text-slate-500">
                    {chat.group}
                  </p>

                </div>

                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    deleteChat(chat.id);
                  }}
                  className="opacity-0 group-hover:opacity-100 text-red-400 transition"
                >
                  🗑
                </button>

              </div>

            </div>

          ))}

        </div>

      </div>

      {/* Profile */}

      <div className="border-t border-slate-800 p-5">

        <div className="flex items-center gap-3">

          <div className="h-12 w-12 rounded-full bg-gradient-to-r from-cyan-500 to-blue-600 flex items-center justify-center text-white font-bold">
            V
          </div>

          <div>

            <p className="font-semibold text-white">
              Vaishnavi
            </p>

            <div className="flex items-center gap-2 mt-1">

              <div className="h-2 w-2 rounded-full bg-green-500"></div>

              <span className="text-xs text-slate-400">
                Online
              </span>

            </div>

          </div>

        </div>

      </div>

    </aside>
  );
}