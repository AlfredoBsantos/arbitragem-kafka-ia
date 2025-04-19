const { ethers } = require("hardhat");
require("dotenv").config();

const INITIAL_SUPPLY = ethers.utils.parseEther("1000000"); // 1 milhão de tokens

async function main() {
  // Deploy dos Tokens Mock
  const TokenA = await ethers.getContractFactory("TokenA");
  const tokenA = await TokenA.deploy(INITIAL_SUPPLY);
  await tokenA.deployed();
  console.log("Token A deployed to:", tokenA.address);

  const TokenB = await ethers.getContractFactory("TokenB");
  const tokenB = await TokenB.deploy(INITIAL_SUPPLY);
  await tokenB.deployed();
  console.log("Token B deployed to:", tokenB.address);

  // Deploy dos DEXs Simples
  const SimpleDEX = await ethers.getContractFactory("SimpleDEX");
  const dexA = await SimpleDEX.deploy(tokenA.address, tokenB.address);
  await dexA.deployed();
  console.log("SimpleDEX A deployed to:", dexA.address);

  const dexB = await SimpleDEX.deploy(tokenA.address, tokenB.address);
  await dexB.deployed();
  console.log("SimpleDEX B deployed to:", dexB.address);

  // Deploy do Contrato de Arbitragem com Flash Loan
  const FlashLoanArbitrage = await ethers.getContractFactory("FlashLoanArbitrage");
  const arbitrage = await FlashLoanArbitrage.deploy(/* Aqui você pode precisar de argumentos, como o endereço de um pool de flash loan */);
  await arbitrage.deployed();
  console.log("FlashLoanArbitrage deployed to:", arbitrage.address);

  // Aprovação e Adição de Liquidez (Exemplo para DEX A)
  const amountA = ethers.utils.parseEther("10000"); // 10 mil tokens A
  const amountB = ethers.utils.parseEther("1000");  // 1 mil tokens B

  // Aprovar DEX A a gastar tokens do deployer
  await tokenA.approve(dexA.address, amountA);
  await tokenB.approve(dexA.address, amountB);
  console.log("Approved DEX A to spend tokens");

  // Adicionar liquidez ao DEX A
  await dexA.addLiquidity(amountA, amountB);
  console.log("Liquidity added to DEX A:", amountA.toString(), "Token A,", amountB.toString(), "Token B");

  // Adição de Liquidez ao DEX B (com preços diferentes para simular arbitragem)
  const amountADexB = ethers.utils.parseEther("5000"); // 5 mil tokens A
  const amountBDexB = ethers.utils.parseEther("1000");  // 1 mil tokens B

  // Aprovar DEX B a gastar tokens do deployer
  await tokenA.approve(dexB.address, amountADexB);
  await tokenB.approve(dexB.address, amountBDexB);
  console.log("Approved DEX B to spend tokens");

  // Adicionar liquidez ao DEX B
  await dexB.addLiquidity(amountADexB, amountBDexB);
  console.log("Liquidity added to DEX B:", amountADexB.toString(), "Token A,", amountBDexB.toString(), "Token B");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });