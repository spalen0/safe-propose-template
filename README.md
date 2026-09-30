# Safe multisig

Propose [Safe](https://safe.global) transactions from pull requests with
[safe-propose](https://github.com/spalen0/safe-propose). Write a transaction as a Python
function, open a PR, and comment:

```
/safe-propose fn=<name> network=<net> send=false
```

The workflow simulates the batch on a fork and posts the calldata, a wallet-verifiable
preview, and the `safe_tx_hash` to the PR. With `send=true` it proposes the transaction
to the Safe queue with a delegate key; the Safe owners still sign it.

## Setup

1. **Create a repository from this template** (Use this template → Create a new
   repository). Only people with write access can trigger the workflow, and PRs from
   forks are rejected, so the repository can be private or public.
2. **Keep only your chains** in [`ape-config.yaml`](ape-config.yaml).
3. **Pin the engine.** Add the repository variable `SAFE_PROPOSE_REF` with a reviewed
   commit SHA of safe-propose; bump it to upgrade:

   ```bash
   git ls-remote https://github.com/spalen0/safe-propose.git master
   ```

4. **Add a proposer.** Create a fresh key used only for this, and add its address as a
   proposer (delegate) of the Safe on every chain you send on, in the Safe web app or
   with `ape safe delegates add`. It can queue transactions but not sign them.
5. **Set secrets and variables** (Settings → Secrets and variables → Actions) for the
   chains you use.
6. **Try it:** open a PR and comment `/safe-propose fn=smoke_test network=<net> send=false`.

### Secrets

| Name | Needed for | Purpose |
|---|---|---|
| `PROPOSER_PRIVATE_KEY` | `send` | Proposer (delegate) key from step 4. |
| `<PREFIX>_RPC` | each chain you use | Fork-capable RPC URL: `ETH_RPC`, `BASE_RPC`, `ARB_RPC`, `OP_RPC`, `HYPEREVM_RPC`, `KATANA_RPC`, `RISE_RPC`, `ROBINHOOD_RPC`. |
| `APE_SAFE_GATEWAY_API_KEY` | `send` on gateway chains | Safe API key for `api.safe.global` (Ethereum, Base, Arbitrum, Optimism, HyperEVM, Robinhood). Not needed for Katana or RISE. |
| `ETHERSCAN_TOKEN`, `BASESCAN_TOKEN`, `ARBISCAN_TOKEN`, `OPTIMISTIC_ETHERSCAN_TOKEN` | optional | Explorer ABI lookups for `ctx.contract` without `abi=`. |
| `TELEGRAM_TOKEN` | optional | Bot token for the "tx queued" message. |

### Variables

| Name | Needed for | Purpose |
|---|---|---|
| `SAFE_PROPOSE_REF` | always | Engine commit SHA (step 3). |
| `ETH_SAFE_ADDRESS` | fallback | Safe address for any chain without its own `<PREFIX>_SAFE_ADDRESS`. |
| `<PREFIX>_SAFE_ADDRESS` | each chain whose Safe differs | e.g. `BASE_SAFE_ADDRESS`, `KATANA_SAFE_ADDRESS`. |
| `TELEGRAM_CHAT_ID` | optional | Telegram group id for notifications. |

No personal access token is needed: the workflow uses the built-in `GITHUB_TOKEN`.

## Writing transactions

Add `@txn` functions to [`scripts/safe_txs.py`](scripts/safe_txs.py). The function name is
the `fn=` value:

```python
from safe_propose import txn


@txn
def approve_usdc(batch, ctx):
    """Approve SPENDER for 1,000 USDC."""
    usdc = ctx.contract(ctx.const["USDC"], abi=ERC20)
    batch.add(usdc.approve, ctx.const["SPENDER"], 1_000 * 10**6)
```

- `batch.add(method, *args)` queues one call; several calls become one MultiSend batch.
- `ctx.contract(address, abi=None)` loads a contract. Pass `abi=` when the chain has no
  explorer support (e.g. Katana).
- Shared addresses go in an optional `constants.py` at the repo root and are read with
  `ctx.const["NAME"]`.
- Extra Python packages your functions import go in `requirements.txt`. Do not add
  `safe-propose` there; the workflow installs the pinned engine itself.

## Proposing

| Comment | Result |
|---|---|
| `/safe-propose fn=<name> network=<net> send=false` | Dry-run: simulation and calldata posted to the PR. |
| `/safe-propose fn=<name> network=<net> send=true sha=<head sha>` | Simulates, proposes to the Safe queue, labels and closes the PR, opens a reminder issue, and notifies Telegram. |

`send=true` needs `sha=` equal to the PR's current head commit (`git rev-parse HEAD`), so
a later push cannot ride an earlier approval. Both can also be started from the Actions
tab (workflow_dispatch).

## Running locally

Set `SAFE_PROPOSE_REF` to the same reviewed commit SHA as the repository variable used
by CI, then install that revision:

```bash
python -m venv .venv && . .venv/bin/activate
export SAFE_PROPOSE_REF="<reviewed-commit-sha>"
pip install "safe-propose @ git+https://github.com/spalen0/safe-propose.git@${SAFE_PROPOSE_REF}"
# plus the anvil binary: https://book.getfoundry.sh/getting-started/installation
export ETH_RPC=... ETH_SAFE_ADDRESS=0x...
safe-propose dry-run --fn smoke_test --network ethereum
```

The CLI reads the environment only. [`.env.example`](.env.example) lists every variable;
never commit a filled copy.

Supported chains, adding a chain, and all CLI options:
[safe-propose README](https://github.com/spalen0/safe-propose#readme).
