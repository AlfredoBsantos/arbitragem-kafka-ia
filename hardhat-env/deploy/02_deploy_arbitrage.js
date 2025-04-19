const { ethers } = require("hardhat");
const fs = require("fs");
const path = require("path");

async function main() {
  const ArbitrageExecutor = await ethers.getContractFactory("ArbitrageExecutor");
  const arbitrageExecutor = await ArbitrageExecutor.deploy();
  await arbitrageExecutor.deployed();

  console.log("ArbitrageExecutor deployed to:", arbitrageExecutor.address);

  // Salvando o endereço do contrato
  const deployedAddressesPath = path.join(__dirname, "..", "deployed_addresses.json");

  let addresses = {};
  if (fs.existsSync(deployedAddressesPath)) {
    addresses = JSON.parse(fs.readFileSync(deployedAddressesPath));
  }

  addresses["ArbitrageExecutor"] = arbitrageExecutor.address;

  fs.writeFileSync(deployedAddressesPath, JSON.stringify(addresses, null, 2));
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
