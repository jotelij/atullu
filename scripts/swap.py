import brownie
from brownie import (
  Contract,
  accounts,
  config,
  network,
  chain,
  MultiTrade,
  interface,
)
from web3 import Web3
from rich.console import Console
from scripts.utils import chain_data
from scripts.helpers import get_account, approve_erc20, FORKED_LOCAL_ENVIROMENTS
from scripts.chainlink.chainlink import get_asset_price


chain_tokens, _ = chain_data()

console = Console()
multi_factor = 1200

def get_token_for_exact_eth(eth_amount, address_to_token, router_address, to_account=None):
  account = get_account()
  amount_to_swap = Web3.toWei(eth_amount, "ether")
  if account.balance() <= amount_to_swap:
    raise "No enough balance"
  min_amount_needed = eth_amount * multi_factor
  to_account_address = to_account.address if to_account is not None else account.address
  
  address_from_token = chain_tokens["WETH"]
  path = [
    address_from_token,
    address_to_token,
  ]
  timestamp = chain[brownie.web3.eth.get_block_number()]["timestamp"] + 120
  routerv2 = interface.IUniswapV2Router02(router_address)
  swap_tx = routerv2.swapExactETHForTokens(
    min_amount_needed, path, to_account_address, timestamp, {"from": account, "value": amount_to_swap}
  )
  swap_tx.wait(1)
  return swap_tx
  
def swap(
  address_from_token,
  address_to_token,
  amount,
  account,
  price_feed_address,
  swap_router_address,
  reverse_feed=False,
):
  path = [
    address_from_token,
    address_to_token,
  ]
  # The pool jumping path to swap your token
  from_to_price = get_asset_price(address_price_feed=price_feed_address)
  if reverse_feed:
    from_to_price = 1 / from_to_price
  # amountOutMin = int((from_to_price * 0.5) * 10 ** 18)
  # 98 is 2% slippage
  # I get a little weird with units here
  # from_to_price isn't in wei, but amount is
  amountOutMin = int((from_to_price * 0.90) * amount)
  timestamp = chain[brownie.web3.eth.get_block_number()]["timestamp"] + 120
  routerv2 = interface.IUniswapV2Router02(swap_router_address)
  swap_tx = routerv2.swapExactTokensForTokens(
    amount, amountOutMin, path, account.address, timestamp, {"from": account}
  )
  swap_tx.wait(1)
  return swap_tx

