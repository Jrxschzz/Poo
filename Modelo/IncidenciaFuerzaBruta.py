from Modelo.Incidencia import Incidencia


class IncidenciaFuerzaBruta(Incidencia):
    def __init__(self, id, titulo, descripcion, fecha, afectados, num_intentos):
        super().__init__(id, titulo, descripcion, fecha, afectados)
        self.num_intentos = num_intentos
        self.riesgo = "ALTO"

    def limpieza_datos(self):
        super().limpieza_datos()
        self.num_intentos = int(self.num_intentos)

    def calcular_riesgo(self):
        try:
            numero_intentos = int(self.num_intentos)
            if numero_intentos > 1000:
                self.riesgo = "CRÍTICO"
            elif numero_intentos > 100:
                self.riesgo = "ALTO"
            else:
                self.riesgo = "MEDIO"
        except Exception:
            self.riesgo = "MEDIO"
        return self.riesgo

    def recomendaciones(self):
        return "Bloquear IPs sospechosas, reforzar contraseñas y activar autenticación en dos pasos."