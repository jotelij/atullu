import brownie
import json
from brownie import (
  Contract,
  accounts,
  config,
  chain,
  network,
  interface,
  AdvancedMultiTrade
)
from web3 import Web3
from rich.console import Console
from scripts.get_weth import get_weth
from scripts.helpers import get_account, FORKED_LOCAL_ENVIROMENTS, approve_erc20
from scripts.utils import chain_data

console = Console()
chain_tokens, chain_routers = chain_data()

starting_eth = 0.1

# usdc_address = chain_tokens["USDC"]
# usdt_address = chain_tokens["USDT"]
# dai_address = chain_tokens["DAI"]
# weth_address = chain_tokens["WETH"]

# sushiswap = chain_routers["sushiswap_v2_02"]
# uniswap = chain_routers["uniswap_v2_02"]


def deploy_contract(account_deploy, eth_amount=0.1, log=False):
  constractf = None
  if len(AdvancedMultiTrade) <= 0:
    amount = Web3.toWei(eth_amount, "ether")
    contractf = AdvancedMultiTrade.deploy({"from": account_deploy})
    #contractf = AdvancedMultiTrade.deploy({"from": account_deploy, "value": amount})
    if log:
      console.log(f"Contract newly deployed: {AdvancedMultiTrade[-1].address}")
  else:
    contractf = AdvancedMultiTrade[-1]
    if log:
      console.log(f"Contract already deployed: {AdvancedMultiTrade[-1].address}")
  return contractf

def token_to_wei(amount, decimal=18):
  return amount * (10**decimal)

def token_read(amount, decimal=18):
  return amount / (10**decimal)

def calc_avg(in_amount, out_amount):
  if out_amount > in_amount:
    avg = ((out_amount - in_amount) / in_amount) * 100
  elif out_amount < in_amount: 
    avg = -1 * (((in_amount - out_amount) /in_amount) * 100)
  else:
    return 0
  return avg

def main():
  account = get_account()
  
  amount = Web3.toWei(starting_eth, "ether")
  adv_trade = AdvancedMultiTrade.deploy({"from": account})
  tx = adv_trade.addStables(["0xC9BdeEd33CD01541e1eeD10f90519d2C06Fe3feB","0xC42C30aC6Cc15faC9bD938618BcaA1a1FaE8501d","0x4988a896b1227218e4A686fdE5EabdcAbd91571f","0x8BEc47865aDe3B172A928df8f990Bc7f2A3b9f79","0x5ce9F0B6AFb36135b5ddBF11705cEB65E634A9dC","0xB12BFcA5A55806AaF64E99521918A4bf0fC40802"], {"from": account})
  tx.wait(1)
  tx2 = adv_trade.addTokens(["0x5ac53f985ea80c6af769b9272f35f122201d0f56","0x4e834cdcc911605227eedddb89fad336ab9dc00a","0x2BAe00C8BC1868a5F7a216E881Bae9e662630111","0xC4bdd27c33ec7daa6fcfd8532ddB524Bf4038096","0x5ce9F0B6AFb36135b5ddBF11705cEB65E634A9dC","0x5C92A4A7f59A9484AFD79DbE251AD2380E589783","0x0fAD0ED848A7A16526E8a7574e418B015Dbf41B5","0x0f00576d07B594Bdc1caf44b6014A6A02E5AFd48","0xdc7acde9ff18b4d189010a21a44ce51ec874ea7c","0xb7e3617adb58dc34068522bd20cfe1660780b750","0x8bec47865ade3b172a928df8f990bc7f2a3b9f79","0x8973c9ec7b79fe880697cdbca744892682764c37","0xb59d0fdaf498182ff19c4e80c00ecfc4470926e2","0x2b9025aecc5ce7a8e6880d3e9c6e458927ecba04","0xe4baf0af161bf03434d1c5a53957981493c12c99","0xdeacf0faa2b80af41470003b5f6cd113d47b4dcd","0xabe9818c5fb5e751c4310be6f0f18c8d85f9bd7f","0x026dda7f0f0a2e42163c9c80d2a5b6958e35fc49","0xe3520349f477a5f6eb06107066048508498a291b","0xe301ed8c7630c9678c39e4e45193d1e7dfb914f7","0xea62791aa682d455614eaa2a12ba3d9a2fd197af","0xda2585430fef327ad8ee44af8f1f989a2a91a3d2","0xc8fdd32e0bf33f0396a18209188bb8c6fb8747d2","0x6454e4a4891c6b78a5a85304d34558dda5f3d6d8","0xE4eB03598f4DCAB740331fa432f4b85FF58AA97E","0x94190d8ef039c670c6d6b9990142e0ce2a1e3178","0xfca152a9916895bf564e3f26a611f9e1e6aa6e73","0x1d1f82d8b8fc72f29a8c268285347563cb6cd8b3","0xd126b48c072f4668e944a8895bc74044d5f2e85b","0x74974575d2f1668c63036d51ff48dbaa68e52408","0xC86Ca2BB9C9c9c9F140d832dE00BfA9e153FA1e3","0xC42C30aC6Cc15faC9bD938618BcaA1a1FaE8501d","0x6EBA841F1201fFDDe7DDC2ba995D3308f6C4aEa0","0x90eb16621274fb47a071001fbbf7550948874cb5","0x449f661c53aE0611a24c2883a910A563A7e42489","0x951cfdc9544b726872a8faf56792ef6704731aae","0x07b2055fbd17b601c780aeb3abf4c2b3a30c7aae","0x885f8CF6E45bdd3fdcDc644efdcd0AC93880c781","0x291c8fceaca3342b29cc36171deb98106f712c66","0x8828a5047d093f6354e3fe29ffcb2761300dc994","0x18921f1e257038e538ba24d49fa6495c8b1617bc","0xdc9be1ff012d3c6da818d136a3b2e5fdd4442f74","0x7821c773a12485b12a2b5b7bc451c3eb200986b1","0xFa94348467f64D5A457F75F8bc40495D33c65aBB","0x984c2505a14da732d7271416356f535953610340","0x1bc741235ec0ee86ad488fa49b69bb6c823ee7b7","0xb12bfca5a55806aaf64e99521918a4bf0fc40802","0x4988a896b1227218e4a686fde5eabdcabd91571f","0x098d5b6a26bca1d71f2335805d71b244f94e8a5f","0xf4eb217ba2454613b15dbdea6e5f22276410e89e","0xf34d508bac379825255cc80f66cbc89dfeff92e4","0x7ca1c28663b76cfde424a9494555b94846205585","0xa64514a8af3ff7366ad3d5daa5a548eefcef85e0","0xE9F226a228Eb58d408FdB94c3ED5A18AF6968fE1"], {"from": account});
  tx2.wait(1)
  amount_wei = Web3.toWei(starting_eth, "ether")
  
  with open('data/aurora_routes.json', "r") as f:
    abconf = json.load(f)
    
  for x in range(1, 3):
    router1 = abconf['routers'][x]['address']
    baseAsset = abconf['baseAssets'][x]['address']
    tradeSize = 0.01 * 10*24
    console.log(f"search for {router1}")
    returnArray = adv_trade.instaSearch(router1, baseAsset, tradeSize)
    amtBack = returnArray[0]
    token2 = returnArray[1]
    token3 = returnArray[2]
    token4 = returnArray[4]
    
    multiplier = 1.01
    profitTarget = tradeSize * multiplier
    if amtBack > profitTarget:
      console.print(f"[green]Good[/green]: {calc_avg(tradeSize, amtBack)}%")
    else:
      console.print(f"[red]Bad[/red]: {calc_avg(tradeSize, amtBack)}%")
 
def aaaaa():
  with open('scripts/routes.json', "r") as f:
    routes = json.load(f)
  
  i = 0
  tager_token = "0xC42C30aC6Cc15faC9bD938618BcaA1a1FaE8501d"
  for route in routes:
    if i == 10:
      pass
    token1 = route[2];
    token2 = route[3];
    if token1.lower() == tager_token.lower():
      otherT = "[yellow]"+token2+"[/yellow]"
      router1 = route[0];
      router2 = route[1];
      
      i += 1
      tradeSize = 7 * 10**24;
      amtBack = adv_trade.estimateDualDexTrade(router1, router2, token1, token2, tradeSize)
      multiplier = 1
      profitTarget = tradeSize * multiplier
      if amtBack > profitTarget:
        console.print(f"[green]Good[/green]: {calc_avg(tradeSize, amtBack)}% - {otherT}")
      else:
        console.print(f"[red]Bad[/red]: {calc_avg(tradeSize, amtBack)}%")

def ana():
  token0= chain_tokens["USDC"]
  token1= chain_tokens["wNEAR"]
  token2= chain_tokens["AURORA"]
  token3= chain_tokens["WANNA"]
  dec = 6
  dec1 = 24
  dec2 = 18
  in_amount = token_to_wei(0.1, decimal=dec)
  
  est_out1 = getAmountOutMin(adv_trade, route1, token0, token1, in_amount)
  console.log(f"T1: {token_read(est_out1, decimal=dec1)}")
  est_out2 = getAmountOutMin(adv_trade, route1, token1, token2, est_out1)
  console.log(f"T2: {token_read(est_out2, decimal=dec2)}")
  est_out3 = getAmountOutMin(adv_trade, route1, token2, token0, est_out2)
  console.log(f"T3: {token_read(est_out3, decimal=dec)}")
  console.log(f"{calc_avg(in_amount, est_out3)}%")
  
# getAmountOutMin(address router, address _tokenIn, address _tokenOut, uint256 _amount) public view returns (uint256 )
def getAmountOutMin(adv_trade, router_add, token_in, token_out, amount):
  try:
    res = adv_trade.getAmountOutMin(router_add, token_in, token_out, amount)
    return res
  except:
    console.log(f"[red]Get minimum amount error")
    return None

# dualDexTrade(address _router1, address _router2, address _token1, address _token2, uint256 _amount) external onlyOwner
def dualDexTrade():
  pass


def recoverEth():
  pass

# getBalance(address _tokenContractAddress) external view  returns (uint256)
def getBalance():
  pass

# recoverTokens(address tokenAddress) external onlyOwner
def recoverTokens():
  pass

# estimateDualDexTrade(address _router1, address _router2, address _token1, address _token2, uint256 _amount) external view returns (uint256)
def estimateDualDexTrade():
  pass
