import uuid
from datetime import datetime
from ...core.repositories.repository_factory import get_repository
import csv
import json

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

    def _exportar_medicoes(self, area_id: str, output_path: str, formato: str):
        if not self.repo.area_existe(area_id):
            raise ValueError(f"Área '{area_id}' não encontrada.")

        if not self.repo.sensores_existem_na_area(area_id):
            raise ValueError(f"Não há sensores cadastrados para a área '{area_id}'.")

        leituras = self.repo.listar_leituras_por_area(area_id)
        if not leituras:
            raise ValueError(f"Não há medições registradas para a área '{area_id}'.")

        if formato == "csv":
            with open(output_path, mode='w', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["sensor_id", "codigo_patrimonio", "valor", "timestamp"])
                for leitura in leituras:
                    writer.writerow([leitura["sensor_id"], leitura["codigo_patrimonio"], leitura["valor"], leitura["timestamp"]])
        elif formato == "json":
            with open(output_path, mode='w', encoding='utf-8') as file:
                json.dump(leituras, file, indent=4, default=str)
        else:
            raise ValueError("Formato de exportação inválido. Use 'csv' ou 'json'.")

        print(f"✅ Medições da área '{area_id}' exportadas com sucesso para '{output_path}'.")

    def exportar_medicoes_area_csv(self, area_id: str, output_csv_path: str):
        self._exportar_medicoes(area_id, output_csv_path, "csv")

    def exportar_medicoes_area_json(self, area_id: str, output_json_path: str):
        self._exportar_medicoes(area_id, output_json_path, "json")

    def conectar_sensores(self, area_id: str, sensores: dict, serial_url: str):
        for tipo, codigo_patrimonio in sensores.items():
            if not self.repo.sensor_existe_na_area(codigo_patrimonio, area_id):
                raise ValueError(f"Sensor '{codigo_patrimonio}' ({tipo}) não encontrado na área '{area_id}'.")

        print("📡 Conectando à serial...")
        try:
            import serial
            with serial.serial_for_url(serial_url, baudrate=115200) as ser:
                print("✅ Conexão estabelecida. Pressione Ctrl+C para encerrar.")
                while True:
                    try:
                        linha = ser.readline().decode("utf-8").strip()
                        if linha.startswith("DATA:"):
                            dados = {
                                item.split("=")[0]: item.split("=")[1]
                                for item in linha.replace("DATA:", "").split(",")
                            }
                            for tipo, codigo_patrimonio in sensores.items():
                                valor = None
                                if tipo == "umidade":
                                    valor = float(dados.get("H", -1))
                                elif tipo == "ph":
                                    valor = float(dados.get("PH", -1))
                                elif tipo == "p":
                                    valor = int(dados.get("P", 0))
                                elif tipo == "f":
                                    valor = int(dados.get("K", 0))

                                if valor is not None:
                                    self.cadastrar_metrica(codigo_patrimonio, valor, datetime.utcnow().isoformat())
                    except KeyboardInterrupt:
                        print("\n👋 Conexão encerrada pelo usuário.")
                        break
        except Exception as e:
            raise RuntimeError(f"Erro ao conectar à serial: {e}")