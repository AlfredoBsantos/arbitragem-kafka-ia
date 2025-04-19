const hre = require("hardhat");

async function main() {
    const [deployer] = await hre.ethers.getSigners();
    console.log("Usando a conta:", deployer.address);

    // Deploy do UniswapMock
    const UniswapMock = await hre.ethers.getContractFactory("UniswapMock");
    console.log("Implantando UniswapMock...");
    const uniswap = await UniswapMock.deploy();
    await uniswap.waitForDeployment();

    const uniswapAddress = await uniswap.getAddress(); // ou uniswap.target

    console.log("UniswapMock implantado em:", uniswapAddress);

    // Deploy do Arbitrage, passando o endereço do UniswapMock
    const Arbitrage = await hre.ethers.getContractFactory("Arbitrageur");
    console.log("Implantando Arbitrage...");
    const arbitrage = await Arbitrage.deploy([uniswapAddress]);
    await arbitrage.waitForDeployment();

    const arbitrageAddress = await arbitrage.getAddress();
    console.log("Arbitrage implantado em:", arbitrageAddress);
}

main().catch((error) => {
    console.error("Erro ao executar o script:", error);
    process.exitCode = 1;
});
