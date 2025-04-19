// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "./SimpleDEX.sol";

contract Arbitrageur {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function executeArbitrage(
        address tokenA,
        address tokenB,
        uint256 amountIn,
        address dex1,
        address dex2
    ) external {
        require(msg.sender == owner, "Only owner can execute arbitrage");

        // Approve tokenA for DEX1
        IERC20(tokenA).approve(dex1, amountIn);

        // Swap tokenA -> tokenB on DEX1
        SimpleDEX(dex1).swap(tokenA, tokenB, amountIn);
        uint256 tokenBReceived = IERC20(tokenB).balanceOf(address(this));

        // Approve tokenB for DEX2
        IERC20(tokenB).approve(dex2, tokenBReceived);

        // Swap tokenB -> tokenA on DEX2
        SimpleDEX(dex2).swap(tokenB, tokenA, tokenBReceived);
        uint256 tokenAReceived = IERC20(tokenA).balanceOf(address(this));

        require(tokenAReceived > amountIn, "Arbitrage not profitable");
    }

    // Emergency withdrawal just in case
    function withdrawToken(address token) external {
        require(msg.sender == owner, "Only owner can withdraw");
        uint256 balance = IERC20(token).balanceOf(address(this));
        IERC20(token).transfer(owner, balance);
    }
}
