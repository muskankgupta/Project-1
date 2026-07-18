"use client";

import { useEffect, useRef, useState } from "react";
import ChatInput from "./ChatInput";
import ChatMessage from "./ChatMessage";

type Message = {
id: number;
sender: "user" | "ai";
text: string;
time: string;
};

export default function ChatWindow() {
const [messages, setMessages] = useState<Message[]>([
{
id: 1,
sender: "ai",
text: `👋 Welcome to AI Business Intelligence Assistant

I'm your Enterprise Analytics Engine.

I can help you with:

📈 Revenue Analysis
📊 KPI Dashboard
👥 Customer Insights
📉 Sales Forecast
📋 Business Reports

Choose one of the suggestions below or ask your own business question.`,
time: "Now",
},
]);

const [loading, setLoading] = useState(false);

const bottomRef = useRef<HTMLDivElement>(null);

useEffect(() => {
bottomRef.current?.scrollIntoView({
behavior: "smooth",
});
}, [messages, loading]);

const getTime = () =>
new Date().toLocaleTimeString([], {
hour: "2-digit",
minute: "2-digit",
});

const getAIResponse = (question: string): string => {
const q = question.toLowerCase();

if (q.includes("revenue")) {  
  return `📊 Revenue Summary

• Total Revenue
$245,000

• Growth
+18.2%

• Best Region
North America

• Recommendation
Increase investment in digital marketing to maintain growth.`;
}

if (q.includes("kpi")) {  
  return `📈 KPI Dashboard

• KPI Health Score
96%

• Conversion Rate
8.7%

• Customer Satisfaction
94%

• Recommendation
Overall performance is excellent.`;
}

if (q.includes("customer")) {  
  return `👥 Customer Insights

• New Customers
1,240

• Returning Customers
64%

• Churn Rate
2.8%

• Recommendation
Launch loyalty campaigns.`;
}

if (q.includes("forecast")) {  
  return `📉 Sales Forecast

• Expected Growth
15%

• Confidence
92%

• Recommendation
Increase inventory for next month.`;
}

return `🤖 Thank you for your question.

This chatbot is currently running in demo mode.

It is fully prepared for Gemini/OpenAI integration to provide real-time business intelligence responses.`;
};

const handleSend = (message: string) => {
if (!message.trim()) return;

const userMessage: Message = {  
  id: Date.now(),  
  sender: "user",  
  text: message,  
  time: getTime(),  
};  

setMessages((prev) => [...prev, userMessage]);  

setLoading(true);  

setTimeout(() => {  
  const aiMessage: Message = {  
    id: Date.now() + 1,  
    sender: "ai",  
    text: getAIResponse(message),  
    time: getTime(),  
  };  

  setMessages((prev) => [...prev, aiMessage]);  

  setLoading(false);  
}, 1200);

};

const suggestedPrompts = [
"📈 Revenue Analysis",
"📊 KPI Dashboard",
"👥 Customer Insights",
"📉 Sales Forecast",
];

return (
<div className="flex h-full flex-col">
{/* Chat Area */}
<div className="flex-1 overflow-y-auto p-8 space-y-6">

{/* Suggested Prompts */}  

    <div className="grid grid-cols-2 gap-4 mb-8">  

      {suggestedPrompts.map((prompt) => (  

        <button  
          key={prompt}  
          onClick={() => handleSend(prompt)}  
          className="rounded-2xl border border-cyan-500/20 bg-slate-900 px-5 py-4 text-left shadow-lg transition-all duration-300 hover:border-cyan-400 hover:bg-slate-800 hover:scale-[1.02]"  
        >  
          <p className="font-semibold text-cyan-300">  
            {prompt}  
          </p>  

          <p className="mt-2 text-sm text-slate-400">  
            Click to instantly generate an AI business analysis.  
          </p>  

        </button>  

      ))}  

    </div>  

    {/* Chat History */}  

    {messages.map((message) => (  

      <ChatMessage  
        key={message.id}  
        message={message}  
      />  

    ))}  

    {/* AI Typing */}  

    {loading && (  

      <div className="flex justify-start">  

        <div className="rounded-3xl border border-cyan-500/20 bg-slate-800 px-6 py-5 shadow-xl">  

          <div className="flex items-center gap-3">  

            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-r from-cyan-500 to-blue-600">  

              🤖  

            </div>  

            <div>  

              <p className="font-semibold text-cyan-300">  
                AI Business Intelligence Assistant  
              </p>  

              <p className="text-sm text-slate-400">  
                Enterprise Analytics Engine  
              </p>  

            </div>  

          </div>  

          <div className="mt-5 flex items-center gap-2">  

            <div className="h-2 w-2 rounded-full bg-cyan-400 animate-bounce"></div>  

            <div className="h-2 w-2 rounded-full bg-cyan-400 animate-bounce [animation-delay:0.2s]"></div>  

            <div className="h-2 w-2 rounded-full bg-cyan-400 animate-bounce [animation-delay:0.4s]"></div>  

            <span className="ml-3 text-slate-400">  
              Analyzing business metrics...  
            </span>  

          </div>  

        </div>  

      </div>  

    )}  

    <div ref={bottomRef} />  

  </div>  

  {/* Input */}  

  <ChatInput  
    onSend={handleSend}  
    loading={loading}  
  />  

</div>

);
}