from scripts.helpers import get_account
from brownie import interface, network, config
from web3 import Web3
from rich.console import Console
from scripts.utils import chain_data


chain_tokens, _ = chain_data()
console = Console()

def main():
  get_weth()

def get_weth(account=None, deposit_eth = 0.1):
  """
  Mints WETH by depositing ETH
  """
  console.log("Getting WETH...")
  #account = get_account()
  account = (
    account if account else get_account()
  )
  weth = interface.IWETH9(
    chain_tokens["WETH"]
  )
  tx = weth.deposit({"from": account, "value": (deposit_eth * 1e18)})
  tx.wait(1)
  console.log({
    'Deposited': f'{deposit_eth} ETH',
    'Recieved': f'{weth.balanceOf(account) / (10 ** 18)} weth',
  })
  
  return tx

def get_weth_wei(amount, account=None):
  """
  Mints WETH by depositing ETH
  """
  console.log("Getting WETH...")
  account = (
    account if account else get_account()
  )
  weth = interface.IWETH9(chain_tokens["WETH"])
  tx = weth.deposit({"from": account, "value": amount})
  tx.wait(1)
  console.log(f"Minted WETH: {deposit_eth}")
  return tx