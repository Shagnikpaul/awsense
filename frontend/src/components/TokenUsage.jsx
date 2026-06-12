import { ArrowDown, ArrowUp } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip"

export function TokenUsage({ tokenUsage }) {
  if (!tokenUsage) return null;

  return (
    <div className="flex flex-wrap gap-2">
      <Tooltip>
        <TooltipTrigger>
          <Badge variant="secondary" >
            <ArrowDown data-icon="inline-start" />
            {tokenUsage.inputTokens}
          </Badge>
        </TooltipTrigger>
        <TooltipContent side="bottom">
          <div className="flex flex-col gap-1">
            <h1 className="text-sm font-bold  ">
              Input Tokens
            </h1>
            Input tokens are calculated based on the number of tokens in the user's message, which can vary depending on the length and complexity of the input.
          </div>

        </TooltipContent>
      </Tooltip>


      <Tooltip>
        <TooltipTrigger><Badge variant="secondary" >
          <ArrowUp data-icon="inline-end" />
          {tokenUsage.outputTokens}
        </Badge></TooltipTrigger>
        <TooltipContent side="bottom">
          <div className="flex flex-col gap-1">
            <h1 className="text-sm font-bold  ">
              Output Tokens
            </h1>
            Output tokens are calculated based on the number of tokens in the model's response, which can vary depending on the length and complexity of the answer.
          </div>

        </TooltipContent>
      </Tooltip>

    </div>
  )
}
