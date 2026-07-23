# Estructura de los JSON de una memoria

    data/
    └── memory_01/
        ├── metadata.json
        ├── story.json
        ├── rooms.json
        ├── objects.json
        ├── computers.json
        ├── documents.json
        ├── npcs.json
        ├── dialogues.json
        └── events.json

## metadata.json

Identifica la memoria. No afecta al gameplay.

``` json
{
  "id": "memory_01",
  "name": "The Interview",
  "author": "Alex",
  "version": "1.0.0"
}
```

## story.json

Información narrativa global.

``` json
{
  "title": "The Interview",
  "objective": "Discover what happened to Daniel.",
  "time_limit": 600,
  "intro": "...",
  "ending": "..."
}
```

## rooms.json

Define únicamente el mapa.

``` json
{
  "reception": {
    "name": "Reception",
    "background": "reception",
    "connections": [
      "hall",
      "waiting_room"
    ],
    "objects": [
      "pc_reception",
      "agenda",
      "phone"
    ]
  }
}
```

## objects.json

Define los objetos interactivos.

``` json
{
  "pc_reception": {
    "type": "computer",
    "position": [520,180],
    "computer_id": "reception_pc"
  },
  "agenda": {
    "type": "document",
    "position": [300,420],
    "document_id": "agenda_01"
  },
  "door_archive": {
    "type": "door",
    "position": [780,220],
    "destination": "archive"
  }
}
```

## computers.json

Contenido de cada ordenador.

``` json
{
  "reception_pc": {
    "emails": [],
    "chats": [],
    "files": []
  }
}
```

## documents.json

Contenido de documentos físicos.

``` json
{
  "agenda_01": {
    "title": "Reception Agenda",
    "pages": [
      "...",
      "..."
    ]
  },
  "note_01": {
    "title": "Sticky Note",
    "text": "..."
  }
}
```

## npcs.json

Define personajes y horarios.

``` json
{
  "anna": {
    "name": "Anna",
    "sprite": "anna",
    "schedule": [
      {
        "time": "08:00",
        "room": "reception"
      },
      {
        "time": "08:05",
        "room": "archive"
      }
    ],
    "dialogue": "anna_default"
  }
}
```

## dialogues.json

Todo el texto de los diálogos.

``` json
{
  "anna_default": [
    { "text": "Buenos días." },
    { "text": "¿Necesitas algo?" }
  ]
}
```

## events.json

Eventos automáticos del nivel.

``` json
[
  {
    "time": "08:02",
    "action": "npc_move",
    "npc": "anna",
    "room": "archive"
  },
  {
    "time": "08:05",
    "action": "sound",
    "sound": "alarm"
  },
  {
    "time": "08:10",
    "action": "end_loop"
  }
]
```
