const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();

  const UniswapMock = await hre.ethers.getContractFactory("UniswapMock");
  const uniswap = await UniswapMock.deploy();
  await uniswap.deployed();
  console.log("UniswapMock deployed to:", uniswap.address);

  const Arbitrage = await hre.ethers.getContractFactory("Arbitrage");
  const arbitrage = await Arbitrage.deploy(uniswap.address);
  await arbitrage.deployed();
  console.log("Arbitrage deployed to:", arbitrage.address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
