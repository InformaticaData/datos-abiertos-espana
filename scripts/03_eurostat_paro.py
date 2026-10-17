"""
Tasa de paro mensual de España desde Eurostat (dataset une_rt_m).

Fuente: Eurostat - Licencia CC BY 4.0 - https://ec.europa.eu/eurostat/data/database
Filtros: España (ES), ambos sexos (T), todas las edades (TOTAL),
serie desestacionalizada (SA) y porcentaje de población activa (PC_ACT).
Artículo: https://informaticadata.es/donde-encontrar-datos-abiertos-en-espana-11-fuentes-para-practicar-analisis-de-datos/
"""
import eurostat

paro = eurostat.get_data_df(
    "une_rt_m",
    filter_pars={"geo": ["ES"], "sex": ["T"], "age": ["TOTAL"],
                 "s_adj": ["SA"], "unit": ["PC_ACT"]},
)

# Formato ancho: una columna por mes. Los primeros meses salen vacíos
# (la serie de España empieza en abril de 1986) y el último puede no estar publicado.
print(paro.iloc[:, -6:])   # los 6 últimos meses

# Formato largo (una fila por mes), más cómodo para analizar o graficar
largo = paro.melt(id_vars=paro.columns[:6], var_name="mes", value_name="tasa_paro")
largo = largo.dropna(subset=["tasa_paro"])
print(f"Meses con dato: {len(largo)} (desde {largo['mes'].iloc[0]})")
print(largo.tail())
