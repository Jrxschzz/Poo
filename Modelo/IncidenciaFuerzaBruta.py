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
            n = int(self.num_intentos)
            if n > 1000:
                self.riesgo = 'CRÍTICO'
            elif n > 100:
                self.riesgo = 'ALTO'
            else:
                self.riesgo = 'MEDIO'
        except Exception:
            self.riesgo = 'MEDIO'
        return self.riesgo

    def recomendaciones(self):
        return 'Bloquear IPs, forzar restablecimiento de contraseñas y activar autenticación multifactor.'