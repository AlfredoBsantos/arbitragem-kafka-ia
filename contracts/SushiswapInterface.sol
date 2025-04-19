// contracts/SushiswapInterface.sol
// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

interface ISushiswap {
    function getReserves() external view returns (uint112 reserve0, uint112 reserve1, uint32 blockTimestampLast);
    function swapExactTokensForTokens(uint amountIn, uint amountOutMin, address[] calldata path, address to, uint deadline) external returns (uint[] memory amounts);
}
