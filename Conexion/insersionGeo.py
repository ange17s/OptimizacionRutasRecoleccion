from pymongo import MongoClient
from pyproj import Proj, transform
import json

try:
    in_proj = Proj('epsg:3857')
    out_proj = Proj('epsg:4326')

    client = MongoClient('localhost',27017)
    database = client['rutas']
    collection = database['ubicaciones']
    docgeo = 'database\contenerizacion.geojson'

    #Crear indice geoespacial
    collection.create_index([('geometry', '2dsphere')])

    #Leer para insersion 
    if not collection.find_one():
        with open(docgeo, 'r', encoding='utf-8') as geojson_file:
            geojson_data = json.load(geojson_file)

        #conversion de coordenadas
        for feature in geojson_data['features']:
            x, y = feature['geometry']['coordinates']
            lon, lat = transform(in_proj, out_proj, x, y)
            feature['geometry']['coordinates'] = [lon, lat]

        #insercion de datos
        collection.insert_many(geojson_data['features'])
        print(f'Se han insertado {len(geojson_data['features'])} registros en la coleccion ')
    else:
        print('No se han realizado inserciones')

except Exception as ex:
    print('Error durante la conexión: {}'.format(ex))
finally:
    client.close()
    print('Conexión finalizada.')
