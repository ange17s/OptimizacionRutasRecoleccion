from pymongo import MongoClient
import random

try:

    client = MongoClient('localhost',27017)
    database = client['rutas']
    collection = database['ubicaciones']
    documents = collection.find()

    alertas = []
    limLlenado = 40

    for record in collection.find():
        capacidad = record['properties'].get('CAPACIDAD')
        coordenadas = record['geometry'].get('coordinates')
        idd = str(record['_id'])

        porLlenado = int((capacidad * random.randint(0,100))/100)

        if porLlenado > (limLlenado/100)*capacidad:
            alerta = {
                'id':idd,
                'coordinates': coordenadas,
                'llenado': porLlenado
            }

            alertas.append(alerta)

except Exception as ex:
    print('Error durante la conexión: {}'.format(ex))
finally:
    client.close()
    print('Conexión finalizada.')

def obtener_alertas():
    return alertas

if __name__ == "__main__":
    # Imprimir las alertas solo si se ejecuta directamente
    for alerta in alertas:
        print(alerta)