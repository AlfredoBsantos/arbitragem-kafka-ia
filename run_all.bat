@echo off
setlocal

echo [1] Iniciando Hardhat node...
start "Hardhat Node" cmd /k "cd hardhat-env && npx hardhat node"

REM Espera o Hardhat Node iniciar
timeout /t 10 /nobreak >nul

echo [2] Fazendo deploy dos contratos...
start "Deploy Scripts" cmd /k "cd hardhat-env && npx hardhat run scripts\deploy.js --network localhost"

REM Espera o deploy terminar
timeout /t 10 /nobreak >nul

echo [3] Iniciando Kafka com Docker...
start "Kafka Docker" cmd /k "cd kafka-setup && docker-compose up"

REM Tempo extra para Kafka levantar completamente
timeout /t 15 /nobreak >nul

echo [4] Iniciando o Producer Kafka...
start "Kafka Producer" cmd /k "cd producer && python arbitrage_producer.py"

timeout /t 5 /nobreak >nul

echo [5] Iniciando o Consumer Kafka...
start "Kafka Consumer" cmd /k "cd consumer && python price_consumer.py"

echo [✓] Todos os serviços foram iniciados!
pause
