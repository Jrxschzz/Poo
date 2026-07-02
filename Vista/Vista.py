import sys
import os
import streamlit as st
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import date
from Control.Control import gestorIncidencias
from Modelo.IncidenciaMalware import IncidenciaMalware
from Modelo.IncidenciaPhishing import IncidenciaPhishing
from Modelo.IncidenciaFuerzaBruta import IncidenciaFuerzaBruta
from Modelo.IncidenciaAccesoNoAutorizado import IncidenciaAccesoNoAutorizado
from Modelo.IncidenciaFugaDeDatos import IncidenciaFugaDeDatos
from Modelo.Excepciones import ValidacionCargaException

st.set_page_config(page_title='Gestor de Incidencias de Ciberseguridad', layout='wide')
st.subheader("Guarda tus incidencias de forma segura")

ruta_json = os.path.join(os.path.dirname(__file__), '..', 'incidencias.json')

#Tipos de clases que hemos usado
clases_usadas= [
    ('Phishing', IncidenciaPhishing),
    ('Malware', IncidenciaMalware),
    ('Fuerza Bruta', IncidenciaFuerzaBruta),
    ('Fuga de Datos', IncidenciaFugaDeDatos), 
    ('Acceso No Autorizado', IncidenciaAccesoNoAutorizado),
]
#Utilizar diccionarios para obtener clases a partir de su nombre
constructor = {
    'IncidenciaPhishing': IncidenciaPhishing,
    'IncidenciaMalware': IncidenciaMalware,
    'IncidenciaFuerzaBruta': IncidenciaFuerzaBruta,
    'IncidenciaFugaDeDatos': IncidenciaFugaDeDatos,
    'IncidenciaAccesoNoAutorizado': IncidenciaAccesoNoAutorizado
}

if 'gestor' not in st.session_state:
    gestor_inicial = gestorIncidencias()
    gestor_inicial.cargar_json(ruta_json, constructor_map=constructor)
    st.session_state['gestor'] = gestor_inicial
gestor = st.session_state['gestor']

st.title('Centro de Control de Incidencias de Seguridad')

tab_form, tab_historial, tab_graficas = st.tabs(['Registrar alerta', 'Historial', 'Gráficas'])

with tab_form:
    st.header('Registrar alerta')
    #Comparamos el tipo elegido con las clases dispoibles de nuestra lista
    tipo_seleccionado = st.selectbox('Categoría de la amenaza', [t[0] for t in clases_usadas], key='tipo_seleccionado')
    with st.form('formulario_incidencia', clear_on_submit=True):
        id = st.text_input('ID de la incidencia')
        titulo = st.text_input('Título descriptivo')
        descripcion = st.text_area('Descripción detallada del suceso')
        fecha = st.date_input('Fecha de detección', value=date.today())
        
        if tipo_seleccionado == 'Phishing':
            campo_diferente = st.text_input('URL sospechosa o enlace del correo', key='campo_phishing')
        elif tipo_seleccionado == 'Malware':
            campo_diferente = st.text_input('Tipo de malware detectado', key='campo_malware')
        elif tipo_seleccionado == 'Fuerza Bruta':
            campo_diferente = st.number_input('Número de intentos  registrados', min_value=1, step=1, value=1, key='campo_fuerza')
        elif tipo_seleccionado == 'Fuga de Datos':
            campo_diferente = st.text_input('Tipo de información expuesta', key='campo_fuga')
        else:
            campo_diferente = st.text_input('URL de acceso empleado', key='campo_acceso')

        if st.form_submit_button('Dar de alta incidencia'):
            try:
                if not id.strip() or not titulo.strip() or not descripcion.strip():
                    raise ValidacionCargaException('Todos los campos principales son obligatorios.')

                clase_elegida = next(c[1] for c in clases_usadas if c[0] == tipo_seleccionado)
                datos = {
                    "id": id,
                    "titulo": titulo,
                    "descripcion": descripcion,
                    "fecha": fecha
                }
                if tipo_seleccionado == "Phishing":
                    datos["url_sospechosa"] = campo_diferente
                elif tipo_seleccionado == "Malware":
                    datos["tipo_malware"] = campo_diferente
                elif tipo_seleccionado == "Fuerza Bruta":
                    datos["num_intentos"] = campo_diferente
                elif tipo_seleccionado == "Fuga de Datos":
                    datos["tipo_dato"] = campo_diferente
                elif tipo_seleccionado == "Acceso No Autorizado":
                    datos["metodo_acceso"] = campo_diferente


                nueva_incidencia = clase_elegida(**datos)
                nueva_incidencia.limpieza_datos()
                nueva_incidencia.calcular_riesgo()
                gestor.agregar_incidencia(nueva_incidencia)
                gestor.guardar_json(ruta_json)

                st.success('Incidencia registrada.')
                st.rerun()
            except ValidacionCargaException as error:
                st.error(f'Ocurrio un problema para registrar la incidencia, revisar: {error}')

with tab_historial:
    st.header("Historial y Análisis de Riesgo")
    
    incidencias_actuales = gestor.obtener_incidencias()
    
    if not incidencias_actuales:
        st.info("No hay incidencias registradas en el sistema actualmente.")
    else:
        datos_tabla = []
        for inc in incidencias_actuales:
            datos = inc.pasar_diccionario()
            datos['tipo'] = inc.__class__.__name__.replace('Incidencia', '')
            datos['riesgo'] = inc.riesgo
            datos['objeto_real'] = inc
            datos_tabla.append(datos)
            
        tabla = pd.DataFrame(datos_tabla)
        if not tabla.empty:
            tabla['fecha'] = pd.to_datetime(tabla['fecha']).dt.date
        
        filtro_tipo, filtro_riesgo, filtro_fecha = st.columns(3)
        with filtro_tipo:
            tipo_filtro = st.selectbox('Filtrar por categoría', ['Todos'] + sorted(tabla['tipo'].unique()))
        with filtro_riesgo:
            riesgo_filtro = st.selectbox('Filtrar por nivel de riesgo', ['Todos', 'MEDIO', 'ALTO', 'CRÍTICO', 'BAJO'])
        with filtro_fecha:
            fecha_filtro = st.date_input('Filtrar por fecha', value=date.today())

        if tipo_filtro != 'Todos':
            tabla = tabla[tabla['tipo'] == tipo_filtro]
        if riesgo_filtro != 'Todos':
            tabla = tabla[tabla['riesgo'] == riesgo_filtro]
        tabla = tabla[tabla['fecha'] == fecha_filtro]
        
        st.button("Borrar filtros", on_click=lambda: st.session_state.update({'filtro_tipo': 'Todos', 'filtro_riesgo': 'Todos', 'filtro_fecha': date.today()}))
        
        resultado = []
        for inc in tabla['objeto_real']:
            resultado.append(inc.recomendaciones())
        tabla['recomendaciones'] = resultado

        st.metric('Total', len(tabla))
        st.metric('Riesgos altos o críticos', int(tabla['riesgo'].astype(str).str.upper().isin(['ALTO', 'CRÍTICO']).sum()))

        for _, fila in tabla.iterrows(): 
            inc_obj = fila['objeto_real']
            with st.expander(f"{fila['titulo']} — {fila['tipo']} ({fila['riesgo']})"):
                st.write(f"**ID:** {fila['id']}")
                st.write(f"**Fecha:** {fila['fecha']}")
                st.write(f"**Descripción:** {fila['descripcion']}")
                
                #Buscamos en nuestro objeto creado si contiene ciertos atributos
                
                if hasattr(inc_obj, 'url_sospechosa'):
                    st.write(f"**URL:** `{inc_obj.url_sospechosa}`")
                elif hasattr(inc_obj, 'tipo_malware'):
                    st.write(f"**Malware:** `{inc_obj.tipo_malware}`")
                elif hasattr(inc_obj, 'num_intentos'):
                    st.write(f"**Intentos:** `{inc_obj.num_intentos}`")
                elif hasattr(inc_obj, 'tipo_dato'):
                    st.write(f"**Datos expuestos:** `{inc_obj.tipo_dato}`")
                elif hasattr(inc_obj, 'metodo_acceso'):
                    st.write(f"**Método acceso:** `{inc_obj.metodo_acceso}`")
                st.info(f"{fila['recomendaciones']}")


with tab_graficas:
    st.header('Gráficas de riesgo')
    incidencias_actuales = gestor.obtener_incidencias()
    if not incidencias_actuales:
        st.info('No hay incidencias para graficar todavía.')
    else:
        datos_graficas = []
        for inc in incidencias_actuales:
            datos_graficas.append({
                'tipo': inc.__class__.__name__.replace('Incidencia', ''),
                'riesgo': inc.riesgo,
            })
        tabla_graficas = pd.DataFrame(datos_graficas)
        c1, c2 = st.columns(2)
        with c1:
            st.write('Por tipo:')
            st.bar_chart(tabla_graficas['tipo'].value_counts())
        with c2:
            st.write('Por riesgo:')
            st.bar_chart(tabla_graficas['riesgo'].value_counts())