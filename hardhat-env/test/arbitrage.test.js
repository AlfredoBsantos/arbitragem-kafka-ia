const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("FlashLoan Arbitrage", function () {
  let arbitrageContract;
  let tokenA, tokenB, aavePool;
  let owner;

  before(async function () {
    [owner] = await ethers.getSigners();
    
    // Deploy tokens mock
    const Token = await ethers.getContractFactory("MockERC20");
    tokenA = await Token.deploy("Token A", "TA");
    tokenB = await Token.deploy("Token B", "TB");
    
    // Deploy mock Aave Pool
    const AavePool = await ethers.getContractFactory("AaveMock");
    aavePool = await AavePool.deploy();
    
    // Deploy contrato de arbitragem
    const FlashLoanArbitrage = await ethers.getContractFactory("AaveFlashLoanReceiver");
    arbitrageContract = await FlashLoanArbitrage.deploy(aavePool.address);
    
    // Configurar saldos iniciais
    await tokenA.mint(owner.address, ethers.utils.parseEther("10000"));
  });

  it("Should execute arbitrage and repay loan", async function () {
    // Aprovar o contrato para gastar tokens
    await tokenA.connect(owner).approve(arbitrageContract.address, ethers.utils.parseEther("1000"));
    
    // Definir parâmetros para o flashloan (endereços mock)
    const params = ethers.utils.defaultAbiCoder.encode(
      ["address", "address", "address"],
      [
        "0x0000000000000000000000000000000000000001", // Router 1
        "0x0000000000000000000000000000000000000002", // Router 2
        tokenB.address // Token alvo
      ]
    );

    // Executar flashloan
    const tx = arbitrageContract.connect(owner).requestFlashLoan(
      tokenA.address,
      ethers.utils.parseEther("1000"),
      params
    );

    await expect(tx).to.not.be.reverted;
  });
});