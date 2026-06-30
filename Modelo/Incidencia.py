from abc import ABC, abstractmethod
from datetime import date

class Incidencia(ABC):
    def __init__(self, id, titulo, descripcion, fecha):
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion

        if isinstance(fecha, str):
            self.fecha = date.fromisoformat(fecha)
        elif isinstance(fecha, date):
            self.fecha = fecha
        elif fecha is None:
            self.fecha = date.today()
        else:
            raise ValueError('Fecha inválida; debe ser un objeto date o una cadena ISO.')

        self.riesgo = "MEDIO"

    def limpieza_datos(self):
        if isinstance(self.titulo, str):
            self.titulo = self.titulo.strip()
        if isinstance(self.descripcion, str):
            self.descripcion = self.descripcion.strip()

    def pasar_diccionario(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'fecha': self.fecha.isoformat() if isinstance(self.fecha, date) else str(self.fecha),
        }

    @abstractmethod
    def calcular_riesgo(self):
        pass

    @abstractmethod
    def recomendaciones(self):
        pass