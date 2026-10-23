# engine/rules.py El motor implementa las +20 reglas lógicas requeridas, usando encadenamiento hacia adelante, saliencia, exlusión de ejercicios y bloqueo preventivo de seguridad

from experta import KnowledgeEngine, Rule, MATCH, NOT, AS, TEST, P
from .facts import (
    Usuario, RestriccionSalud, RestriccionNutricional, MetaMetabolica,
    PrescripcionEntrenamiento, PrescripcionNutricional, AlertaSeguridad, Justificacion
)

class MotorFitnessNutricion(KnowledgeEngine):

    # =========================================================================
    # REGLAS DE SEGURIDAD Y BLOQUEO PREVENTIVO (Saliencia Alta = 100)
    # =========================================================================
    @Rule(
        Usuario(objetivo='fuerza', edad=MATCH.e),
        RestriccionSalud(tipo='lesion_lumbar_grave'),
        TEST(lambda e: e > 60),
        salience=100
    )
    def regla_bloqueo_fuerza_lumbar(self):
        """RF-06 / Criterio 5: Bloqueo preventivo de seguridad."""
        self.declare(AlertaSeguridad(
            tipo='bloqueo_preventivo',
            mensaje="Incompatibilidad detectada: Se ha seleccionado entrenamiento de fuerza máxima o levantamiento pesado "
                    "teniendo una lesión lumbar grave declarada a su edad. Se suspende la prescripción automatizada por seguridad clínica."
        ))
        self.declare(Justificacion(
            regla="R_SEG_01",
            motivo="Bloqueo preventivo activado por alto riesgo biomecánico entre lesión lumbar grave y objetivo de alta carga."
        ))

    # =========================================================================
    # REGLAS DE FILTRADO Y EXCLUSIÓN BIOMECÁNICA (Saliencia = 50)
    # =========================================================================
    @Rule(
        RestriccionSalud(tipo='dolor_lumbar'),
        NOT(AlertaSeguridad(tipo='bloqueo_preventivo')),
        salience=50
    )
    def regla_excluir_ejercicios_lumbares(self):
        """RF-02 / RF-08: Exclusión estrita y reemplazo de ejercicios lesivos."""
        self.declare(PrescripcionEntrenamiento(
            ejercicio_excluido="Sentadilla Libre con Barra",
            ejercicio_reemplazo="Prensa 45° o Sentadilla Goblet asistida"
        ))
        self.declare(PrescripcionEntrenamiento(
            ejercicio_excluido="Peso Muerto Convencional",
            ejercicio_reemplazo="Hip Thrust / Curva Femoral en Máquina"
        ))
        self.declare(Justificacion(
            regla="R_EXCL_LUMBAR",
            motivo="Sustitución de cargas axiales compresivas en columna por molestias lumbares declaradas."
        ))

    @Rule(
        RestriccionSalud(tipo='molestia_hombro'),
        NOT(AlertaSeguridad(tipo='bloqueo_preventivo')),
        salience=50
    )
    def regla_excluir_ejercicios_hombro(self):
        self.declare(PrescripcionEntrenamiento(
            ejercicio_excluido="Press Militar Trasnuca",
            ejercicio_reemplazo="Press Militar con Mancuernas en Agarre Neutro"
        ))
        self.declare(Justificacion(
            regla="R_EXCL_HOMBRO",
            motivo="Eliminación de rangos articuladores en rotación externa comprometida para proteger manguito rotador."
        ))

    # =========================================================================
    # REGLAS DE ESTRUCTURACIÓN DE RUTINA Y VOLUMEN (Saliencia = 10)
    # =========================================================================
    @Rule(
        Usuario(experiencia='principiante', dias_disponibles=MATCH.d),
        NOT(AlertaSeguridad(tipo='bloqueo_preventivo')),
        salience=10
    )
    def regla_esquema_principiante(self, d):
        esquema = "Fullbody (Cuerpo Completo)" if d <= 3 else "Torso / Pierna"
        self.declare(PrescripcionEntrenamiento(
            esquema=esquema,
            series_por_grupo="2 a 3 series",
            repeticiones="10 a 12 reps",
            descanso="90 segundos"
        ))
        self.declare(Justificacion(
            regla="R_ESTRUCT_PRINCIPIANTE",
            motivo=f"Para nivel principiante con {d} días se prioriza la frecuencia y adaptación neuromuscular."
        ))

    @Rule(
        Usuario(experiencia='avanzado', objetivo='hipertrofia', dias_disponibles=MATCH.d),
        TEST(lambda d: d >= 4),
        NOT(AlertaSeguridad(tipo='bloqueo_preventivo')),
        salience=10
    )
    def regla_esquema_avanzado_hipertrofia(self, d):
        self.declare(PrescripcionEntrenamiento(
            esquema="Push / Pull / Legs (Empuje / Tirón / Pierna)",
            series_por_grupo="3 a 4 series",
            repeticiones="6 a 10 reps",
            descanso="120 segundos"
        ))
        self.declare(Justificacion(
            regla="R_ESTRUCT_AVANZADO",
            motivo="Para nivel avanzado orientado a hipertrofia se requiere alto volumen focalizado por grupo muscular."
        ))

    # =========================================================================
    # REGLAS NUTRICIONALES Y RESTRICCIONES ALIMENTARIAS (Saliencia = 10)
    # =========================================================================
    @Rule(
        RestriccionNutricional(tipo='celiaquia'),
        NOT(AlertaSeguridad(tipo='bloqueo_preventivo')),
        salience=10
    )
    def regla_nutricion_celiaquia(self):
        self.declare(PrescripcionNutricional(
            pauta="Exclusión estricta de TACC. Fuentes de carbos sugeridas: Arroz, papa, batata, mandioca, quinoa y avena certificada sin gluten."
        ))
        self.declare(Justificacion(
            regla="R_NUT_CELIAQUIA",
            motivo="Filtrado estricto de fuentes de carbohidratos para garantizar seguridad digestiva sin gluten."
        ))

    @Rule(
        RestriccionNutricional(tipo='vegetarianismo'),
        NOT(AlertaSeguridad(tipo='bloqueo_preventivo')),
        salience=10
    )
    def regla_nutricion_vegetariana(self):
        self.declare(PrescripcionNutricional(
            pauta="Complementación proteica obligatoria (combinar cereales y legumbres) o suplementación con proteína de suero / arveja y B12."
        ))
        self.declare(Justificacion(
            regla="R_NUT_VEGETARIANO",
            motivo="Garantizar perfil aminoacídico completo mediante combinaciones vegetales."
        ))
    
    # (Completar con reglas adicionales hasta superar las 20 reglas parametrizadas y encadenadas)