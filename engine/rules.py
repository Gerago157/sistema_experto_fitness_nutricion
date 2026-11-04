# engine/rules.py El motor implementa las +20 reglas lógicas requeridas, usando encadenamiento hacia adelante, saliencia, exlusión de ejercicios y bloqueo preventivo de seguridad


from experta import KnowledgeEngine, Rule, MATCH, NOT, AS, TEST, P
from .facts import (
    Usuario, RestriccionSalud, RestriccionNutricional, EvaluacionFisica,
    PerfilBiomecanico, EsquemaBase, EstrategiaNutricional,
    PrescripcionEntrenamiento, PrescripcionNutricional, AlertaSeguridad, Justificacion
)

class MotorFitnessNutricion(KnowledgeEngine):

    # =========================================================================
    # REGLAS DE SEGURIDAD (Saliencia 100)
    # =========================================================================
    @Rule(
        Usuario(objetivo='fuerza', edad=MATCH.e),
        RestriccionSalud(tipo='lesion_lumbar_grave'),
        TEST(lambda e: e > 60),
        salience=100
    )
    def r01_bloqueo_fuerza_lumbar(self):
        self.declare(AlertaSeguridad(
            tipo='bloqueo_preventivo',
            mensaje="Riesgo clínico: Lesión lumbar grave y objetivo de fuerza máxima en edad avanzada."
        ))
        self.declare(Justificacion(regla="R01", motivo="Bloqueo preventivo por riesgo biomecánico extremo."))

    @Rule(
        Usuario(experiencia='principiante'),
        RestriccionSalud(tipo='lesion_lumbar_grave'),
        salience=100
    )
    def r02_bloqueo_principiante_lesionado(self):
        self.declare(AlertaSeguridad(
            tipo='bloqueo_preventivo',
            mensaje="Derivación médica obligatoria: Principiante con diagnóstico lumbar grave requiere kinesiólogo."
        ))
        self.declare(Justificacion(regla="R02", motivo="Protección al usuario sin experiencia motriz con lesiones graves."))

    # =========================================================================
    # NIVEL 1: DIAGNÓSTICO FÍSICO Y BIOMECÁNICO (Saliencia 90)
    # =========================================================================
    @Rule(Usuario(edad=MATCH.e, actividad=MATCH.act), TEST(lambda e, act: e < 40 and act in ['moderado', 'fuerte']), salience=90)
    def r03_diag_recuperacion_alta(self, e, act):
        self.declare(EvaluacionFisica(capacidad_recuperacion='alta'))
        self.declare(Justificacion(regla="R03", motivo="Capacidad de recuperación alta inferida por edad menor a 40 y vida activa."))

    @Rule(Usuario(edad=MATCH.e, actividad=MATCH.act), TEST(lambda e, act: e >= 40 or act == 'sedentario'), salience=90)
    def r04_diag_recuperacion_baja(self, e, act):
        self.declare(EvaluacionFisica(capacidad_recuperacion='baja'))
        self.declare(Justificacion(regla="R04", motivo="Capacidad de recuperación adaptada (baja/moderada) inferida por edad o sedentarismo."))

    @Rule(RestriccionSalud(tipo='dolor_lumbar') | RestriccionSalud(tipo='lesion_lumbar_grave'), salience=90)
    def r05_diag_biomec_axial(self):
        self.declare(PerfilBiomecanico(restriccion_axial=True))
        self.declare(Justificacion(regla="R05", motivo="Se establece perfil de restricción axial por antecedentes lumbares."))

    @Rule(RestriccionSalud(tipo='molestia_hombro'), salience=90)
    def r06_diag_biomec_overhead(self):
        self.declare(PerfilBiomecanico(restriccion_overhead=True))
        self.declare(Justificacion(regla="R06", motivo="Se establece perfil de restricción de empujes verticales (overhead)."))

    # =========================================================================
    # NIVEL 2: DEFINICIÓN DE ESTRATEGIA (Saliencia 70)
    # =========================================================================
    @Rule(Usuario(experiencia='principiante'), EvaluacionFisica(capacidad_recuperacion='baja'), NOT(AlertaSeguridad()), salience=70)
    def r07_estr_principiante_baja(self):
        self.declare(EsquemaBase(tipo='Fullbody', volumen='bajo_adaptativo'))
        self.declare(Justificacion(regla="R07", motivo="Esquema base Fullbody de bajo volumen para principiantes con menor recuperación."))

    @Rule(Usuario(experiencia='principiante'), EvaluacionFisica(capacidad_recuperacion='alta'), NOT(AlertaSeguridad()), salience=70)
    def r08_estr_principiante_alta(self):
        self.declare(EsquemaBase(tipo='Fullbody', volumen='moderado'))
        self.declare(Justificacion(regla="R08", motivo="Esquema base Fullbody estándar para adaptación neuromuscular."))

    @Rule(Usuario(experiencia='intermedio'), NOT(AlertaSeguridad()), salience=70)
    def r09_estr_intermedio(self):
        self.declare(EsquemaBase(tipo='Torso/Pierna', volumen='moderado'))
        self.declare(Justificacion(regla="R09", motivo="Esquema Torso/Pierna asignado por experiencia intermedia."))

    @Rule(Usuario(experiencia='avanzado', dias_disponibles=MATCH.d), TEST(lambda d: d >= 4), NOT(AlertaSeguridad()), salience=70)
    def r10_estr_avanzado_alta_frecuencia(self, d):
        self.declare(EsquemaBase(tipo='Push/Pull/Legs', volumen='alto'))
        self.declare(Justificacion(regla="R10", motivo="Esquema avanzado dividido (Push/Pull/Legs) para maximizar volumen tolerado con 4+ días."))

    @Rule(Usuario(experiencia='avanzado', dias_disponibles=MATCH.d), TEST(lambda d: d < 4), NOT(AlertaSeguridad()), salience=70)
    def r10b_estr_avanzado_baja_frecuencia(self, d):
        self.declare(EsquemaBase(tipo='Torso/Pierna', volumen='alto'))
        self.declare(Justificacion(regla="R10b", motivo="Esquema avanzado compactado (Torso/Pierna) adaptado a menos de 4 días disponibles."))

    @Rule(Usuario(objetivo='perdidagrasa'), NOT(AlertaSeguridad()), salience=70)
    def r11_estr_nut_deficit(self):
        self.declare(EstrategiaNutricional(enfoque='deficit_hipocalorico'))
        self.declare(Justificacion(regla="R11", motivo="Estrategia nutricional seteada en déficit calórico para pérdida de grasa."))

    @Rule(Usuario(objetivo='hipertrofia'), NOT(AlertaSeguridad()), salience=70)
    def r12_estr_nut_superavit(self):
        self.declare(EstrategiaNutricional(enfoque='superavit_hipercalorico'))
        self.declare(Justificacion(regla="R12", motivo="Estrategia nutricional seteada en superávit para síntesis muscular."))

    @Rule(Usuario(objetivo=MATCH.obj), TEST(lambda obj: obj in ['fuerza', 'mantenimiento']), NOT(AlertaSeguridad()), salience=70)
    def r12b_estr_nut_mantenimiento(self, obj):
        self.declare(EstrategiaNutricional(enfoque='mantenimiento_calorico'))
        self.declare(Justificacion(regla="R12b", motivo="Estrategia nutricional seteada en normocalórica para fuerza o mantenimiento."))

    # =========================================================================
    # NIVEL 3: PRESCRIPCIÓN FINAL ENTRENAMIENTO Y EXCLUSIONES (Saliencia 50)
    # =========================================================================
    @Rule(EsquemaBase(tipo='Fullbody', volumen='bajo_adaptativo'), NOT(AlertaSeguridad()), salience=50)
    def r13_pres_fb_bajo(self):
        self.declare(PrescripcionEntrenamiento(esquema="Fullbody Adaptativo", series_por_grupo="2 series", repeticiones="12 a 15 reps", descanso="90 a 120 seg"))

    @Rule(EsquemaBase(tipo='Fullbody', volumen='moderado'), NOT(AlertaSeguridad()), salience=50)
    def r14_pres_fb_mod(self):
        self.declare(PrescripcionEntrenamiento(esquema="Fullbody Estándar", series_por_grupo="3 series", repeticiones="10 a 12 reps", descanso="90 seg"))

    @Rule(EsquemaBase(tipo='Torso/Pierna', volumen='moderado'), NOT(AlertaSeguridad()), salience=50)
    def r15_pres_tp_mod(self):
        self.declare(PrescripcionEntrenamiento(esquema="División Torso / Pierna", series_por_grupo="3 a 4 series", repeticiones="8 a 12 reps", descanso="90 a 120 seg"))

    @Rule(EsquemaBase(tipo='Push/Pull/Legs', volumen='alto'), NOT(AlertaSeguridad()), salience=50)
    def r16_pres_ppl_alto(self):
        self.declare(PrescripcionEntrenamiento(esquema="Push / Pull / Legs", series_por_grupo="4 a 5 series", repeticiones="6 a 10 reps", descanso="120 seg"))

    @Rule(PerfilBiomecanico(restriccion_axial=True), NOT(AlertaSeguridad()), salience=50)
    def r17_pres_excl_axial(self):
        self.declare(PrescripcionEntrenamiento(ejercicio_excluido="Sentadilla Libre con Barra / Peso Muerto Convencional", ejercicio_reemplazo="Prensa 45° / Sentadilla Búlgara / Hip Thrust"))
        self.declare(Justificacion(regla="R17", motivo="Sustitución de cargas axiales compresivas debido a restricción biomecánica lumbar."))

    @Rule(PerfilBiomecanico(restriccion_overhead=True), NOT(AlertaSeguridad()), salience=50)
    def r18_pres_excl_overhead(self):
        self.declare(PrescripcionEntrenamiento(ejercicio_excluido="Press Militar con Barra / Jalón Trasnuca", ejercicio_reemplazo="Press de Hombro Neutro con Mancuernas / Elevaciones Laterales"))
        self.declare(Justificacion(regla="R18", motivo="Eliminación de empujes sobre la cabeza por restricción biomecánica de hombro."))

    # =========================================================================
    # NIVEL 3: PRESCRIPCIÓN FINAL NUTRICIONAL (Saliencia 50)
    # =========================================================================
    @Rule(EstrategiaNutricional(enfoque='deficit_hipocalorico'), RestriccionNutricional(tipo='vegetarianismo'), NOT(AlertaSeguridad()), salience=50)
    def r19_pres_nut_deficit_veg(self):
        self.declare(PrescripcionNutricional(pauta="Déficit calórico vegetariano: Priorizar tofu, seitan, proteína aislada y fibras para saciedad con bajo aporte graso."))
        self.declare(Justificacion(regla="R19", motivo="Ajuste de fuentes proteicas vegetales concentradas para lograr déficit sin perder masa magra."))

    @Rule(EstrategiaNutricional(enfoque='superavit_hipercalorico'), RestriccionNutricional(tipo='celiaquia'), NOT(AlertaSeguridad()), salience=50)
    def r20_pres_nut_sup_cel(self):
        self.declare(PrescripcionNutricional(pauta="Superávit sin TACC: Aumentar carbohidratos mediante arroz, quinoa, batata y harina de maíz; evitar avena no certificada."))
        self.declare(Justificacion(regla="R20", motivo="Selección de carbohidratos calóricamente densos libres de gluten para superávit."))

    @Rule(EstrategiaNutricional(enfoque='deficit_hipocalorico'), NOT(RestriccionNutricional()), NOT(AlertaSeguridad()), salience=50)
    def r21_pres_nut_deficit_std(self):
        self.declare(PrescripcionNutricional(pauta="Priorizar proteína magra (pollo, huevos, pescados) y vegetales fibrosos. Reducir carbohidratos en comidas alejadas del entrenamiento."))
        self.declare(Justificacion(regla="R21", motivo="Recomendación estándar de déficit para optimizar saciedad y rendimiento."))

    @Rule(EstrategiaNutricional(enfoque='superavit_hipercalorico'), NOT(RestriccionNutricional()), NOT(AlertaSeguridad()), salience=50)
    def r22_pres_nut_sup_std(self):
        self.declare(PrescripcionNutricional(pauta="Superávit estándar: Aumentar la ingesta de carbohidratos complejos (avena, arroz, pasta) alrededor del entrenamiento para maximizar el rendimiento y la recuperación."))
        self.declare(Justificacion(regla="R22", motivo="Recomendación estándar de superávit para apoyar el crecimiento muscular."))

    @Rule(EstrategiaNutricional(enfoque='mantenimiento_calorico'), NOT(AlertaSeguridad()), salience=50)
    def r23_pres_nut_mant_std(self):
        self.declare(PrescripcionNutricional(pauta="Mantenimiento calórico: Balancear macronutrientes asegurando un aporte proteico adecuado para sostener la masa muscular y el nivel de fuerza."))
        self.declare(Justificacion(regla="R23", motivo="Recomendación de mantenimiento enfocada en sostener el rendimiento y la composición corporal actual."))