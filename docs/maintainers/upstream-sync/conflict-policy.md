# Conflict policy

## Principle

Minimal divergence. ForgeGuard does not patch vLLM Omni; this fork is documentation only.

## ForgeGuard-owned paths

Upstream does not write to these, so a refresh should never conflict:

```text
SUPPORT.md  FORK_UPSTREAM_BASE  .forgeguard/  docs/site/  docs/maintainers/
.github/workflows/forgeguard-*.yml
```

`README.md` is the one shared file. On a refresh, upstream's new README goes to
`docs/site/fork/upstream-readme.md` and the ForgeGuard README stays at the root.

If upstream ever introduces a file at a ForgeGuard-owned path, ForgeGuard renames its own file
rather than shadowing upstream content, and records the rename in the delta inventory.

## Code patches

This fork carries none, and should carry none. If a downstream code patch ever becomes necessary it
must be recorded in [the delta inventory](../../site/fork/forgeguard-changes.md) with reason,
affected files, upstream issue/PR, whether it is dropped at the next sync, and covering tests — and
it should be raised upstream if it is upstreamable.

## Never

- Never rewrite or squash upstream history.
- Never modify or delete an upstream file other than `README.md`.
- Never carry an undocumented patch.
- Never let a ForgeGuard document claim an artifact that is not published.
