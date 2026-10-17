"""
Listar las operaciones estadísticas disponibles en la API JSON del INE.

Fuente: Instituto Nacional de Estadística (INE) - https://www.ine.es
API sin clave. Patrón: https://servicios.ine.es/wstempus/js/{idioma}/{función}/{input}
Artículo: https://informaticadata.es/donde-encontrar-datos-abiertos-en-espana-11-fuentes-para-practicar-analisis-de-datos/
"""
import requests
import pandas as pd

URL = "https://servicios.ine.es/wstempus/js/ES/OPERACIONES_DISPONIBLES"

respuesta = requests.get(URL, timeout=30)
respuesta.raise_for_status()          # Error si la petición falla

operaciones = pd.DataFrame(respuesta.json())
print(f"Operaciones disponibles: {len(operaciones)}")
print(operaciones[["Id", "Codigo", "Nombre"]].head(10))
