import { useState, useEffect } from "react"
import { useChat } from "./hooks/useChat"
import { Sidebar } from "./components/Sidebar"
import { ChatWindow } from "./components/ChatWindow"
import { InputBar } from "./components/InputBar"
import { RateLimitBanner } from "./components/RateLimitBanner"
import { ThemeToggle } from "./components/ThemeToggle"
import { TooltipProvider } from "@/components/ui/tooltip"

function App() {
  const [darkMode, setDarkMode] = useState(true)
  
  const {
    messages,
    isLoading,
    isRateLimited,
    setIsRateLimited,
    topicFilter,
    setTopicFilter,
    sendMessage,
    clearConversation
  } = useChat()

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }, [darkMode])

  return (
    <TooltipProvider>
      <div className="flex h-screen w-full bg-dg-base text-dg-textPrimary overflow-hidden font-sans">
        <Sidebar 
          messages={messages} 
          clearConversation={clearConversation} 
        />
        
        <div className="flex flex-1 flex-col relative h-full w-full">
          <RateLimitBanner 
            isRateLimited={isRateLimited} 
            setIsRateLimited={setIsRateLimited} 
          />
          
          <div className="h-10 flex items-center justify-end px-4 shrink-0">
            <ThemeToggle darkMode={darkMode} setDarkMode={setDarkMode} />
          </div>

          <ChatWindow 
            messages={messages} 
            isLoading={isLoading} 
          />
          
          <InputBar 
            onSendMessage={sendMessage}
            isLoading={isLoading}
            topicFilter={topicFilter}
            setTopicFilter={setTopicFilter}
          />
        </div>
      </div>
    </TooltipProvider>
  )
}

export default App
