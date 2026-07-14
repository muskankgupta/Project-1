import { useState } from "react";

export default function App() {
  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");

  const sendQuery = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: input }),
      });

      const data = await res.json();
      setResponse(data.answer);
    } catch (err) {
      setResponse("Error connecting to backend");
    }
  };

  return (
    <div>
      <h1>MetricMind</h1>
      <input value={input} onChange={(e) => setInput(e.target.value)} />
      <button onClick={sendQuery}>Ask</button>
      <p>{response}</p>
    </div>
  );
}
