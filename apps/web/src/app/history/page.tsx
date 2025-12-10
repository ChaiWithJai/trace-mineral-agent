import { Header } from "@/components";
import { History, FileText } from "lucide-react";

export default function HistoryPage() {
  return (
    <div className="min-h-screen flex flex-col bg-cream-100">
      <Header />
      <main className="flex-1 max-w-3xl w-full mx-auto px-6 py-12">
        <div className="flex items-center gap-3 mb-10">
          <div className="w-12 h-12 rounded-2xl bg-accent/10 flex items-center justify-center">
            <History className="w-6 h-6 text-accent" />
          </div>
          <h1 className="font-serif text-3xl font-bold text-charcoal">Research History</h1>
        </div>

        <div className="bg-white rounded-3xl border border-cream-300 p-12 text-center">
          <div className="w-16 h-16 rounded-2xl bg-cream-200 flex items-center justify-center mx-auto mb-6">
            <FileText className="w-8 h-8 text-charcoal-light" />
          </div>
          <p className="text-charcoal font-medium mb-2">No research history yet</p>
          <p className="text-sm text-charcoal-light">
            Your past research sessions will appear here.
          </p>
        </div>
      </main>
    </div>
  );
}
