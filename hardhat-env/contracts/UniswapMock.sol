// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract UniswapMock {
    // Mapeamento de taxas de câmbio: tokenIn => tokenOut => rate
    mapping(address => mapping(address => uint256)) public rates;
    
    // Evento para registrar swaps
    event Swap(
        address indexed sender,
        uint256 amountIn,
        uint256 amountOut,
        address[] path
    );

    // Configura a taxa de câmbio entre dois tokens
    function setRate(
        address tokenIn, 
        address tokenOut, 
        uint256 rate
    ) external {
        rates[tokenIn][tokenOut] = rate;
    }

    // Função mock para simular swap no Uniswap
    function swapExactTokensForTokens(
        uint256 amountIn,
        uint256 amountOutMin,
        address[] calldata path,
        address to,
        uint256 /* deadline */
    ) external returns (uint256[] memory amounts) {
        require(path.length == 2, "UniswapMock: INVALID_PATH");
        
        address tokenIn = path[0];
        address tokenOut = path[1];
        uint256 rate = rates[tokenIn][tokenOut];
        require(rate > 0, "UniswapMock: RATE_NOT_SET");
        
        uint256 amountOut = (amountIn * rate) / 1e18;
        require(amountOut >= amountOutMin, "UniswapMock: INSUFFICIENT_OUTPUT_AMOUNT");
        
        // Simular transferência de tokens
        IERC20(tokenIn).transferFrom(msg.sender, address(this), amountIn);
        IERC20(tokenOut).transfer(to, amountOut);
        
        // Retornar amounts como no Uniswap real
        amounts = new uint256[](2);
        amounts[0] = amountIn;
        amounts[1] = amountOut;
        
        emit Swap(msg.sender, amountIn, amountOut, path);
        
        return amounts;
    }

    // Função auxiliar para depositar tokens no mock (para testes)
    function depositToken(address token, uint256 amount) external {
        IERC20(token).transferFrom(msg.sender, address(this), amount);
    }
}