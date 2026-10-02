# Distribution validation

Read this before making claims about compatibility, sandbox access, signing, notarization, or store readiness. Build success, valid signatures, app launch, IPC, and App Store acceptance are different evidence.

## Build an evidence matrix

For every distribution path that matters, record the exact artifact and the behavior checked. Keep development, Mac App Store, and Developer ID results separate.

| Evidence layer | Inspect or exercise | What it establishes | What it does not establish |
|---|---|---|---|
| Source/configuration | Target settings, deployment target, package manifest, entitlements, build phases, installer scripts | Intended targets and configured capabilities | Effective signed entitlements or runtime access |
| Build/archive | Build and archive the exact app/helper target; inspect archive layout | Compiler and packaging outputs exist | Distribution signature, permissions, successful helper launch |
| Signature/profile | Inspect each executable, nested code, entitlements, identifiers, team, provisioning profile; verify seals | Artifact has the checked signature/configuration | App Group access works in context, IPC succeeds, or review approves |
| Runtime boundary | Exercise the real command from intended shell/agent against the signed app; test app-open/closed states, authentication and revocation | The tested build can perform the tested operations over the real boundary | Other channels, OS versions, upgrades, or unsupported states |
| Lifecycle | Relocation, upgrade, rollback, uninstall/reinstall, app/CLI version mismatch, credential revocation | Behavior for the explicitly tested transitions | Untested package managers or future releases |
| Distribution service | Notarization result or App Store submission/review outcome | The corresponding service accepted the submitted artifact or request | Product UX correctness, all machine configurations, or approval of unsubmitted changes |

## Use isolated evidence

Use disposable stores, in-memory containers, test credentials, and clearly synthetic records. Verify which environment and signed identity the running app actually selected before a test. Do not use everyday personal stores or live cloud records as fixtures. Keep an operation log of what was run, the artifact hash/version, environment, signing channel, result, and cleanup evidence.

Prefer contract tests for parsing, validation, DTOs, auth gates, and domain behavior, then at least one end-to-end proof for each materially different signed topology. Do not describe a protocol unit test as a signed IPC test. If a signed test produces any record, verify cleanup within the same authorized isolated environment; state clearly if cleanup is only user-confirmed.

## Inspect effective signatures

For app and every nested executable/helper, capture the output of appropriate Apple tools such as `codesign -dv --verbose=4`, `codesign -d --entitlements :-`, `codesign --verify --deep --strict`, and `spctl` or the applicable distribution workflow. Use `security`/profile inspection where profiles are relevant. Check the output for:

- Signing identity, Team ID, code-signing identifier, architectures, hardened runtime, and sealed resources.
- Effective entitlements and whether restricted entitlements are authorized in the embedded profile.
- Every nested Mach-O/helper’s signature, team, identifier, and sandbox configuration.
- App Group IDs and keychain access groups actually present in the signed products.
- Archive contents and installer behavior: no unintended standalone duplicate, missing helper, stale version, or unsigned nested code.

A top-level `codesign --verify` pass does not prove every intended helper entitlement or runtime launch path. Read the detailed signature for each nested executable and exercise it.

## Separate the channels

- **Development:** useful for fast iteration, but development entitlements, signing identity, launch environment, and app-container association may differ from distribution.
- **Developer ID:** follow current Apple signing and notarization requirements for the particular app, tool, installer, or disk image. Notarization is an automated security scan and is not App Review.
- **Mac App Store:** macOS apps distributed through the store must use App Sandbox. Embedded tools and app group access have Apple-documented patterns, but the actual archive and product flow still require validation. Store submission and review are separate evidence from a development or Developer ID run.

Current Apple references:

- [Preparing a macOS app for distribution](https://developer.apple.com/documentation/xcode/preparing-your-app-for-distribution)
- [Embedding a command-line tool in a sandboxed app](https://developer.apple.com/documentation/xcode/embedding-a-helper-tool-in-a-sandboxed-app)
- [Creating distribution-signed code for the Mac](https://developer.apple.com/documentation/xcode/creating-distribution-signed-code-for-the-mac)
- [Notarizing macOS software before distribution](https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution) — notarization is for Developer ID distribution and is not App Review.
- [App Sandbox](https://developer.apple.com/documentation/security/app-sandbox)

## Report evidence precisely

Use concrete statements such as “The Developer ID archive’s embedded helper was signed with the expected team and launched from a temporary isolated store” or “The App Store archive was not exercised.” Name version/build, OS version, test environment, and exact distribution type when known. Do not write “App Store compatible,” “secure,” “production ready,” or “works after reinstall” without evidence covering that claim.
