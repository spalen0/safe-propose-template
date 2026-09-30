# Safe multisig agent instructions

This template prepares onchain transactions for a Safe multisig using safe-propose.
Keep transaction PRs small and easy to review: the diff should show the requested
onchain actions and only the code needed to build them.

The transaction rules below apply to transaction-only changes and take precedence
over general development defaults that require adding tests or validation code.
Changes to the template, workflow, configuration, or documentation follow normal
development checks and may include relevant tests and documentation updates.

## Transaction changes

- Append a small, clearly named `@txn` function in `scripts/safe_txs.py`. Build calls
  with `batch.add(method, *args)` and use `ctx` for contracts and transaction context.
- Preserve existing functions and formatting; avoid unrelated cleanup, refactoring,
  file moves, or changes to historical transactions.
- Prefer direct contract calls with explicit addresses, amounts, and arguments. Reuse
  existing interfaces and address definitions, including `ctx.const` from an optional
  root-level `constants.py`, when available.
- Include only the requested onchain calls, necessary contract setup, and onchain
  reads needed to calculate arguments. Add an ABI only when a required interface is
  missing; pass `abi=` explicitly on chains without explorer support.
- Do not add unnecessary checks, assertions, address/network validation, balance or
  allowance guards, retries, fallback paths, logging, or defensive wrappers. Rely on
  existing transaction tooling and contract reverts for behavior they already enforce.
- Avoid new helpers, abstractions, dependencies, configuration, CI changes, or README
  edits unless the user explicitly requests that work.

## Transaction verification

- Never add tests when creating transactions or preparing/opening transaction PRs.
  Leave existing tests untouched. Do not add fixtures, mocks, test infrastructure,
  coverage requirements, or test dependencies to a transaction PR.
- Verify transactions through review and the existing local dry-run/simulation
  workflow documented in `README.md`; verification must not expand the committed diff.
- Use the same reviewed safe-propose commit as the repository's `SAFE_PROPOSE_REF`
  for local simulation. Do not install the engine from a moving branch or add it to
  `requirements.txt`.
- Never commit private keys, API tokens, RPC URLs containing credentials, or a filled
  `.env`. Use untracked environment files and GitHub secrets for credentials.

## Review and transaction PRs

- Check the intended chain, Safe, target contracts, recipients, amounts, token decimals,
  and call order before preparing the batch. Resolve missing transaction details rather
  than inventing them or adding speculative validation code.
- Run `safe-propose dry-run --fn <function> --network <network>` locally before opening
  a transaction PR, including a draft PR. Review the decoded calls and simulation
  result. Open the PR only after the local simulation succeeds. If simulation fails
  or cannot run, resolve the failure or report the blocker before opening the PR.
- Before opening a transaction PR, inspect the diff and remove changes unrelated to
  the requested transactions. Prefer changing only `scripts/safe_txs.py`.
- Keep the PR title and description brief and factual: requested action, network,
  relevant addresses/amounts, and the local simulation command and result.
- Preparing or opening a PR does not authorize proposing, signing, or executing the
  transaction. Use `send=true` only when the user explicitly authorizes sending; a
  PR-comment request must include `sha=<current PR head commit>`.

## Template maintenance

- Keep `README.md`, `ape-config.yaml`, `.env.example`, and the workflow consistent with
  the files and behavior that actually ship. Keep the engine pinned to a reviewed SHA.
- Run checks relevant to the changed files. The transaction-only restrictions and
  local transaction simulation gate do not apply to template maintenance PRs.
