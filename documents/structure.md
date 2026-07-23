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