"""
Paro registrado por municipios (SEPE), año 2022.

Fuente: Servicio Público de Empleo Estatal (SEPE) - Licencia CC BY 4.0
Ficha: https://datos.gob.es/es/catalogo/ea0041513-paro-registrado-por-municipio
Artículo: https://informaticadata.es/donde-encontrar-datos-abiertos-en-espana-11-fuentes-para-practicar-analisis-de-datos/
"""
import pandas as pd

URL = ("https://sede.sepe.gob.es/es/portaltrabaja/resources/sede/"
       "datos_abiertos/datos/Paro_por_municipios_2022_csv.csv")

# La primera línea del fichero es un título: la saltamos con skiprows=1.
# Separador ';' y codificación latin-1, habituales en la Administración.
paro = pd.read_csv(URL, sep=";", encoding="latin-1", skiprows=1)

# Algunos nombres de columna traen espacios sobrantes (' Municipio')
paro.columns = paro.columns.str.strip()
print(paro.shape)   # (97608, 20): un registro por municipio y mes

# '<5' = menos de 5 personas (secreto estadístico): lo tratamos como no disponible
cols_paro = [c for c in paro.columns
             if c.lower().startswith("paro") or c.lower().startswith("total")]
n_menor5 = (paro[cols_paro] == "<5").sum().sum()
paro[cols_paro] = (paro[cols_paro].replace("<5", pd.NA)
                   .apply(pd.to_numeric, errors="coerce"))
print(f"Celdas con '<5': {n_menor5:,}".replace(",", "."))

# Total de enero de 2022 (la oficial del SEPE es 3.123.078)
col_total = next(c for c in cols_paro if c.lower().startswith("total"))
col_mes = next(c for c in paro.columns if "mes" in c.lower())
enero = paro[paro[col_mes].astype(str).str.endswith("01")]
print(f"Total enero 2022 (sin los '<5'): {enero[col_total].sum():,.0f}".replace(",", "."))
