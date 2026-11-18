import pandas as pd
from pathlib import Path

# Rutas del proyecto
carpeta_proyecto = Path(__file__).resolve().parent.parent
entrada = carpeta_proyecto / "datos" / "mapreduce_actores.txt"
salida = carpeta_proyecto / "datos" / "mapreduce_actores.csv"

# Leer el resultado de Hadoop
df = pd.read_csv(
    entrada,
    sep="\t",
    header=None,
    names=["actor", "cantidad_titulos"],
    encoding="utf-8"
)

# Ordenar por cantidad descendente y actor ascendente
df["cantidad_titulos"] = pd.to_numeric(
    df["cantidad_titulos"]
)

df = df.sort_values(
    by=["cantidad_titulos", "actor"],
    ascending=[False, True]
)

# Exportar CSV
df.to_csv(salida, index=False, encoding="utf-8")

print("=" * 55)
print("EXPORTACIÓN DEL RESULTADO MAPREDUCE")
print("=" * 55)
print(f"Total de actores: {len(df)}")
print(f"Archivo generado: {salida}")
print("\nTOP 10 ACTORES:")
print(df.head(10).to_string(index=False))