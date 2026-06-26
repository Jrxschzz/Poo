from Modelo.Incidencia import Incidencia


class IncidenciaFugaDeDatos(Incidencia):
    def __init__(self, id, titulo, descripcion, fecha, afectados, tipo_dato):
        super().__init__(id, titulo, descripcion, fecha, afectados)
        self.tipo_dato = tipo_dato
        self.riesgo = "ALTO"

    def limpieza_datos(self):
        super().limpieza_datos()
        if isinstance(self.tipo_dato, str):
            self.tipo_dato = self.tipo_dato.strip()

    def calcular_riesgo(self):
        texto = str(self.tipo_dato).lower()
        if "sensibl" in texto or "credit" in texto or "dni" in texto:
            self.riesgo = "CRÍTICO"
        else:
            self.riesgo = "ALTO"
        return self.riesgo

    def recomendaciones(self):
        return "Notificar a los afectados, investigar el alcance y reforzar los controles de acceso."