# Simula um motor da TurboMotors com ESP32 no Wokwi

**https://wokwi.com/**

Variação do projeto `esp32-temperatura` usada na Aula 10 (manutenção preditiva).
O ESP32 representa um dos motores da TurboMotors Industrial e envia ao ThingsBoard
as mesmas grandezas da planilha `turbomotors_telemetria.xlsx`.

| Componente no simulador        | O que representa                     | Chave da telemetria |
| ------------------------------ | ------------------------------------ | ------------------- |
| DHT22 (D14)                    | Temperatura da carcaça (°C)          | `temperatura_c`     |
| Potenciômetro 1 (D34)          | Vibração, de 0 a 12 mm/s             | `vibracao_mm_s`     |
| Potenciômetro 2 (D35)          | Corrente, de 0 a 20 A                | `corrente_a`        |
| LED amarelo (D2)               | Vibração acima de 4,5 mm/s (alerta)  | `status`            |
| LED vermelho (D15)             | Motor parado pela regra local (Edge) | `parada_local`      |
| Botão verde (D4)               | Rearme manual feito pelo técnico     |                     |

A regra de parada (vibração acima de 7,1 mm/s) roda **no próprio ESP32**: o LED
vermelho acende mesmo sem internet. O alarme no ThingsBoard é a regra **na nuvem**.

# Comandos úteis

## Atualizar e Executar.

Rode estes comandos dentro da pasta `esp32-motor`, com o simulador aberto em outra aba.

### Para usuários Windows

```bat
py -m mpremote connect port:rfc2217://localhost:4000 fs cp simple.py :simple.py + fs cp secrets.py :secrets.py + run main.py
```

### Para usuários MacOs e Linux

```bash
mpremote connect port:rfc2217://localhost:4000 \
	fs cp simple.py :simple.py + \
	fs cp secrets.py :secrets.py + \
	run main.py
```

Antes de executar, crie `secrets.py` com o token do dispositivo no ThingsBoard
(o mesmo formato usado em `esp32-temperatura`):

```python
ACCESS_TOKEN = "token-do-dispositivo"
MQTT_CLIENT_ID = "motor-318"
```

O arquivo e ignorado pelo Git para evitar publicar a credencial.

### Importante:

O firmware é reaproveitado da pasta `esp32-temperatura` (veja `wokwi.toml`).
Se o Wokwi não encontrar o arquivo `.bin`, copie-o para esta pasta e ajuste o caminho no `wokwi.toml`.
Caso ocorra erros do tipo **could not enter raw repl**, pare o simulador, execute novamente e posteriormente rode o comando **mpremote** novamente.
