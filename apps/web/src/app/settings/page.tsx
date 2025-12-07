"use client";

import { Header } from "@/components";
import { Settings, Server } from "lucide-react";
import { useState } from "react";

export default function SettingsPage() {
  const [apiUrl, setApiUrl] = useState(
    process.env.LANGGRAPH_API_URL || "http://127.0.0.1:2024"
  );

  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-1 max-w-4xl w-full mx-auto p-8">
        <div className="flex items-center gap-3 mb-8">
          <Settings className="w-8 h-8 text-mineral-500" />
          <h1 className="text-2xl font-bold">Settings</h1>
        </div>

        <div className="space-y-6">
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
            <div className="flex items-center gap-2 mb-4">
              <Server className="w-5 h-5 text-gray-500" />
              <h2 className="font-semibold">API Configuration</h2>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  LangGraph API URL
                </label>
                <input
                  type="text"
                  value={apiUrl}
                  onChange={(e) => setApiUrl(e.target.value)}
                  className="w-full px-3 py-2 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-mineral-500"
                />
                <p className="mt-1 text-xs text-gray-500">
                  The URL of the LangGraph API server
                </p>
              </div>

              <button
                onClick={() => {
                  // In a real app, this would save to localStorage or context
                  alert("Settings saved!");
                }}
                className="px-4 py-2 bg-mineral-500 text-white rounded-lg hover:bg-mineral-600 transition-colors"
              >
                Save Settings
              </button>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
            <h2 className="font-semibold mb-4">About</h2>
            <div className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
              <p>
                <strong>TraceMineralDiscoveryAgent</strong> is a multi-paradigm
                research agent for trace mineral therapeutics.
              </p>
              <p>
                It synthesizes evidence from Allopathy, Naturopathy, Ayurveda,
                TCM, Unani, and Siddha medicine traditions.
              </p>
              <p className="pt-2">
                Version: 0.1.0
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
