// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract MockERC20 is ERC20 {
    address public owner;

    constructor(string memory name, string memory symbol) ERC20(name, symbol) {
        owner = msg.sender;
        _mint(owner, 1000000 * 10**decimals());
    }

    // Função para criar mais tokens, restrita ao dono do contrato
    function mint(address to, uint256 amount) public {
        require(msg.sender == owner, "Only owner can mint tokens");
        _mint(to, amount);
    }
}
