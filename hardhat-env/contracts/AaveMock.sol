// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IERC20 {
    function balanceOf(address account) external view returns (uint256);
    function transfer(address to, uint256 amount) external returns (bool);
}

contract AaveMock {
    mapping(address => uint256) public balances;

    function deposit(address asset, uint256 amount) external {
        balances[asset] += amount;
    }

 function flashLoanSimple(
    address receiver,
    address asset,
    uint256 amount,
    bytes calldata params,
    uint16  // referralCode (parâmetro mantido mas não nomeado)
) external {
        uint256 balanceBefore = IERC20(asset).balanceOf(address(this));
        IERC20(asset).transfer(receiver, amount);
        
        (bool success,) = receiver.call(
            abi.encodeWithSignature(
                "executeOperation(address,uint256,uint256,address,bytes)",
                asset,
                amount,
                0,
                msg.sender,
                params
            )
        );
        require(success, "Callback failed");

        uint256 balanceAfter = IERC20(asset).balanceOf(address(this));
        require(balanceAfter >= balanceBefore, "Loan not repaid");
    }
}