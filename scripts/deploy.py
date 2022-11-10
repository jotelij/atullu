import brownie
from brownie import (
  Contract,
  accounts,
  config,
  chain,
  network,
  interface,
  MultiTrade
)
from web3 import Web3
from scripts.get_weth import get_weth
from scripts.helpers import get_account, FORKED_LOCAL_ENVIROMENTS, approve_erc20
from scripts.swap import swap
from rich.console import Console
from scripts.utils import chain_data
from chainlink_mapping import price_feed_mapping
from scripts.chainlink.chainlink import get_asset_price


chain_tokens, chain_routers = chain_data()

console = Console()
amount_eth = 0.1

def main():
  multi_swap()

def get_token():
  console.log("stating...")
  account = get_account()
  bnt_address = chain_tokens["BNT"]
  dai_address = chain_tokens["DAI"]
  weth_address = chain_tokens["WETH"]
  sushiswap02_router02 = chain_routers["uniswap_v2_02"]
  amount_to_swap = Web3.toWei(amount_eth, "ether")
  dai = interface.IERC20(dai_address)
  bnt = interface.IERC20(bnt_address)
  console.log(f"[green]DAI is: [/green]{Web3.fromWei(dai.balanceOf(account.address), 'ether')}")
  console.log(f"[green]BNT is: [/green]{Web3.fromWei(bnt.balanceOf(account.address), 'ether')}")
  # if network.show_active() in FORKED_LOCAL_ENVIROMENTS:
  #   get_weth(account=account)
  # tx = approve_erc20(amount_to_swap, sushiswap02_router02, weth_address, account)
  # tx.wait(1)
  #get_token_for_exact_eth(amount_eth, dai_address, sushiswap02_router02)
  #console.log(f"[green]BNT is: [/green]{Web3.fromWei(bnt_amount, 'ether')}")
  bancor_eth_address = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
  
  # bacor_weth = interface.IERC20(bancor_eth_address)
  # txa = bacor_weth.deposit({"from": account, "value": amount_to_swap})
  # txa.wait(1)
  price_feed_address = price_feed_mapping[network.show_active()][
    (bnt_address, weth_address)
  ]
  from_to_price = get_asset_price(address_price_feed=price_feed_address)
  from_to_price = 1 / from_to_price
  bnt_amount = int((from_to_price * 0.90) * amount_to_swap)
  # swap(
  #   weth_address,
  #   bnt_address,
  #   amount_to_swap,
  #   account,
  #   price_feed_address,
  #   sushiswap02_router02,
  #   reverse_feed=True,
  # )
  #console.log(f"[green]BNT is: [/green]{Web3.fromWei(bnt.balanceOf(account.address), 'ether')}")
  cont = deploy_con(account)
  console.log(f"[green]My start ETH is: [/green]{Web3.fromWei(account.balance(), 'ether')}")
  console.log(f"[green]Contract start ETH is: [/green]{Web3.fromWei(cont.balance(), 'ether')}")
  timestamp = chain[brownie.web3.eth.get_block_number()]["timestamp"] + 200
  tx2 = cont.multiSwap(timestamp, bnt_amount,  bnt_amount, bnt_amount,  {"from": account, "value": amount_to_swap})
  #tx2 = cont.multiSwap(timestamp, Web3.toWei(bnt_amount, 'ether'),  Web3.toWei(bnt_amount, 'ether'), Web3.toWei(bnt_amount, 'ether'),  {"from": account, "value": amount_to_swap})
  tx2.wait(1)
  #console.log(f"Tx DIA: {tx}")
  console.log(f"[green]My end ETH is: [/green]{Web3.fromWei(account.balance(), 'ether')}")
  console.log(f"[green]Contract end ETH is: [/green]{Web3.fromWei(cont.balance(), 'ether')}")
  console.log(f"[green]BNT is: [/green]{Web3.fromWei(dai.balanceOf(cont.address), 'ether')}")
  #console.log(f"[green]DAI is: [/green]{Web3.fromWei(dai.balanceOf(account.address), 'ether')}")

def multi_swap():
  console.log("stating...")
  account = get_account()
  bnt_address = chain_tokens["BNT"]
  dai_address = chain_tokens["DAI"]
  weth_address = chain_tokens["WETH"]
  sushiswap02_router02 = chain_routers["uniswap_v2_02"]
  amount_to_swap = Web3.toWei(amount_eth, "ether")
  dai = interface.IERC20(dai_address)
  bnt = interface.IERC20(bnt_address)
  
  price_feed_address = price_feed_mapping[network.show_active()][
    (bnt_address, weth_address)
  ]
  from_to_price = get_asset_price(address_price_feed=price_feed_address)
  from_to_price = 1 / from_to_price
  min_bnt_out = int((from_to_price * 0.90) * amount_to_swap)
  cont = deploy_con(account)
  console.log(f"[green]Contract start ETH is: [/green]{Web3.fromWei(cont.balance(), 'ether')}")
  timestamp = chain[brownie.web3.eth.get_block_number()]["timestamp"] + 200
  tx2 = cont.multiSwapPreview({"from": account, "value": amount_to_swap})
  #tx2 = cont.multiSwap(timestamp, min_bnt_out,  min_bnt_out, min_bnt_out,  {"from": account, "value": amount_to_swap})
  tx2.wait(1)
  console.log(tx2)
  console.log(f"[green]My end ETH is: [/green]{Web3.fromWei(account.balance(), 'ether')}")
  console.log(f"[green]Contract end ETH is: [/green]{Web3.fromWei(cont.balance(), 'ether')}")
  console.log(f"[green]DAI is: [/green]{Web3.fromWei(dai.balanceOf(cont.address), 'ether')}")
  console.log(f"[green]BNT is: [/green]{Web3.fromWei(bnt.balanceOf(cont.address), 'ether')}")

def deploy_con(account):
  constractf = None
  if len(MultiTrade) <= 0:
    contractf = MultiTrade.deploy({"from": account})
    console.log(f"Contract newly deployed: {MultiTrade[-1].address}")
  else:
    contractf = MultiTrade[-1]
    console.log(f"Contract already deployed: {MultiTrade[-1].address}")
  return contractf

def delopy_tokens(account=None):
  account = account if account is not None else get_account()
  