import { Link2, ExternalLink } from "lucide-react";
import {
  Item,
  ItemActions,
  ItemContent,
  ItemGroup,
  ItemMedia,
  ItemTitle,
} from "@/components/ui/item";

export function SourceCitations({ sources }) {
  if (!sources || sources.length === 0) return null;

  return (
    <div className="mt-4 flex flex-col gap-2 pt-5">
      <span className="font-inter text-xs text-dg-textMuted uppercase tracking-widest">
        Sources
      </span>
      <ItemGroup className="flex flex-col gap-2">
        {sources.map((source, idx) => (
          <Item key={idx} size="xs" asChild>
            <a
              href={source}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 w-full"
            >
              <ItemMedia>
                <Link2 className="size-4" />
              </ItemMedia>

              <ItemContent>
                <ItemTitle className="truncate font-medium text-xs">
                  {source}
                </ItemTitle>
              </ItemContent>

              <ItemActions>
                <ExternalLink className="size-4" />
              </ItemActions>
            </a>
          </Item>
        ))}
      </ItemGroup>
    </div>
  );
}
