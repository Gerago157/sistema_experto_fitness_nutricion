# engine/calculations.py
#Calculos metabólicos base: Implementación de las ecuaciones recomendadas por la bibliografía (Mifflin-St Jeor / Harris-Benedict) e ISS

# engine/calculations.py
def calcular_metabolismo(edad, peso_kg, altura_cm, sexo, nivel_actividad, objetivo):
    if sexo.lower() == 'masculino':
        tmb = (10 * peso_kg) + (6.25 * altura_cm) - (5 * edad) + 5
    else:
        tmb = (10 * peso_kg) + (6.25 * altura_cm) - (5 * edad) - 161

    factores = {
        'sedentario': 1.2,
        'ligero': 1.375,
        'moderado': 1.55,
        'fuerte': 1.725
    }
    tdee = tmb * factores.get(nivel_actividad, 1.2)

    if objetivo == 'hipertrofia':
        calorias_target = tdee + 300 
        proteina_g_kg = 2.0
    elif objetivo == 'perdidagrasa':
        calorias_target = tdee - 400 
        proteina_g_kg = 2.2 
    elif objetivo == 'fuerza':
        calorias_target = tdee + 150
        proteina_g_kg = 1.8
    else: 
        calorias_target = tdee
        proteina_g_kg = 1.6

    proteinas_g = peso_kg * proteina_g_kg
    grasas_g = (calorias_target * 0.25) / 9 
    carbos_g = (calorias_target - (proteinas_g * 4) - (grasas_g * 9)) / 4

    return {
        'tmb': round(tmb),
        'tdee': round(tdee),
        'calorias_target': round(calorias_target),
        'proteinas_g': round(proteinas_g),
        'grasas_g': round(grasas_g),
        'carbos_g': round(carbos_g)
    }