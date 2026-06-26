class gestorIncidencias:
    def __init__(self):
        self.incidencias = []

    def agregar_incidencia(self, incidencia):
        self.incidencias.append(incidencia)

    def obtener_incidencias(self):
        return self.incidencias
    
    def guardar_json(self, ruta):
        import json
        lista = []
        for inc in self.incidencias:
            d = dict(inc.__dict__)
            d['tipo'] = inc.__class__.__name__
            lista.append(d)
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(lista, f, ensure_ascii=False, indent=2)

    def cargar_json(self, ruta, constructor_map=None):
        import json
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                datos = json.load(f)
        except FileNotFoundError:
            self.incidencias = []
            return
        self.incidencias = []
        for d in datos:
            tipo = d.pop('tipo', None)
            if constructor_map and tipo in constructor_map:
                ctor = constructor_map[tipo]
                try:
                    obj = ctor(**d)
                except TypeError:
                    obj = ctor(d.get('id'), d.get('titulo'), d.get('descripcion'), d.get('fecha'), d.get('afectados'))
                self.incidencias.append(obj)
            else:
                from Modelo.Incidencia import Incidencia
                obj = Incidencia(d.get('id'), d.get('titulo'), d.get('descripcion'), d.get('fecha'), d.get('afectados'))
                self.incidencias.append(obj)