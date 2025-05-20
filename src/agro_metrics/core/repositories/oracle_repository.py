import os
import oracledb

class OracleRepository:
    def __init__(self):
        user = os.getenv("ORACLE_USER")
        password = os.getenv("ORACLE_PASSWORD")
        dsn = os.getenv("ORACLE_DSN")
        self.conn = oracledb.connect(user=user, password=password, dsn=dsn)

    # Área
    def area_existe(self, area_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM areas WHERE area_id = :1", [area_id])
        result = cursor.fetchone()[0]
        cursor.close()
        return result > 0

    def inserir_area(self, area_id, nome, coordenadas):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO areas (area_id, nome, latitude, longitude)
            VALUES (:1, :2, :3, :4)
        """, (area_id, nome, coordenadas[0], coordenadas[1]))
        self.conn.commit()
        cursor.close()

    def listar_areas(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT area_id, nome, latitude, longitude FROM areas")
        areas = []
        for row in cursor.fetchall():
            areas.append({
                "area_id": row[0],
                "nome": row[1],
                "coordenadas": [row[2], row[3]]
            })
        cursor.close()
        return areas

    def remover_area(self, area_id):
        cursor = self.conn.cursor()
        try:
            cursor.execute("DELETE FROM areas WHERE area_id = :1", [area_id])
            self.conn.commit()
        except oracledb.IntegrityError as e:
            if "SYSTEM.FK_AREA" in str(e):
                raise ValueError(f"Não é possível remover a área '{area_id}' porque ela está vinculada a sensores.")
            else:
                raise
        finally:
            cursor.close()

    def get_coordenadas_area(self, area_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT latitude, longitude FROM areas WHERE area_id = :1", [area_id])
        row = cursor.fetchone()
        cursor.close()
        return [row[0], row[1]] if row else None

    # Sensor
    def sensor_existe(self, sensor_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sensores WHERE sensor_id = :1", [sensor_id])
        result = cursor.fetchone()[0]
        cursor.close()
        return result > 0

    def sensor_codigo_existe(self, codigo_patrimonio):
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sensores WHERE codigo_patrimonio = :1", [codigo_patrimonio])
        result = cursor.fetchone()[0]
        cursor.close()
        return result > 0

    def inserir_sensor(self, sensor_id, tipo, area_id, coordenadas, codigo_patrimonio):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO sensores (sensor_id, tipo, area_id, latitude, longitude, ativo, codigo_patrimonio)
            VALUES (:1, :2, :3, :4, :5, :6, :7)
        """, (sensor_id, tipo, area_id, coordenadas[0], coordenadas[1], 1, codigo_patrimonio))
        self.conn.commit()
        cursor.close()

    def listar_sensores(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT sensor_id, codigo_patrimonio, tipo, area_id, ativo FROM sensores")
        sensores = []
        for row in cursor.fetchall():
            sensores.append({
                "sensor_id": row[0],
                "codigo_patrimonio": row[1],
                "tipo": row[2],
                "area_id": row[3],
                "ativo": bool(row[4])
            })
        cursor.close()
        return sensores

    def listar_sensores_por_area(self, area_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT sensor_id, codigo_patrimonio
            FROM sensores
            WHERE area_id = :1
        """, [area_id])
        sensores = [{"sensor_id": row[0], "codigo_patrimonio": row[1]} for row in cursor.fetchall()]
        cursor.close()
        return sensores

    def remover_sensor(self, sensor_id):
        cursor = self.conn.cursor()
        try:
            cursor.execute("DELETE FROM sensores WHERE sensor_id = :1", [sensor_id])
            self.conn.commit()
        except oracledb.IntegrityError as e:
            if "FK_SENSOR" in str(e):
                raise ValueError(f"Não é possível remover o sensor '{sensor_id}' porque ele está vinculado a leituras.")
            else:
                raise
        finally:
            cursor.close()

    def get_sensor_id_by_codigo(self, codigo_patrimonio):
        cursor = self.conn.cursor()
        cursor.execute("SELECT sensor_id FROM sensores WHERE codigo_patrimonio = :1", [codigo_patrimonio])
        row = cursor.fetchone()
        cursor.close()
        if not row:
            raise ValueError(f"Sensor com código de patrimônio '{codigo_patrimonio}' não encontrado.")
        return row[0]

    def sensores_existem_na_area(self, area_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT COUNT(*)
            FROM sensores
            WHERE area_id = :1
        """, [area_id])
        result = cursor.fetchone()[0]
        cursor.close()
        return result > 0

    def listar_leituras_por_area(self, area_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT l.sensor_id, s.codigo_patrimonio, l.valor, l.timestamp
            FROM leituras l
            JOIN sensores s ON l.sensor_id = s.sensor_id
            WHERE s.area_id = :1
        """, [area_id])
        leituras = [{"sensor_id": row[0], "codigo_patrimonio": row[1], "valor": row[2], "timestamp": row[3]} for row in cursor.fetchall()]
        cursor.close()
        return leituras

    def salvar_leitura(self, leitura: dict):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO leituras (sensor_id, valor, timestamp)
            VALUES (:1, :2, :3)
        """, (
            leitura["sensor_id"],
            leitura["valor"],
            leitura["timestamp"],
        ))
        self.conn.commit()
        cursor.close()

    def sensor_existe_na_area(self, codigo_patrimonio, area_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT COUNT(*)
            FROM sensores
            WHERE codigo_patrimonio = :1 AND area_id = :2
        """, [codigo_patrimonio, area_id])
        result = cursor.fetchone()[0]
        cursor.close()
        return result > 0
