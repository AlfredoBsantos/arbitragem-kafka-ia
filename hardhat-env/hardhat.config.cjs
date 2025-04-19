require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config(); // Para carregar variáveis de ambiente do .env

module.exports = {
  solidity: "0.8.21",
  networks: {
    hardhat: {},
    goerli: {
      url: process.env.GOERLI_RPC_URL || "https://goerli.infura.io/v3/YOUR_INFURA_KEY",
      accounts: [process.env.PRIVATE_KEY],
    },
  },
};