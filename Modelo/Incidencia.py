import json
import os

class Incidencia:
    def __init__(self, id, titulo, descripcion, fecha, afectados):
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha = fecha
        self.afectados = afectados
        self.riesgo = "MEDIO"  # Valor por defecto del riesgo
        