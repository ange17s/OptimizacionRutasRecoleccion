import math
from alertas import obtenerAlertas

def calcular_distancia(coord1, coord2):
    """
    Calcula la distancia entre dos puntos utilizando la fórmula de la distancia euclidiana.
    """
    x1, y1 = coord1
    x2, y2 = coord2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def encontrar_ruta_optima(alertas):
    """
    Encuentra la ruta óptima para visitar todas las alertas sin repetir puntos.
    """
    alertas_visitadas = set()  # Conjunto para mantener las alertas visitadas
    ruta_optima = []  # Lista para almacenar la ruta óptima

    # Comenzar desde la primera alerta
    alerta_actual = alertas[0]
    alertas_visitadas.add(tuple(alerta_actual['coordinates']))  # Convertir a tupla
    ruta_optima.append(alerta_actual)

    while len(ruta_optima) < len(alertas):
        distancia_minima = float('inf')
        siguiente_alerta = None

        # Buscar la alerta más cercana que no haya sido visitada
        for alerta in alertas:
            if tuple(alerta['coordinates']) not in alertas_visitadas:  # Convertir a tupla
                distancia = calcular_distancia(alerta_actual['coordinates'], alerta['coordinates'])
                if distancia < distancia_minima:
                    distancia_minima = distancia
                    siguiente_alerta = alerta

        # Verificar si se encontró una alerta disponible para visitar
        if siguiente_alerta is not None:
            # Marcar la alerta como visitada y actualizar la alerta actual
            alertas_visitadas.add(tuple(siguiente_alerta['coordinates']))  # Convertir a tupla
            alerta_actual = siguiente_alerta
            ruta_optima.append(siguiente_alerta)
        else:
            break  # Si no se encontró una alerta disponible, salir del bucle

    return ruta_optima


# Uso del algoritmo para obtener la ruta óptima
alertas = obtenerAlertas()
ruta_optima = encontrar_ruta_optima(alertas)

# Imprimir la ruta óptima
for alerta in ruta_optima:
    print(alerta)
