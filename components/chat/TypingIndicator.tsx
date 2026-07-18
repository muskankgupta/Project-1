export default function TypingIndicator() {
  return (
    <div className="flex justify-start animate-fade-in">

      <div className="rounded-3xl border border-slate-700 bg-slate-800/90 backdrop-blur-xl px-6 py-4 shadow-lg">

        <div className="flex items-center gap-2">

          <div className="h-2 w-2 rounded-full bg-cyan-400 animate-bounce"></div>

          <div
            className="h-2 w-2 rounded-full bg-cyan-400 animate-bounce"
            style={{ animationDelay: "0.2s" }}
          ></div>

          <div
            className="h-2 w-2 rounded-full bg-cyan-400 animate-bounce"
            style={{ animationDelay: "0.4s" }}
          ></div>

          <span className="ml-3 text-sm text-slate-400">
            AI is thinking...
          </span>

        </div>

      </div>

    </div>
  );
}