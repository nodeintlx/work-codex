# Private GitHub Setup

This repository should be hosted privately.

## Recommended approach

1. Create a new private GitHub repository.
2. Add the new repository as `origin`.
3. Push the current branch.

## Commands

```bash
git remote remove origin 2>/dev/null || true
git remote add origin git@github.com:<your-org-or-user>/work-codex.git
git branch -M main
git push -u origin main
```

## Notes

- Review sensitive files before the first push.
- `knowledge/memory.jsonl` is already ignored because it is volatile and sensitive.
- You may want to keep some large evidence files out of GitHub long-term and move them to encrypted object storage with manifests in Git.
- If you want multi-computer access immediately, GitHub is the right next step after this initial cleanup and first commit.
