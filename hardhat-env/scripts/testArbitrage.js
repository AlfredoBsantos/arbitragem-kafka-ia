const { ethers } = require("hardhat");

async function main() {
  // Obtemos o deployer
  const [deployer] = await ethers.getSigners();
  console.log("Usando a conta:", deployer.address);

  // Deploy do UniswapMock
  const UniswapMock = await ethers.getContractFactory("contracts/UniswapMock.sol:UniswapMock");
  const uniswap = await UniswapMock.deploy();
  await uniswap.waitForDeployment();
  console.log("UniswapMock implantado em:", await uniswap.getAddress());

  // Deploy do Arbitrage sem parâmetros (já que o contrato não exige argumentos)
  const Arbitrage = await ethers.getContractFactory("Arbitrageur");
  const arbitrage = await Arbitrage.deploy();
  await arbitrage.waitForDeployment();
  console.log("Arbitrage implantado em:", await arbitrage.getAddress());

  // Se o Arbitrageur precisar do endereço do UniswapMock após o deploy
  // Você pode fazer algo assim:
  // await arbitrage.setUniswapAddress(await uniswap.getAddress()); // Exemplo, se você tiver uma função de setter no contrato

  // Chamada de getRateFromUniswap (não existe essa função no seu código atualmente)
  // const rate = await arbitrage.getRateFromUniswap(); 
  // console.log("Taxa obtida de getRateFromUniswap():", rate.toString());
}

main().catch((error) => {
  console.error("Erro ao executar o script:", error);
  process.exitCode = 1;
});
