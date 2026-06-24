from Modelo.Incidencia import Incidencia

class IncidenciaFuerzaBruta(Incidencia):
    def __init__(self, id, titulo, descripcion, fecha, afectados, num_intentos):
        super().__init__(id, titulo, descripcion, fecha, afectados)
        self.num_intentos = num_intentos
        self.riesgo = "ALTO"
    
    def limpieza_datos(self):
        super().limpieza_datos()
        self.num_intentos = int(self.num_intentos)