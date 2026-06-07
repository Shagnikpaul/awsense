import { AWS_TOPICS } from "@/constants/awsTopics"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

export function TopicFilter({ topicFilter, setTopicFilter }) {
  return (
    <Select value={topicFilter} onValueChange={setTopicFilter}>
      <SelectTrigger className="w-[140px] bg-background">
        <SelectValue placeholder="Select topic" />
      </SelectTrigger>
      <SelectContent>
        {AWS_TOPICS.map((topic) => (
          <SelectItem key={topic} value={topic}>
            {topic}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  )
}
