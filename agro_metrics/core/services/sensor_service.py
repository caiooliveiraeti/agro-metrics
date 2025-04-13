import uuid
from datetime import datetime
from ...core.repositories.repository_factory import get_repository
import csv

class SensorService:
    def __init__(self):
        self.repo = get_repository()

    def adicionar_sensor(self, tipo: str, area_id: str, codigo_patrimonio: str):
        if self.repo.sensor_codigo_existe(codigo_patrimonio):
            raise ValueError(f"Sensor com código de patrimônio '{codigo_patrimonio}' já cadastrado.")

        if not self.repo.area_existe(area_id):
            raise ValueError(f"Área '{area_id}' não cadastrada.")

        coordenadas = self.repo.get_coordenadas_area(area_id)
        if not coordenadas:
            raise ValueError(f"Coordenadas da área '{area_id}' não definidas.")

        sensor_id = str(uuid.uuid4())  # Generate a UUID for the sensor_id
        self.repo.inserir_sensor(sensor_id, tipo, area_id, coordenadas, codigo_patrimonio)
        print(f"✅ Sensor com código de patrimônio '{codigo_patrimonio}' adicionado com sucesso à área '{area_id}'.")

    def listar_sensores(self):
        sensores = self.repo.listar_sensores()
        if not sensores:
            print("📭 Nenhum sensor cadastrado.")
            return
        print(f"{'ID':<40} | {'Código Patrimônio':<20} | {'Tipo':<10} | {'Área':<40} | {'Status':<10}")
        print("-" * 135)
        for sensor in sensores:
            status = "Ativo" if sensor.get("ativo", False) else "Inativo"
            print(f"{sensor['sensor_id']:<40} | {sensor['codigo_patrimonio']:<20} | {sensor['tipo']:<10} | {sensor['area_id']:<40} | {status:<10}")

    def remover_sensor(self, sensor_id: str):
        if not self.repo.sensor_existe(sensor_id):
            raise ValueError(f"Sensor '{sensor_id}' não encontrado.")
        self.repo.remover_sensor(sensor_id)
        print(f"🗑️ Sensor '{sensor_id}' removido com sucesso.")

    def cadastrar_metrica(self, codigo_patrimonio: str, valor: float, timestamp: str):
        if not self.repo.sensor_codigo_existe(codigo_patrimonio):
            raise ValueError(f"Sensor com código de patrimônio '{codigo_patrimonio}' não encontrado.")

        try:
            timestamp_utc = datetime.fromisoformat(timestamp)
        except ValueError:
            raise ValueError("O timestamp deve estar no formato ISO 8601 (YYYY-MM-DDTHH:MM:SS).")

        sensor_id = self.repo.get_sensor_id_by_codigo(codigo_patrimonio)
        self.repo.salvar_leitura({
            "sensor_id": sensor_id,
            "valor": valor,
            "timestamp": timestamp_utc,
            "classificacao": None  # Placeholder for classification logic
        })
        print(f"✅ Métrica registrada para o sensor '{codigo_patrimonio}' com valor '{valor}' no timestamp '{timestamp_utc}'.")

    def importar_leituras_csv(self, csv_file_path: str):
        try:
            with open(csv_file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    timestamp = row.get("timestamp")
                    codigo_patrimonio = row.get("codigo_patrimonio")
                    medida = float(row.get("medida"))

                    if not timestamp or not codigo_patrimonio or not medida:
                        print(f"⚠️ Linha inválida no arquivo CSV: {row}")
                        continue

                    # Validate and process the timestamp
                    try:
                        timestamp_utc = datetime.fromisoformat(timestamp)
                    except ValueError:
                        print(f"⚠️ Timestamp inválido: {timestamp}")
                        continue

                    # Register the metric
                    self.cadastrar_metrica(codigo_patrimonio, medida, timestamp)
                print("✅ Importação de leituras concluída com sucesso.")
        except FileNotFoundError:
            print(f"❌ Arquivo CSV não encontrado: {csv_file_path}")
        except Exception as e:
            print(f"❌ Erro ao importar leituras: {e}")

    def exportar_medicoes_area(self, area_id: str, output_csv_path: str):
        if not self.repo.area_existe(area_id):
            raise ValueError(f"Área '{area_id}' não encontrada.")

        if not self.repo.sensores_existem_na_area(area_id):
            raise ValueError(f"Não há sensores cadastrados para a área '{area_id}'.")

        leituras = self.repo.listar_leituras_por_area(area_id)
        if not leituras:
            raise ValueError(f"Não há medições registradas para a área '{area_id}'.")

        with open(output_csv_path, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["sensor_id", "codigo_patrimonio", "valor", "timestamp"])
            for leitura in leituras:
                writer.writerow([leitura["sensor_id"], leitura["codigo_patrimonio"], leitura["valor"], leitura["timestamp"]])

        print(f"✅ Medições da área '{area_id}' exportadas com sucesso para '{output_csv_path}'.")