import { Trash2, MessageSquare, Cloud } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"

export function Sidebar({ messages, clearConversation }) {
  // Extract previous topics from history
  const historyItems = messages
    .filter(m => m.role === 'user')
    .slice(-5)
    .reverse();

  return (
    <div className="w-[260px] h-full flex-col bg-muted/20 border-r hidden md:flex">
      <div className="p-4 flex items-center gap-2">
        <div className="w-8 h-8 bg-[#FF9900] rounded-lg flex items-center justify-center text-white shadow-sm">
          <Cloud className="w-5 h-5" />
        </div>
        <span className="font-bold text-lg">AWSense</span>
      </div>
      
      <div className="px-4 py-2 flex-1 overflow-y-auto">
        <Button 
          variant="outline" 
          className="w-full justify-start gap-2 mb-6"
          onClick={clearConversation}
        >
          <MessageSquare className="h-4 w-4" />
          New chat
        </Button>
        
        {historyItems.length > 0 && (
          <div className="space-y-1">
            <h3 className="text-xs font-semibold text-muted-foreground px-2 mb-2 uppercase tracking-wider">
              Recent Activity
            </h3>
            {historyItems.map((item, i) => (
              <div 
                key={i}
                className="px-3 py-3 text-sm font-medium text-foreground/80 truncate hover:bg-accent hover:text-accent-foreground rounded-md cursor-pointer transition-colors"
                title={item.content}
              >
                {item.content}
              </div>
            ))}
          </div>
        )}
      </div>

      <Separator />
      
      <div className="p-4">
        <Button 
          variant="ghost" 
          className="w-full justify-start gap-2 text-destructive hover:text-destructive hover:bg-destructive/10"
          onClick={clearConversation}
        >
          <Trash2 className="h-4 w-4" />
          Clear conversation
        </Button>
      </div>
    </div>
  )
}
