import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
key = "eaec773a-2976-42f9-ac9b-8b27efebffb6"

while True:
    print("\n--- Calculadora de Rutas GraphHopper ---")
    print("Para salir del programa, ingresa 'q' en cualquier momento.")
    
    origen = input("Ingresa la Ciudad de Origen: ")
    if origen.lower() == 'q':
        break
        
    destino = input("Ingresa la Ciudad de Destino: ")
    if destino.lower() == 'q':
        break

    # Obtener coordenadas de origen
    url_geocode = f"https://graphhopper.com/api/1/geocode?q={urllib.parse.quote(origen)}&key={key}"
    geo_data_orig = requests.get(url_geocode).json()
    
    # Obtener coordenadas de destino
    url_geocode_dest = f"https://graphhopper.com/api/1/geocode?q={urllib.parse.quote(destino)}&key={key}"
    geo_data_dest = requests.get(url_geocode_dest).json()

    if geo_data_orig['hits'] and geo_data_dest['hits']:
        # Corrección aplicada en las siguientes 4 líneas:
        lat_orig = geo_data_orig['hits'][0]['point']['lat']
        lng_orig = geo_data_orig['hits'][0]['point']['lng']
        lat_dest = geo_data_dest['hits'][0]['point']['lat']
        lng_dest = geo_data_dest['hits'][0]['point']['lng']

        # Consultar la ruta
        url_ruta = f"{route_url}point={lat_orig},{lng_orig}&point={lat_dest},{lng_dest}&vehicle=car&locale=es&calc_turn_info=true&key={key}"
        res_ruta = requests.get(url_ruta).json()

        paths = res_ruta.get("paths", [])
        if paths:
            ruta = paths[0]
            # Distancia en Km
            distancia_km = ruta["distance"] / 1000
            # Duración en horas, minutos y segundos
            tiempo_ms = ruta["time"]
            segundos_totales = int(tiempo_ms / 1000)
            horas = segundos_totales // 3600
            minutos = (segundos_totales % 3600) // 60
            segundos = segundos_totales % 60
            
            # Combustible requerido (asumiendo rendimiento promedio de 10 km/l)
            combustible_lts = distancia_km / 10.0

            print("\n=============================================")
            print(f"Ruta: {origen.capitalize()} a {destino.capitalize()}")
            print(f"Distancia: {distancia_km:.2f} km")
            print(f"Duración: {horas:02d} horas, {minutos:02d} minutos, {segundos:02d} segundos")
            print(f"Combustible requerido: {combustible_lts:.2f} litros")
            print("=============================================\n")

            # Narrativa de la ruta
            print("Instrucciones de la ruta:")
            for instruccion in ruta["instructions"]:
                print(f"- {instruccion['text']} ({instruccion['distance']/1000:.2f} km)")
        else:
            print("No se encontró una ruta válida.")
    else:
        print("Error: No se encontraron las coordenadas de las ciudades ingresadas.")