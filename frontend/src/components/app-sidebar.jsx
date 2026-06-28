"use client"

import * as React from "react"
import { MessageSquare, BotIcon, PlusIcon, Loader2 } from "lucide-react"

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
  SidebarGroup,
  SidebarGroupLabel,
  SidebarGroupContent,
} from "@/components/ui/sidebar"

/** Format an ISO timestamp into a short relative or absolute label. */
function formatUpdatedAt(isoString) {
  if (!isoString) return null;
  const date = new Date(isoString);
  const now = new Date();
  const diffMs = now - date;
  const diffMins = Math.floor(diffMs / 60_000);
  const diffHours = Math.floor(diffMs / 3_600_000);
  const diffDays = Math.floor(diffMs / 86_400_000);

  if (diffMins < 1) return "Just now";
  if (diffMins < 60) return `${diffMins}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  if (diffDays < 7) return `${diffDays}d ago`;
  return date.toLocaleDateString(undefined, { month: "short", day: "numeric" });
}

export function AppSidebar({
  newChat,
  conversations = [],
  isLoadingConversations = false,
  loadConversation,
  conversationId,
  ...props
}) {
  return (
    <Sidebar collapsible="icon" {...props}>
      {/* Header: Logo + Subheading */}
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              size="lg"
              className="pointer-events-none select-none"
              tooltip="AWSense"
            >
              <div className="flex aspect-square size-8 items-center justify-center rounded-lg bg-sidebar-primary text-sidebar-primary-foreground">
                <BotIcon className="size-4" />
              </div>
              <div className="grid flex-1 text-left text-sm leading-tight">
                <span className="truncate font-bold tracking-widest font-syne text-base">
                  AWSense
                </span>
                <span className="truncate text-xs text-sidebar-foreground/60 font-inter font-semibold tracking-wide">
                  AWS Docs Assistant
                </span>
              </div>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>

      {/* Content: Conversation History */}
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Recent Chats</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {isLoadingConversations ? (
                /* Loading skeleton */
                <SidebarMenuItem>
                  <div className="flex items-center gap-2 px-2 py-2 text-sidebar-foreground/50 text-sm">
                    <Loader2 className="h-4 w-4 animate-spin shrink-0" />
                    <span className="font-inter text-xs">Loading…</span>
                  </div>
                </SidebarMenuItem>
              ) : conversations.length === 0 ? (
                /* Empty state */
                <SidebarMenuItem>
                  <div className="px-2 py-4 text-sidebar-foreground/40 text-xs font-inter text-center select-none">
                    No conversations yet
                  </div>
                </SidebarMenuItem>
              ) : (
                /* Real conversation list */
                conversations.map((conv) => {
                  const isActive = conv.conversationId === conversationId;
                  const updatedLabel = formatUpdatedAt(conv.updatedAt);

                  return (
                    <SidebarMenuItem key={conv.conversationId}>
                      <SidebarMenuButton
                        //tooltip={conv.title}
                        isActive={isActive}
                        onClick={() => loadConversation(conv.conversationId)}
                        className={
                          isActive
                            ? "bg-orange-700 text-sidebar-accent-foreground p-5"
                            : "hover:bg-sidebar-accent/50 p-5"
                        }
                      >
                        <MessageSquare className="shrink-0" />
                        <div className="flex flex-col min-w-0 flex-1">
                          <span className="truncate text-sm font-medium leading-tight">
                            {conv.title}
                          </span>
                          {updatedLabel && (
                            <span className="truncate text-xs text-sidebar-foreground/50 font-inter leading-tight">
                              {updatedLabel}
                            </span>
                          )}
                        </div>
                      </SidebarMenuButton>
                    </SidebarMenuItem>
                  );
                })
              )}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>

      {/* Footer: New Chat */}
      <SidebarFooter>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              tooltip="New Chat"
              onClick={newChat}
              className="text-sidebar-foreground/70 hover:text-sidebar-foreground hover:bg-sidebar-accent/50"
            >
              <PlusIcon className="shrink-0" />
              <span>New Chat</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>

      <SidebarRail />
    </Sidebar>
  )
}
