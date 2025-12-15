"use client";

import { useState, useRef, useEffect } from "react";
import { ArrowRight, Loader2, AlertCircle, Sparkles } from "lucide-react";
import { clsx } from "clsx";
import { ChatMessage } from "./ChatMessage";
import {
  createThread,
  sendMessage,
  pollForCompletion,
  cancelActiveRun,
} from "@/lib/api";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
}

const QUICK_QUERIES = [
  {
    title: "Chromium & Insulin",
    query: "What does the research say about chromium and insulin sensitivity?",
  },
  {
    title: "Zinc & Immunity",
    query: "Is there evidence for zinc supporting immune function?",
  },
  {
    title: "Selenium & Thyroid",
    query: "How does selenium affect thyroid health?",
  },
  {
    title: "Magnesium Forms",
    query: "Compare magnesium forms for sleep support",
  },
];

function TypingIndicator() {
  return (
    <div className="flex items-center gap-3 p-6 animate-fade-in">
      <div className="w-8 h-8 rounded-xl bg-accent/10 flex items-center justify-center">
        <Sparkles className="w-4 h-4 text-accent" />
      </div>
      <div className="flex gap-1.5">
        <div className="typing-dot" />
        <div className="typing-dot" />
        <div className="typing-dot" />
      </div>
    </div>
  );
}

export function ResearchChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [status, setStatus] = useState<string>("");
  const [threadId, setThreadId] = useState<string | null>(null);
  const [isFocused, setIsFocused] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Auto-focus input on mount and cleanup on unmount
  useEffect(() => {
    inputRef.current?.focus();

    // Cancel any active runs when component unmounts
    return () => {
      cancelActiveRun();
    };
  }, []);

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
      let currentThreadId = threadId;
      if (!currentThreadId) {
        setStatus("Starting session...");
        currentThreadId = await createThread();
        setThreadId(currentThreadId);
      }

      setStatus("Researching...");
      const run = await sendMessage(currentThreadId, query);

      const response = await pollForCompletion(
        currentThreadId,
        run.run_id,
        (s, elapsedSeconds) => {
          const elapsed = elapsedSeconds ? ` (${elapsedSeconds}s)` : "";
          if (s === "pending") setStatus(`Queuing...${elapsed}`);
          else if (s === "running")
            setStatus(`Analyzing across paradigms...${elapsed}`);
          else setStatus(`${s}${elapsed}`);
        }
      );

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: response,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      // Don't show error for cancelled requests
      if (err instanceof Error && err.message === "Request cancelled.") {
        // Request was cancelled, likely due to a new query - ignore
        return;
      }
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setIsLoading(false);
      setStatus("");
    }
  };

  const showWelcome = messages.length === 0;

  return (
    <div className="flex flex-col h-[calc(100vh-73px)]">
      {/* Messages area */}
      <div className="flex-1 overflow-y-auto">
        {showWelcome ? (
          <div className="flex flex-col items-center justify-center min-h-full px-6 py-16 animate-fade-in">
            {/* Hero */}
            <div className="text-center max-w-2xl mb-12">
              <h1 className="font-serif text-4xl md:text-5xl font-bold text-charcoal mb-4 tracking-tight">
                Discover the science of
                <span className="block italic text-accent mt-1">trace minerals</span>
              </h1>
              <p className="text-lg text-charcoal-light leading-relaxed">
                Research synthesized from Allopathy, Naturopathy, Ayurveda, TCM, Unani, and Siddha traditions.
              </p>
            </div>

            {/* Input - Prominent on welcome */}
            <div className="w-full max-w-2xl mb-12">
              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  handleSubmit(input);
                }}
                className="relative"
              >
                <input
                  ref={inputRef}
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onFocus={() => setIsFocused(true)}
                  onBlur={() => setIsFocused(false)}
                  placeholder="Ask about trace minerals..."
                  className={clsx(
                    "w-full px-6 py-5 pr-14 rounded-2xl text-lg",
                    "bg-white border-2",
                    "placeholder-charcoal-light/50",
                    "input-silky",
                    isFocused
                      ? "border-accent shadow-xl shadow-accent/10"
                      : "border-cream-300 shadow-lg shadow-charcoal/5",
                    "focus:outline-none"
                  )}
                  disabled={isLoading}
                  autoComplete="off"
                />
                <button
                  type="submit"
                  disabled={isLoading || !input.trim()}
                  className={clsx(
                    "absolute right-3 top-1/2 -translate-y-1/2",
                    "w-10 h-10 rounded-xl flex items-center justify-center",
                    "transition-all duration-300",
                    input.trim()
                      ? "bg-accent text-white hover:bg-accent-dark scale-100"
                      : "bg-cream-200 text-charcoal-light scale-95",
                    "disabled:cursor-not-allowed"
                  )}
                >
                  {isLoading ? (
                    <Loader2 className="w-5 h-5 animate-spin" />
                  ) : (
                    <ArrowRight className="w-5 h-5" />
                  )}
                </button>
              </form>
            </div>

            {/* Quick queries */}
            <div className="w-full max-w-2xl">
              <p className="text-sm text-charcoal-light mb-4 text-center">
                Or try one of these:
              </p>
              <div className="grid grid-cols-2 gap-3">
                {QUICK_QUERIES.map((item) => (
                  <button
                    key={item.title}
                    onClick={() => handleSubmit(item.query)}
                    className={clsx(
                      "px-5 py-4 text-left rounded-2xl",
                      "bg-white border border-cream-300",
                      "hover:border-accent/30 hover:shadow-lg hover:shadow-accent/5",
                      "transition-all duration-300",
                      "group card-hover"
                    )}
                    disabled={isLoading}
                  >
                    <span className="font-medium text-charcoal group-hover:text-accent transition-colors">
                      {item.title}
                    </span>
                    <span className="block text-sm text-charcoal-light mt-1 line-clamp-2">
                      {item.query}
                    </span>
                  </button>
                ))}
              </div>
            </div>
          </div>
        ) : (
          <div className="max-w-4xl mx-auto px-4 py-6 space-y-6">
            {messages.map((message, index) => (
              <div
                key={message.id}
                className="animate-slide-up"
                style={{ animationDelay: `${index * 0.05}s` }}
              >
                <ChatMessage role={message.role} content={message.content} />
              </div>
            ))}

            {isLoading && (
              <div className="animate-slide-up">
                <div className="bg-white rounded-2xl border border-cream-300 overflow-hidden">
                  <TypingIndicator />
                  {status && (
                    <div className="px-6 pb-4 text-sm text-charcoal-light">
                      {status}
                    </div>
                  )}
                </div>
              </div>
            )}

            {error && (
              <div className="flex items-center gap-3 p-4 bg-red-50 border border-red-200 rounded-2xl animate-slide-up">
                <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0" />
                <span className="text-red-700">{error}</span>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Sticky input - only show when there are messages */}
      {!showWelcome && (
        <div className="sticky bottom-0 bg-gradient-to-t from-cream-100 via-cream-100 to-cream-100/80 pt-4 pb-6 px-4">
          <div className="max-w-4xl mx-auto">
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleSubmit(input);
              }}
              className="relative"
            >
              <input
                ref={inputRef}
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onFocus={() => setIsFocused(true)}
                onBlur={() => setIsFocused(false)}
                placeholder="Ask a follow-up question..."
                className={clsx(
                  "w-full px-5 py-4 pr-14 rounded-2xl",
                  "bg-white border-2",
                  "placeholder-charcoal-light/50",
                  "input-silky",
                  isFocused
                    ? "border-accent shadow-xl shadow-accent/10"
                    : "border-cream-300 shadow-lg shadow-charcoal/5",
                  "focus:outline-none"
                )}
                disabled={isLoading}
                autoComplete="off"
              />
              <button
                type="submit"
                disabled={isLoading || !input.trim()}
                className={clsx(
                  "absolute right-3 top-1/2 -translate-y-1/2",
                  "w-10 h-10 rounded-xl flex items-center justify-center",
                  "transition-all duration-300",
                  input.trim()
                    ? "bg-accent text-white hover:bg-accent-dark scale-100"
                    : "bg-cream-200 text-charcoal-light scale-95",
                  "disabled:cursor-not-allowed"
                )}
              >
                {isLoading ? (
                  <Loader2 className="w-5 h-5 animate-spin" />
                ) : (
                  <ArrowRight className="w-5 h-5" />
                )}
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
