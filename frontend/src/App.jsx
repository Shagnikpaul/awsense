import { useState, useEffect } from "react";
import { useChat } from "./hooks/useChat";
import { ChatWindow } from "./components/ChatWindow";
import { InputBar } from "./components/InputBar";
import { RateLimitBanner } from "./components/RateLimitBanner";
import { ThemeToggle } from "./components/ThemeToggle";
import { TooltipProvider } from "@/components/ui/tooltip";
import {
  SidebarProvider,
  SidebarInset,
  SidebarTrigger,
} from "@/components/ui/sidebar";
import { AppSidebar } from "./components/app-sidebar";

function App() {
  const [darkMode, setDarkMode] = useState(true);

  const {
    messages,
    isLoading,
    isRateLimited,
    setIsRateLimited,
    topicFilter,
    setTopicFilter,
    sendMessage,
    clearConversation,
  } = useChat();

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [darkMode]);

  return (
    <TooltipProvider>
      <SidebarProvider>
        <AppSidebar clearConversation={clearConversation} />

        <SidebarInset>
          <div className="flex h-screen flex-col bg-dg-base text-dg-textPrimary overflow-hidden font-sans">
            {/* Top bar: SidebarTrigger + ThemeToggle */}
            <header className="flex h-12 shrink-0 items-center gap-2 px-4 border-b border-dg-border">
              <SidebarTrigger className="-ml-1" />
              <div className="ml-auto">
                <ThemeToggle darkMode={darkMode} setDarkMode={setDarkMode} />
              </div>
            </header>

            <RateLimitBanner
              isRateLimited={isRateLimited}
              setIsRateLimited={setIsRateLimited}
            />

            <div className="relative flex-1 min-h-0 flex flex-col">
              <ChatWindow messages={messages} isLoading={isLoading} />

              <InputBar
                onSendMessage={sendMessage}
                isLoading={isLoading}
                topicFilter={topicFilter}
                setTopicFilter={setTopicFilter}
              />
            </div>
          </div>
        </SidebarInset>
      </SidebarProvider>
    </TooltipProvider>
  );
}

export default App;
