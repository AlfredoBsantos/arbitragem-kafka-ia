require("@nomicfoundation/hardhat-toolbox");

module.exports = {
  solidity: "0.8.21", // Defina a versão do Solidity conforme seu contrato
  networks: {
    hardhat: {
      chainId: 1337, // Ajuste conforme necessário (para rede local)
    },
    // Adicione outras redes como Rinkeby, Sepolia, Mainnet, etc., se precisar
  },
  paths: {
    sources: "./contracts", // Onde seus contratos .sol estão armazenados
    tests: "./test", // Onde seus testes são armazenados (se necessário)
    cache: "./cache", // Cache de compilação
    artifacts: "./artifacts", // Onde os artefatos de compilação são armazenados
  },
  mocha: {
    timeout: 20000, // Ajuste o tempo limite para testes, se for necessário
  }
};
