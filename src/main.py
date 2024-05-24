from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
import folium
import numpy as np
from alertas import obtenerAlertas
from ruta import encontrar_ruta_optima  # Importa la función encontrar_ruta_optima

app = FastAPI()

@app.get('/', response_class=HTMLResponse)
def root():
    return FileResponse('index.html')

@app.post('/generarRuta')
def generarRuta():
    alertas = obtenerAlertas()

    # Filtrar y obtener las coordenadas de las alertas
    coordenadas = np.array([
        alerta['coordinates'] for alerta in alertas 
        if 'coordinates' in alerta 
        and isinstance(alerta['coordinates'], list) 
        and len(alerta['coordinates']) == 2
        and all(isinstance(coord, (int, float)) for coord in alerta['coordinates'])
    ])

    # Encontrar la ruta óptima utilizando la función encontrar_ruta_optima
    ruta_optima_alertas = encontrar_ruta_optima(alertas)

    # Convertir la ruta óptima en índices de coordenadas
    mejorRuta = [alertas.index(alerta) for alerta in ruta_optima_alertas]

    # Guardar estados globales para acceder desde el endpoint del mapa
    app.state.mejorRuta = mejorRuta
    app.state.coordenadas = coordenadas
    app.state.alertas = alertas

    return {'message': 'Ruta generada exitosamente'}

@app.get('/mapa', response_class=HTMLResponse)
def getMapa():
    if not hasattr(app.state, 'mejorRuta'):
        return 'Primero genere una ruta'
    
    mejorRuta = app.state.mejorRuta
    coordenadas = app.state.coordenadas
    alertas = app.state.alertas

    # Calcular el centro de todas las coordenadas disponibles
    latitudes = [coord[0] for coord in coordenadas]
    longitudes = [coord[1] for coord in coordenadas]
    center_lat = np.mean(latitudes)
    center_lon = np.mean(longitudes)

    # Crear el mapa de Folium centrado en el punto calculado
    mapa = folium.Map(location=[center_lat, center_lon], zoom_start=13)

    # Añadir marcadores para las alertas
    for i, alerta in enumerate(alertas):
        coords = alerta.get('coordinates')
        if coords and isinstance(coords, list) and len(coords) == 2 and all(isinstance(coord, (int, float)) for coord in coords):
            if i== mejorRuta[0]:
              if i == mejorRuta[0]:  # Alerta inicial
                folium.Marker(location=coords, 
                              popup=f"Alerta {i} - ID: {alerta['id']} - Llenado: {alerta['llenado']}", 
                              icon=folium.Icon(color='green', icon='play', prefix='fa')).add_to(mapa)
            elif i == mejorRuta[-1]:  # Alerta final
                folium.Marker(location=coords, 
                              popup=f"Alerta {i} - ID: {alerta['id']} - Llenado: {alerta['llenado']}", 
                              icon=folium.Icon(color='red', icon='stop', prefix='fa')).add_to(mapa)
            else:  # Otras alertas
                folium.Marker(location=coords, 
                              popup=f"Alerta {i} - ID: {alerta['id']} - Llenado: {alerta['llenado']}", 
                              icon=folium.Icon(color='blue', icon='info-sign')).add_to(mapa)


    # Añadir la ruta óptima
    folium.PolyLine(locations=[coordenadas[idx] for idx in mejorRuta], color='blue', weight=2.5, opacity=1).add_to(mapa)

    # Guardar el mapa en un archivo temporal y devolverlo como HTML
    mapa.save('map.html')
    with open('map.html', 'r') as f:
        html_content = f.read()

    return HTMLResponse(content=html_content, status_code=200)
