from Modelo.Incidencia import Incidencia

class IncidenciaPhishing(Incidencia):
    def __init__(self, id, titulo, descripcion, fecha, afectados, url_sospechosa):
        super().__init__(id, titulo, descripcion, fecha, afectados)
        self.url_sospechosa = url_sospechosa
        self.calcular_riesgo()

    def to_dict(self):
        datos = super().to_dict()
        datos['url_sospechosa'] = self.url_sospechosa
        return datos

    def limpieza_datos(self):
        super().limpieza_datos()
        if isinstance(self.url_sospechosa, str):
            self.url_sospechosa = self.url_sospechosa.strip()

    def calcular_riesgo(self):
        if not self.url_sospechosa:
            self.riesgo = "MEDIO"
        else:
            self.riesgo = "ALTO"
        return self.riesgo

    def recomendaciones(self):
        return "avisar a los usuarios y cambiar credenciales comprometidas."
