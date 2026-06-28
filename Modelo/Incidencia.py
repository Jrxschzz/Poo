from abc import ABC, abstractmethod

class Incidencia(ABC):
    def __init__(self, id, titulo, descripcion, fecha, afectados):
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha = fecha
        self.afectados = afectados or []
        self.riesgo = "MEDIO"

    def limpieza_datos(self):
        if isinstance(self.titulo, str):
            self.titulo = self.titulo.strip()
        if isinstance(self.descripcion, str):
            self.descripcion = self.descripcion.strip()

    @abstractmethod
    def calcular_riesgo(self):
        pass

    @abstractmethod
    def recomendaciones(self):
        pass