# ==============================================================================
# MÓDULO: engine/facts.py
# Propósito: Definición del modelo de datos de la memoria de trabajo (Facts)
# ==============================================================================

import collections
import collections.abc

for nombre in ["Mapping", "MutableMapping", "Iterable", "Sequence"]:
    if not hasattr(collections, nombre):
        setattr(collections, nombre, getattr(collections.abc, nombre))

from experta import Fact

# --- HECHOS BASE (Nivel 0) ---
class Usuario(Fact): pass
class RestriccionSalud(Fact): pass
class RestriccionNutricional(Fact): pass
class MetaMetabolica(Fact): pass

# --- HECHOS DERIVADOS INTERMEDIOS (Niveles 1 y 2) ---
class EvaluacionFisica(Fact):
    """Representa la capacidad de recuperación inferida (Nivel 1)"""
    pass

class PerfilBiomecanico(Fact):
    """Agrupa las limitaciones estructurales inferidas de las restricciones de salud (Nivel 1)"""
    pass

class EsquemaBase(Fact):
    """Define la estructura teórica de entrenamiento antes de los ajustes finos (Nivel 2)"""
    pass

class EstrategiaNutricional(Fact):
    """Define el enfoque de macronutrientes según objetivo (Nivel 2)"""
    pass

# --- HECHOS CONCLUSIVOS (Nivel 3) ---
class PrescripcionEntrenamiento(Fact): pass
class PrescripcionNutricional(Fact): pass
class AlertaSeguridad(Fact): pass
class Justificacion(Fact): pass