import sys
import os
import streamlit as st
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Control.Control import gestorIncidencias
from Modelo.Incidencia import Incidencia
from Modelo.IncidenciaMalware import IncidenciaMalware
from Modelo.IncidenciaPhishing import IncidenciaPhishing
from Modelo.IncidenciaFuerzaBruta import IncidenciaFuerzaBruta
from Modelo.IncidenciaAccesoNoAutorizado import IncidenciaAccesoNoAutorizado
from Modelo.IncidenciaFugaDeDatos import IncidenciaFugaDeDatos
from Modelo.Excepciones import ValidacionException, GestorDatosException

st.set_page_config(page_title='Gestor de Incidencias de Ciberseguridad', layout='wide')

ruta_json = os.path.join(os.path.dirname(__file__), '..', 'incidencias.json')

clases_incidentes = [
    ('Phishing', IncidenciaPhishing),
    ('Malware', IncidenciaMalware),
    ('Fuerza Bruta', IncidenciaFuerzaBruta),
    ('Fuga de Datos', IncidenciaFugaDeDatos),
    ('Acceso No Autorizado', IncidenciaAccesoNoAutorizado),
]

constructor_map_json = {
    'IncidenciaPhishing': IncidenciaPhishing,
    'IncidenciaMalware': IncidenciaMalware,
    'IncidenciaFuerzaBruta': IncidenciaFuerzaBruta,
    'IncidenciaFugaDeDatos': IncidenciaFugaDeDatos,
    'IncidenciaAccesoNoAutorizado': IncidenciaAccesoNoAutorizado
}

if 'gestor' not in st.session_state:
    gestor_inicial = gestorIncidencias()
    gestor_inicial.cargar_json(ruta_json, constructor_map=constructor_map_json)
    st.session_state['gestor'] = gestor_inicial
gestor = st.session_state['gestor']

st.title("Centro de Control de Incidencias de Seguridad")

columna_formulario, columna_listado = st.columns([1, 2])

with columna_formulario:
    st.header("Registrar Alerta")
    
    with st.form("formulario_incidencia", clear_on_submit=True):
        id_input = st.text_input("ID de la Incidencia (Ej: INC-001)")
        titulo_input = st.text_input("Título descriptivo")
        desc_input = st.text_area("Descripción detallada del suceso")
        fecha_input = st.date_input("Fecha de detección")
        afectados_input = st.text_input("Usuarios/Sistemas afectados (separados por comas)")
        
        tipo_seleccionado = st.selectbox("Categoría de la Amenaza", [t[0] for t in clases_incidentes])
        
        campo_especifico = ""
        if tipo_seleccionado == 'Phishing':
            campo_especifico = st.text_input("URL Sospechosa / Enlace del correo")
        elif tipo_seleccionado == 'Malware':
            campo_especifico = st.text_input("Tipo de Malware detectado (Ej: Ransomware)")
        elif tipo_seleccionado == 'Fuerza Bruta':
            campo_especifico = st.number_input("Número de intentos de login registrados", min_value=1, step=1, value=1)
        elif tipo_seleccionado == 'Fuga de Datos':
            campo_especifico = st.text_input("Tipo de información expuesta (Ej: DNI, Tarjetas)")
        elif tipo_seleccionado == 'Acceso No Autorizado':
            campo_especifico = st.text_input("Método de acceso empleado (Ej: Root)")

        boton_enviar = st.form_submit_button("Dar de alta incidencia")

        if boton_enviar:
            try:
                if not id_input.strip() or not titulo_input.strip() or not desc_input.strip():
                    raise ValidacionException("Todos los campos principales son obligatorios.")
                
                lista_afectados = [a.strip() for a in afectados_input.split(",") if a.strip()] if afectados_input else []
                
                clase_elegida = next(c[1] for c in clases_incidentes if c[0] == tipo_seleccionado)
                
                kwargs = {
                    'id': id_input.strip(),
                    'titulo': titulo_input.strip(),
                    'descripcion': desc_input.strip(),
                    'fecha': str(fecha_input),
                    'afectados': lista_afectados
                }
                
                if tipo_seleccionado == 'Phishing': kwargs['url_sospechosa'] = campo_especifico
                elif tipo_seleccionado == 'Malware': kwargs['tipo_malware'] = campo_especifico
                elif tipo_seleccionado == 'Fuerza Bruta': kwargs['num_intentos'] = campo_especifico
                elif tipo_seleccionado == 'Fuga de Datos': kwargs['tipo_dato'] = campo_especifico
                elif tipo_seleccionado == 'Acceso No Autorizado': kwargs['metodo_acceso'] = campo_especifico
                
                nueva_incidencia = clase_elegida(**kwargs)
                
                nueva_incidencia.limpieza_datos()
                nueva_incidencia.calcular_riesgo()
                
                gestor.agregar_incidencia(nueva_incidencia)
                gestor.guardar_json(ruta_json)
                
                st.success(f"✔️ Incidencia registrada correctamente.")
                st.rerun()

            except ValidacionException as error_v:
                st.error(f"Error en el formulario: {error_v}")
            except GestorDatosException as error_d:
                st.error(f"Error en el archivo de datos: {error_d}")
            except Exception as e:
                st.error(f"Error inesperado: {e}")

with columna_listado:
    st.header("Historial y Análisis de Riesgo")
    
    incidencias_actuales = gestor.obtener_incidencias()
    
    if not incidencias_actuales:
        st.info("No hay incidencias registradas en el sistema actualmente.")
    else:
        datos_tabla = []
        for inc in incidencias_actuales:
            datos_tabla.append({
                'id': inc.id,
                'titulo': inc.titulo,
                'tipo': inc.__class__.__name__.replace('Incidencia', ''),
                'riesgo': inc.riesgo,
                'fecha': inc.fecha,
                'descripcion': inc.descripcion,
                'objeto_real': inc  
            })
            
        tabla = pd.DataFrame(datos_tabla)
        
        columna_filtro_tipo, columna_filtro_riesgo = st.columns(2)
        with columna_filtro_tipo:
            filtro_tipo = st.selectbox("Filtrar por Categoría", ["Todos"] + list(tabla['tipo'].unique()))
        with columna_filtro_riesgo:
            filtro_riesgo = st.selectbox("Filtrar por Nivel de Riesgo", ["Todos", "MEDIO", "ALTO", "CRÍTICO", "BAJO"])
            
        tabla_filtrada = tabla.copy()
        
        
        def obtener_recomendacion(fila):
            return fila['objeto_real'].recomendaciones()
            
        tabla_filtrada['recomendaciones'] = tabla_filtrada.apply(obtener_recomendacion, axis=1)
        
        if filtro_tipo != 'Todos':
            tabla_filtrada = tabla_filtrada[tabla_filtrada['tipo'] == filtro_tipo]
        if filtro_riesgo != 'Todos':
            tabla_filtrada = tabla_filtrada[tabla_filtrada['riesgo'] == filtro_riesgo]

        st.metric('Total', len(tabla_filtrada))
        st.metric('Riesgos altos o críticos', int((tabla_filtrada['riesgo'].astype(str).str.upper().isin(['ALTO', 'CRÍTICO'])).sum()))

        for _, fila in tabla_filtrada.iterrows():
            with st.expander(f"{fila['titulo']} — {fila['tipo']} ({fila['riesgo']})"):
                st.write(f"**ID:** {fila.get('id', '')}")
                st.write(f"**Fecha:** {fila.get('fecha', '')}")
                st.write(f"**Descripción:** {fila.get('descripcion', '')}")
                
                
                inc_obj = fila['objeto_real']
                if hasattr(inc_obj, 'url_sospechosa'): st.write(f"**URL:** `{inc_obj.url_sospechosa}`")
                elif hasattr(inc_obj, 'tipo_malware'): st.write(f"**Malware:** `{inc_obj.tipo_malware}`")
                elif hasattr(inc_obj, 'num_intentos'): st.write(f"**Intentos:** `{inc_obj.num_intentos}`")
                elif hasattr(inc_obj, 'tipo_dato'): st.write(f"**Datos Expuestos:** `{inc_obj.tipo_dato}`")
                elif hasattr(inc_obj, 'metodo_acceso'): st.write(f"**Método Acceso:** `{inc_obj.metodo_acceso}`")
                
                if fila.get('recomendaciones'):
                    st.info(f"💡 **Recomendación:** {fila['recomendaciones']}")

        st.subheader('Estadísticas')
        columna_estadistica_tipo, columna_estadistica_riesgo = st.columns(2)
        with columna_estadistica_tipo:
            st.write('Por tipo:')
            st.bar_chart(tabla['tipo'].value_counts())
        with columna_estadistica_riesgo:
            st.write('Por riesgo:')
            st.bar_chart(tabla['riesgo'].value_counts())