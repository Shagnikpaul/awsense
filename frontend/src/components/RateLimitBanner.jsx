import { X } from "lucide-react"
import { Button } from "@/components/ui/button"

export function RateLimitBanner({ isRateLimited, setIsRateLimited }) {
  if (!isRateLimited) return null;

  return (
    <div className="bg-destructive/10 border-b border-destructive/20 px-4 py-3 flex items-center justify-between z-10 sticky top-0">
      <div className="text-sm text-destructive font-medium">
        You've reached the request limit. Please wait before sending more messages.
      </div>
      <Button 
        variant="ghost" 
        size="icon" 
        className="h-6 w-6 text-destructive hover:bg-destructive/20 hover:text-destructive"
        onClick={() => setIsRateLimited(false)}
      >
        <X className="h-4 w-4" />
        <span className="sr-only">Dismiss</span>
      </Button>
    </div>
  )
}
