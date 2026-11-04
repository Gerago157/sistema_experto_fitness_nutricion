# Asistente Experto en Entrenamiento y Nutrición

**Materia:** Análisis de Datos II

## Descripción del Sistema
Este proyecto es un sistema experto basado en reglas lógicas diseñado para la prescripción personalizada de rutinas de entrenamiento y pautas nutricionales. El motor de inferencia está desarrollado en Python utilizando la librería `experta` (basada en encadenamiento hacia adelante), y la interfaz gráfica está construida con `streamlit`.

El sistema evalúa el perfil biométrico, nivel de experiencia, disponibilidad horaria y restricciones de salud o alimentarias del usuario para:
1. Calcular el gasto metabólico y requerimientos de macronutrientes.
2. Determinar la capacidad de recuperación física.
3. Asignar esquemas de entrenamiento biomecánicamente seguros (adaptando ejercicios si existen lesiones).
4. Proveer justificaciones explicables para cada decisión tomada por el motor (Traza de inferencia).

## Grilla de Reglas del Motor de Inferencia

| ID Regla | Categoría | Condición (Antecedente) | Acción / Conclusión (Consecuente) |
| :--- | :--- | :--- | :--- |
| **R01** | Seguridad | Objetivo fuerza + Lesión lumbar grave + Edad > 60 | Bloqueo preventivo de seguridad. |
| **R02** | Seguridad | Principiante + Lesión lumbar grave | Bloqueo preventivo y derivación médica. |
| **R03** | Diagnóstico | Edad < 40 + Actividad moderada/fuerte | Capacidad de recuperación: Alta. |
| **R04** | Diagnóstico | Edad >= 40 o Actividad sedentaria | Capacidad de recuperación: Baja. |
| **R05** | Biomecánica | Dolor lumbar o Lesión lumbar grave | Restricción axial activada. |
| **R06** | Biomecánica | Molestia en hombro | Restricción overhead (empujes verticales) activada. |
| **R07** | Esquema | Principiante + Recuperación baja | Esquema Base: Fullbody Adaptativo (volumen bajo). |
| **R08** | Esquema | Principiante + Recuperación alta | Esquema Base: Fullbody Estándar (volumen moderado). |
| **R09** | Esquema | Intermedio | Esquema Base: Torso/Pierna (volumen moderado). |
| **R10** | Esquema | Avanzado + Días disponibles >= 4 | Esquema Base: Push/Pull/Legs (volumen alto). |
| **R10b** | Esquema | Avanzado + Días disponibles < 4 | Esquema Base: Torso/Pierna (volumen alto). |
| **R11** | Estrategia Nut. | Objetivo: Pérdida de grasa | Enfoque: Déficit hipocalórico. |
| **R12** | Estrategia Nut. | Objetivo: Hipertrofia | Enfoque: Superávit hipercalórico. |
| **R12b** | Estrategia Nut. | Objetivo: Fuerza o Mantenimiento | Enfoque: Mantenimiento (normocalórico). |
| **R13** | Prescripción | Esquema Fullbody Adaptativo | 2 series, 12-15 reps, descanso 90-120s. |
| **R14** | Prescripción | Esquema Fullbody Estándar | 3 series, 10-12 reps, descanso 90s. |
| **R15** | Prescripción | Esquema Torso/Pierna | 3-4 series, 8-12 reps, descanso 90-120s. |
| **R16** | Prescripción | Esquema Push/Pull/Legs | 4-5 series, 6-10 reps, descanso 120s. |
| **R17** | Adaptación | Restricción axial | Excluye Sentadilla/Peso Muerto -> Reemplaza por Prensa/Hip Thrust. |
| **R18** | Adaptación | Restricción overhead | Excluye Press Militar/Jalón -> Reemplaza por Press Neutro/Elevaciones. |
| **R19** | Pauta Nutricional | Déficit + Vegetarianismo | Pauta hiperproteica vegetal baja en grasas. |
| **R20** | Pauta Nutricional | Superávit + Celiaquía | Pauta sin TACC rica en carbohidratos densos (arroz, batata). |
| **R21** | Pauta Nutricional | Déficit + Sin restricciones | Pauta estándar para saciedad y retención de masa magra. |
| **R22** | Pauta Nutricional | Superávit + Sin restricciones | Pauta estándar para maximizar rendimiento y síntesis muscular. |
| **R23** | Pauta Nutricional | Mantenimiento | Pauta normocalórica para sostener rendimiento y masa actual. |

## Instalación y Ejecución
1. Instalar dependencias: `pip install -r requirements.txt`
2. Ejecutar la aplicación: `streamlit run app.py`