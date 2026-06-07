export function SourceCitations({ sources }) {
  if (!sources || sources.length === 0) return null;

  return (
    <div className="mt-3 flex flex-wrap gap-2 text-xs">
      <span className="text-muted-foreground font-medium flex items-center">Sources:</span>
      {sources.map((source, idx) => (
        <a
          key={idx}
          href={source.url}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center rounded-sm bg-accent/50 px-2 py-0.5 text-accent-foreground hover:bg-accent hover:underline transition-colors"
          title={source.title}
        >
          {source.title}
        </a>
      ))}
    </div>
  )
}
