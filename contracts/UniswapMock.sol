// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract UniswapMock {
    function getRate() external pure returns (uint256) {
        return 1000; // valor mockado
    }
}
