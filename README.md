# Agro Metrics

O **Agro Metrics** é um sistema de linha de comando para a gestão de sensores agrícolas e o processamento de leituras. Ele permite o gerenciamento de áreas, sensores e medições, além de importar e exportar dados em formato CSV.

## Funcionalidades

- **Gerenciamento de Áreas**: Adicionar, listar e remover áreas agrícolas.
- **Gerenciamento de Sensores**: Adicionar, listar e remover sensores vinculados a áreas.
- **Registro de Leituras**: Cadastrar medições para sensores.
- **Importação de Leituras**: Importar medições de sensores a partir de arquivos CSV.
- **Exportação de Leituras**: Exportar todas as medições de uma área para um arquivo CSV.

## Requisitos

- Python 3.8 ou superior
- Banco de dados Oracle (configurado via `docker-compose.yml`)
- Dependências Python (listadas em `requirements.txt`)

## Instalação

1. Clone o repositório:
   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd agro_metrics
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

- **`agro_metrics/core/services`**: Contém a lógica de negócios para áreas e sensores.
- **`agro_metrics/core/repositories`**: Implementa a comunicação com o banco de dados Oracle.
- **`database/schema.sql`**: Script para criar as tabelas no banco de dados.
- **`database/seed.sql`**: Script para popular o banco de dados com dados iniciais.
- **`database/rollback.sql`**: Script para remover as tabelas do banco de dados.

## Contribuindo

Contribuições são bem-vindas! Siga os passos abaixo para contribuir:

1. Faça um fork do repositório.
2. Crie uma branch para sua feature ou correção:
   ```bash
   git checkout -b minha-feature
   ```
3. Faça suas alterações e adicione os commits:
   ```bash
   git add .
   git commit -m "Descrição da minha feature"
   ```
4. Envie suas alterações para o repositório remoto:
   ```bash
   git push origin minha-feature
   ```
5. Abra um Pull Request no repositório original.