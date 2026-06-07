import { Trash2, Plus } from "lucide-react"
import { Button } from "@/components/ui/button"

export function Sidebar({ messages, clearConversation }) {
  return (
    <div className="w-60 shrink-0 h-full flex flex-col bg-dg-surface border-r border-dg-border hidden md:flex">
      <div className="p-4 flex flex-col gap-1 border-b border-dg-border">
        <span className="font-syne font-bold text-xl tracking-widest text-dg-textPrimary">AWSense</span>
        <span className="font-inter text-xs tracking-wide text-dg-textMuted">AWS Docs Assistant</span>
      </div>
      
      <div className="px-4 py-10 flex-1 overflow-y-auto">
   
        
        <div className="space-y-1">
          <h3 className="font-inter text-xs text-dg-textMuted uppercase tracking-widest px-2 mb-2">
            Recent
          </h3>
          
          {/* TODO [BACKEND INTEGRATION]: Replace static placeholders with real session history when persistence is implemented */}
          <div className="px-3 py-3 text-sm font-medium text-dg-textMuted truncate cursor-default opacity-50">
            How to configure VPC Peering
          </div>
          <div className="px-3 py-3 text-sm font-medium text-dg-textMuted truncate cursor-default opacity-50">
            S3 Bucket Policy for CloudFront
          </div>
          <div className="px-3 py-3 text-sm font-medium text-dg-textMuted truncate cursor-default opacity-50">
            Lambda execution role permissions
          </div>
        </div>
      </div>

      <div className="p-4">
        <Button 
          variant="ghost" 
          className="w-full justify-start gap-2 text-dg-textMuted hover:text-dg-accent hover:bg-transparent font-inter text-sm px-2"
          onClick={clearConversation}
        >
          <Trash2 className="h-4 w-4" />
          Clear Conversation
        </Button>
      </div>
    </div>
  )
}
