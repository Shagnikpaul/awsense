export function TokenUsage({ tokenUsage }) {
  if (!tokenUsage) return null;

  return (
    <div className="mt-1 text-dg-textMuted font-inter text-xs text-left">
      ⬡ {tokenUsage.inputTokens} in · {tokenUsage.outputTokens} out
    </div>
  )
}
