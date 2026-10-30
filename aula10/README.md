# Aula 10 · TurboMotors: do sensor à decisão com Big Data

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/eltonbarbosa/iot/blob/main/aula10/TurboMotors_BigData.ipynb)

Notebook pronto para o Trabalho 02. Executar as células na ordem e trocam os limites da regra de alerta nos campos ✏️.
Os resultados são os mesmos da aba **SIMULADOR** da planilha `turbomotors_telemetria.xlsx`.

| Etapa | Conteúdo | V do Big Data |
|---|---|---|
| 1 | Tamanho da amostra × operação real (500 motores, leitura a cada 5 s) | Volume, Velocidade |
| 2 | Telemetria da plataforma IoT + ordens de serviço do ERP | Variedade |
| 3 | Leituras impossíveis, duplicadas e motor parado; limpeza | Veracidade |
| 4 | Resumo diário por motor e gráficos de vibração e temperatura | |
| 5 | Simulador: falhas avisadas, alarmes falsos e economia | Valor |
| 6 | Comparação de várias regras lado a lado | Valor |

## Dados

O notebook pede o upload dos dois arquivos ao rodar a primeira célula (eles não ficam neste repositório):

- `turbomotors_leituras.csv`: telemetria horária de 30 motores por 60 dias (exportada da plataforma IoT).
- `turbomotors_manutencoes.csv`: ordens de serviço do ERP (preventivas e corretivas).
