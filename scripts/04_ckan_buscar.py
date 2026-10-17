"""
Buscar conjuntos de datos en portales CKAN por palabra clave.

Fuentes (licencia CC BY 4.0):
  Open Data BCN (Ajuntament de Barcelona) - https://opendata-ajuntament.barcelona.cat
  Portal de Datos Abiertos del Ayuntamiento de Madrid - https://datos.madrid.es
Artículo: https://informaticadata.es/donde-encontrar-datos-abiertos-en-espana-11-fuentes-para-practicar-analisis-de-datos/
"""
import sys
import requests

PORTALES = {
    "Barcelona": "https://opendata-ajuntament.barcelona.cat/data/api/3/action/",
    "Madrid": "https://datos.madrid.es/api/3/action/",
}


def buscar_datasets(base_url: str, termino: str, filas: int = 5) -> list[str]:
    """Devuelve los títulos de los conjuntos que coinciden con el término."""
    respuesta = requests.get(
        base_url + "package_search",
        params={"q": termino, "rows": filas},
        timeout=30,
    )
    respuesta.raise_for_status()
    resultados = respuesta.json()["result"]["results"]
    return [d["title"] for d in resultados]


if __name__ == "__main__":
    # Uso: python scripts/04_ckan_buscar.py [término]   (por defecto: bicicleta)
    termino = sys.argv[1] if len(sys.argv) > 1 else "bicicleta"
    for nombre, url in PORTALES.items():
        print(f"--- {nombre} ---")
        for titulo in buscar_datasets(url, termino):
            print("·", titulo)
