import { cn } from "@/lib/utils"
import { SourceCitations } from "./SourceCitations"
import { TokenUsage } from "./TokenUsage"

export function MessageBubble({ role, content, sources, tokenUsage }) {
  const isUser = role === 'user';

  return (
    <div className={cn("flex w-full mb-6", isUser ? "justify-end" : "justify-start")}>
      <div 
        className={cn(
          "max-w-[85%] rounded-2xl px-5 py-4 text-sm leading-relaxed",
          isUser 
            ? "bg-secondary text-secondary-foreground" 
            : "bg-transparent border border-border shadow-sm text-foreground"
        )}
      >
        <div className="whitespace-pre-wrap">{content}</div>
        
        {!isUser && (
          <>
            <SourceCitations sources={sources} />
            <TokenUsage tokenUsage={tokenUsage} />
          </>
        )}
      </div>
    </div>
  )
}
