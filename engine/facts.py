# ==============================================================================
# MÓDULO: engine/facts.py
# Propósito: Definición del modelo de datos de la memoria de trabajo (Facts)
# ==============================================================================

import collections
import collections.abc

# ------------------------------------------------------------------------------
# PARCHE DE COMPATIBILIDAD
# Experta utiliza clases de 'collections' que fueron movidas a 'collections.abc'
# en versiones de Python 3.10 o superiores. Este bloque garantiza que el código
# funcione en entornos modernos sin lanzar un AttributeError.
# ------------------------------------------------------------------------------
for nombre in ["Mapping", "MutableMapping", "Iterable", "Sequence"]:
    if not hasattr(collections, nombre):
        setattr(collections, nombre, getattr(collections.abc, nombre))

from experta import Fact

# ------------------------------------------------------------------------------
# CLASES DE HECHOS (FACTS)
# Cada clase hereda de 'Fact' y representa un tipo específico de conocimiento.
# ------------------------------------------------------------------------------

class Usuario(Fact):
    """
    Representa los datos demográficos, antropométricos y de disponibilidad.
    Atributos esperados:
        - edad (int), peso (float), altura (int), sexo (str)
        - experiencia (str): 'principiante' | 'intermedio' | 'avanzado'
        - objetivo (str): 'hipertrofia' | 'perdidagrasa' | 'fuerza' | 'mantenimiento'
        - dias_disponibles (int): 2 a 6
    """
    pass


class RestriccionSalud(Fact):
    """
    Representa patologías, lesiones o contraindicaciones declaradas por el usuario.
    Permite activar las reglas de exclusión estricta y seguridad biomecánica.
    Atributo esperado:
        - tipo (str): ej. 'dolor_lumbar', 'lesion_lumbar_grave', 'molestia_hombro'
    """
    pass


class RestriccionNutricional(Fact):
    """
    Representa alergias, intolerancias o filosofías alimentarias.
    Atributo esperado:
        - tipo (str): ej. 'celiaquia', 'vegetarianismo', 'intolerancia_lactosa'
    """
    pass


class PrescripcionEntrenamiento(Fact):
    """
    Conclusión intermedia o final generada por el motor respecto a la rutina.
    Atributos posibles:
        - esquema (str): ej. 'Fullbody', 'Push/Pull/Legs'
        - series_por_grupo (str), repeticiones (str), descanso (str)
        - ejercicio_excluido (str), ejercicio_reemplazo (str)
    """
    pass


class PrescripcionNutricional(Fact):
    """
    Pautas y recomendaciones cualitativas o distributivas sobre la nutrición.
    Atributos posibles:
        - pauta (str): Indicación específica (ej. excluir gluten, combinar legumbres)
    """
    pass


class AlertaSeguridad(Fact):
    """
    Hecho prioritario que representa una incompatibilidad crítica de salud.
    Si se declara este hecho, se activa un bloqueo preventivo que impide
    emitir una rutina automatizada sin antes derivar a un profesional.
    Atributos:
        - tipo (str): ej. 'bloqueo_preventivo'
        - mensaje (str): Explicación del riesgo clínico detectado
    """
    pass


class Justificacion(Fact):
    """
    Representa el registro de la traza de inferencia (Explicabilidad).
    Cada vez que una regla se dispara, genera una 'Justificacion' para que el
    usuario pueda auditar POR QUÉ el sistema llegó a esa conclusión.
    Atributos:
        - regla (str): Código o nombre identificador de la regla
        - motivo (str): Explicación amigable del razonamiento aplicado
    """
    pass

class MetaMetabolica(Fact):
    """
    Representa las metas metabólicas calculadas (TMB, TDEE, objetivo calórico).
    """
    pass