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
        
class IncidenciaPhishing(Incidencia):
    def __init__(self, id, titulo, descripcion, fecha, afectados, url_sospechosa):
        super().__init__(id, titulo, descripcion, fecha, afectados)
        self.url_sospechosa = url_sospechosa
        self.riesgo = "ALTO"  # Valor por defecto del riesgo para phishing

class IncidenciaMalware(Incidencia):
    def __init__(self, id, titulo, descripcion, fecha, afectados, tipo_malware):
        super().__init__(id, titulo, descripcion, fecha, afectados)
        self.tipo_malware = tipo_malware
        self.riesgo = "ALTO"  # Valor por defecto del riesgo para malware