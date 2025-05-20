from .core.services.sensor_service import SensorService
from .core.services.area_service import AreaService
import questionary

area_service = AreaService()
sensor_service = SensorService()

def executar():
    while True:
        escolha = questionary.select(
            "O que você deseja fazer?",
            choices=[
                "1. Adicionar Área",
                "2. Listar Áreas",
                "3. Remover Área",
                "4. Adicionar Sensor",
                "5. Listar Sensores",
                "6. Remover Sensor",
                "7. Cadastrar Leitura",
                "8. Importar Leituras de CSV",
                "9. Exportar Leituras de uma Área",
                "10. Conectar Sensores",
                "99. Sair"
            ]
        ).ask()

        if escolha is None:  # Handle interruption gracefully
            print("\n👋 Encerrando...")
            break

        try:
            if escolha.startswith("1."):
                nome = questionary.text("Nome da área:").ask()
                lat = float(questionary.text("Latitude:").ask())
                lon = float(questionary.text("Longitude:").ask())
                area_service.adicionar_area(nome, [lat, lon])

            elif escolha.startswith("2."):
                area_service.listar_areas()

            elif escolha.startswith("3."):
                area_id = questionary.text("ID da área a remover:").ask()
                if not area_service.repo.area_existe(area_id):
                    print(f"⚠️ Área '{area_id}' não encontrada.")
                    continue
                area_service.remover_area(area_id)

            elif escolha.startswith("4."):
                tipo = questionary.select("Tipo do sensor:", choices=["umidade", "ph", "ce"]).ask()
                area_id = questionary.text("ID da área vinculada:").ask()
                if not area_service.repo.area_existe(area_id):
                    print(f"⚠️ Área '{area_id}' não encontrada.")
                    continue
                codigo_patrimonio = questionary.text("Código de patrimônio do sensor:").ask()
                sensor_service.adicionar_sensor(tipo, area_id, codigo_patrimonio)

            elif escolha.startswith("5."):
                sensor_service.listar_sensores()

            elif escolha.startswith("6."):
                sensor_id = questionary.text("ID do sensor a remover:").ask()
                if not sensor_service.repo.sensor_existe(sensor_id):
                    print(f"⚠️ Sensor '{sensor_id}' não encontrado.")
                    continue
                sensor_service.remover_sensor(sensor_id)

            elif escolha.startswith("7."):
                codigo_patrimonio = questionary.text("Código de patrimônio do sensor:").ask()
                if not sensor_service.repo.sensor_codigo_existe(codigo_patrimonio):
                    print(f"⚠️ Sensor com código de patrimônio '{codigo_patrimonio}' não encontrado.")
                    continue
                valor = float(questionary.text("Valor medido:").ask())
                timestamp = questionary.text("Timestamp (UTC, formato ISO 8601):").ask()
                sensor_service.cadastrar_metrica(codigo_patrimonio, valor, timestamp)

            elif escolha.startswith("8."):
                csv_file_path = questionary.text("Caminho do arquivo CSV:").ask()
                sensor_service.importar_leituras_csv(csv_file_path)

            elif escolha.startswith("9."):
                area_id = questionary.text("ID da área:").ask()
                if not area_service.repo.area_existe(area_id):
                    print(f"⚠️ Área '{area_id}' não encontrada.")
                    continue

                formato = questionary.select(
                    "Escolha o formato de exportação:",
                    choices=["CSV", "JSON"]
                ).ask()

                output_path = questionary.text("Caminho para salvar o arquivo:").ask()

                if formato == "CSV":
                    sensor_service.exportar_medicoes_area_csv(area_id, output_path)
                elif formato == "JSON":
                    sensor_service.exportar_medicoes_area_json(area_id, output_path)

            elif escolha.startswith("10."):
                area_id = questionary.text("ID da área:").ask()
                if not area_service.repo.area_existe(area_id):
                    print(f"⚠️ Área '{area_id}' não encontrada.")
                    continue

                sensores = {
                    "umidade": questionary.text("Código de patrimônio do sensor de umidade:").ask(),
                    "ph": questionary.text("Código de patrimônio do sensor de pH:").ask(),
                    "p": questionary.text("Código de patrimônio do sensor de fósforo (P):").ask(),
                    "f": questionary.text("Código de patrimônio do sensor de potássio (F):").ask(),
                }

                # Filtrar sensores com código de patrimônio vazio
                sensores = {tipo: codigo for tipo, codigo in sensores.items() if codigo}

                if not sensores:
                    print("⚠️ Nenhum sensor válido foi informado.")
                    continue

                for tipo, codigo in sensores.items():
                    if not sensor_service.repo.sensor_existe_na_area(codigo, area_id):
                        print(f"⚠️ Sensor '{codigo}' ({tipo}) não encontrado na área '{area_id}'.")
                        break
                else:
                    serial_url = questionary.text("Serial url (ex: rfc2217://localhost:4400)").ask()
                    try:
                        sensor_service.conectar_sensores(area_id, sensores, serial_url)
                    except Exception as e:
                        print(f"⚠️ Erro ao conectar sensores: {e}")

            elif escolha.startswith("99."):
                print("👋 Encerrando...")
                break

        except Exception as e:
            print(f"⚠️ Erro: {e}")
