# CLI interface design

Read this when defining commands, JSON, errors, or write behavior. The goal is a CLI that remains clear to a person at a terminal and predictable for an agent using a shell.

## Start from user tasks

List the user outcomes first, then expose a small set of discoverable verbs and subcommands. Prefer meaningful, bounded operations over exposing every model field or an unrestricted query language. Use consistent `list`, `show`, `create`, `update`, and narrowly named state-change operations where those fit the domain. Ensure `--help` explains required fields, valid values, defaults, and examples.

Use stable identifiers for update, delete, and relationship operations. If users may start from a name, provide a bounded search or a disambiguation result with IDs; do not silently choose among duplicate names. Bound list sizes and support pagination or a continuation token for larger collections.

## Define the wire-facing contract

Document and keep stable:

- JSON shape, schema/version evolution, encoding, and whether exactly one JSON value is written to stdout.
- Human-readable mode, quiet mode if useful, and which diagnostics or prompts go to stderr.
- Exit codes or machine-readable error codes for usage, ambiguity, authorization, unavailable app, validation, conflict, and internal failures.
- Omitted versus `null` versus empty-string/empty-array semantics, including whether an omitted update field preserves the old value.
- Date/time formats, time zone used for interpreting local times, and the output representation.
- Pagination boundaries, default sort order, maximum result size, and stable ordering when values compare equally.
- Which operations are idempotent, how request IDs or idempotency keys work, and what the caller should do after a timeout with an unknown write outcome.
- Whether stdin accepts structured input, how large payloads are bounded, and how shell quoting is expected to work.

Keep data on stdout easy to pipe and parse. Send progress, warnings, and prompts to stderr. A JSON option should produce machine-readable output on every successful command, not an ad hoc mix of text and JSON. Return concise fields relevant to the task; provide a detail operation when the full record is needed. Do not truncate structured output silently.

## Keep decisions with the user or agent

Automate repeatable mechanics such as parsing, field validation, relationship resolution, and a known multi-step save flow. Return enough context for the agent to decide among ambiguous records or consequential choices. Avoid hidden fuzzy matching that turns an uncertain selection into a write.

For writes, use per-operation field allowlists and explicit stable record IDs. Define what deletion means and how destructive it is. Support dry run or confirmation when the cost of a mistake justifies it; machine callers need a documented noninteractive mode that does not accidentally hang or bypass safety. State whether a successful response means accepted, saved locally, or synced remotely.

## Treat the CLI as a public boundary

Even if only a local agent calls it, parse and validate untrusted arguments and payloads. Bound frame and field sizes, query breadth, duration, and results. Avoid leaking sensitive values in errors. Never require credentials in command arguments or environment variables. If authentication or pairing is needed, keep secrets out of shell history, process listings, logs, and generated skill text; choose an interactive or OS-mediated flow that fits the host.

Prefer application domain services and validation over recreating app rules in the CLI. If app and CLI versions can differ, define compatibility behavior and make unsupported versions fail with an actionable error.

## Useful examples, not templates

The public `agendactl` example demonstrates structured JSON, distinct exit classes, explicit local time-zone behavior, stable IDs, and TCC authorization failures. Its EventKit-specific direct access model is not a template for an app with a separate persistence owner. See [example projects](example-projects.md).
