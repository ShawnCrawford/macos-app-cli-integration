---
name: macos-app-cli-integration
description: Design and build a user-facing, agent-callable CLI integrated with a macOS app, including Swift, sandboxed, and Mac App Store apps. Use when creating or changing the CLI and its app boundary; not for operating an existing CLI or automating Xcode.
metadata:
  short-description: Build agent-friendly CLIs for macOS apps
---

# Build a CLI integrated with a macOS app

Help the user add a practical command-line interface through which people and their local AI agents can read or change app data. Make architecture and distribution choices from the product's real constraints and evidence. Do not assume a CLI, MCP server, transport, or packaging style is inherently best.

## Workflow

1. **Discover the app.** Read applicable `AGENTS.md` files, architecture and CLI docs, the macOS target, package manifests, entitlements, build phases, settings, signing/release tooling, existing command or MCP surfaces, and relevant tests. Identify the macOS minimum, distribution channels, data owner, domain services, sandbox boundaries, and user changes. Treat checked-in code and current signed artifacts as evidence; reconcile stale or conflicting docs. Read [macOS integration choices](references/macos-integration.md) before selecting a boundary.
2. **Decide the contract.** Shape commands around bounded user tasks. Define stable IDs, explicit write scope, JSON and human output, errors and exit status, pagination, dates/time zones, null and empty values, stdin/stdout/stderr, retry/idempotency behavior, and help. Read [CLI interface design](references/cli-interface.md) when defining this contract.
3. **Choose an owner and boundary.** Preserve the app as data owner when persistence, sync, relationships, validation, or audit behavior lives there. Reuse app domain services and validation; avoid duplicating rules in a second persistence path. Use direct framework access only when the app’s architecture and platform permissions make it a deliberate, supported design. Treat an App Group as a sharing/IPC capability, not proof that a caller is authorized for every operation.
4. **Implement least authority.** Use narrow operations and field allowlists. Authenticate and authorize requests according to the actual threat model; include pairing, revocation, credential storage, replay/response integrity, and fail-closed behavior when the boundary needs them. Never put secrets in argv, environment variables, logs, source, or agent instructions. Make destructive writes explicit and add confirmation or dry run where it meaningfully prevents mistakes.
5. **Validate the chosen distribution.** Start with isolated stores and synthetic data. Validate development, Developer ID, and Mac App Store paths separately when relevant. Inspect signed entitlements and nested code, and exercise the real app/CLI boundary in the applicable signed artifact. A build, a successful signature check, or notarization alone does not prove IPC, sandbox access, app lifecycle, update behavior, or store acceptance. Read [distribution validation](references/distribution-validation.md) and consult current Apple documentation.
6. **Hand off evidence.** Report the selected pattern and alternatives, why it fits, data/security boundaries, commands and interface behavior, exact builds/tests/signatures/distribution paths exercised, and unresolved questions. If a decision depends on unproven platform behavior, name the smallest signed-build proof needed instead of presenting an assumption as fact.

## Guardrails

- Preserve unrelated work and do not use real personal records as test fixtures. Do not reset, seed, inspect, or mutate live stores for validation.
- Do not publish, submit, change release settings, or modify external services unless the user asks.
- Keep the agent in control of ambiguous and consequential decisions. Encode known mechanical procedures as deterministic commands; avoid giving an agent arbitrary code execution when a bounded command contract suffices.
- Keep skill guidance separate from the runtime CLI contract. This skill helps build the CLI and app integration; it does not teach agents to use an already-built CLI or automate Xcode projects.

## References

- Choose among transports, lifecycle models, sandbox and App Group boundaries in [macOS integration choices](references/macos-integration.md).
- Define command and output behavior with [CLI interface design](references/cli-interface.md).
- Plan signed-build and channel-specific evidence with [distribution validation](references/distribution-validation.md).
- Review the limitations of the inspected examples in [example projects](references/example-projects.md).
