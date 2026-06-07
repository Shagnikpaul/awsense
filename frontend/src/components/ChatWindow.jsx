import { useEffect, useRef } from "react"
import { Sparkles } from "lucide-react"
import { ScrollArea } from "@/components/ui/scroll-area"
import { MessageBubble } from "./MessageBubble"

export function ChatWindow({ messages, isLoading }) {
  const scrollRef = useRef(null)

  useEffect(() => {
    if (scrollRef.current) {
      const scrollContainer = scrollRef.current.querySelector('[data-radix-scroll-area-viewport]')
      if (scrollContainer) {
        scrollContainer.scrollTop = scrollContainer.scrollHeight
      }
    }
  }, [messages, isLoading])

  if (messages.length === 0) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center p-8 text-center animate-in fade-in duration-700 bg-dg-base pb-48">
        <div className="w-12 h-1 bg-dg-accent rounded-full mb-6 opacity-80"></div>
        <h2 className="font-syne font-bold text-3xl text-dg-textPrimary mb-3">Welcome to AWSense</h2>
        <p className="font-inter text-dg-textSecondary text-sm max-w-sm text-center">
          Your intelligent AWS documentation assistant. Ask anything about EC2, S3, IAM, Lambda, VPC, and more.
        </p>
      </div>
    )
  }

  return (
    <ScrollArea className="flex-1 p-4 sm:p-6 bg-dg-base" ref={scrollRef}>
      <div className="max-w-4xl mx-auto flex flex-col pb-48">
        {messages.map((msg) => (
          <MessageBubble
            key={msg.id}
            role={msg.role}
            content={msg.content}
            sources={msg.sources}
            tokenUsage={msg.tokenUsage}
          />
        ))}
        
        {isLoading && (
          <div className="flex w-full mb-6 justify-start">
            <div className="flex items-end gap-2 max-w-[85%]">
              <div className="w-7 h-7 shrink-0 rounded-full bg-dg-elevated border border-dg-border flex items-center justify-center">
                <Sparkles className="w-3.5 h-3.5 text-dg-textMuted" />
              </div>
              <div className="rounded-squircle px-5 py-4 bg-dg-surface text-dg-textPrimary flex items-center gap-1.5 h-[52px]">
                <span className="flex h-2 w-2 rounded-full bg-dg-accent animate-bounce" style={{ animationDelay: '0ms' }} />
                <span className="flex h-2 w-2 rounded-full bg-dg-accent animate-bounce" style={{ animationDelay: '150ms' }} />
                <span className="flex h-2 w-2 rounded-full bg-dg-accent animate-bounce" style={{ animationDelay: '300ms' }} />
              </div>
            </div>
          </div>
        )}
      </div>
    </ScrollArea>
  )
}
