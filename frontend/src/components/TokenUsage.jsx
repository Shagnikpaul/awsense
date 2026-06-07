export function TokenUsage({ tokenUsage }) {
  if (!tokenUsage) return null;

  return (
    <div className="mt-2 text-[11px] text-muted-foreground/70 text-right">
      Tokens: {tokenUsage.inputTokens} in / {tokenUsage.outputTokens} out
    </div>
  )
}
