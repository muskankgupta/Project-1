export type ChatMessage = {
  id: number;
  sender: "user" | "assistant";
  text: string;
  time: string;
};