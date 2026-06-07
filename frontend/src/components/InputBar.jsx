import { useState, useRef, useEffect } from "react"
import { Send } from "lucide-react"
import { Button } from "@/components/ui/button"
import { TopicFilter } from "./TopicFilter"

export function InputBar({ onSendMessage, isLoading, topicFilter, setTopicFilter }) {
  const [input, setInput] = useState("")
  const textareaRef = useRef(null)

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto"
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`
    }
  }, [input])

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const handleSend = () => {
    if (!input.trim() || isLoading) return
    onSendMessage(input)
    setInput("")
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto"
    }
  }

  return (
    <div className="bg-background border-t p-4 sm:p-6 w-full max-w-4xl mx-auto flex flex-col gap-3">
      <div className="flex items-end gap-2">
        <TopicFilter topicFilter={topicFilter} setTopicFilter={setTopicFilter} />
        
        <div className="relative flex-1 flex items-end shadow-sm border rounded-xl bg-muted/30 focus-within:ring-1 focus-within:ring-ring overflow-hidden">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask a question about AWS..."
            className="w-full max-h-[200px] resize-none bg-transparent border-0 py-3 pl-4 pr-12 text-sm focus-visible:outline-none focus-visible:ring-0 overflow-y-auto"
            rows={1}
            disabled={isLoading}
            maxLength={500}
          />
          <div className="absolute right-2 bottom-2">
            <Button 
              size="icon" 
              onClick={handleSend} 
              disabled={!input.trim() || isLoading}
              className={`h-8 w-8 rounded-lg transition-colors ${input.trim() && !isLoading ? 'bg-[#FF9900] hover:bg-[#FF9900]/90 text-white' : ''}`}
            >
              <Send className="h-4 w-4" />
              <span className="sr-only">Send message</span>
            </Button>
          </div>
        </div>
      </div>
      
      <div className="flex justify-between items-center text-[10px] text-muted-foreground px-1">
        <span>AWSense Chatbot</span>
        <span className={input.length > 450 ? "text-destructive" : ""}>
          {input.length}/500
        </span>
      </div>
    </div>
  )
}
