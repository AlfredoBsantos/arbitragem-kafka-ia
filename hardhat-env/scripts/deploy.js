// scripts/deploy.js
const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();

  console.log("Deploying contracts with the account:", deployer.address);

  const TokenA = await hre.ethers.getContractFactory("TokenA");
  const tokenA = await TokenA.deploy(ethers.utils.parseEther("1000000"));
  await tokenA.deployed();

  console.log("TokenA deployed to:", tokenA.address);

  const TokenB = await hre.ethers.getContractFactory("TokenB");
  const tokenB = await TokenB.deploy(ethers.utils.parseEther("1000000"));
  await tokenB.deployed();

  console.log("TokenB deployed to:", tokenB.address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
