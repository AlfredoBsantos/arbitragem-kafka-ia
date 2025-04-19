const { ethers } = require("hardhat");

async function main() {
  // Obtemos o deployer
  const [deployer] = await ethers.getSigners();
  console.log("Usando a conta:", deployer.address);

  // Endereço do token A e B (você pode usar tokens de teste ou Mock tokens)
  const tokenA = "endereço_do_token_A"; // Defina o endereço de um token ERC20
  const tokenB = "endereço_do_token_B"; // Defina o endereço de outro token ERC20
  const amountIn = ethers.utils.parseUnits("1", 18); // Quantidade de tokenA para arbitragem

  // Obtenção do contrato UniswapMock implantado
  const UniswapMock = await ethers.getContractFactory("contracts/UniswapMock.sol:UniswapMock");
  const uniswap = await UniswapMock.deploy();
  await uniswap.waitForDeployment();
  console.log("UniswapMock implantado em:", await uniswap.getAddress());

  // Implantação do contrato Arbitrageur
  const Arbitrage = await ethers.getContractFactory("Arbitrageur");
  const arbitrage = await Arbitrage.deploy(await uniswap.getAddress());
  await arbitrage.waitForDeployment();
  console.log("Arbitrage implantado em:", await arbitrage.getAddress());

  // Chamando a função de arbitragem
  console.log("Executando arbitragem...");
  try {
    await arbitrage.executeArbitrage(tokenA, tokenB, amountIn, await uniswap.getAddress(), await uniswap.getAddress());
    console.log("Arbitragem executada com sucesso!");
  } catch (error) {
    console.error("Erro na execução da arbitragem:", error);
  }

  // Retirar tokens após a execução
  try {
    const token = "endereço_do_token"; // Endereço do token a ser retirado
    await arbitrage.withdrawToken(token);
    console.log("Tokens retirados com sucesso!");
  } catch (error) {
    console.error("Erro na retirada de tokens:", error);
  }
}

main().catch((error) => {
  console.error("Erro ao executar o script:", error);
  process.exitCode = 1;
});
