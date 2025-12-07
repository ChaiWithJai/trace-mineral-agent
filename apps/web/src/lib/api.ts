const API_URL = process.env.LANGGRAPH_API_URL || "http://127.0.0.1:2024";
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

export async function pollForCompletion(
  threadId: string,
  runId: string,
  onProgress?: (status: string) => void,
  maxAttempts = 120,
  interval = 2000
): Promise<string> {
  for (let i = 0; i < maxAttempts; i++) {
    const status = await getRunStatus(threadId, runId);

    if (onProgress) {
      onProgress(status.status);
    }

    if (status.status === "success") {
      const state = await getThreadState(threadId);
      const messages = state.values.messages;
      const lastMessage = messages[messages.length - 1];
      return lastMessage?.content || "No response received.";
    }

    if (status.status === "error" || status.status === "failed") {
      throw new Error("Research query failed. Please try again.");
    }

    await new Promise((resolve) => setTimeout(resolve, interval));
  }

  throw new Error("Request timed out. Please try a simpler query.");
}

export type { Message, ThreadResponse, RunResponse, ThreadState };
