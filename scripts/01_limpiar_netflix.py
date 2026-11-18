
import re
from pathlib import Path

import pandas as pd


# ============================================================
# RETO 1: LIMPIEZA DEL CATALOGO DE NETFLIX
# Programa: 01_limpiar_netflix.py
# ============================================================

# Rutas del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent
ARCHIVO_ENTRADA = BASE_DIR / "datos" / "netflix_titles.csv"
ARCHIVO_SALIDA = BASE_DIR / "datos" / "netflix_clean.csv"


def limpiar_netflix():

    print("=" * 60)
    print("         PROCESO DE LIMPIEZA DEL CATALOGO NETFLIX")
    print("=" * 60)

    # 1. Leer archivo original y registrar filas y columnas
    df = pd.read_csv(ARCHIVO_ENTRADA, dtype="string")

    filas_iniciales = len(df)
    columnas_iniciales = len(df.columns)

    print(f"\nRegistros iniciales: {filas_iniciales}")
    print(f"Columnas originales: {columnas_iniciales}")

    columnas_originales = list(df.columns)

    # Comprobar las columnas necesarias
    columnas_requeridas = ["show_id", "type", "date_added", "duration"]

    for columna in columnas_requeridas:
        if columna not in df.columns:
            raise ValueError(f"No se encuentra la columna: {columna}")

    # 2. Eliminar espacios al inicio y al final
    for columna in df.select_dtypes(include=["string"]).columns:
        df[columna] = df[columna].str.strip()

    # 3. Sustituir saltos de línea y tabulaciones por espacios
    for columna in df.select_dtypes(include=["string"]).columns:
        df[columna] = df[columna].str.replace(
            r"[\r\n\t]+", " ", regex=True
        )

    # 4. Convertir textos vacíos en valores nulos
    for columna in df.select_dtypes(include=["string"]).columns:
        df[columna] = df[columna].replace("", pd.NA)

    # 5. Eliminar filas completamente duplicadas
    antes = len(df)
    df = df.drop_duplicates()
    duplicados_eliminados = antes - len(df)

    # 6. Eliminar registros sin show_id
    antes = len(df)
    df = df.dropna(subset=["show_id"])
    sin_show_id_eliminados = antes - len(df)

    # 7. Conservar la primera aparición de cada show_id
    antes = len(df)
    df = df.drop_duplicates(subset=["show_id"], keep="first")
    show_id_repetidos_eliminados = antes - len(df)

    # 8. Convertir date_added al formato dd/mm/aaaa
    fechas = pd.to_datetime(
        df["date_added"],
        format="mixed",
        errors="coerce"
    )

    df["date_added"] = fechas.dt.strftime("%d/%m/%Y").astype("string")

    # 9. Crear duration_min únicamente para películas
    duraciones = df["duration"].str.extract(
        r"^\s*(\d+)\s*min\s*$",
        flags=re.IGNORECASE,
        expand=False
    )

    duration_min = pd.to_numeric(
        duraciones,
        errors="coerce"
    ).astype("Int64")

    df["duration_min"] = duration_min.where(
        df["type"].str.casefold() == "movie",
        pd.NA
    )

    # 10. Conservar las columnas originales y agregar duration_min al final
    df = df[columnas_originales + ["duration_min"]]

    # Mantener los datos desconocidos como nulos
    registros_finales = len(df)

    # 11. Guardar el CSV limpio en UTF-8, sin índice
    df.to_csv(
        ARCHIVO_SALIDA,
        index=False,
        encoding="utf-8",
        na_rep=""
    )

    # Calcular indicadores de duración
    peliculas = df["type"].str.casefold() == "movie"

    peliculas_validas = (
        peliculas & df["duration_min"].gt(0).fillna(False)
    )

    peliculas_sin_duracion = peliculas & ~peliculas_validas

    cantidad_peliculas_validas = int(peliculas_validas.sum())
    cantidad_peliculas_sin_duracion = int(peliculas_sin_duracion.sum())

    # Mostrar tabla completa de limpieza
    resultados = pd.DataFrame({
        "Indicador": [
            "Registros del archivo original, sin cabecera",
            "Columnas del archivo original",
            "Filas completamente duplicadas eliminadas",
            "Registros sin show_id eliminados después de retirar duplicados",
            "Registros con show_id repetido eliminados posteriormente",
            "Registros del archivo limpio",
            "Películas con duration_min numérica mayor que cero",
            "Películas sin una duración numérica mayor que cero"
        ],
        "Cantidad": [
            filas_iniciales,
            columnas_iniciales,
            duplicados_eliminados,
            sin_show_id_eliminados,
            show_id_repetidos_eliminados,
            registros_finales,
            cantidad_peliculas_validas,
            cantidad_peliculas_sin_duracion
        ]
    })

    print("\n" + "=" * 60)
    print("             TABLA DE RESULTADOS DE LIMPIEZA")
    print("=" * 60)
    print(resultados.to_string(index=False))

    print("\n" + "=" * 60)
    print("LIMPIEZA FINALIZADA CORRECTAMENTE")
    print(f"Archivo generado: {ARCHIVO_SALIDA}")
    print("=" * 60)


if __name__ == "__main__":
    limpiar_netflix()
