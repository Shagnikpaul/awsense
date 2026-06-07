import { cn } from "@/lib/utils"
import { Sparkles, User } from "lucide-react"
import { SourceCitations } from "./SourceCitations"
import { TokenUsage } from "./TokenUsage"

export function MessageBubble({ role, content, sources, tokenUsage }) {
  const isUser = role === 'user';
  
  // Use current time for timestamp since it's not provided
  const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  return (
    <div className={cn("flex w-full mb-6", isUser ? "justify-end" : "justify-start")}>
      <div className={cn("flex items-end gap-2", isUser ? "flex-row-reverse max-w-[70%]" : "flex-row max-w-[85%]")}>
        
        {/* Avatar */}
        <div className={cn(
          "w-7 h-7 shrink-0 rounded-full flex items-center justify-center",
          isUser ? "bg-dg-accent" : "bg-dg-elevated border border-dg-border"
        )}>
          {isUser ? (
            <User className="w-4 h-4 text-white" />
          ) : (
            <Sparkles className="w-3.5 h-3.5 text-dg-textMuted" />
          )}
        </div>

        {/* Bubble contents */}
        <div className="flex flex-col gap-1 min-w-0">
          <div 
            className={cn(
              "rounded-squircle px-5 py-4 text-sm leading-relaxed font-inter overflow-hidden",
              isUser 
                ? "bg-dg-accent text-white" 
                : "bg-dg-surface text-dg-textPrimary"
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
          <span className={cn(
            "text-dg-textMuted text-xs font-inter px-2",
            isUser ? "text-right" : "text-left"
          )}>
            {time}
          </span>
        </div>
      </div>
    </div>
  )
}
