# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Agro Metrics

### Integrantes:
- <a href="https://www.linkedin.com/in/caiooliveiraeti">Caio Oliveira</a>
- <a href="https://www.linkedin.com/in/en%C3%A9as-moreira-4bbaab136">Enéas Moreira</a>
- <a href="https://www.linkedin.com/in/william--xavier">William Xavier</a> 

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
- **Registro de Leituras**: Cadastrar medições para sensores.
- **Importação de Leituras**: Importar medições de sensores a partir de arquivos CSV.
- **Exportação de Leituras**: Exportar todas as medições de uma área para arquivos CSV ou JSON.

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
   git clone <URL_DO_REPOSITORIO>
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