# Tracking and sync policy

> **Maintained fork.** This is a ForgeGuard-maintained downstream fork of [`vllm-project/vllm-omni`](https://github.com/vllm-project/vllm-omni). vLLM Omni is upstream-owned and upstream-developed. ForgeGuard-specific documentation is **not** endorsed, supported, or reviewed by the upstream project.

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

## What this fork is, and is not

This fork's `main` branch mirrors the upstream default branch as of the base commit above. It
is **not** a curated release channel, and ForgeGuard does not test, build, or distribute it.

The base is an untagged development commit (`9f3a73df1775`) of the upstream default branch — **not an upstream release**.

For anything you intend to run, use an upstream release:
<https://github.com/vllm-project/vllm-omni/releases>

## Product notes

Properties of vLLM Omni itself, stated so readers understand the project. ForgeGuard has
verified none of them by execution:

- vLLM Omni is strictly version-coupled to vLLM; a given vLLM Omni release expects a matching vLLM release line.
- Different omni pipelines need different launchers, ports, and stage counts. There is no single universal serving command.

For authoritative and current requirements, use upstream: <https://github.com/vllm-project/vllm-omni>

## Sync cadence

ForgeGuard refreshes the fork from upstream on a best-effort basis, following
[`docs/maintainers/upstream-sync/sync-checklist.md`](../../maintainers/upstream-sync/sync-checklist.md).
There is no SLA. When the fork is refreshed, `FORK_UPSTREAM_BASE` is updated to the new base commit.

## Relationship to upstream distribution

Upstream's own distribution is the only distribution. ForgeGuard does not publish an alternative and
does not suggest that upstream packaging is deficient.
