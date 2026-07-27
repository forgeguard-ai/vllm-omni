# Upstream sync

How the ForgeGuard vLLM Omni fork is refreshed from upstream.

## Model

This is a **documentation-only** fork of [`vllm-project/vllm-omni`](https://github.com/vllm-project/vllm-omni).
ForgeGuard publishes no container image, package, or release, and the fork is not a release channel.

The `main` branch mirrors upstream; ForgeGuard adds only the documentation overlay on top. Everything
ForgeGuard owns lives in ForgeGuard-owned paths (see the
[delta inventory](../../site/fork/forgeguard-changes.md)), so refreshing from upstream should never
conflict with ForgeGuard content.

Current recorded base: `9f3a73df17757eb9c198b4ce230f77ed092439f4`.

## When to sync

- Periodically, to keep the fork close to upstream.
- After a notable upstream release, so the preserved upstream README and product notes stay current.

## Procedure

See [`sync-checklist.md`](./sync-checklist.md). Conflict handling is in
[`conflict-policy.md`](./conflict-policy.md).
