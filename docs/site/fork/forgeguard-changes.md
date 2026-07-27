# ForgeGuard changes — delta inventory

> **Maintained fork.** This is a ForgeGuard-maintained downstream fork of [`vllm-project/vllm-omni`](https://github.com/vllm-project/vllm-omni). vLLM Omni is upstream-owned and upstream-developed. ForgeGuard-specific documentation is **not** endorsed, supported, or reviewed by the upstream project.

Complete inventory of what ForgeGuard changes relative to the fork's `main` branch.

## Summary

| Classification | Count | Notes |
|---|---|---|
| Documentation only | all | README, `docs/site/`, `docs/maintainers/`, `SUPPORT.md` |
| Metadata | 2 | `FORK_UPSTREAM_BASE`, `.forgeguard/` |
| CI | 1 | Documentation validation workflow only |
| Packaging / build | **0** | No image, package, or release is produced |
| Source code change | **0** | No upstream file is modified except `README.md` |

## ForgeGuard-owned paths

```text
README.md                                     # rewritten; upstream content preserved
SUPPORT.md
FORK_UPSTREAM_BASE
.forgeguard/                                  # docs manifest, schemas, validator
docs/site/                                    # fork documentation and banners
docs/maintainers/upstream-sync/               # sync runbooks
.github/workflows/forgeguard-docs-validate.yml
```

CI fails if anything outside these paths is added, modified, or deleted relative to `main`.

## README handling

`README.md` is the only upstream file replaced. The upstream README is **not deleted**: it is
preserved verbatim at [`upstream-readme.md`](./upstream-readme.md) and linked prominently.

## Code patches

None.

If one is ever added it must be recorded here with reason, affected files, upstream issue/PR link,
whether it is dropped at the next sync, and covering tests. See
[`conflict-policy.md`](../../maintainers/upstream-sync/conflict-policy.md).

## Deliberately not done

ForgeGuard previously scoped a canonical CUDA container image, GPU validation workflows, a release
pipeline, and a tree pinned to an upstream release tag. **That scope was withdrawn.** The
corresponding files were removed rather than left describing artifacts that do not exist:
`ghcr.io/forgeguard-ai/vllm-omni` is not published, and no ForgeGuard release tag exists.
