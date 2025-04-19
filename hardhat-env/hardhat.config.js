require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();


module.exports = {
  solidity: "0.8.21",
  networks: {
    localhost: {
      url: "http://127.0.0.1:8545", // Ou a URL do seu nó local
      accounts: [process.env.PRIVATE_KEY], // Substitua com uma chave privada de uma conta local
    },
  },
};
