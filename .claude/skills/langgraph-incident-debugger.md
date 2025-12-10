# LangGraph Incident Debugger Skill

## Description
Debug and resolve issues with LangGraph-powered agent applications. This skill guides systematic investigation of UI hangs, API errors, polling issues, and agent performance problems.

## Triggers
- User reports UI hanging or not responding
- 422 errors from LangGraph API
- Agent queries taking too long
- Polling not updating UI
- "Analyzing..." or loading states stuck

## Workflow

### 1. Initial Triage
```bash
# Check if LangGraph API is running
curl -s -X POST "http://127.0.0.1:2024/assistants/search" -H "Content-Type: application/json" -d '{}'

# Check API logs for errors
tmux capture-pane -t <session>:<window> -p | grep -i "error\|422\|failed" | tail -20
```

### 2. Worker Queue Analysis
Look for these patterns in logs:
```
active=N available=-N max=1 n_running=N
```
If `available` is negative, you have **worker queue saturation**.

### 3. Manual API Test
```bash
# Create thread
THREAD_ID=$(curl -s -X POST "http://127.0.0.1:2024/threads" -H "Content-Type: application/json" -d '{}' | python3 -c "import sys, json; print(json.load(sys.stdin)['thread_id'])")

# Send message
RUN_ID=$(curl -s -X POST "http://127.0.0.1:2024/threads/$THREAD_ID/runs" \
  -H "Content-Type: application/json" \
  -d '{"assistant_id": "<graph-id>", "input": {"messages": [{"role": "user", "content": "test"}]}}' \
  | python3 -c "import sys, json; print(json.load(sys.stdin)['run_id'])")

# Poll status
curl -s "http://127.0.0.1:2024/threads/$THREAD_ID/runs/$RUN_ID" | python3 -c "import sys, json; print('Status:', json.load(sys.stdin)['status'])"
```

### 4. Common Issues & Fixes

#### Issue: No elapsed time feedback
**Symptom**: Static "Loading..." with no progress indication
**Fix**: Update polling callback to include elapsed time
```typescript
pollForCompletion(threadId, runId, (status, elapsedSeconds) => {
  setStatus(`${status} (${elapsedSeconds}s)`);
});
```

#### Issue: Can't cancel in-flight requests
**Symptom**: Old requests keep polling after new query submitted
**Fix**: Add AbortController support
```typescript
let activeAbortController: AbortController | null = null;

export function cancelActiveRun(): void {
  if (activeAbortController) {
    activeAbortController.abort();
    activeAbortController = null;
  }
}
```

#### Issue: Worker saturation
**Symptom**: `available=-N` in queue stats
**Fix**:
- Increase worker count in langgraph config
- Add request throttling on frontend
- Implement queue position indicator

### 5. Create Incident Report
Always document findings in JSON format:
```json
{
  "incident_id": "INC-YYYY-MM-DD-NNN",
  "title": "Brief description",
  "severity": "low|medium|high|critical",
  "root_cause": { "primary": "...", "contributing_factors": [...] },
  "resolution": { "changes": [...] },
  "lessons_learned": [...]
}
```

### 6. Regression Tests
Add e2e tests for:
- Loading status visibility
- Elapsed time display
- Input disabled during loading
- Error state handling

## Key Files to Check
- `src/lib/api.ts` - API client and polling logic
- `src/components/*Chat*.tsx` - Chat UI and state management
- `langgraph.json` - Agent configuration
- API server logs (via tmux)

## Output
- Patched code with fix
- Regression tests
- Incident report JSON
- Updated documentation
