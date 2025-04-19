// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

interface IToken {
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
    function transfer(address recipient, uint256 amount) external returns (bool);
}


contract SimpleDEX {
    IToken public tokenA;
    IToken public tokenB;
    
    uint256 public reserveA;
    uint256 public reserveB;

    constructor(address _tokenA, address _tokenB) {
        tokenA = IToken(_tokenA);
        tokenB = IToken(_tokenB);
    }

    // Função para adicionar liquidez
    function addLiquidity(uint256 amountA, uint256 amountB) external {
        tokenA.transferFrom(msg.sender, address(this), amountA);
        tokenB.transferFrom(msg.sender, address(this), amountB);
        reserveA += amountA;
        reserveB += amountB;
    }

    // Função de swap (compra/venda de tokens)
    function swap(address tokenIn, address tokenOut, uint256 amountIn) external {
        require(tokenIn == address(tokenA) || tokenIn == address(tokenB), "Invalid token");
        
        uint256 amountOut;
        if (tokenIn == address(tokenA)) {
            // Swap de A para B
            amountOut = amountIn * reserveB / reserveA;
            reserveA += amountIn;
            reserveB -= amountOut;
        } else {
            // Swap de B para A
            amountOut = amountIn * reserveA / reserveB;
            reserveB += amountIn;
            reserveA -= amountOut;
        }

        IToken(tokenIn).transferFrom(msg.sender, address(this), amountIn);
        IToken(tokenOut).transfer(msg.sender, amountOut);
    }

    // Função para obter as reservas atuais de cada token
    function getReserves() external view returns (uint256, uint256) {
        return (reserveA, reserveB);
    }
}
