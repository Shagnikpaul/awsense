import { Moon, Sun } from "lucide-react"

import { Button } from "@/components/ui/button"

export function ThemeToggle({ darkMode, setDarkMode }) {
  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={() => setDarkMode(!darkMode)}
      title="Toggle theme"
    >
      {darkMode ? (
        <Sun className="h-5 w-5 text-[#FF9900]" />
      ) : (
        <Moon className="h-5 w-5 text-slate-700" />
      )}
      <span className="sr-only">Toggle theme</span>
    </Button>
  )
}
