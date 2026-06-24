from Modelo.Incidencia import Incidencia

class IncidenciaFugaDeDatos(Incidencia):
    def __init__(self, id, titulo, descripcion, fecha, afectados, tipo_dato):
        super().__init__(id, titulo, descripcion, fecha, afectados)
        self.tipo_dato = tipo_dato
        self.riesgo = "ALTO"
    
    def limpieza_datos(self):
        super().limpieza_datos()
        self.tipo_dato = self.tipo_dato.strip()