---
name: self-configuration
description: Configures Letta agents' own runtime behavior, including model, context window, system prompt, reasoning, conversation overrides, compaction settings, and compaction prompts. Use when an agent or user asks to self-modify, tune summarization/compaction, change identity/system instructions, adjust model settings, or test conversation-scoped overrides.
license: MIT
---

# Letta self-configuration

Use the Letta API when an agent needs to change its own persistent defaults or the current conversation's temporary runtime settings.

## Safety rule

Ask before changing persistent agent defaults unless the user explicitly requested the change. Persistent changes include agent model, system prompt, context window, model settings, and compaction settings. Prefer conversation-scoped changes for experiments.

## Decision tree

- Need a temporary model/context experiment? Patch the **current conversation**.
- Need persistent model, system prompt, or compaction behavior? Patch the **agent**.
- Need better summaries after context eviction? Use the **Compaction settings** section and prompt patterns.
- Need provider keys, BYOK setup, or server deployment env vars? Use the broader Letta configuration/API skills instead.
- Need to design a new agent from scratch? Use the agent-development skill.

## Environment

```bash
BASE_URL="${LETTA_BASE_URL:-https://api.letta.com}"
: "${LETTA_API_KEY:?Set LETTA_API_KEY}"
: "${AGENT_ID:?Set AGENT_ID}"
```

Use `AGENT_ID` for yourself. Use `CONVERSATION_ID` for the current thread when it is available.

## Inspect first

```bash
curl -sS "$BASE_URL/v1/agents/$AGENT_ID" \
  -H "Authorization: Bearer $LETTA_API_KEY" | \
  jq '{id, model, context_window_limit, llm_config, model_settings, compaction_settings, system_chars: (.system | length)}'
```

## Choose the API target

| Target | Endpoint | Persistence | Use for |
| --- | --- | --- | --- |
| Agent | `PATCH /v1/agents/$AGENT_ID` | Persistent across conversations | model defaults, context window, system prompt, compaction settings |
| Conversation | `PATCH /v1/conversations/$CONVERSATION_ID` | Current conversation only | temporary model/context/reasoning experiments |

## Quick patches

### Context window only

`context_window_limit` is top-level. Do not put it inside `model_settings`.

```bash
curl -sS -X PATCH "$BASE_URL/v1/agents/$AGENT_ID" \
  -H "Authorization: Bearer $LETTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"context_window_limit": 64000}'
```

Conversation-scoped:

```bash
: "${CONVERSATION_ID:?Set CONVERSATION_ID}"

curl -sS -X PATCH "$BASE_URL/v1/conversations/$CONVERSATION_ID" \
  -H "Authorization: Bearer $LETTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"context_window_limit": 64000}'
```

### Agent-level model update

`model_settings` is usually treated as a replacement object, not a deep merge. Read the current agent first and include any existing settings you want to keep. Provider-specific examples live in [references/model-settings.md](references/model-settings.md).

```bash
curl -sS -X PATCH "$BASE_URL/v1/agents/$AGENT_ID" \
  -H "Authorization: Bearer $LETTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-5.2",
    "context_window_limit": 272000,
    "model_settings": {
      "provider_type": "openai",
      "parallel_tool_calls": true,
      "reasoning": { "reasoning_effort": "medium" },
      "max_output_tokens": 128000
    }
  }'
```

### Conversation-scoped model update

```bash
: "${CONVERSATION_ID:?Set CONVERSATION_ID}"

curl -sS -X PATCH "$BASE_URL/v1/conversations/$CONVERSATION_ID" \
  -H "Authorization: Bearer $LETTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-5.2",
    "context_window_limit": 64000,
    "model_settings": {
      "provider_type": "openai",
      "parallel_tool_calls": true,
      "reasoning": { "reasoning_effort": "low" }
    }
  }'
```

### Safe conversation-scoped model test

A successful `PATCH` means the API accepted the configuration shape. It does **not** always prove the selected model handle can generate at runtime for the current server, provider, account, or routing configuration. The first actual model call may still fail with a resolver/provider error.

For model experiments, prefer this bounded recipe:

1. Save or inspect the current agent/conversation configuration.
2. Patch the **current conversation**, not persistent agent defaults.
3. Verify the response or re-fetch the conversation to confirm the config changed.
4. Run a tiny low-risk runtime test in the same conversation.
5. If the runtime test fails, revert the conversation to the saved known-good model/settings.

This keeps failed model-handle experiments from damaging the agent's persistent continuity or requiring the user to repair global defaults.

### System prompt replacement

Only use `system` when the user explicitly asks to change the persistent system prompt. It is a full replacement, not an append.

```bash
curl -sS "$BASE_URL/v1/agents/$AGENT_ID" \
  -H "Authorization: Bearer $LETTA_API_KEY" | jq -r '.system'
```

Then send the complete replacement prompt:

```bash
curl -sS -X PATCH "$BASE_URL/v1/agents/$AGENT_ID" \
  -H "Authorization: Bearer $LETTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"system": "<FULL replacement system prompt. Preserve important existing instructions.>"}'
```

## Safer bundled updater

Use `scripts/update-agent-settings.ts` when you want a dry-runable patch that can optionally merge existing `model_settings` or `compaction_settings` before updating.

```bash
npx tsx <SKILL_DIR>/scripts/update-agent-settings.ts \
  --target agent \
  --context-window-limit 64000 \
  --dry-run
```

Examples and all flags are in [references/api-patch-examples.md](references/api-patch-examples.md).

## Compaction settings

Compaction runs when message history grows too large for the context window. Letta replaces older messages with a summary while keeping recent messages in context. The summary appears before the remaining recent messages, so a custom compaction prompt should preserve enough background for the later messages to make sense.

Customize compaction when the default summary loses important continuity, tone, relationship context, implementation details, or user feedback.

### Compaction fields

| Field | Use |
| --- | --- |
| `mode` | `sliding_window`, `all`, `self_compact_sliding_window`, or `self_compact_all`. |
| `prompt` | Custom summarization prompt. |
| `model` | Optional cheaper/faster summarizer model. |
| `model_settings` | Optional summarizer model settings. |
| `prompt_acknowledgement` | Optional boolean for summarizers that add acknowledgements/meta-commentary. |
| `clip_chars` | Max summary length in characters. Default is 50000. |
| `sliding_window_percentage` | Fraction of messages to summarize in sliding-window modes. Docs default: `0.3`. |

### Choose a compaction mode

- Use `sliding_window` by default. It summarizes older messages with a separate summarizer call and keeps recent messages intact.
- Use `self_compact_sliding_window` when the agent's own persona/system prompt is important for summary quality or prompt-cache reuse.
- Use `all` only when maximum space reduction matters more than preserving recent raw messages.
- Use `self_compact_all` for all-message compaction with the agent system prompt included.

### Prompt requirements

Every custom compaction prompt should:

- State whether evicted messages come from the beginning of the context window.
- Say the summary will appear before remaining recent messages.
- Say not to continue the conversation, answer transcript questions, or call tools.
- Require incorporation of any existing summary being evicted.
- Preserve exact user requests, names, IDs, URLs, file paths, dates, and quoted phrases when they matter.
- Include lookup hints for detailed content that cannot fit.
- End with "Only output the summary."

For complete prompt templates, read [references/compaction-prompt-patterns.md](references/compaction-prompt-patterns.md).

### Update compaction with the bundled script

```bash
npx tsx <SKILL_DIR>/scripts/update-compaction-prompt.ts \
  --prompt-file /tmp/compaction-prompt.txt \
  --mode self_compact_sliding_window \
  --clip-chars 50000 \
  --dry-run
```

The script preserves existing `compaction_settings` fields unless flags override them. It uses `LETTA_API_KEY`, `AGENT_ID`, and `LETTA_BASE_URL` unless corresponding flags are provided.

## SDK examples

TypeScript and Python examples live in [references/api-patch-examples.md](references/api-patch-examples.md).

## Verify

```bash
curl -sS "$BASE_URL/v1/agents/$AGENT_ID" \
  -H "Authorization: Bearer $LETTA_API_KEY" | \
  jq '{id, model, context_window_limit, llm_config_context_window: .llm_config.context_window, model_settings, compaction_settings, system_chars: (.system | length)}'
```

## Guardrails

- Ask before changing persistent agent defaults unless explicitly requested.
- Prefer conversation-scoped updates for experiments.
- Keep context windows only as large as needed. Bigger windows increase latency and cost.
- Preserve existing `model_settings` and `compaction_settings` fields unless intentionally changing them.
- For self-compaction prompts, always forbid tool use and conversation continuation.
- If an update returns `400`, first check model handle validity, provider type, and whether settings are in the expected shape.
