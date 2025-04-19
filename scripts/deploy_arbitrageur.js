async function main() {
    const [deployer] = await ethers.getSigners();
    console.log("Deploying contracts with the account:", deployer.address);

    const Arbitrageur = await ethers.getContractFactory("Arbitrageur");
    const arbitrageur = await Arbitrageur.deploy();
    console.log("Arbitrageur contract deployed to:", arbitrageur.address);
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });
