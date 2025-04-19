const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying contracts with the account:", deployer.address);

  // Deployando o contrato mock Uniswap
  const UniswapMock = await hre.ethers.getContractFactory("UniswapMock");
  const uniswapMock = await UniswapMock.deploy();
  await uniswapMock.waitForDeployment();
  console.log("UniswapMock deployed to:", uniswapMock.target);

  // Deployando o contrato principal Arbitrage
  const Arbitrage = await hre.ethers.getContractFactory("Arbitrage");
  const arbitrage = await Arbitrage.deploy(uniswapMock.target); // passando o endereço do mock
  await arbitrage.waitForDeployment();
  console.log("Arbitrage deployed to:", arbitrage.target);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
