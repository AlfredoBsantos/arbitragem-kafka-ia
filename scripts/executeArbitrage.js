// scripts/executeArbitrage.js
async function main() {
    const [deployer] = await ethers.getSigners();
    console.log("Executing arbitrage with the account:", deployer.address);

    const Arbitrage = await ethers.getContractFactory("Arbitrage");
    const arbitrage = await Arbitrage.attach("endereco_do_contrato");  // Attach to deployed contract

    // Lógica de execução de arbitragem
    const tx = await arbitrage.executeArbitrage();
    console.log("Arbitrage transaction sent:", tx.hash);
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });
