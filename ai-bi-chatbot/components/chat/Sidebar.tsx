"use client";

import { useMemo, useState } from "react";

type Chat = {
id: number;
title: string;
group: "Today" | "Yesterday";
};

const initialChats: Chat[] = [
{ id: 1, title: "Revenue Dashboard", group: "Today" },
{ id: 2, title: "Sales Performance", group: "Today" },
{ id: 3, title: "Customer Insights", group: "Today" },
{ id: 4, title: "KPI Analytics", group: "Yesterday" },
{ id: 5, title: "Forecast Report", group: "Yesterday" },
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
title: "+ New Conversations",
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

<aside className="w-80 bg-[#0b1220] border-r border-slate-800 flex flex-col">    <div className="p-6 border-b border-slate-800">  <div className="flex items-center gap-3">        <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center text-white text-xl">      
    📊      
  </div>        <div>      
    <h1 className="text-xl font-bold text-white">      
      MetricMind      
    </h1>      <p className="text-xs text-slate-400">      
  Business Intelligence      
</p>

  </div>      </div>      </div>    <div className="p-5">  <button      
  onClick={createChat}      
  className="w-full rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 py-3 text-white font-semibold shadow-xl hover:shadow-cyan-500/40 transition-all duration-300 hover:-translate-y-1"      
>      
  + New Chat      
</button>      </div>    <div className="px-5">  <input      
  value={search}      
  onChange={(e) => setSearch(e.target.value)}      
  placeholder="Search..."      
  className="w-full rounded-xl bg-slate-900 border border-slate-700 px-4 py-3 text-white focus:border-cyan-500 outline-none"      
/>      </div>      
<div className="flex-1 overflow-y-auto px-5 py-6">    <p className="text-xs uppercase tracking-widest text-slate-500 mb-4">      
    Recent Conversations      
  </p>    <div className="space-y-3">  {filteredChats.map((chat) => (        <div      
    key={chat.id}      
    onClick={() => setActiveChat(chat.id)}      
    className={`cursor-pointer rounded-2xl p-4 transition-all duration-300 ${      
      activeChat === chat.id      
        ? "bg-cyan-500/15 border border-cyan-500 shadow-lg shadow-cyan-500/20"      
        : "bg-slate-900 border border-slate-800 hover:border-cyan-400 hover:bg-slate-800"      
    }`}      
  >      <div className="flex justify-between items-center">      

  <div>      

    <p className="text-white font-semibold">      
      {chat.title}      
    </p>      

    <p className="text-xs text-slate-400 mt-1">      
      {chat.group}      
    </p>      

  </div>      

  <button      
    onClick={(e) => {      
      e.stopPropagation();      
      deleteChat(chat.id);      
    }}      
    className="text-red-400 hover:text-red-500"      
  >      
    ✕      
  </button>      

</div>

  </div>      ))}

  </div>  </div>      
<div className="border-t border-slate-800 p-5">    <div className="rounded-2xl bg-slate-900 border border-slate-800 p-4">  <div className="flex items-center gap-3">        <div className="h-14 w-14 rounded-full bg-gradient-to-r from-cyan-500 to-blue-600 flex items-center justify-center text-white font-bold text-xl">      
    V      
  </div>        <div>      <h3 className="text-white font-semibold">      
  Vaishnavi      
</h3>      

<p className="text-sm text-slate-400">      
  Business Intelligence    
</p>      

<div className="flex items-center gap-2 mt-2">      

  <div className="w-2 h-2 rounded-full bg-green-500"></div>      

  <span className="text-xs text-green-400">      
    Active      
  </span>      

</div>

  </div>      </div>    

  </div>  </div>  </aside>      
  );      
}