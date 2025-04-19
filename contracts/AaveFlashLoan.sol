
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

import "@aave/core-v3/contracts/flashloan/base/FlashLoanSimpleReceiverBase.sol";
import "@aave/core-v3/contracts/interfaces/IPoolAddressesProvider.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract AaveFlashLoan is FlashLoanSimpleReceiverBase {
    constructor(IPoolAddressesProvider _provider)
        FlashLoanSimpleReceiverBase(_provider)
    {}

    function executeOperation(
        address asset,
        uint256 amount,
        uint256 premium,
        address initiator,
        bytes calldata params
    ) external override returns (bool) {
        // ⚡ Aqui vai a lógica de arbitragem (Uniswap -> Sushiswap etc.)

        uint256 totalAmount = amount + premium;
        IERC20(asset).approve(address(POOL), totalAmount);
        return true;
    }

    function requestFlashLoan(address asset, uint256 amount) external {
        POOL.flashLoanSimple(
            address(this),
            asset,
            amount,
            bytes(""),
            0
        );
    }
}
