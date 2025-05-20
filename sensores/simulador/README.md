## Simulação no Wokwi e Interpretação dos Dados Seriais

### Prefixos das mensagens seriais

- `DATA:` — Linha de **dados dos sensores** enviados para integração com o sistema externo (Python, banco de dados etc).
  - Exemplo:  
    `DATA:1,1,7.40,52.50`
    - Fósforo presente (1), Potássio presente (1), pH 7.40, Umidade 52.50%
- `LOG:` — Mensagens de **log, status, avisos e modo de decisão** do sistema embarcado.
  - Exemplo:  
    `LOG:[INFO] Irrigacao ATIVA (decisao EXTERNA).`
    `LOG:[MODO] Mudando para decisao LOCAL (ESP32)`

### Como funciona no Wokwi

- **Botão Fósforo (P):** GPIO12 — Simula presença/ausência do nutriente.
- **Botão Potássio (K):** GPIO14 — Simula presença/ausência do nutriente.
- **Botão Modo (Mode):** GPIO33 — Pressione para alternar entre lógica de irrigação externa (decisão pelo Python/PC) e lógica local no ESP32.
- **LDR:** GPIO34 — Simula leitura analógica para pH.
- **DHT22:** GPIO27 — Mede umidade do solo (simulada).
- **Relé:** GPIO26 — Representa bomba de irrigação (ligada/desligada).
- **LED embutido:** GPIO2 — Indica status da bomba/irrigação.

> Sempre monitore o **Serial Monitor** no Wokwi para acompanhar o funcionamento do sistema, distinguir logs e leituras de dados, e depurar/testar sua integração Python.

---

Se quiser visualizar no Python apenas os dados dos sensores, basta filtrar por linhas começadas em `DATA:`!

---
