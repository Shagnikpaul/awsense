import { ExternalLink } from "lucide-react"

export function SourceCitations({ sources }) {
  if (!sources || sources.length === 0) return null;

  return (
    <div className="mt-3 flex flex-col gap-1.5 text-xs">
      <span className="font-inter text-xs text-dg-textMuted uppercase tracking-widest mb-1">Sources</span>
      <div className="flex flex-wrap gap-2">
        {sources.map((source, idx) => (
          <a
            key={idx}
            href={source.url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1 bg-dg-elevated border border-dg-border rounded-pill px-2 py-0.5 font-inter text-xs text-dg-textSecondary hover:text-dg-accent hover:border-dg-accent transition-colors"
            title={source.title}
          >
            {source.title}
            <ExternalLink size={10} className="shrink-0" />
          </a>
        ))}
      </div>
    </div>
  )
}
