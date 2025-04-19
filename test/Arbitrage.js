const { expect } = require("chai");

describe("Arbitrage Contract", function () {
  let arbitrage, uniswapMock;

  beforeEach(async function () {
    const UniswapMock = await ethers.getContractFactory("UniswapMock");
    uniswapMock = await UniswapMock.deploy();
    await uniswapMock.waitForDeployment();

    const Arbitrage = await ethers.getContractFactory("Arbitrage");
    arbitrage = await Arbitrage.deploy(uniswapMock.target);
    await arbitrage.waitForDeployment();
  });

  it("Deve retornar a taxa do UniswapMock", async function () {
    const rate = await arbitrage.getRateFromUniswap();
    expect(rate).to.equal(1000); // ou o valor esperado
  });
});
