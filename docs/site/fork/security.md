# Security policy — ForgeGuard fork

This page covers the **ForgeGuard fork** of
[`vllm-project/vllm-omni`](https://github.com/vllm-project/vllm-omni). It does not replace the upstream
project's own security policy.

## Where to report

| Issue | Report to |
|---|---|
| Vulnerability in vLLM Omni itself | Upstream — see the upstream project's process at <https://github.com/vllm-project/vllm-omni/security> |
| A problem with ForgeGuard documentation, such as an incorrect fork base or misleading security guidance | ForgeGuard — privately, see below |

**Never open a public issue for a suspected vulnerability.**

Report ForgeGuard documentation issues privately through
[GitHub private vulnerability reporting](https://github.com/forgeguard-ai/vllm-omni/security/advisories/new).

## Scope

ForgeGuard publishes **no container image, package, or release** for this repository, so there is no
ForgeGuard supply chain to attack and no ForgeGuard artifact to verify. The surface ForgeGuard owns
is limited to:

- the accuracy of the recorded base in [`FORK_UPSTREAM_BASE`](../../../FORK_UPSTREAM_BASE),
- the documentation-validation workflow under `.github/workflows/`.

Everything about running vLLM Omni — its dependencies, its images, its runtime security — is
upstream's, and should be evaluated against upstream's published artifacts.

## Deployment security notes

- vLLM Omni is strictly version-coupled to vLLM; a given vLLM Omni release expects a matching vLLM release line.
- Different omni pipelines need different launchers, ports, and stage counts. There is no single universal serving command.

Verify these against upstream documentation before relying on them.
