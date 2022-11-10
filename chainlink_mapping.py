from brownie import config, network
from scripts.utils import chain_data

chain_tokens, _ = chain_data()

price_feed_mapping = {
  "mainnet-fork": {
    (
      chain_tokens["DAI"],
      chain_tokens["WETH"],
    ): "0x773616E4D11A78F511299002DA57A0A94577F1F4",
    (
      chain_tokens["BNT"],
      chain_tokens["WETH"],
    ): "0xcf61d1841b178fe82c8895fe60c2edda08314416",
  },
  "ganache-local": {
    (
      chain_tokens["DAI"],
      chain_tokens["WETH"],
    ): "0x773616E4D11A78F511299002DA57A0A94577F1F4",
    (
      chain_tokens["BNT"],
      chain_tokens["WETH"],
    ): "0xcf61d1841b178fe82c8895fe60c2edda08314416",
  },
  "ropsten": {
    (
      chain_tokens["DAI"],
      chain_tokens["WETH"],
    ): "0x773616E4D11A78F511299002DA57A0A94577F1F4",
  }
}