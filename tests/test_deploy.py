import pytest
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

test_deploy_con()
  account = get_account()
  