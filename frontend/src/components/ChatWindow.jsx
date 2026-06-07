import { useEffect, useRef } from "react"
import { Cloud } from "lucide-react"
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
      <div className="flex-1 flex flex-col items-center justify-center p-8 text-center animate-in fade-in duration-700">
        <div className="w-16 h-16 bg-accent/20 rounded-2xl flex items-center justify-center mb-6 shadow-sm border border-border/50">
          <Cloud className="w-8 h-8 text-[#FF9900]" />
        </div>
        <h2 className="text-2xl font-semibold mb-2">Welcome to AWSense</h2>
        <p className="text-muted-foreground max-w-md">
          Ask any question about AWS architecture, services, or documentation. 
          I'll search the official AWS docs to find the answer.
        </p>
      </div>
    )
  }

  return (
    <ScrollArea className="flex-1 p-4 sm:p-6" ref={scrollRef}>
      <div className="max-w-4xl mx-auto flex flex-col">
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
            <div className="max-w-[85%] rounded-2xl px-5 py-4 bg-transparent border border-border shadow-sm flex items-center gap-2 text-muted-foreground">
              <span className="flex h-2 w-2 rounded-full bg-muted-foreground/50 animate-bounce" style={{ animationDelay: '0ms' }} />
              <span className="flex h-2 w-2 rounded-full bg-muted-foreground/50 animate-bounce" style={{ animationDelay: '150ms' }} />
              <span className="flex h-2 w-2 rounded-full bg-muted-foreground/50 animate-bounce" style={{ animationDelay: '300ms' }} />
            </div>
          </div>
        )}
      </div>
    </ScrollArea>
  )
}
