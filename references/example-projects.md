# Example projects

These projects are useful for different parts of the design. They are examples, not platform authorities, benchmarks, or templates to copy wholesale. Re-check current repository status before relying on implementation details.

## Agent-Native CLI

[agent-native-cli](https://github.com/a-dithya-b/agent-native-cli) explores deterministic commands and reducing repeated procedural actions and irrelevant output. Its README explicitly labels the project an open experiment, says its reported runs are small practical experiments rather than a benchmark, and notes that an agent may independently build reusable abstractions. Borrow the questions about action compression and decision-relevant observations; do not infer a universal efficiency gain or Swift/macOS guidance.

## agendactl

[agendactl](https://github.com/henrywen98/agendactl) packages a Swift command-line binary with an agent skill and documents JSON output, exit classes, stable IDs, bounded commands, and macOS privacy authorization. It illustrates one coherent implementation where the CLI itself uses EventKit. That data-owner model differs from an app that must mediate access to its own persistence, validation, sync, or audit services. Its authorization and packaging choices are project-specific and do not establish App Store compatibility for other apps.

## Swift Argument Parser

[Swift Argument Parser](https://github.com/apple/swift-argument-parser) is an official Swift package for constructing command-line interfaces. It can provide typed arguments and generated help when it fits the project. It is optional: inspect the existing package/tooling and compatibility constraints before selecting a parser.
