"use client"

import * as React from "react"
import { Trash2, MessageSquare, BotIcon } from "lucide-react"

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

// Placeholder chat history items
const chatHistory = [
  { id: 1, title: "How to configure VPC Peering" },
  { id: 2, title: "S3 Bucket Policy for CloudFront" },
  { id: 3, title: "Lambda execution role permissions" },
]

export function AppSidebar({ clearConversation, ...props }) {
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

      {/* Content: Chat History */}
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Recent Chats</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {/* TODO [BACKEND INTEGRATION]: Replace static placeholders with real session history when persistence is implemented */}
              {chatHistory.map((chat) => (
                <SidebarMenuItem key={chat.id}>
                  <SidebarMenuButton tooltip={chat.title} className="opacity-50 cursor-default pointer-events-none">
                    <MessageSquare className="shrink-0" />
                    <span>{chat.title}</span>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>

      {/* Footer: Clear Conversation */}
      <SidebarFooter>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              tooltip="Clear Conversation"
              onClick={clearConversation}
              className="text-sidebar-foreground/70 hover:text-destructive hover:bg-destructive/10"
            >
              <Trash2 className="shrink-0" />
              <span>Clear Conversation</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>

      <SidebarRail />
    </Sidebar>
  )
}
