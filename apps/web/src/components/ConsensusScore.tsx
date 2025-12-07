"use client";

import { clsx } from "clsx";

interface ConsensusScoreProps {
  score: number;
  className?: string;
}

export function ConsensusScore({ score, className }: ConsensusScoreProps) {
  const percentage = Math.round(score * 100);

  const getColor = () => {
    if (percentage >= 75) return "bg-green-500";
    if (percentage >= 50) return "bg-yellow-500";
    if (percentage >= 25) return "bg-orange-500";
    return "bg-red-500";
  };

  const getLabel = () => {
    if (percentage >= 75) return "Strong Consensus";
    if (percentage >= 50) return "Moderate Consensus";
    if (percentage >= 25) return "Weak Consensus";
    return "Limited Consensus";
  };

  return (
    <div className={clsx("space-y-2", className)}>
      <div className="flex justify-between items-center text-sm">
        <span className="font-medium">Cross-Paradigm Consensus</span>
        <span className="text-gray-600 dark:text-gray-400">{percentage}%</span>
      </div>
      <div className="w-full h-3 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
        <div
          className={clsx("h-full rounded-full transition-all duration-500", getColor())}
          style={{ width: `${percentage}%` }}
        />
      </div>
      <p className="text-xs text-gray-500 dark:text-gray-400">{getLabel()}</p>
    </div>
  );
}
