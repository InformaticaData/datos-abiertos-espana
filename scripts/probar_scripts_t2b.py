"""
Pruebas de los 4 bloques de código del artículo
"Dónde encontrar datos abiertos en España" (T2b).

Requisitos:  pip install requests pandas eurostat
Ejecutar:    python3 probar_scripts_t2b.py

Cada prueba imprime OK o FALLO y la información necesaria para ajustar
el artículo. Pégame la salida completa.
"""
import io
import traceback

import pandas as pd
import requests


def cabecera(titulo: str) -> None:
    print("\n" + "=" * 70)
    print(titulo)
    print("=" * 70)


# ---------------------------------------------------------------------------
# 1. INE - API JSON (sin clave)
# Fuente: Instituto Nacional de Estadística (INE) - https://www.ine.es
# ---------------------------------------------------------------------------
def probar_ine() -> None:
    cabecera("1. INE · OPERACIONES_DISPONIBLES")
    url = "https://servicios.ine.es/wstempus/js/ES/OPERACIONES_DISPONIBLES"
    respuesta = requests.get(url, timeout=30)
    respuesta.raise_for_status()
    operaciones = pd.DataFrame(respuesta.json())
    print("Columnas devueltas:", list(operaciones.columns))
    print(operaciones[["Id", "Codigo", "Nombre"]].head(5))
    print(f"OK · {len(operaciones)} operaciones")


# ---------------------------------------------------------------------------
# 2. SEPE - Paro registrado por municipios 2022 (CC BY 4.0)
# https://datos.gob.es/es/catalogo/ea0041513-paro-registrado-por-municipio
# ---------------------------------------------------------------------------
def probar_sepe() -> None:
    cabecera("2. SEPE · Paro_por_municipios_2022_csv.csv")
    url = ("https://sede.sepe.gob.es/es/portaltrabaja/resources/sede/"
           "datos_abiertos/datos/Paro_por_municipios_2022_csv.csv")
    respuesta = requests.get(url, timeout=60)
    respuesta.raise_for_status()
    bruto = respuesta.content

    # Mostramos las 3 primeras líneas tal cual para ver separador y cabecera
    texto = bruto.decode("latin-1")
    print("Primeras líneas en bruto:")
    for linea in texto.splitlines()[:3]:
        print("   ", linea[:150])

    # Lectura tal como aparece en el artículo
    paro = pd.read_csv(io.BytesIO(bruto), sep=";", encoding="latin-1",
                       skiprows=1)
    paro.columns = paro.columns.str.strip()          # NUEVO: quitar espacios
    print("\nColumnas limpias:", list(paro.columns)[:8], "...")
    print(paro.shape)

    # NUEVO: convertir a número tratando '<5' como dato no disponible
    cols_paro = [c for c in paro.columns
                 if c.lower().startswith("paro") or c.lower().startswith("total")]
    print("Columnas numéricas detectadas:", len(cols_paro))
    paro[cols_paro] = (paro[cols_paro].replace("<5", pd.NA)
                       .apply(pd.to_numeric, errors="coerce"))
    print(paro[cols_paro].dtypes.value_counts())     # deben salir como numéricas
    print("Celdas '<5' convertidas a NaN:", int(paro[cols_paro].isna().sum().sum()))
    print("Total paro España, enero 2022:",
          int(paro.loc[paro["Código mes"] == 202201, "total Paro Registrado"].sum()))
    print(f"OK · {len(paro)} filas, {paro.shape[1]} columnas")


# ---------------------------------------------------------------------------
# 3. Eurostat - Tasa de paro mensual de España (une_rt_m, CC BY 4.0)
# https://ec.europa.eu/eurostat/data/database
# ---------------------------------------------------------------------------
def probar_eurostat() -> None:
    cabecera("3. Eurostat · une_rt_m")
    import eurostat

    paro = eurostat.get_data_df(
        "une_rt_m",
        filter_pars={"geo": ["ES"], "sex": ["T"], "age": ["TOTAL"],
                     "s_adj": ["SA"], "unit": ["PC_ACT"]},
    )
    if paro is None or paro.empty:
        print("FALLO · el filtro no devuelve datos. Valores válidos:")
        for dim in ["sex", "age", "s_adj", "unit"]:
            print(f"   {dim}:", eurostat.get_par_values("une_rt_m", dim))
        return
    print(paro.iloc[:, -6:])                         # NUEVO: últimos 6 meses

    # NUEVO: formato largo, una fila por mes
    largo = paro.melt(id_vars=paro.columns[:6], var_name="mes",
                      value_name="tasa_paro")
    largo = largo.dropna(subset=["tasa_paro"])
    print("Columnas identificadoras:", list(paro.columns[:6]))
    print(largo.tail())
    print(f"Primer mes con dato: {largo['mes'].iloc[0]} · meses con dato: {len(largo)}")
    print(f"OK · {paro.shape[1]} columnas (las últimas son meses)")


# ---------------------------------------------------------------------------
# 4. CKAN - Barcelona y Madrid (CC BY 4.0)
# https://opendata-ajuntament.barcelona.cat · https://datos.madrid.es
# ---------------------------------------------------------------------------
def probar_ckan() -> None:
    cabecera("4. CKAN · package_search 'bicicleta'")
    portales = {
        "Barcelona": "https://opendata-ajuntament.barcelona.cat/data/api/3/action/",
        "Madrid": "https://datos.madrid.es/api/3/action/",
    }
    for nombre, base in portales.items():
        respuesta = requests.get(base + "package_search",
                                 params={"q": "bicicleta", "rows": 5},
                                 timeout=30)
        respuesta.raise_for_status()
        resultados = respuesta.json()["result"]["results"]
        print(f"--- {nombre} ({len(resultados)} resultados) ---")
        for d in resultados:
            print("   ·", d["title"])
    print("OK")


if __name__ == "__main__":
    for prueba in (probar_ine, probar_sepe, probar_eurostat, probar_ckan):
        try:
            prueba()
        except Exception:
            print("FALLO:")
            traceback.print_exc()