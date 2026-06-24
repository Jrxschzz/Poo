from Modelo.Incidencia import Incidencia

class IncidenciaAccesoNoAutorizado(Incidencia):
    def __init__(self, id, titulo, descripcion, fecha, afectados, metodo_acceso):
        super().__init__(id, titulo, descripcion, fecha, afectados)
        self.metodo_acceso = metodo_acceso
        self.riesgo = "ALTO"
    
    def limpieza_datos(self):
        super().limpieza_datos()
        self.metodo_acceso = self.metodo_acceso.strip()