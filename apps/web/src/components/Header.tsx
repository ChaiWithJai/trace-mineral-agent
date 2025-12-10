"use client";

import { Sparkles, History, Settings } from "lucide-react";
import Link from "next/link";

export function Header() {
  return (
    <header className="bg-cream-100/80 backdrop-blur-sm sticky top-0 z-50 border-b border-cream-300/50">
      <div className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
        <Link
          href="/"
          className="flex items-center gap-3 group"
        >
          <div className="w-10 h-10 rounded-2xl bg-accent/10 flex items-center justify-center group-hover:bg-accent/20 transition-colors">
            <Sparkles className="w-5 h-5 text-accent" />
          </div>
          <div>
            <span className="font-serif text-lg font-bold text-charcoal tracking-tight">
              Trace Mineral
            </span>
            <span className="font-serif text-lg italic text-charcoal-light ml-1">
              Discovery
            </span>
          </div>
        </Link>

        <nav className="flex items-center gap-1">
          <Link
            href="/history"
            className="flex items-center gap-2 px-4 py-2 rounded-xl text-charcoal-light hover:text-charcoal hover:bg-cream-200 transition-all"
          >
            <History className="w-4 h-4" />
            <span className="text-sm font-medium">History</span>
          </Link>
          <Link
            href="/settings"
            className="flex items-center gap-2 px-4 py-2 rounded-xl text-charcoal-light hover:text-charcoal hover:bg-cream-200 transition-all"
          >
            <Settings className="w-4 h-4" />
            <span className="text-sm font-medium">Settings</span>
          </Link>
        </nav>
      </div>
    </header>
  );
}
