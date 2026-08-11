Proyecto/

assets/
│
├── rooms/
├── ui/
└── npcs/

data/
│
└── memories/
    └── <<memory>>/
        ├── metadata.json
        ├── story.json
        ├── rooms.json
        ├── objects.json
        ├── computers.json
        ├── documents.json
        ├── npcs.json
        ├── dialogues.json
        └── events.json

src/

    main.py
    constants.py

    core/
    │
    ├── game.py
    ├── clock.py
    └── memory_loader.py

    world/
    │
    ├── objects/
        │
        ├── computer.py
        ├── document.py
        └── door.py
    ├── room.py
    ├── object_factory.py
    └── object.py

    entities/
    │
    └── npc.py

    managers/
    │
    └── event_manager.py

    ui/
    │
    ├── ui.py
    └── computer.py

documents/

test/


## Nueva estructura de memoria:
memory_X/
│
├── assets/                    ← COMPARTIDO
│   ├── rooms/
│   ├── npcs/
│   ├── ui/
│   └── ...
│
├── metadata.json              ← COMPARTIDO
├── rooms.json                 ← COMPARTIDO
├── objects.json               ← COMPARTIDO
├── npcs.json                  ← COMPARTIDO
├── events.json                ← COMPARTIDO
│
└── locales/
    ├── es/
    │   ├── story.json
    │   ├── dialogues.json
    │   ├── computers.json
    │   ├── documents.json
    │   ├── files.json
    │   └── documents/
    │
    └── en/
        ├── story.json
        ├── dialogues.json
        ├── computers.json
        ├── documents.json
        ├── files.json
        └── documents/