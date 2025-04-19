// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@aave/core-v3/contracts/interfaces/IPoolAddressesProvider.sol";
import "@aave/core-v3/contracts/interfaces/IPool.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

interface IUniswapV2Router {
    function swapExactTokensForTokens(
        uint amountIn,
        uint amountOutMin,
        address[] calldata path,
        address to,
        uint deadline
    ) external returns (uint[] memory amounts);
}

contract AaveFlashLoanReceiver {
    IPoolAddressesProvider public immutable ADDRESSES_PROVIDER;
    IPool public immutable POOL;
    address public owner;

    constructor(address provider) {
        ADDRESSES_PROVIDER = IPoolAddressesProvider(provider);
        POOL = IPool(ADDRESSES_PROVIDER.getPool());
        owner = msg.sender;
    }

    function executeOperation(
        address asset,
        uint256 amount,
        uint256 premium,
        address initiator,
        bytes calldata params
    ) external returns (bool) {
        require(msg.sender == address(POOL), "Caller must be pool");
        require(initiator == address(this), "Initiator must be this contract");

        // 1. Decodificar parâmetros
        (address router1, address router2, address tokenOut) = abi.decode(
            params, 
            (address, address, address)
        );

        // 2. Aprovar o router para gastar os tokens
        IERC20(asset).approve(router1, amount);

        // 3. Primeiro swap (compra)
        address[] memory path = new address[](2);
        path[0] = asset;
        path[1] = tokenOut;
        
        IUniswapV2Router(router1).swapExactTokensForTokens(
            amount,
            1, // amountOutMin mínimo
            path,
            address(this),
            block.timestamp + 300
        );

        // 4. Segundo swap (venda)
        uint256 receivedAmount = IERC20(tokenOut).balanceOf(address(this));
        IERC20(tokenOut).approve(router2, receivedAmount);
        
        path[0] = tokenOut;
        path[1] = asset;
        
        IUniswapV2Router(router2).swapExactTokensForTokens(
            receivedAmount,
            1,
            path,
            address(this),
            block.timestamp + 300
        );

        // 5. Pagar o flash loan
        uint256 totalOwed = amount + premium;
        IERC20(asset).approve(address(POOL), totalOwed);
        
        return true;
    }

    function requestFlashLoan(
        address asset,
        uint256 amount,
        bytes memory params
    ) external {
        require(msg.sender == owner, "Only owner");
        POOL.flashLoanSimple(
            address(this),
            asset,
            amount,
            params,
            0
        );
    }
}