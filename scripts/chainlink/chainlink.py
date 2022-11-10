from web3 import Web3
from brownie import interface, network, config
from scripts.helpers import get_contract
from rich.console import Console

console = Console()
  
def get_asset_price(address_price_feed="0x773616E4d11A78F511299002da57A0a94577F1f4"):
  # For mainnet we can just do:
  # return Contract(f"{pair}.data.eth").latestAnswer() / 1e8
  console.log(f"Getting asset price: [yellow]{address_price_feed}")
  price_feed = interface.IAggregatorV3(address_price_feed)
  latest_price = Web3.fromWei(price_feed.latestRoundData()[1], "ether")
  console.log(f"Price is [yellow]{float(latest_price)}")
  return float(latest_price)