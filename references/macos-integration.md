# macOS integration choices

Read this before choosing how the CLI reaches app data. Begin with requirements: must the app be running? Does the CLI need to work from any shell process? Who owns persistence and sync? Is the product sandboxed or Mac App Store distributed? Can the app and CLI share a signing team and group? Which installer and upgrade model can the owner support?

## Compare candidate patterns

| Pattern | Useful when | Questions and costs to prove |
|---|---|---|
| Separate CLI calling an app-owned local service | Users want a shell command independent of the GUI process, while the app must own persistence or domain rules | How is the endpoint found and started? Must the app be open? How are callers authenticated, authorized, rate-limited, and revoked? Can the distribution channel authorize the IPC and shared resources for both signed products? |
| Executable/helper embedded in the app | The app can supply the executable and version it atomically with its own release; a full path under the app bundle is acceptable | Can the desired host agent launch it? Does the helper inherit or need its own sandbox? Which entitlements are valid? What is its lifecycle? How do archive, signing, nested code, updates, and store submission handle it? Apple documents helper-tool embedding, but each product still needs signed-artifact validation. |
| XPC service | A service boundary, launch-on-demand behavior, process isolation, or typed IPC is useful | Is this an app-bundled private XPC service or a separately managed service? Can the intended CLI process connect under the selected topology? What happens when app/service lifecycle differs? XPC service shape and access policy must match the actual caller. |
| App Group plus IPC (including Unix-domain socket or supported XPC/Mach mechanism) | Related signed products need a shared IPC namespace or shared container | Confirm group membership in the actual signatures/profiles and use the API’s exact naming/path constraints. Group membership enables sharing or IPC; it is not, by itself, per-user consent or authorization for every command. A socket location does not establish caller identity. |
| URL scheme or another app activation request | A small request can ask a GUI app to open, focus, or handle a user-mediated action | This is an activation/routing mechanism, not automatically a durable request/response API. Consider payload limits, encoding, spoofing, user prompts, result delivery, and app-not-running behavior. Do not put secrets or sensitive records in URLs. |
| LaunchAgent or other launchd-managed process | Work must be available outside the GUI app’s lifetime or have an OS-managed lifecycle | Who installs, updates, removes, and supervises it? Which user/session owns it? How are signing, sandboxing, entitlements, helper registration, login/logout, crash/restart, revocation, and upgrades handled? It adds product lifecycle and support obligations. |
| Optional MCP adapter around a bounded CLI or app service | The host agent requires MCP or the same operation surface serves both MCP and shell callers | Do not make MCP mandatory if the goal only requires shell commands. Keep authorization, validation, and domain rules at a shared narrow boundary; avoid multiplying independent privileged paths. |
| User-visible export or narrower integration | Live read/write access is too risky, unsupported, or not worth the maintenance cost | Specify freshness, user selection, import conflict behavior, and whether the export is read-only. A narrower workflow can be the right product outcome. |

These are candidates, not recommendations. A Swift package executable, app target, helper, or adapter is an implementation choice after the boundary is selected. Libraries such as Swift Argument Parser can help with typed commands and help text, but are optional and should match project conventions.

## Data and authorization boundaries

Map where the source of truth lives and which process already performs validation, relationship maintenance, audit events, conflict handling, and sync. Keep that process as the owner when bypassing it would create a second writer or skip required behavior. Do not open an app’s private container or database by deriving its path. A group container is a documented sharing capability and IPC namespace; do not treat the database inside it as a supported cross-process API unless the product intentionally defines that design and concurrency behavior.

Separate these questions:

1. **Discovery:** How does a client find the executable and endpoint after app relocation or upgrade?
2. **Transport:** How are bounded requests and responses exchanged, and how does the app behave while closed or busy?
3. **Process identity:** What can the OS or signature actually establish about the peer in this topology?
4. **Application authority:** Which user action grants access, to what operations, and how can it be revoked?
5. **Data ownership:** Which process validates and commits the write, and what does the response promise about sync?

Do not infer authorization from an executable path, bundle ID, Team ID, App Group membership, socket permissions, or successful connection alone. Verify the platform-supported peer identity mechanism and add app-level authentication/authorization appropriate to the threat model. Fail closed when credentials are missing, malformed, expired, or revoked.

## macOS-specific validation questions

- Inspect the app and helper’s effective signed entitlements, not only source `.entitlements` files. Verify group IDs, app sandbox state, keychain groups, code-signing identifiers, team IDs, profiles, hardened runtime, and nested executable signatures.
- For an embedded helper, follow current Apple guidance for the exact build system and inspect the archived/exported product. Apple’s sample instructions include sandbox inheritance and code-sign-on-copy details; do not mechanically transplant those settings to a different helper model.
- For App Groups, distinguish `group.` identifiers, provisioning/profile behavior, and macOS team-prefixed identifier support. Check current Apple docs for platform-specific constraints.
- Test launch with the app open and closed, from the real host agent’s shell environment, after moving or updating the app, and with missing/revoked credentials.
- Evaluate Mac App Store, Developer ID, and development builds independently. A same-team development run does not prove distribution permissions or store acceptance.
- If a separate executable is not discoverable through `PATH`, a stable full path or user-visible export may still meet the user’s goal. Treat a short command name as a product convenience, not a platform requirement.

## Apple references

These were checked on 2026-10-02. Re-check them when making a platform decision; documentation does not replace testing the exact artifact.

- [App Groups entitlement](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.security.application-groups) — shared containers and IPC options, including constraints for UNIX-domain socket paths.
- [Configuring App Groups](https://developer.apple.com/documentation/xcode/configuring-app-groups)
- [Accessing App Group containers in an existing macOS app](https://developer.apple.com/documentation/xcode/accessing-app-group-containers)
- [Embedding a command-line tool in a sandboxed app](https://developer.apple.com/documentation/xcode/embedding-a-helper-tool-in-a-sandboxed-app) — helper embedding, signing, and validation guidance.
- [App Sandbox](https://developer.apple.com/documentation/security/app-sandbox) — Mac App Store sandbox requirement and related references.
- [Creating XPC services](https://developer.apple.com/documentation/xpc/creating-xpc-services)
- [Accessing files from the macOS App Sandbox](https://developer.apple.com/documentation/security/accessing-files-from-the-macos-app-sandbox)
