"use client";

import { useState, useRef, useEffect } from "react";
import { Send, Loader2, AlertCircle } from "lucide-react";
import { clsx } from "clsx";
import { ChatMessage } from "./ChatMessage";
import { createThread, sendMessage, pollForCompletion } from "@/lib/api";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
}

const QUICK_QUERIES = [
  "What does the research say about chromium and insulin sensitivity?",
  "Is there evidence for zinc supporting immune function?",
  "How does selenium affect thyroid health?",
  "Compare magnesium forms for sleep support",
];

export function ResearchChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [status, setStatus] = useState<string>("");
  const [threadId, setThreadId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (query: string) => {
    if (!query.trim() || isLoading) return;

    setError(null);
    setIsLoading(true);
    setInput("");

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: query,
    };
    setMessages((prev) => [...prev, userMessage]);

    try {
      // Create thread if needed
      let currentThreadId = threadId;
      if (!currentThreadId) {
        setStatus("Creating research session...");
        currentThreadId = await createThread();
        setThreadId(currentThreadId);
      }

      // Send message
      setStatus("Submitting query...");
      const run = await sendMessage(currentThreadId, query);

      // Poll for completion
      const response = await pollForCompletion(
        currentThreadId,
        run.run_id,
        (s) => {
          if (s === "pending") setStatus("Queuing research...");
          else if (s === "running") setStatus("Researching across paradigms...");
          else setStatus(s);
        }
      );

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: response,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setIsLoading(false);
      setStatus("");
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Messages area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center py-12">
            <h2 className="text-2xl font-bold text-gray-800 dark:text-gray-200 mb-2">
              TraceMineralDiscoveryAgent
            </h2>
            <p className="text-gray-600 dark:text-gray-400 mb-8">
              Multi-paradigm research for trace mineral therapeutics
            </p>

            <div className="space-y-2">
              <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">
                Try one of these queries:
              </p>
              <div className="flex flex-wrap justify-center gap-2">
                {QUICK_QUERIES.map((query) => (
                  <button
                    key={query}
                    onClick={() => handleSubmit(query)}
                    className="px-3 py-2 text-sm bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-mineral-500 hover:text-mineral-600 transition-colors text-left"
                  >
                    {query}
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        {messages.map((message) => (
          <ChatMessage
            key={message.id}
            role={message.role}
            content={message.content}
          />
        ))}

        {isLoading && (
          <div className="flex items-center gap-2 text-gray-500 dark:text-gray-400 p-4">
            <Loader2 className="w-5 h-5 animate-spin" />
            <span>{status || "Processing..."}</span>
          </div>
        )}

        {error && (
          <div className="flex items-center gap-2 text-red-500 p-4 bg-red-50 dark:bg-red-900/20 rounded-lg">
            <AlertCircle className="w-5 h-5" />
            <span>{error}</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input area */}
      <div className="border-t border-gray-200 dark:border-gray-700 p-4">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSubmit(input);
          }}
          className="flex gap-2"
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about trace minerals..."
            className={clsx(
              "flex-1 px-4 py-3 rounded-lg border",
              "bg-white dark:bg-gray-800",
              "border-gray-200 dark:border-gray-700",
              "focus:outline-none focus:ring-2 focus:ring-mineral-500",
              "placeholder-gray-400"
            )}
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className={clsx(
              "px-4 py-3 rounded-lg font-medium transition-colors",
              "bg-mineral-500 text-white",
              "hover:bg-mineral-600",
              "disabled:opacity-50 disabled:cursor-not-allowed"
            )}
          >
            {isLoading ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <Send className="w-5 h-5" />
            )}
          </button>
        </form>
      </div>
    </div>
  );
}
