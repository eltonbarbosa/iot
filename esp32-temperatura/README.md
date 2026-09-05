# Simula um ESP32 utilizando Wokwi

**https://wokwi.com/**

# Comandos úteis

## Atualizar e Executar.

Rode este comando toda vez que desejar rodar a simulação ou quando atualizar algum **.py**

### Para usuários Windows

`py -m mpremote connect port:rfc2217://localhost:4000 fs cp simple.py :simple.py + run main.py`

### Para usuários MacOs e Linux

`mpremote connect port:rfc2217://localhost:4000 fs cp simple.py :simple.py + run main.py`

### Importante:

O simulador deve estar aberto em outra aba.
Caso ocorra erros do tipo **could not enter raw repl**, pare o simulador, execute novamente e posteriormente rode o comando **mpremote** novamente.
Caso o erro persista, pause a simulação via extensão Wokwi e tente novamente executar o simulador e posteriormente executar o comando **mpremote** novamente.
