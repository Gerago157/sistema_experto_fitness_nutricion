#Interfaz, La aplicación web toma las entradas, evalúa el motor de inferencia y despliega las conclusiones junto con la traza de inferencia explicativa

# app.py
import streamlit as st
import pandas as pd
from engine.facts import Usuario, RestriccionSalud, RestriccionNutricional
from engine.rules import MotorFitnessNutricion
from engine.calculations import calcular_metabolismo

st.set_page_config(page_title="Sistema Experto - Entrenamiento & Nutrición", layout="wide")

st.title("🏋️‍♂️ Asistente Experto en Entrenamiento y Nutrición")
st.markdown("Sistema basado en reglas explicables para la prescripción biomecánica y nutricional personalizada.")

# Sidebar - Carga de Datos (RF-01, RF-02, RF-03, RF-04)
with st.sidebar:
    st.header("📋 Perfil del Usuario")
    edad = st.number_input("Edad", min_value=18, max_value=80, value=25)
    sexo = st.selectbox("Sexo Biológico", ["Masculino", "Femenino"])
    peso = st.number_input("Peso (kg)", min_value=40.0, max_value=200.0, value=70.0)
    altura = st.number_input("Altura (cm)", min_value=120, max_value=220, value=170)
    
    actividad = st.selectbox(
        "Nivel de Actividad Diaria",
        ["sedentario", "ligero", "moderado", "fuerte"]
    )
    
    experiencia = st.selectbox(
        "Nivel de Experiencia",
        ["principiante", "intermedio", "avanzado"]
    )
    
    objetivo = st.selectbox(
        "Objetivo Principal",
        ["hipertrofia", "perdidagrasa", "fuerza", "mantenimiento"]
    )
    
    dias = st.slider("Días disponibles por semana", 2, 6, 3)
    
    st.subheader("🩺 Restricciones de Salud")
    lesion_lumbar = st.checkbox("Dolor / Lesión Lumbar")
    lesion_lumbar_grave = st.checkbox("Lesión Lumbar Grave (Hernia/Diagnóstico Clínico)")
    molestia_hombro = st.checkbox("Molestia en Hombro")
    
    st.subheader("🥗 Restricciones Alimentarias")
    celiaquia = st.checkbox("Celiaquía (Sin TACC)")
    vegetarianismo = st.checkbox("Vegetarianismo")

if st.button("🚀 Generar Plan Personalizado"):
    # 1. Ejecutar Cálculos Metabólicos Base
    metabolismo = calcular_metabolismo(edad, peso, altura, sexo, actividad, objetivo)
    
    # 2. Inicializar y Ejecutar Motor de Inferencia (Experta)
    engine = MotorFitnessNutricion()
    engine.reset()
    
    # Declarar hechos iniciales
    engine.declare(Usuario(
        edad=edad, peso=peso, altura=altura, sexo=sexo,
        experiencia=experiencia, objetivo=objetivo, dias_disponibles=dias
    ))
    
    if lesion_lumbar_grave:
        engine.declare(RestriccionSalud(tipo='lesion_lumbar_grave'))
    if lesion_lumbar:
        engine.declare(RestriccionSalud(tipo='dolor_lumbar'))
    if molestia_hombro:
        engine.declare(RestriccionSalud(tipo='molestia_hombro'))
        
    if celiaquia:
        engine.declare(RestriccionNutricional(tipo='celiaquia'))
    if vegetarianismo:
        engine.declare(RestriccionNutricional(tipo='vegetarianismo'))
        
    engine.run()
    
    # 3. Procesar Resultados de la Memoria de Trabajo
    hechos = list(engine.facts.values())
    
    # Verificar si hubo un Bloqueo Preventivo de Seguridad (RF-06 / Criterio 5)
    alertas = [h for h in hechos if h.get('tipo') == 'bloqueo_preventivo']
    
    if alertas:
        st.error(f"⛔ **BLOQUEO PREVENTIVO DE SEGURIDAD**")
        st.warning(alertas[0]['mensaje'])
        st.info("Por favor, consulte con un profesional médico o kinesiólogo antes de iniciar una rutina.")
    else:
        st.success("✅ Plan Generado con Éxito")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Pauta Nutricional & Metabólica")
            st.metric("Calorías Objetivo", f"{metabolismo['calorias_target']} kcal")
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Proteínas", f"{metabolismo['proteinas_g']} g")
            c2.metric("Carbohidratos", f"{metabolismo['carbos_g']} g")
            c3.metric("Grasas", f"{metabolismo['grasas_g']} g")
            
            pautas_nut = [h['pauta'] for h in hechos if 'pauta' in h]
            if pautas_nut:
                st.markdown("**Indicaciones Nutricionales Especiales:**")
                for p in pautas_nut:
                    st.write(f"- {p}")

        with col2:
            st.subheader("🏋️‍♂️ Plan de Entrenamiento")
            esquemas = [h for h in hechos if 'esquema' in h]
            if esquemas:
                e = esquemas[0]
                st.write(f"**Esquema:** {e['esquema']}")
                st.write(f"**Volumen:** {e['series_por_grupo']} | {e['repeticiones']}")
                st.write(f"**Descanso:** {e['descanso']}")
            
            reemplazos = [h for h in hechos if 'ejercicio_excluido' in h]
            if reemplazos:
                st.markdown("**🚫 Adaptaciones Biomecánicas (Exclusiones):**")
                for r in reemplazos:
                    st.write(f"- ~~{r['ejercicio_excluido']}~~ ➡️ **Reemplazo:** {r['ejercicio_reemplazo']}")

        # 4. Mostrar Traza de Inferencia Explicativa (RF-05 / Criterio 3)
        st.markdown("---")
        st.subheader("🔍 Traza de Inferencia (Explicabilidad del Motor Expert)")
        st.caption("A continuación se detallan las reglas lógicas disparadas que justifican la recomendación emitida:")
        
        justificaciones = [h for h in hechos if 'regla' in h and 'motivo' in h]
        df_traza = pd.DataFrame(justificaciones)[['regla', 'motivo']]
        st.table(df_traza)