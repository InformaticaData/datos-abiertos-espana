# Dónde encontrar datos abiertos en España

Código del artículo **[Dónde encontrar datos abiertos en España: 11 fuentes para practicar análisis de datos](https://informaticadata.es/donde-encontrar-datos-abiertos-en-espana-11-fuentes-para-practicar-analisis-de-datos/)**, publicado en [InformaticaData España](https://informaticadata.es).

Cuatro scripts cortos en Python para empezar a trabajar con datos públicos reales de España desde código: la API del INE, el paro registrado del SEPE, la tasa de paro de Eurostat y la API CKAN de los portales de Madrid y Barcelona.

## Contenido

| Script | Fuente | Qué hace |
|---|---|---|
| `scripts/01_ine_operaciones.py` | [INE](https://www.ine.es) | Lista las operaciones estadísticas de la API JSON (sin clave) |
| `scripts/02_sepe_paro_municipios.py` | [SEPE](https://datos.gob.es/es/catalogo/ea0041513-paro-registrado-por-municipio) | Lee el paro registrado por municipio de 2022 y trata los valores `<5` |
| `scripts/03_eurostat_paro.py` | [Eurostat](https://ec.europa.eu/eurostat/data/database) | Descarga la tasa de paro mensual de España (`une_rt_m`) y la pasa a formato largo |
| `scripts/04_ckan_buscar.py` | [Madrid](https://datos.madrid.es) · [Barcelona](https://opendata-ajuntament.barcelona.cat) | Busca conjuntos de datos por palabra clave en dos portales CKAN |
| `scripts/probar_scripts_t2b.py` | Todas | Ejecuta las comprobaciones usadas para verificar el artículo |

## Cómo ejecutarlo

Requisitos: Python 3.10 o superior.

```bash
git clone https://github.com/InformaticaData/datos-abiertos-espana.git
cd datos-abiertos-espana

python3 -m venv venv
source venv/bin/activate          # En Windows: venv\Scripts\activate
pip install -r requirements.txt

python scripts/01_ine_operaciones.py
```

Los scripts descargan los datos directamente de las fuentes oficiales; este repositorio **no incluye ficheros de datos**.

## Fuentes y licencias de los datos

Los datos pertenecen a sus organismos y se usan según sus condiciones:

| Fuente | Licencia |
|---|---|
| INE | Condiciones propias: reutilización citando la fuente ([aviso legal](https://www.ine.es/aviso_legal)) |
| SEPE | CC BY 4.0 |
| Eurostat | CC BY 4.0 (salvo datos de países no UE/AELC/candidatos para uso comercial) |
| Ayuntamiento de Madrid | CC BY 4.0 |
| Ajuntament de Barcelona | CC BY 4.0 |

Probado el 13/10/2026. Si alguna URL o formato cambia, abre un *issue*.

## Licencia del código

El código de este repositorio se publica bajo licencia [MIT](LICENSE).

---

¿Te ha resultado útil? En [informaticadata.es](https://informaticadata.es) publico tutoriales de análisis de datos con datasets reales de España. **Suscríbete a la newsletter** para recibir el siguiente: qué preocupa a los españoles según los barómetros del CIS.
