
import sys

actor_actual = None
titulos = set()

for linea in sys.stdin:
    linea = linea.strip()

    if not linea:
        continue

    partes = linea.split("\t", 1)

    if len(partes) != 2:
        continue

    actor, show_id = partes

    if actor_actual is not None and actor != actor_actual:
        print(f"{actor_actual}\t{len(titulos)}")
        titulos = set()

    actor_actual = actor
    titulos.add(show_id)

if actor_actual is not None:
    print(f"{actor_actual}\t{len(titulos)}")
