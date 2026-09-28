"""Safe transactions for this multisig.

Each ``@txn`` function builds one Safe batch. Run it from a PR with
``/safe-propose fn=<function name> network=<net>``. The docstring is the fallback
Telegram description when the PR has no body.

``batch.add(method, *args)`` queues a call; ``ctx`` gives you:
  ctx.contract(address, abi=None)  Ape contract (pass ``abi=`` on chains without an explorer)
  ctx.safe_address, ctx.network, ctx.chain_id
  ctx.const                        names from an optional ``constants.py`` at the repo root
"""

from safe_propose import txn


@txn
def smoke_test(batch, ctx):
    """Re-set the Safe's threshold to its current value (no-op to test the setup)."""
    safe = ctx.contract(ctx.safe_address)
    batch.add(safe.changeThreshold, safe.getThreshold())


# Example: approve a spender on an ERC-20. Put the addresses in constants.py, e.g.
#   USDC = "0x..."
#   SPENDER = "0x..."
#
# ERC20 = [
#     {
#         "name": "approve",
#         "type": "function",
#         "stateMutability": "nonpayable",
#         "inputs": [{"name": "spender", "type": "address"}, {"name": "amount", "type": "uint256"}],
#         "outputs": [{"type": "bool"}],
#     }
# ]
#
#
# @txn
# def approve_usdc(batch, ctx):
#     """Approve SPENDER for 1,000 USDC."""
#     usdc = ctx.contract(ctx.const["USDC"], abi=ERC20)
#     batch.add(usdc.approve, ctx.const["SPENDER"], 1_000 * 10**6)
