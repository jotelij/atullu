// contracts/GLDToken.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract TulluToken is ERC20 {
    constructor(uint256 initialSupply) public ERC20("Tullu", "TLL") {
        _mint(msg.sender, initialSupply);
    }
}