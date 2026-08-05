"use client";

type Message = {
  id: number;
  sender: "user" | "ai";
  text: string;
  time: string;
};

type Props = {
  message: Message;
};

export default function ChatMessage({ message }: Props) {
  const isUser = message.sender === "user";

  const copyMessage = async () => {
    await navigator.clipboard.writeText(message.text);
  };

  return (
    <div
      className={`flex ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      <div
        className={`max-w-3xl rounded-3xl px-6 py-5 shadow-2xl ${
          isUser
            ? "bg-gradient-to-r from-cyan-500 to-blue-600 text-white"
            : "bg-slate-800 border border-cyan-500/20 text-slate-200"
        }`}
      >
        <div className="flex items-center gap-3 mb-3">

          <div className="w-10 h-10 rounded-full bg-gradient-to-r from-cyan-500 to-blue-600 flex items-center justify-center">

            {isUser ? "👤" : "🤖"}

          </div>

          <div>

            <p className="font-bold">
              {isUser ? "You" : "AI Assistant"}
            </p>

            <p className="text-xs opacity-70">
              {message.time}
            </p>

          </div>

        </div>

        <p className="leading-8">
          {message.text}
        </p>

        {!isUser && (

          <div className="flex gap-3 mt-5">

            <button className="rounded-lg bg-slate-700 px-3 py-2 hover:bg-slate-600 transition">
              👍
            </button>

            <button className="rounded-lg bg-slate-700 px-3 py-2 hover:bg-slate-600 transition">
              👎
            </button>

            <button
              onClick={copyMessage}
              className="rounded-lg bg-slate-700 px-3 py-2 hover:bg-slate-600 transition"
            >
              📋 Copy
            </button>

            <button className="rounded-lg bg-slate-700 px-3 py-2 hover:bg-slate-600 transition">
              🔄 Retry
            </button>

          </div>

        )}

      </div>

    </div>
  );
}