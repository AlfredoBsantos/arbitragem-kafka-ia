const { expect } = require("chai");

describe("Arbitrage", function () {
  it("Deve retornar a taxa do UniswapMock", async function () {
    const UniswapMock = await ethers.getContractFactory("UniswapMock");
    const uniswapMock = await UniswapMock.deploy();
    await uniswapMock.waitForDeployment();

    const Arbitrage = await ethers.getContractFactory("Arbitrage");
    const arbitrage = await Arbitrage.deploy(uniswapMock.target);
    await arbitrage.waitForDeployment();

    const rate = await arbitrage.getRateFromUniswap();
    expect(rate).to.equal(1000);
  });
});
