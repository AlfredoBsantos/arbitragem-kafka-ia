// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@aave/core-v3/contracts/flashloan/base/FlashLoanSimpleReceiverBase.sol";
import "@aave/core-v3/contracts/interfaces/IPoolAddressesProvider.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

interface IDEX {
    function swap(address tokenIn, address tokenOut, uint amountIn) external returns (uint amountOut);
}

contract ArbitrageExecutor is FlashLoanSimpleReceiverBase {
    address public owner;
    IDEX public dex1;
    IDEX public dex2;

    constructor(address _provider, address _dex1, address _dex2)
        FlashLoanSimpleReceiverBase(IPoolAddressesProvider(_provider))
    {
        owner = msg.sender;
        dex1 = IDEX(_dex1);
        dex2 = IDEX(_dex2);
    }

    function executeOperation(
        address asset,
        uint256 amount,
        uint256 premium,
        address initiator,
        bytes calldata params
    ) external override returns (bool) {
        require(msg.sender == address(POOL), "Caller must be lending pool");
        require(initiator == address(this), "Only this contract can initiate");

        // Decode token arbitrage pair
        (address tokenIn, address tokenOut) = abi.decode(params, (address, address));

        IERC20(asset).approve(address(dex1), amount);
        uint received = dex1.swap(tokenIn, tokenOut, amount);

        IERC20(tokenOut).approve(address(dex2), received);
        uint finalAmount = dex2.swap(tokenOut, tokenIn, received);

        require(finalAmount > amount + premium, "Arbitrage not profitable");

        uint totalRepayment = amount + premium;
        IERC20(asset).approve(address(POOL), totalRepayment);

        return true;
    }

    function initiateFlashLoan(address asset, uint amount, address tokenOut) external {
        require(msg.sender == owner, "Only owner");
        bytes memory params = abi.encode(asset, tokenOut);
        POOL.flashLoanSimple(address(this), asset, amount, params, 0);
    }
}
