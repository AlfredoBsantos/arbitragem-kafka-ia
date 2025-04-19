const hre = require("hardhat");
const { ethers } = hre;

async function main() {
  const address = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266";

  const provider = ethers.provider;
  console.log("Conectado à rede:", (await provider.getNetwork()).name);

  const balance = await provider.getBalance(address);
  console.log(`Saldo de ${address}: ${ethers.formatEther(balance)} ETH`);
}

main().catch((error) => {
  console.error("Erro ao executar o script:", error);
  process.exitCode = 1;
});
