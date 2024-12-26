import requests
from datetime import datetime
from SPARQLWrapper import SPARQLWrapper, JSON
import json
# Configuración del endpoint SPARQL
ENDPOINT_URL = "https://query.wikidata.org/sparql"

# Definición de la consulta SPARQL
SPARQL_QUERY = """
SELECT DISTINCT ?elemento ?imagen ?coordenadas ?provinciaLabel
WHERE { 
    ?elemento wdt:P11804 ?valor . 
    ?elemento wdt:P625 ?coordenadas.
    ?elemento wdt:P131 ?ciudad.
    ?ciudad wdt:P131 ?provincia.
    {
        ?elemento wdt:P18 ?imagen . 
    } 
    UNION 
    { 
        ?elemento wdt:P373 ?imagen . 
    }
     SERVICE wikibase:label { 
        bd:serviceParam wikibase:language "es" . 
        ?provincia rdfs:label ?provinciaLabel .
    }
}
"""

# Configuración del cliente SPARQL
sparql = SPARQLWrapper(ENDPOINT_URL)
sparql.setQuery(SPARQL_QUERY)
sparql.setReturnFormat(JSON)

# Ejecutar la consulta SPARQL y procesar los resultados
results = sparql.query().convert()

# Crear un diccionario para almacenar los elementos recuperados
diccionario_elementos = dict()
for result in results["results"]["bindings"]:
    elemento_id = result['elemento']['value'].replace("http://www.wikidata.org/entity/", "") # Obtener ID de Wikidata
    coordenadas = result['coordenadas']['value'].replace("Point(", "").replace(")", "").replace(" ", ",") # Limpiar coordenadas del punto
    intercambiadas = ",".join(coordenadas.split(",")[::-1])
    provincias= result['provinciaLabel']['value'].split(" ") # Valor de la provincia de Andalucia


    lista_elemento = list()
    lista_elemento.append(intercambiadas)
    lista_elemento.append(provincias[len(provincias)-1])
    diccionario_elementos.setdefault(elemento_id,lista_elemento)  # Almacenar el ID del elemento y sus coordenadas


# Función para obtener las revisiones de un elemento de Wikidata
def get_revisions(title, limit=40):
    """
    Obtiene las revisiones de un elemento de Wikidata.

    Parámetros:
    - title: ID del elemento de Wikidata (por ejemplo, Q42)
    - limit: Límite de revisiones a recuperar (por defecto, 40)

    Retorna:
    - Una lista de revisiones del elemento.
    """
    url = "https://www.wikidata.org/w/api.php"
    params = {
        "action": "query",
        "prop": "revisions",
        "titles": title,
        "rvprop": "ids|timestamp|user|comment",
        "rvlimit": limit,
        "format": "json"
    }
    
    revisions = []
    while True:
        response = requests.get(url, params=params).json()
        pages = response.get("query", {}).get("pages", {})
        
        # Obtener las revisiones del elemento
        for page_id, page_data in pages.items():
            revisions.extend(page_data.get("revisions", []))
        
        # Continuar si hay más revisiones, de lo contrario, salir del bucle
        if "continue" in response:
            params["rvcontinue"] = response["continue"]["rvcontinue"]
        else:
            break
    
    return revisions


# Variables para la fecha de comparación y la lista final
otra_fecha = datetime.strptime("2021-01-01", "%Y-%m-%d").date()
lista_final = dict()

# Recorrer cada elemento recuperado y obtener sus revisiones
for i, title in enumerate(diccionario_elementos.keys()):
    print(f"Elemento: {i+1} - {title}")
    
    # Obtener todas las revisiones del elemento
    all_revisions = get_revisions(title)
    
    # Filtrar las revisiones que modificaron la propiedad P18 antes de la fecha especificada
    for rev in all_revisions:
        # Extraer la fecha de la revisión
        fecha_str = rev['timestamp'].split("T")[0]  # Obtener solo la parte de la fecha (YYYY-MM-DD)
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()  # Convertir a formato de fecha

        # Comprobar si la revisión tiene un comentario que incluye la propiedad P18
        if "Property:P18" in rev.get('comment', '') and fecha > otra_fecha:
            lista_final[title] = diccionario_elementos[title]
            break  # No necesitamos más revisiones de este elemento que cumplan la condición


# Mostrar los elementos finales que cumplieron con la condición
print("Lista de elementos que cumplieron la condición:")

lista_de_documentos = [{"id": clave, "coordenadas": valor[0],"provincia": valor[1]} for clave, valor in lista_final.items()]

# Mostrar el resultado
print(json.dumps(lista_de_documentos,ensure_ascii=False, indent=4))