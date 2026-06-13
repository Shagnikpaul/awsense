import { X, AlertTriangle } from "lucide-react";
import { Button } from "@/components/ui/button";

export function RateLimitBanner({ isRateLimited, setIsRateLimited }) {
  if (!isRateLimited) return null;

  return (
    <div className="bg-dg-warning/20 border-b border-dg-warning/40 px-4 py-3 flex items-center justify-between z-10 sticky top-0">
      <div className="flex items-center gap-2 text-sm text-dg-textPrimary font-inter font-medium">
        <AlertTriangle className="h-4 w-4 text-dg-warning shrink-0" />
        You've reached the request limit. Please wait before sending more
        messages.
      </div>
      <Button
        variant="ghost"
        size="icon"
        className="h-6 w-6 text-dg-textMuted hover:bg-transparent hover:text-dg-textPrimary ml-2 shrink-0"
        onClick={() => setIsRateLimited(false)}
      >
        <X className="h-4 w-4" />
        <span className="sr-only">Dismiss</span>
      </Button>
    </div>
  );
}
