from pathlib import Path
import os

p = Path(r"E:\OneDrive\Personal\Proyectos\Juego de misterio gráfico\Construcción de versiones del juego\assets\notes\aaa")

p.mkdir(exist_ok=True)

print(p.exists())

os.rmdir(p)

print("OK")