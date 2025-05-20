# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Agro Metrics

### Integrantes:
- <a href="https://www.linkedin.com/in/caiooliveiraeti">Caio Oliveira</a>

## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/in/lucas-gomes-moreira-15a8452a/">Lucas Gomes</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/in/andregodoichiovato/">Andre Godoi</a>

O **Agro Metrics** é um sistema de linha de comando para a gestão de sensores agrícolas e o processamento de leituras. Ele permite o gerenciamento de áreas, sensores e medições, além de importar e exportar dados em formato CSV ou JSON.

## Impacto no Agronegócio

O monitoramento de variáveis ambientais e do solo é essencial para a agricultura de precisão, que busca otimizar a produção agrícola, reduzir custos e minimizar impactos ambientais. O **Agro Metrics** oferece uma solução prática para gerenciar sensores que coletam dados como:

- **Umidade do Solo**: Ajuda a determinar a necessidade de irrigação, evitando desperdício de água e garantindo o crescimento saudável das plantas.
- **pH do Solo**: Permite identificar a acidez ou alcalinidade do solo, auxiliando na aplicação de corretivos como calcário.
- **Condutividade Elétrica (CE)**: Indica a concentração de nutrientes no solo, ajudando a ajustar a fertilização.

Com esses dados, agricultores podem tomar decisões informadas sobre irrigação, fertilização e manejo do solo, aumentando a produtividade e a sustentabilidade.

## Funcionalidades

- **Gerenciamento de Áreas**: Adicionar, listar e remover áreas agrícolas.
- **Gerenciamento de Sensores**: Adicionar, listar e remover sensores vinculados a áreas.
- **Conexão de Sensores**: Conectar sensores para registrar leituras em tempo real.
- **Registro de Leituras**: Cadastrar medições para sensores.
- **Importação de Leituras**: Importar medições de sensores a partir de arquivos CSV.
- **Exportação de Leituras**: Exportar todas as medições de uma área para arquivos CSV ou JSON.

## Simulador de Sensores

O projeto inclui um simulador de sensores desenvolvido no Wokwi para testar a integração com o sistema. O simulador utiliza um ESP32 para simular sensores de umidade, pH, fósforo e potássio, além de um relé para controle de irrigação.

Para mais detalhes, consulte o [README do simulador](sensores/simulador/README.md).

## Exemplos de Uso Prático

1. **Monitoramento de Irrigação**:
   - Sensores de umidade do solo são instalados em diferentes áreas da fazenda.
   - As leituras são registradas no sistema e analisadas para determinar quais áreas precisam de irrigação.
   - Isso reduz o consumo de água e evita o estresse hídrico nas plantas.

2. **Correção do Solo**:
   - Sensores de pH identificam áreas com solo ácido.
   - Com base nas leituras, o agricultor aplica calcário apenas nas áreas necessárias, economizando insumos e melhorando a produtividade.

3. **Otimização da Fertilização**:
   - Sensores de condutividade elétrica medem a concentração de nutrientes no solo.
   - As leituras ajudam a ajustar a quantidade de fertilizantes aplicados, evitando desperdício e contaminação ambiental.

## Requisitos para executar o código

- Python 3.8 ou superior
- Banco de dados Oracle (configurado via `docker-compose.yml`)

## 🔧 Como executar o código

1. Clone o repositório:
   ```bash
   git clone https://github.com/caiooliveiraeti/agro-metrics-cap6.git
   ```

2. Inicie o banco de dados Oracle com Docker:
   ```bash
   docker-compose up -d
   ```

3. Execute o sistema:
   ```bash
   make
   ```

## Uso

Ao executar o sistema, você verá um menu interativo com as seguintes opções:

Siga as instruções no terminal para realizar as operações desejadas.

## Estrutura do Projeto

- **`src/agro_metrics/core/services`**: Contém a lógica de negócios para áreas e sensores.
- **`src/agro_metrics/core/repositories`**: Implementa a comunicação com o banco de dados Oracle.
- **`src/agro_metrics/cli.py`**: Implementa a interface de linha de comando.
- **`scripts/database/*`**: Script para criar, e popular as tabelas no banco de dados.
- **`sensores/simulador`**: Contém o simulador de sensores desenvolvido no Wokwi.

## Modelo Entidade-Relacionamento (MER)

O banco de dados do **Agro Metrics** foi projetado para gerenciar áreas agrícolas, sensores e as leituras realizadas por esses sensores. Abaixo está o MER que representa a estrutura do banco de dados:

```mermaid
erDiagram
    AREAS {
        VARCHAR2 area_id PK
        VARCHAR2 nome
        FLOAT latitude
        FLOAT longitude
    }
    SENSORES {
        VARCHAR2 sensor_id PK
        VARCHAR2 tipo
        VARCHAR2 area_id FK
        FLOAT latitude
        FLOAT longitude
        NUMBER ativo
        VARCHAR2 codigo_patrimonio UNIQUE
    }
    LEITURAS {
        NUMBER leitura_id PK
        VARCHAR2 sensor_id FK
        FLOAT valor
        TIMESTAMP timestamp
    }
    AREAS ||--o{ SENSORES : possui
    SENSORES ||--o{ LEITURAS : registra
```

### Motivo da Escolha do Modelo

1. **Modularidade e Clareza**:
   - O modelo separa as entidades em tabelas distintas (`areas`, `sensores`, `leituras`), garantindo modularidade e facilitando a manutenção.

2. **Relacionamentos Claros**:
   - Cada sensor está vinculado a uma área (`area_id` como chave estrangeira em `sensores`).
   - Cada leitura está vinculada a um sensor (`sensor_id` como chave estrangeira em `leituras`).

3. **Integridade Referencial**:
   - O uso de chaves estrangeiras (`FK`) garante que sensores só podem ser associados a áreas existentes e leituras só podem ser registradas para sensores válidos.

4. **Escalabilidade**:
   - O modelo permite a expansão para novas áreas, sensores e leituras sem necessidade de alterações significativas na estrutura.

5. **Unicidade e Controle**:
   - O campo `codigo_patrimonio` em `sensores` é único, garantindo que cada sensor tenha um identificador exclusivo.

Esse modelo foi escolhido para atender às necessidades do sistema, garantindo consistência nos dados e facilidade de integração com o sistema de sensores e o simulador.