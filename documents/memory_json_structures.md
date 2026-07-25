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
  "version": "1.0.0",
  "resolution": {
        "width": 1536,
        "height": 1024
    }
}
```

## story.json

Información narrativa global.

``` json
{
  "title": "The Interview",
  "objective": "Discover what happened to Daniel.",
  "time_limit": 600,
  "initial_room": "waiting_room",
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
El type puede ser document, computer o door, relacionados con document_id, computer_id o destination.

``` json
{
  "magazine": {
        "type": "document",
        "document_id": "magazine",
        "position": [
            374,
            672
        ],
        "polygon": [
            [
                94,
                -11
            ],
            [
                138,
                41
            ],
            [
                33,
                53
            ],
            [
                -1,
                -1
            ]
        ]
    },

    "notepad_waiting": {
        "type": "document",
        "document_id": "waiting_notepad",
        "position": [
            715,
            714
        ],
        "polygon": [
            [
                68,
                -44
            ],
            [
                139,
                -25
            ],
            [
                147,
                -6
            ],
            [
                75,
                26
            ],
            [
                0,
                -2
            ]
        ]
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
Puede tener pages con strings o text directo.

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
    "dialogue": "anna_default",
    "room": "reception"
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
Parámetros varían según la acción.

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
