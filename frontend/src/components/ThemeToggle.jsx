import { Moon, Sun } from "lucide-react";

import { Button } from "@/components/ui/button";

export function ThemeToggle({ darkMode, setDarkMode }) {
  return (
    <Button
      variant="ghost"
      size="icon"
      className="text-dg-textMuted hover:text-dg-textPrimary hover:bg-transparent"
      onClick={() => setDarkMode(!darkMode)}
      title="Toggle theme"
    >
      {darkMode ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
      <span className="sr-only">Toggle theme</span>
    </Button>
  );
}
