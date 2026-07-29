launcher/
│
├── main_window.py          # Ventana principal
│
├── header.py               # Barra superior
├── sidebar.py              # Menú lateral
├── workspace.py            # Área central
├── footer.py               # Barra inferior
│
├── navigation.py           # Historial del workspace
│
├── styles.py               # Colores, márgenes, tamaños
│
├── modules/
│   ├── __init__.py
│   │
│   ├── home.py             # Principal
│   ├── profile.py          # Perfil
│   └── settings.py         # Ajustes
│
├── home/
│   ├── __init__.py
│   │
│   ├── incursions.py
│   ├── notes.py
│   └── inventory.py
│
└── widgets/
    ├── button.py
    ├── list_item.py
    ├── section_title.py
    └── empty_view.py


launcher/
└── notes/
    ├── __init__.py
    ├── note.py
    ├── folder.py
    ├── filesystem.py
    └── notes_manager.py