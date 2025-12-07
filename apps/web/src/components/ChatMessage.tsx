"use client";

import ReactMarkdown from "react-markdown";
import { clsx } from "clsx";
import { User, Bot } from "lucide-react";

interface ChatMessageProps {
  role: "user" | "assistant";
  content: string;
}

export function ChatMessage({ role, content }: ChatMessageProps) {
  const isUser = role === "user";

  return (
    <div
      className={clsx(
        "flex gap-4 p-4 rounded-lg",
        isUser ? "bg-mineral-50 dark:bg-mineral-900/20" : "bg-white dark:bg-gray-800"
      )}
    >
      <div
        className={clsx(
          "flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center",
          isUser ? "bg-mineral-500 text-white" : "bg-gray-200 dark:bg-gray-700"
        )}
      >
        {isUser ? <User className="w-5 h-5" /> : <Bot className="w-5 h-5" />}
      </div>
      <div className="flex-1 overflow-hidden">
        <div className="font-medium text-sm text-gray-500 dark:text-gray-400 mb-1">
          {isUser ? "You" : "TraceMineralDiscoveryAgent"}
        </div>
        <div className="prose prose-sm dark:prose-invert max-w-none">
          <ReactMarkdown>{content}</ReactMarkdown>
        </div>
      </div>
    </div>
  );
}
