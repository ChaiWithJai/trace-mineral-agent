"use client";

import { FlaskConical, Settings, History } from "lucide-react";
import Link from "next/link";

export function Header() {
  return (
    <header className="border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900">
      <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2">
          <FlaskConical className="w-6 h-6 text-mineral-500" />
          <span className="font-bold text-lg">TraceMineralDiscoveryAgent</span>
        </Link>

        <nav className="flex items-center gap-4">
          <Link
            href="/history"
            className="flex items-center gap-1 text-gray-600 dark:text-gray-400 hover:text-mineral-500 transition-colors"
          >
            <History className="w-4 h-4" />
            <span className="text-sm">History</span>
          </Link>
          <Link
            href="/settings"
            className="flex items-center gap-1 text-gray-600 dark:text-gray-400 hover:text-mineral-500 transition-colors"
          >
            <Settings className="w-4 h-4" />
            <span className="text-sm">Settings</span>
          </Link>
        </nav>
      </div>
    </header>
  );
}
