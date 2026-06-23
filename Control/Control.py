class gestorIncidencias:
    def __init__(self):
        self.incidencias = []

    def agregar_incidencia(self, incidencia):
        self.incidencias.append(incidencia)

    def obtener_incidencias(self):
        return self.incidencias