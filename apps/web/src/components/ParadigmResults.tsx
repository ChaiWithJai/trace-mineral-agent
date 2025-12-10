"use client";

import { useState } from "react";
import { ChevronDown, ChevronRight } from "lucide-react";
import { clsx } from "clsx";

interface ParadigmResultsProps {
  paradigm: string;
  grade?: string;
  findings: string;
  icon: string;
}

const PARADIGM_COLORS: Record<string, string> = {
  allopathy: "border-blue-500 bg-blue-50 dark:bg-blue-900/20",
  naturopathy: "border-green-500 bg-green-50 dark:bg-green-900/20",
  ayurveda: "border-orange-500 bg-orange-50 dark:bg-orange-900/20",
  tcm: "border-red-500 bg-red-50 dark:bg-red-900/20",
  unani: "border-purple-500 bg-purple-50 dark:bg-purple-900/20",
  siddha: "border-teal-500 bg-teal-50 dark:bg-teal-900/20",
};

const GRADE_COLORS: Record<string, string> = {
  A: "bg-green-500 text-white",
  B: "bg-blue-500 text-white",
  C: "bg-yellow-500 text-white",
  D: "bg-orange-500 text-white",
  F: "bg-red-500 text-white",
};

export function ParadigmResults({
  paradigm,
  grade,
  findings,
  icon,
}: ParadigmResultsProps) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div
      className={clsx(
        "border-l-4 rounded-lg overflow-hidden transition-all",
        PARADIGM_COLORS[paradigm.toLowerCase()] || "border-gray-500 bg-gray-50"
      )}
    >
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between p-4 hover:bg-black/5 dark:hover:bg-white/5 transition-colors"
      >
        <div className="flex items-center gap-3">
          <span className="text-2xl">{icon}</span>
          <span className="font-medium capitalize">{paradigm}</span>
          {grade && (
            <span
              className={clsx(
                "px-2 py-0.5 text-xs font-bold rounded",
                GRADE_COLORS[grade.toUpperCase()] || "bg-gray-500 text-white"
              )}
            >
              Grade {grade}
            </span>
          )}
        </div>
        {isOpen ? (
          <ChevronDown className="w-5 h-5 text-gray-500" />
        ) : (
          <ChevronRight className="w-5 h-5 text-gray-500" />
        )}
      </button>

      {isOpen && (
        <div className="px-4 pb-4 prose prose-sm dark:prose-invert max-w-none">
          <div className="whitespace-pre-wrap text-sm text-gray-700 dark:text-gray-300">
            {findings}
          </div>
        </div>
      )}
    </div>
  );
}
