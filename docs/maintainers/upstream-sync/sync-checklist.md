# Upstream sync checklist

## 1. Refresh the default branch from upstream

```bash
git remote add upstream https://github.com/vllm-project/vllm-omni 2>/dev/null || true
git fetch upstream main
git checkout main
git merge --ff-only upstream/main      # a mirror should fast-forward
git push origin main
```

- [ ] `main` fast-forwards cleanly. If it does not, stop and read
      [`conflict-policy.md`](./conflict-policy.md).

## 2. Refresh the documentation overlay

```bash
git checkout -b forgeguard/docs-refresh main
```

- [ ] `FORK_UPSTREAM_BASE`: update `base.commit` to the new `main` tip, update `tag_at_commit`
      (use `git tag --points-at <sha>`; record `null` if untagged), update `recorded_on`.
- [ ] `docs/site/fork/upstream-readme.md` refreshed from the new upstream `README.md`.
- [ ] Product notes in `docs/site/fork/compatibility.md` re-checked against upstream docs.
- [ ] README install guidance re-checked (versions, package names, image names).
- [ ] Delta inventory still accurate.

## 3. Validate

```bash
python3 .forgeguard/scripts/validate_overlay.py --base origin/main
```

- [ ] Validation passes.
- [ ] The diff against `main` still modifies only `README.md` and adds only ForgeGuard-owned files.
- [ ] No ForgeGuard document has started claiming a build artifact.

## 4. Land it

- [ ] Open a pull request.

There is no release step. This fork publishes no container image, package, or release. If that ever
changes, reintroduce build and release tooling deliberately and flip
`forgeguard.publishes_artifacts` in `FORK_UPSTREAM_BASE`.
