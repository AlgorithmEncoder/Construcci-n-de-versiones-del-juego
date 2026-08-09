assets/

No debe contener lógica.

Solo recursos gráficos.

assets/

rooms/

Fondos de cada sala.

office.png
hall.png
archive.png
assets/ui/

Botones.

Cursor.

Panel del ordenador.

Iconos.

assets/npcs/

Sprites o retratos de personajes.

data/

Aquí vive TODO el juego.

El objetivo es que un escritor pueda crear una memoria nueva sin tocar Python.

memory_01/

Una memoria completa.

Más adelante existirán

memory_02

memory_03

memory_04

y el motor será exactamente el mismo.

rooms.json

Este será probablemente el archivo más importante.

Debe responder únicamente a estas preguntas:

¿Qué salas existen?
¿Cómo se conectan?
¿Qué objetos contiene cada una?

Nada más.

No NPC.

No eventos.

No historia.

computers.json

Todo el contenido de los ordenadores.

Ejemplo:

PC Oficina

- chats

- emails

- archivos

Cada ordenador tendrá un identificador.

Los objetos de rooms.json simplemente dirán

computer_id
npcs.json

Describe los personajes.

Cada NPC debería tener:

nombre
sprite
horario
sala actual
diálogos

El horario será una lista de horas y salas.

events.json

Todo lo que ocurre automáticamente.

Ejemplos:

08:02

Laura entra en Archivo

08:05

Suena alarma

08:07

Se desbloquea documento

08:10

Fin del bucle

El EventManager solo leerá este archivo.

story.json

Este me gusta reservarlo para información global.

Por ejemplo:

Nombre de la memoria

Tiempo máximo

Texto inicial

Texto final

Objetivo

Así no tienes esos datos repartidos.

metadata.json

No para esta versión, sino pensando en el futuro.

Ahí guardaríamos cosas como:

{
    "id": "memory_01",
    "name": "The First Memory",
    "author": "Alex",
    "version": "1.0"
}

No afecta al juego, pero permite identificar memorias, versionarlas o incluso mostrar información en un menú sin mezclarla con la historia (story.json).

src/

Aquí está el motor.

main.py

Solo hace esto.

crear juego

while abierto:

    actualizar

    dibujar

Nada más.

game.py

Es el director.

Coordina todo.

Tiene referencias a:

reloj
sala
NPC
eventos
UI

No implementa ninguna lógica concreta.

Solo coordina.

memory_loader.py

Mi favorito.

Su única misión es leer JSON.

load_rooms()

load_npcs()

load_events()

load_story()

Nada más.

No dibuja.

No calcula.

No actualiza.

room.py

Gestiona la sala actual.

Sabe:

qué fondo cargar
qué objetos contiene
qué puertas existen
object.py

Clase base.

Todo objeto clicable hereda de aquí.

Por ejemplo:

Objeto

↓

Puerta

Ordenador

Documento

Archivador

Todos tienen

posición
tamaño
acción
computer.py

Gestiona la interfaz del ordenador.

No sabe nada del mapa.

Solo sabe mostrar

Chats

Emails

Archivos
npc.py

Cada NPC.

Tiene:

sala
horario
sprite
diálogo
clock.py

Solo hace una cosa.

Contar tiempo.

No sabe qué ocurre cuando son las 08:10.

Solo devuelve la hora.

event_manager.py

Pregunta constantemente

¿Qué hora es?

Y dispara eventos.

Nada más.

ui.py

Todo lo visual.

Ventanas.

Paneles.

Botones.

Cursor.

constants.py

Aquí pondría:

FPS

Resolución

Colores

Fuentes

Ruta de datos

Así nunca escribes números mágicos