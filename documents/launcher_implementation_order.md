# Orden de implementación

## Fase 1 (infraestructura)
    MainWindow
    MainController
    Header
    Sidebar
    Workspace
    Footer
    sistema de historial
    sistema de vistas

## Fase 2 (Incursiones)
    lista de sueños
    ficha de sueño
    botón Iniciar incursión
    integración con Game

## Fase 3 (Notas)
    explorador
    carpetas
    editor
    persistencia
    notas rápidas

## FASE 4 — PROFILE
│
├── 4.1 Logger
│   ├── cargar
│   ├── registrar temporalmente
│   └── guardar
│
├── 4.2 Activity View
│   └── visualizar logger
│
├── 4.3 Integración
│   ├── Game
│   ├── main
│   └── resto del juego
│
├── 4.4 Statistics
│   ├── decidir qué estadísticas queremos
│   ├── identificar qué datos ya existen
│   ├── añadir únicamente las variables necesarias
│   └── persistencia global
│
└── 4.5 Achievements
    ├── definir logros
    ├── sistema de comprobación
    ├── persistencia
    └── vista

## Fase 5 (Ajustes)

## Fase 6 (Inventario)