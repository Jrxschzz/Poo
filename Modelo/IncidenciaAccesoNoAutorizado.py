from Modelo.Incidencia import Incidencia


class IncidenciaAccesoNoAutorizado(Incidencia):
    def __init__(self, id, titulo, descripcion, fecha, afectados, metodo_acceso):
        super().__init__(id, titulo, descripcion, fecha, afectados)
        self.metodo_acceso = metodo_acceso
        self.riesgo = "ALTO"

    def limpieza_datos(self):
        super().limpieza_datos()
        if isinstance(self.metodo_acceso, str):
            self.metodo_acceso = self.metodo_acceso.strip()

    def calcular_riesgo(self):
        texto = str(self.metodo_acceso).lower()
        if "explot" in texto or "root" in texto or "privileg" in texto:
            self.riesgo = "CRÍTICO"
        else:
            self.riesgo = "ALTO"
        return self.riesgo

    def recomendaciones(self):
        return "Revisar el acceso, eliminar credenciales."