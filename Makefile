gup:
	ganache-cli --chain.vmErrorsOnRPCResponse true --wallet.totalAccounts 10 --hardfork istanbul --fork.url https://mainnet.infura.io/v3/7d49c365d9e643f6b241e9de16ff12d2 --miner.blockGasLimit 12000000 --wallet.mnemonic brownie --server.port 8545 --chain.chainId 1
