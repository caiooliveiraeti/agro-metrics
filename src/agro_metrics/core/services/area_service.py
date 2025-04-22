import uuid
from ...core.repositories.repository_factory import get_repository

class AreaService:
    def __init__(self):
        self.repo = get_repository()

    def adicionar_area(self, nome: str, coordenadas: list):
        area_id = str(uuid.uuid4())  # Generate a UUID for the area_id
        if self.repo.area_existe(area_id):
            raise ValueError(f"Área '{area_id}' já cadastrada.")

        self.repo.inserir_area(area_id, nome, coordenadas)
        print(f"✅ Área '{area_id}' cadastrada com sucesso.")

    def listar_areas(self):
        areas = self.repo.listar_areas()
        if not areas:
            print("📭 Nenhuma área cadastrada.")
            return
        print(f"{'ID':<40} | {'Nome':<20} | {'Coordenadas':<30}")
        print("-" * 95)
        for area in areas:
            coords = f"({area['coordenadas'][0]}, {area['coordenadas'][1]})"
            print(f"{area['area_id']:<40} | {area['nome']:<20} | {coords:<30}")

    def remover_area(self, area_id: str):
        if not self.repo.area_existe(area_id):
            raise ValueError(f"Área '{area_id}' não encontrada.")
        self.repo.remover_area(area_id)
        print(f"🗑️ Área '{area_id}' removida com sucesso.")