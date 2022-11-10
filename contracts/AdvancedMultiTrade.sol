// SPDX-License-Identifier: MIT
pragma solidity >=0.8.17;
pragma abicoder v2;

import {IERC20, SafeERC20} from './SafeERC20.sol';
import "@openzeppelin/contracts/access/Ownable.sol";
import "../interfaces/Uniswap/V2/IUniswapV2Router02.sol";
import "../interfaces/Uniswap/V2/IUniswapV2Pair.sol";


contract AdvancedMultiTrade is Ownable {
  using SafeERC20 for IERC20;
  
  address [] public routers;
  address [] public tokens;
  address [] public stables;
  
  function addRouters(address[] calldata _routers) external onlyOwner {
    for (uint i=0; i<_routers.length; i++) {
      routers.push(_routers[i]);
    }
  }

  function addTokens(address[] calldata _tokens) external onlyOwner {
    for (uint i=0; i<_tokens.length; i++) {
      tokens.push(_tokens[i]);
    }
  }

  function addStables(address[] calldata _stables) external onlyOwner {
    for (uint i=0; i<_stables.length; i++) {
      stables.push(_stables[i]);
    }
  }
  
  function swap(address router, address _tokenIn, address _tokenOut, uint256 _amount) private {
    IERC20(_tokenIn).approve(router, _amount);
    address[] memory path;
    path = new address[](2);
    path[0] = _tokenIn;
    path[1] = _tokenOut;
    uint deadline = block.timestamp + 300;
    IUniswapV2Router02(router).swapExactTokensForTokens(_amount, 1, path, address(this), deadline);
  }
    
  function getAmountOutMin(address router, address _tokenIn, address _tokenOut, uint256 _amount) public view returns (uint256 ) {
    address[] memory path;
    path = new address[](2);
    path[0] = _tokenIn;
    path[1] = _tokenOut;
    uint256 result = 0;
    try IUniswapV2Router02(router).getAmountsOut(_amount, path) returns (uint256[] memory amountOutMins) {
      result = amountOutMins[path.length -1];
    } catch {
    }
    return result;
  }

  function estimateDualDexTrade(address _router1, address _router2, address _token1, address _token2, uint256 _amount) external view returns (uint256) {
    uint256 amtBack1 = getAmountOutMin(_router1, _token1, _token2, _amount);
    uint256 amtBack2 = getAmountOutMin(_router2, _token2, _token1, amtBack1);
    return amtBack2;
  }
  
  function dualDexTrade(address _router1, address _router2, address _token1, address _token2, uint256 _amount) external onlyOwner {
    uint startBalance = IERC20(_token1).balanceOf(address(this));
    uint token2InitialBalance = IERC20(_token2).balanceOf(address(this));
    swap(_router1,_token1, _token2,_amount);
    uint token2Balance = IERC20(_token2).balanceOf(address(this));
    uint tradeableAmount = token2Balance - token2InitialBalance;
    swap(_router2,_token2, _token1,tradeableAmount);
    uint endBalance = IERC20(_token1).balanceOf(address(this));
    require(endBalance > startBalance, "Trade Reverted, No Profit Made");
  }
  
  function swapa(address[] memory tos, bytes[] memory data) external payable {
    require(tos.length > 0 && tos.length == data.length, "Invalid input");
  
    for(uint256 i; i < tos.length; i++) {
      (bool success,bytes memory returndata) = tos[i].call{value: address(this).balance, gas: gasleft()}(data[i]);
      require(success, string(returndata));
    }
  }
  
  function instaSearch(address _router, address _baseAsset, uint256 _amount) external view returns (uint256,address,address,address) {
    uint256 amtBack;
    address token1;
    address token2;
    address token3;
    for (uint i1=0; i1<tokens.length; i1++) {
      for (uint i2=0; i2<stables.length; i2++) {
        for (uint i3=0; i3<tokens.length; i3++) {
          amtBack = getAmountOutMin(_router, _baseAsset, tokens[i1], _amount);
          amtBack = getAmountOutMin(_router, tokens[i1], stables[i2], amtBack);
          amtBack = getAmountOutMin(_router, stables[i2], tokens[i3], amtBack);
          amtBack = getAmountOutMin(_router, tokens[i3], _baseAsset, amtBack);
          if (amtBack > _amount) {
            token1 = tokens[i1];
            token2 = tokens[i2];
            token3 = tokens[i3];
            break;
          }
        }
      }
    }
    return (amtBack,token1,token2,token3);
  }

  function instaTrade(address _router1, address _token1, address _token2, address _token3, address _token4, uint256 _amount) external onlyOwner {
    uint startBalance = IERC20(_token1).balanceOf(address(this));
    uint token2InitialBalance = IERC20(_token2).balanceOf(address(this));
    uint token3InitialBalance = IERC20(_token3).balanceOf(address(this));
    uint token4InitialBalance = IERC20(_token4).balanceOf(address(this));
    swap(_router1,_token1, _token2, _amount);
    uint tradeableAmount2 = IERC20(_token2).balanceOf(address(this)) - token2InitialBalance;
    swap(_router1,_token2, _token3, tradeableAmount2);
    uint tradeableAmount3 = IERC20(_token3).balanceOf(address(this)) - token3InitialBalance;
    swap(_router1,_token3, _token4, tradeableAmount3);
    uint tradeableAmount4 = IERC20(_token4).balanceOf(address(this)) - token4InitialBalance;
    swap(_router1,_token4, _token1, tradeableAmount4);
    require(IERC20(_token1).balanceOf(address(this)) > startBalance, "Trade Reverted, No Profit Made");
  }

  
  function getBalance(address _tokenContractAddress) external view  returns (uint256) {
    uint balance = IERC20(_tokenContractAddress).balanceOf(address(this));
    return balance;
  }
  
  function recoverEth() external onlyOwner {
    payable(msg.sender).transfer(address(this).balance);
  }

  function recoverTokens(address tokenAddress) external onlyOwner {
    IERC20 token = IERC20(tokenAddress);
    token.transfer(msg.sender, token.balanceOf(address(this)));
  }
}