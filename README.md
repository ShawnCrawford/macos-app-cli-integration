# macOS App CLI Integration skill

An Agent Skill for coding agents building a practical CLI that lets a Mac user and their local AI agent read or modify data through a macOS app’s supported domain boundary.

It focuses on Swift and macOS, including sandboxed and Mac App Store apps, while keeping transport and distribution decisions open. It covers project discovery, command design, app ownership and security boundaries, integration choices, signed distribution validation, and evidence-based handoff.

## Use this skill when

- You are designing or changing a CLI and its integration with a macOS app.
- The app is sandboxed, uses protected local data, syncs with a service, or is distributed through multiple channels.
- You need to compare a separately installed CLI, an app-bundled helper, an XPC or other service, an optional MCP adapter, or a narrower export path.

This skill is for building and validating the CLI/app integration. It is not for teaching an agent how to operate a completed CLI, and it does not automate Xcode project work.

## Add to a compatible coding agent

Copy this repository’s `SKILL.md` and `references/` directory into the agent’s supported skill folder, keeping their relative paths together. Common skill-capable agents use a user-level or repository-level `skills/<skill-name>/` directory, but the exact location and discovery behavior vary by agent. Follow that agent’s current skill installation documentation. The optional `agents/openai.yaml` contains Codex UI metadata and is not required by every agent.

For example, a repository-level layout may look like:

```text
.agents/skills/macos-app-cli-integration/
├── SKILL.md
└── references/
```

## Limits

Platform documentation describes supported mechanisms and requirements, not proof that a particular product topology works. Signed entitlements, app lifecycle, IPC, helper launch, sandbox behavior, and store review depend on the exact app, helper, signature, and distribution artifact. Validate the paths that matter for the product and label missing evidence.

The skill does not prescribe one architecture, grant permission to access user data, or authorize publishing, App Store submission, release changes, or external service mutations. Use synthetic records and isolated stores for validation.

## Repository contents

- `SKILL.md` — routing and essential workflow.
- `references/cli-interface.md` — command, data, and output contract decisions.
- `references/macos-integration.md` — transport, lifecycle, and packaging comparison.
- `references/distribution-validation.md` — signed artifact and channel validation.
- `references/example-projects.md` — useful patterns and limits of public examples.
- `scripts/validate.py` — dependency-free frontmatter, link, and layout checks.
- `LICENSE` — MIT License.

## Validate

Run `python3 scripts/validate.py` from the repository root. It checks required skill files, required frontmatter keys, local Markdown links, and unresolved scaffold markers. It does not verify technical claims, Apple policy, links over the network, or license suitability.

## License

This repository is licensed under the [MIT License](LICENSE). It permits broad reuse, modification, and redistribution, provided the copyright and license notices are retained; it also includes an “as is” warranty disclaimer.
