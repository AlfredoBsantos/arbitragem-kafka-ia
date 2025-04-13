const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  const initialSupply = hre.ethers.parseUnits("1000000", 18); // 1 milhão de tokens

  console.log("👷 Deploying contracts with account:", deployer.address);

  const TokenA = await hre.ethers.getContractFactory("TokenA");
  const tokenA = await TokenA.deploy("Token A", "TKA", initialSupply);
  await tokenA.waitForDeployment();
  console.log("✅ TokenA deployed to:", tokenA.target);

  const TokenB = await hre.ethers.getContractFactory("TokenB");
  const tokenB = await TokenB.deploy("Token B", "TKB", initialSupply);
  await tokenB.waitForDeployment();
  console.log("✅ TokenB deployed to:", tokenB.target);

  const SimpleDEX = await hre.ethers.getContractFactory("SimpleDEX");
  const dex = await SimpleDEX.deploy(tokenA.target, tokenB.target);
  await dex.waitForDeployment();
  console.log("✅ DEX deployed to:", dex.target);

  const fs = require("fs");
  fs.writeFileSync(
    "deployed_addresses.json",
    JSON.stringify({
      TokenA: tokenA.target,
      TokenB: tokenB.target,
      DEX: dex.target,
    }, null, 2)
  );

  console.log("📦 Endereços salvos em deployed_addresses.json");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("❌ Error in deployment:", error);
    process.exit(1);
  });
