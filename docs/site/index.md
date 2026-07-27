# vLLM Omni — ForgeGuard fork

> **Maintained fork.** This is a ForgeGuard-maintained downstream fork of [`vllm-project/vllm-omni`](https://github.com/vllm-project/vllm-omni). vLLM Omni is upstream-owned and upstream-developed. ForgeGuard-specific documentation is **not** endorsed, supported, or reviewed by the upstream project.

ForgeGuard-maintained downstream fork of vLLM Omni. **Documentation only — no ForgeGuard
build artifacts are published.**

## Fork base

| Field | Value |
|---|---|
| Upstream repository | [`vllm-project/vllm-omni`](https://github.com/vllm-project/vllm-omni) |
| Fork default branch | `main` |
| Base commit | `9f3a73df17757eb9c198b4ce230f77ed092439f4` |
| Tag at that commit | _none — untagged development commit_ |
| Upstream license | Apache-2.0 |
| Documented on | 2026-07-27 |
| ForgeGuard artifacts | **none published** |

This fork's branch adds ForgeGuard documentation on top of the default branch and modifies no
upstream source file. CI verifies that.

## Pages

- [Upstream project and attribution](./fork/upstream.md)
- [ForgeGuard changes (delta inventory)](./fork/forgeguard-changes.md)
- [Tracking and sync policy](./fork/compatibility.md)
- [Security policy](./fork/security.md)
- [Upstream README, preserved verbatim](./fork/upstream-readme.md)
- [Upstream sync runbook](../maintainers/upstream-sync/README.md)

## Installing the software

ForgeGuard publishes nothing. vLLM Omni is installed from the upstream project. It is tightly coupled to a matching vLLM release line: the `docker/Dockerfile.cuda` shipped at `v0.24.1` builds on `vllm/vllm-openai:v0.24.0`. Follow the upstream README and `docker/` directory at the pinned tag for the supported installation and serving recipes.

Authoritative product documentation: <https://github.com/vllm-project/vllm-omni>
