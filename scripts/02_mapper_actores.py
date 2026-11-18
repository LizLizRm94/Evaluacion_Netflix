import sys
import csv

for linea in sys.stdin:
    try:
        fila = next(csv.reader([linea]))

        if len(fila) < 5:
            continue

        if fila[0].strip() == "show_id":
            continue

        show_id = fila[0].strip()
        actores = fila[4]

        if not show_id or not actores:
            continue

        for actor in actores.split(","):
            actor = actor.strip()

            if actor:
                print(f"{actor}\t{show_id}")

    except (csv.Error, StopIteration):
        continue