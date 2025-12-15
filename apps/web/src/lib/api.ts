const API_URL =
  typeof window !== "undefined"
    ? localStorage.getItem("langgraph_api_url") || process.env.NEXT_PUBLIC_LANGGRAPH_API_URL || "http://127.0.0.1:2024"
    : process.env.LANGGRAPH_API_URL || "http://127.0.0.1:2024";
const ASSISTANT_ID = "trace-mineral-discovery";

interface Message {
  role: "user" | "assistant";
  content: string;
}

interface ThreadResponse {
  thread_id: string;
}

interface RunResponse {
  run_id: string;
  thread_id: string;
  status: string;
}

interface ThreadState {
  values: {
    messages: Array<{
      type: string;
      content: string;
    }>;
  };
}

// Track active polling operations for cancellation
let activeAbortController: AbortController | null = null;

export async function createThread(): Promise<string> {
  const response = await fetch(`${API_URL}/threads`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({}),
  });

  if (!response.ok) {
    throw new Error(`Failed to create thread: ${response.statusText}`);
  }

  const data: ThreadResponse = await response.json();
  return data.thread_id;
}

export async function sendMessage(
  threadId: string,
  message: string
): Promise<RunResponse> {
  const response = await fetch(`${API_URL}/threads/${threadId}/runs`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      assistant_id: ASSISTANT_ID,
      input: {
        messages: [{ role: "user", content: message }],
      },
    }),
  });

  if (!response.ok) {
    throw new Error(`Failed to send message: ${response.statusText}`);
  }

  return response.json();
}

export async function getRunStatus(
  threadId: string,
  runId: string
): Promise<RunResponse> {
  const response = await fetch(
    `${API_URL}/threads/${threadId}/runs/${runId}`,
    {
      method: "GET",
    }
  );

  if (!response.ok) {
    throw new Error(`Failed to get run status: ${response.statusText}`);
  }

  return response.json();
}

export async function getThreadState(threadId: string): Promise<ThreadState> {
  const response = await fetch(`${API_URL}/threads/${threadId}/state`, {
    method: "GET",
  });

  if (!response.ok) {
    throw new Error(`Failed to get thread state: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Cancel any active run by aborting the polling operation.
 */
export function cancelActiveRun(): void {
  if (activeAbortController) {
    activeAbortController.abort();
    activeAbortController = null;
  }
}

/**
 * Poll for run completion with cancellation support.
 * Provides elapsed time feedback via onProgress callback.
 */
export async function pollForCompletion(
  threadId: string,
  runId: string,
  onProgress?: (status: string, elapsedSeconds?: number) => void,
  maxAttempts = 120,
  interval = 2000
): Promise<string> {
  // Cancel any existing polling operation
  cancelActiveRun();

  // Create new abort controller for this polling operation
  activeAbortController = new AbortController();
  const { signal } = activeAbortController;

  const startTime = Date.now();

  for (let i = 0; i < maxAttempts; i++) {
    // Check if aborted
    if (signal.aborted) {
      throw new Error("Request cancelled.");
    }

    try {
      const status = await getRunStatus(threadId, runId);
      const elapsedSeconds = Math.floor((Date.now() - startTime) / 1000);

      if (onProgress) {
        onProgress(status.status, elapsedSeconds);
      }

      if (status.status === "success") {
        activeAbortController = null;
        const state = await getThreadState(threadId);
        const messages = state.values.messages;
        const lastMessage = messages[messages.length - 1];
        return lastMessage?.content || "No response received.";
      }

      if (status.status === "error" || status.status === "failed") {
        activeAbortController = null;
        throw new Error("Research query failed. Please try again.");
      }

      // Wait with abort check
      await new Promise((resolve, reject) => {
        const timeout = setTimeout(resolve, interval);
        signal.addEventListener("abort", () => {
          clearTimeout(timeout);
          reject(new Error("Request cancelled."));
        });
      });
    } catch (err) {
      if (err instanceof Error && err.message === "Request cancelled.") {
        throw err;
      }
      // Network error - retry
      console.warn("Polling error, retrying:", err);
    }
  }

  activeAbortController = null;
  throw new Error("Request timed out. Please try a simpler query.");
}

export type { Message, ThreadResponse, RunResponse, ThreadState };
