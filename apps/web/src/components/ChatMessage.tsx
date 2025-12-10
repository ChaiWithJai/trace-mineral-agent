"use client";

import ReactMarkdown from "react-markdown";
import { clsx } from "clsx";
import { User, Sparkles } from "lucide-react";

interface ChatMessageProps {
  role: "user" | "assistant";
  content: string;
}

export function ChatMessage({ role, content }: ChatMessageProps) {
  const isUser = role === "user";

  if (isUser) {
    return (
      <div className="flex justify-end">
        <div className="flex items-start gap-3 max-w-[80%]">
          <div className="bg-charcoal text-cream-100 rounded-2xl rounded-tr-sm px-5 py-3">
            <p className="text-sm leading-relaxed">{content}</p>
          </div>
          <div className="flex-shrink-0 w-8 h-8 rounded-xl bg-charcoal/10 flex items-center justify-center">
            <User className="w-4 h-4 text-charcoal" />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex items-start gap-3">
      <div className="flex-shrink-0 w-8 h-8 rounded-xl bg-accent/10 flex items-center justify-center">
        <Sparkles className="w-4 h-4 text-accent" />
      </div>
      <div className="flex-1 min-w-0">
        <div className="bg-white border border-cream-300 rounded-2xl rounded-tl-sm px-6 py-5 overflow-hidden">
          <div className="prose max-w-none">
            <ReactMarkdown>{content}</ReactMarkdown>
          </div>
        </div>
      </div>
    </div>
  );
}
