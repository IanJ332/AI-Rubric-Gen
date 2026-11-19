# Rubric Generation Isolation Rules

All formal and development generation requests may use only the validated CS50 assignment specification for the condition, an optional reference implementation, and prompts explicitly versioned in the project. Generation calls must not load local skills, personal preferences, chat history, personal instructions, or user configuration. Model requests must not provide shell, filesystem, browser, MCP, or other tools; each assignment uses a separate stateless request.

`python -m rubric_benchmark.luna_run --output <new-directory>` uses a fixed OpenAI Responses API endpoint, explicit system instructions, `tools: []`, and `store: false`. It reads only `OPENAI_API_KEY` for authentication and does not use the Codex CLI or Codex user configuration. If credentials are missing, it fails before creating the output directory or sending a request. The actual returned model ID and input and response hashes should be saved in the manifest. Generation requests do not include the evaluation flaw lists.

The injectable callable in `run_smoke` is a development aid; it does not restrict the caller's capabilities and cannot support a claim that model generation meets these rules. Callers must use an adapter that can demonstrate the same isolation conditions.

Early Codex CLI tests read a local skill; the associated outputs were deleted and did not meet these rules. A truly isolated call requires valid API credentials and a Responses API deployment supporting the specified model; the requested and actual returned models must be recorded separately.
