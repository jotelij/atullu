from web3 import Web3
from brownie import (
  Contract,
  accounts,
  config,
  network,
  MockV3Aggregator,
  interface,
)
from rich.console import Console

console = Console()

DEBUG = True
FORKED_LOCAL_ENVIROMENTS = [
  "mainnet-fork",
  "mainnet-fork-alchemy",
  "mainnet-fork-dev",
  "ganache-local",
  "aurora-main-fork",
  "aurora-local",
]
LOCAL_BLOCKCHAIN_ENVIROMENTS = ["development"]

LOCAL_ENV = FORKED_LOCAL_ENVIROMENTS + LOCAL_BLOCKCHAIN_ENVIROMENTS



ETHERIUM_ENVS = [
  "mainnet-fork",
  "mainnet-fork-alchemy",
  "mainnet-fork-dev",
  "development"
]


DECIMAL = 8
#STARTING_PRICE = 100000000000
STARTING_PRICE = 1.45 * 10**8

contract_to_mock = {
  "dai_eth_price_feed": MockV3Aggregator
}

def is_local_env():
  if network.show_active() in LOCAL_ENV:
    return True
  return False

def get_account(index=None, id=None):
  if index:
    return accounts[index]
  if id:
    return accounts.load(id)
  if is_local_env():
    return accounts[0]
  return accounts.add(config["wallets"]["from_key"])

def deploy_mocks(decimals=DECIMAL, starting_price=STARTING_PRICE):
  MockV3Aggregator.deploy(decimals, starting_price, {"from": get_account()})
  print(
    "A new mock instance for V3Aggregator Contract has been created at address:",
    MockV3Aggregator[-1].address,
  )

def get_contract(contract_name, isInterfaced = False):
  print("****** Getting contract ", contract_name, " ***********")
  contract_type = contract_to_mock[contract_name]
  
  if is_local_env() and isInterfaced == False:
    print(
      "Environment is local .... a mock contract is required for",
      contract_name,
    )
    if len(contract_type) <= 0:
      print("Creating a new mock instance for ", contract_name, " contract...")
      deploy_mocks()
    else:
      print(
        "An existing mock instance for ",
        contract_name,
        " contract has been identified at address:",
        contract_type[-1].address,
      )
    contract = contract_type[-1]
  else:
    print(
      "Environment is not Local .... getting network ",
      contract_name,
      " contract instance",
    )
    contract_address = config["networks"][network.show_active()][contract_name]
    if isInterfaced:
      contract_interface = contract_to_mock[contract_name][1]
      if contract_interface is None:
        #TODO: raise exception
        pass
      contract = contract_interface(contract_address)
    else:
      contract = Contract.from_abi(
        contract_type._name, contract_address, contract_type.abi
      )
  return contract


def approve_erc20(amount, to, erc20_address, account):
  console.log("Approving ERC20...")
  erc20 = interface.IERC20(erc20_address)
  tx_hash = erc20.approve(to, amount, {"from": account})
  tx_hash.wait(1)
  console.log("ERC20 Approved")
  return tx_hash