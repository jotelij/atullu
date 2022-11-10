// SPDX-License-Identifier: MIT
pragma solidity >=0.4.16 <0.9.0;

pragma abicoder v2;

import "../interfaces/Uniswap/V3/ISwapRouter.sol";
import "../interfaces/Uniswap/V3/IQuoter.sol";
//import "../interfaces/IERC20.sol";
import {IERC20, SafeERC20} from './SafeERC20.sol';
 
import "../interfaces/Uniswap/V2/IUniswapV2Router02.sol";
import "../interfaces/Bancor/IBancorNetwork.sol";

interface IUniswapRouter is ISwapRouter {
    function refundETH() external payable;
}

contract MultiTrade {
    using SafeERC20 for IERC20;
    
  // Bancor
  IBancorNetwork private constant bancorNetwork = IBancorNetwork(0x0e936B11c2e7b601055e58c7E32417187aF4de4a);
  address private constant BANCOR_ETH_ADDRESS = 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE;
  address private constant BANCOR_ETHBNT_POOL = 0xb1CD6e4153B2a390Cf00A6556b0fC1458C4A5533;
  address private constant BNT = 0x1F573D6Fb3F13d689FF844B4cE37794d79a7FF1C;
  
  // SushiSwap
  IUniswapV2Router02 private constant sushiRouter = IUniswapV2Router02(0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F);
  address private constant INJ = 0xe28b3B32B6c345A34Ff64674606124Dd5Aceca30;
  
  // Uniswap
  IUniswapRouter private constant uniswapRouter = IUniswapRouter(0xE592427A0AEce92De3Edee1F18E0157C05861564);
  address private constant DAI = 0x6B175474E89094C44Da98b954EedeAC495271d0F;
  
  constructor() {
      IERC20(BNT).safeApprove(address(sushiRouter), type(uint256).max);
      IERC20(INJ).safeApprove(address(uniswapRouter), type(uint256).max);
  }
  
function _tradeOnBancor(uint256 amountIn, uint256 amountOutMin) private {
  bancorNetwork.convertByPath{value: msg.value}(_getPathForBancor(), amountIn, amountOutMin, address(0), address(0), 0);
}
  
function _getPathForBancor() private pure returns (address[] memory) {
    address[] memory path = new address[](3);
    path[0] = BANCOR_ETH_ADDRESS;
    path[1] = BANCOR_ETHBNT_POOL;
    path[2] = BNT;
    
    return path;
}
 
  
function _tradeOnSushi(uint256 amountIn, uint256 amountOutMin, uint256 deadline) private {
    address recipient = address(this);
      
    sushiRouter.swapExactTokensForTokens(
        amountIn,
        amountOutMin,
        _getPathForSushiSwap(),
        recipient,
        deadline
    );
}

function _getPathForSushiSwap() private pure returns (address[] memory) {
    address[] memory path = new address[](2);
    path[0] = BNT;
    path[1] = INJ;
    
    return path;
}

function _tradeOnUniswap(uint256 amountIn, uint256 amountOutMin, uint256 deadline) private {
    address tokenIn = INJ;
    address tokenOut = DAI;
    uint24 fee = 3000;
    address recipient = msg.sender;
    uint160 sqrtPriceLimitX96 = 0;
    
    ISwapRouter.ExactInputSingleParams memory params = ISwapRouter.ExactInputSingleParams(
        tokenIn,
        tokenOut,
        fee,
        recipient,
        deadline,
        amountIn,
        amountOutMin,
        sqrtPriceLimitX96
    );
    
    uniswapRouter.exactInputSingle(params);
    uniswapRouter.refundETH();
    
    // refund leftover ETH to user
    (bool success,) = msg.sender.call{ value: address(this).balance }("");
    require(success, "refund failed");
}
  
// meant to be called as view function
function multiSwapPreview() external payable returns(uint256) {
    uint256 daiBalanceUserBeforeTrade = IERC20(DAI).balanceOf(msg.sender);
    uint256 deadline = block.timestamp + 300;
    
    uint256 amountOutMinBancor = 1;
    uint256 amountOutMinSushiSwap = 1;
    uint256 amountOutMinUniswap = 1;
    
    _tradeOnBancor(msg.value, amountOutMinBancor);
    _tradeOnSushi(IERC20(BNT).balanceOf(address(this)), amountOutMinSushiSwap, deadline);
    _tradeOnUniswap(IERC20(INJ).balanceOf(address(this)), amountOutMinUniswap, deadline);
    
    uint256 daiBalanceUserAfterTrade = IERC20(DAI).balanceOf(msg.sender);
    return daiBalanceUserAfterTrade - daiBalanceUserBeforeTrade;
}
  
function multiSwap(uint256 deadline, uint256 amountOutMinBancor, uint256 amountOutMinSushiSwap, uint256 amountOutMinUniswap) external payable {
    _tradeOnBancor(msg.value, amountOutMinBancor);
    _tradeOnSushi(IERC20(BNT).balanceOf(address(this)), amountOutMinSushiSwap, deadline);
    _tradeOnUniswap(IERC20(INJ).balanceOf(address(this)), amountOutMinUniswap, deadline);
}
  
  // important to receive ETH
  receive() payable external {}
}