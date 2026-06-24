from Modelo.Incidencia import Incidencia

class IncidenciaPhishing(Incidencia):
    def __init__(self, id, titulo, descripcion, fecha, afectados, url_sospechosa):
        super().__init__(id, titulo, descripcion, fecha, afectados)
        self.url_sospechosa = url_sospechosa
        self.riesgo = "ALTO"
    
    def limpieza_datos(self):
        super().limpieza_datos()
        self.url_sospechosa = self.url_sospechosa.strip()
