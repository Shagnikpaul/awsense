import { AWS_TOPICS } from "@/constants/awsTopics";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
  SelectGroup,
  SelectLabel,
} from "@/components/ui/select";

export function TopicFilter({ topicFilter, setTopicFilter }) {
  return (
    <Select value={topicFilter} onValueChange={setTopicFilter}>
      <SelectTrigger className="w-[140px] bg-dg-overlay border border-dg-border rounded-pill px-3 py-1 h-auto min-h-[32px] font-inter text-xs text-dg-textSecondary data-[state=open]:border-dg-accent data-[state=open]:text-dg-accent focus:ring-0 focus:ring-offset-0 focus:border-dg-accent transition-colors">
        <SelectValue placeholder="Select topic" />
      </SelectTrigger>

      <SelectContent className="bg-dg-overlay border-dg-border text-dg-textPrimary font-inter text-sm rounded-xl">
        <SelectGroup>
          <SelectLabel>AWS Topics</SelectLabel>
          {AWS_TOPICS.map((topic) => (
            <SelectItem
              key={topic}
              value={topic}
              className="focus:bg-dg-elevated focus:text-dg-accent cursor-pointer rounded-lg"
            >
              {topic}
            </SelectItem>
          ))}
        </SelectGroup>
      </SelectContent>
    </Select>
  );
}
