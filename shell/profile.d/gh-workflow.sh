#!/usr/bin/env bash
# gh CLI helpers — sourced from ~/.zprofile.d

_repo_from_remote() {
  git remote get-url "$1" 2>/dev/null | awk -F'[/:]' '{gsub(/\.git$/,""); print $(NF-1)"/"$NF}'
}

_upstream_default_branch() {
  git remote show upstream 2>/dev/null | awk '/HEAD branch/ {print $NF}'
}

gh-sync() {
  # Sync fork branch with upstream. Optional branch (default: upstream HEAD).
  local repo branch
  repo=$(_repo_from_remote origin)
  branch=$1
  if [ -z "$branch" ]; then
    branch=$(_upstream_default_branch)
  fi
  branch=${branch:-main}
  gh repo sync "$repo" --branch "$branch"
  git fetch origin "$branch"
  git checkout "$branch"
  git pull --ff-only origin "$branch"
}

gh-rebase-prs() {
  # Rebase open PRs server-side. Optional base branch filter.
  local upstream_repo repo base filter failures pr
  upstream_repo=$(_repo_from_remote upstream)
  if [ -n "$upstream_repo" ]; then
    repo=$upstream_repo
  else
    repo=$(_repo_from_remote origin)
  fi
  base=$1
  filter=()
  [[ -n "${base:-}" ]] && filter=(--base "$base")
  failures=0
  while IFS= read -r pr; do
    [ -z "$pr" ] && continue
    echo "Rebasing PR #$pr..."
    if ! gh pr update-branch "$pr" --rebase --repo "$repo" 2>&1; then
      echo "  FAILED: PR #$pr"
      ((failures++))
    fi
  done < <(gh pr list --author @me --state open "${filter[@]}" --json number -q '.[].number' --repo "$repo")
  if [ "$failures" -gt 0 ]; then
    echo "$failures PR(s) failed to rebase."
    return 1
  fi
}

gh-clean() {
  # Delete local branches whose PRs are merged. Pass --dry-run to preview.
  local dry merged_prs current b
  dry=false
  [[ "${1:-}" == "--dry-run" ]] && dry=true
  merged_prs=$(gh pr list --author @me --state merged --json headRefName -q '.[].headRefName')
  current=$(git branch --show-current)
  while IFS= read -r b; do
    [ -z "$b" ] && continue
    [[ "$b" == "$current" ]] && continue
    if echo "$merged_prs" | grep -qx "$b"; then
      if $dry; then
        echo "  would delete: $b"
      else
        git branch -D "$b"
      fi
    fi
  done < <(git branch --format='%(refname:short)')
}

gh-wip() {
  # List local branches with no open or merged PR. Optional default branch name.
  local open_prs merged_prs current default b last
  open_prs=$(gh pr list --author @me --state open --json headRefName -q '.[].headRefName')
  merged_prs=$(gh pr list --author @me --state merged --json headRefName -q '.[].headRefName')
  current=$(git branch --show-current)
  default=$1
  if [ -z "$default" ]; then
    default=$(_upstream_default_branch)
  fi
  default=${default:-main}
  while IFS= read -r b; do
    [ -z "$b" ] && continue
    [[ "$b" == "$current" || "$b" == "$default" ]] && continue
    if echo "$merged_prs" | grep -qx "$b"; then
      continue
    elif echo "$open_prs" | grep -qx "$b"; then
      continue
    fi
    last=$(git log -1 --format='%cr' "$b")
    echo "  $b  ($last)"
  done < <(git branch --format='%(refname:short)')
}

gh-sync-directory() {
  local target_dir="${1:-.}"
  
  if [[ ! -d "$target_dir" ]]; then
    echo "Error: Directory '$target_dir' not found" >&2
    return 1
  fi
  
  local count=0
  local failed=0
  local original_dir="$PWD"
  
  for repo_path in "$target_dir"/*; do
    [[ -d "$repo_path" ]] || continue
    [[ -d "$repo_path/.git" ]] || continue
    
    echo "Syncing: $(basename "$repo_path")"
    (
      cd "$repo_path" || return 1
      if gh-sync; then
        return 0
      else
        return 1
      fi
    )
    
    if [[ $? -eq 0 ]]; then
      ((count++))
    else
      ((failed++))
      echo "  ✗ Failed: $(basename "$repo_path")" >&2
    fi
  done
  
  cd "$original_dir" || return 1
  
  echo ""
  echo "Synced: $count repos"
  [[ $failed -gt 0 ]] && echo "Failed: $failed repos" >&2
  
  [[ $failed -eq 0 ]]
}