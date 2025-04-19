const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Uniswap Swap Simulation", function () {
  let uniswapMock;
  let tokenA, tokenB;
  let owner;

  before(async function () {
    // Obter signers
    [owner] = await ethers.getSigners();
    
    // Deploy tokens
    const Token = await ethers.getContractFactory("MockERC20");
    tokenA = await Token.deploy("Token A", "TA");
    tokenB = await Token.deploy("Token B", "TB");
    
    // Deploy Uniswap Mock
    const UniswapMock = await ethers.getContractFactory("UniswapMock");
    uniswapMock = await UniswapMock.deploy();
    
    // Configurar taxa de câmbio
    await uniswapMock.setRate(
      tokenA.address, 
      tokenB.address, 
      ethers.utils.parseEther("1.5") // 1 TA = 1.5 TB
    );
    
    // Mint tokens iniciais
    await tokenA.mint(owner.address, ethers.utils.parseEther("1000"));
  });

  it("Should swap tokens successfully", async function () {
    // Aprovar o contrato para gastar tokens
    await tokenA.connect(owner).approve(
      uniswapMock.address, 
      ethers.utils.parseEther("100")
    );
    
    // Executar swap
    await expect(
      uniswapMock.connect(owner).swapExactTokensForTokens(
        ethers.utils.parseEther("100"), // amountIn
        1, // amountOutMin
        [tokenA.address, tokenB.address], // path
        owner.address, // to
        Math.floor(Date.now() / 1000) + 300 // deadline
      )
    ).to.changeTokenBalance(
      tokenB, 
      owner.address, 
      ethers.utils.parseEther("150") // Valor esperado (100 * 1.5)
    );
  });
});