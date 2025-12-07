import { Header } from "@/components";
import { History } from "lucide-react";

export default function HistoryPage() {
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-1 max-w-4xl w-full mx-auto p-8">
        <div className="flex items-center gap-3 mb-8">
          <History className="w-8 h-8 text-mineral-500" />
          <h1 className="text-2xl font-bold">Research History</h1>
        </div>

        <div className="text-center py-12 text-gray-500 dark:text-gray-400">
          <p className="mb-2">No research history yet.</p>
          <p className="text-sm">Your past research sessions will appear here.</p>
        </div>
      </main>
    </div>
  );
}
