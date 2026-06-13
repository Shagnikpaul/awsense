import { useState, useRef, useEffect } from "react";
import { ArrowUp } from "lucide-react";
import { Button } from "@/components/ui/button";
import { TopicFilter } from "./TopicFilter";

export function InputBar({
  onSendMessage,
  isLoading,
  topicFilter,
  setTopicFilter,
}) {
  const [input, setInput] = useState("");
  const textareaRef = useRef(null);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 120)}px`;
    }
  }, [input]);

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleSend = () => {
    if (!input.trim() || isLoading) return;
    onSendMessage(input);
    setInput("");
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
    }
  };

  // Parse elevated color (assuming #2c261e dark mode or similar)
  // Tailwind doesn't easily let us use CSS variables with opacity unless defined as rgb/hsl channels.
  // We'll use a style object for the custom glassmorphism background and shadow.

  return (
    <div className="absolute bottom-0 left-0 right-0 z-20 px-4 pb-4">
      <div
        className="max-w-4xl mx-auto w-full backdrop-blur-console p-4 flex flex-col gap-2"
        style={{
          background:
            "color-mix(in srgb, var(--dg-bg-elevated) 85%, transparent)",
          border: "1px solid var(--dg-border-glow)",
          borderTopLeftRadius: "22px",
          borderTopRightRadius: "22px",
          borderBottomLeftRadius: "22px",
          borderBottomRightRadius: "22px",
          boxShadow: "0 -8px 32px rgba(0,0,0,0.4)",
        }}
      >
        <div className="relative flex flex-col">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask anything about AWS architecture, services, or best practices..."
            className="w-full min-h-[52px] max-h-[120px] resize-none bg-transparent border-none text-dg-textPrimary font-inter text-sm focus-visible:outline-none placeholder:text-dg-textMuted pt-2 pb-6"
            rows={1}
            disabled={isLoading}
            maxLength={500}
          />
          <div
            className={`absolute bottom-0 right-1 text-xs pointer-events-none ${input.length >= 500 ? "text-red-500 font-medium" : "text-dg-textMuted/70"}`}
          >
            {input.length} / 500
          </div>
        </div>

        <div className="flex flex-row justify-between items-center mt-2">
          <TopicFilter
            topicFilter={topicFilter}
            setTopicFilter={setTopicFilter}
          />

          <Button
            onClick={handleSend}
            disabled={!input.trim() || isLoading}
            className="bg-dg-accent hover:bg-dg-warm rounded-pill px-5 py-2 flex items-center gap-2 h-auto disabled:opacity-40 disabled:cursor-not-allowed text-white font-syne font-semibold text-sm"
          >
            <span>Send</span>
            <ArrowUp className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  );
}
