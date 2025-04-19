// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IUniswapMock {
    function getRate() external view returns (uint256);
}

contract Arbitrage {
    address public owner;
    IUniswapMock public uniswap;

    constructor(address _uniswapAddress) {
        owner = msg.sender;
        uniswap = IUniswapMock(_uniswapAddress);
    }

    function getRateFromUniswap() public view returns (uint256) {
        return uniswap.getRate();
    }
}
