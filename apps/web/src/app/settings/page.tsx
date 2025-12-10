"use client";

import { Header } from "@/components";
import { Settings, Server, Info } from "lucide-react";
import { useState } from "react";

export default function SettingsPage() {
  const [apiUrl, setApiUrl] = useState(
    process.env.LANGGRAPH_API_URL || "http://127.0.0.1:2024"
  );

  return (
    <div className="min-h-screen flex flex-col bg-cream-100">
      <Header />
      <main className="flex-1 max-w-3xl w-full mx-auto px-6 py-12">
        <div className="flex items-center gap-3 mb-10">
          <div className="w-12 h-12 rounded-2xl bg-accent/10 flex items-center justify-center">
            <Settings className="w-6 h-6 text-accent" />
          </div>
          <h1 className="font-serif text-3xl font-bold text-charcoal">Settings</h1>
        </div>

        <div className="space-y-6">
          <div className="bg-white rounded-3xl p-8 border border-cream-300 shadow-sm">
            <div className="flex items-center gap-3 mb-6">
              <Server className="w-5 h-5 text-charcoal-light" />
              <h2 className="font-semibold text-lg text-charcoal">API Configuration</h2>
            </div>

            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-charcoal mb-2">
                  LangGraph API URL
                </label>
                <input
                  type="text"
                  value={apiUrl}
                  onChange={(e) => setApiUrl(e.target.value)}
                  className="w-full px-4 py-3 rounded-xl border-2 border-cream-300 bg-cream-50 focus:border-accent focus:ring-2 focus:ring-accent/20 focus:outline-none transition-all"
                />
                <p className="mt-2 text-sm text-charcoal-light">
                  The URL of the LangGraph API server
                </p>
              </div>

              <button
                onClick={() => {
                  alert("Settings saved!");
                }}
                className="px-6 py-3 bg-accent text-white font-medium rounded-xl hover:bg-accent-dark transition-colors shadow-lg shadow-accent/20"
              >
                Save Settings
              </button>
            </div>
          </div>

          <div className="bg-white rounded-3xl p-8 border border-cream-300 shadow-sm">
            <div className="flex items-center gap-3 mb-6">
              <Info className="w-5 h-5 text-charcoal-light" />
              <h2 className="font-semibold text-lg text-charcoal">About</h2>
            </div>
            <div className="space-y-3 text-charcoal-light leading-relaxed">
              <p>
                <strong className="text-charcoal">Trace Mineral Discovery</strong> is a multi-paradigm
                research agent for trace mineral therapeutics.
              </p>
              <p>
                It synthesizes evidence from Allopathy, Naturopathy, Ayurveda,
                TCM, Unani, and Siddha medicine traditions.
              </p>
              <p className="pt-3 text-sm">
                <span className="text-charcoal font-medium">Version:</span> 0.1.0
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
