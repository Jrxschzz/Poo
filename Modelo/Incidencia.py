class Incidencia:
    def __init__(self, id, titulo, descripcion, fecha, afectados):
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha = fecha
        self.afectados = afectados or []
        self.riesgo = "MEDIO"

    def limpieza_datos(self):
        if isinstance(self.titulo, str):
            self.titulo = self.titulo.strip()
        if isinstance(self.descripcion, str):
            self.descripcion = self.descripcion.strip()
        self.fecha = str(self.fecha).strip()
        self.afectados = [str(a).strip() for a in (self.afectados or [])]

    def calcular_riesgo(self):
        return self.riesgo

    def recomendaciones(self):
        return "Revisar y aislar recursos afectados."

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items()}