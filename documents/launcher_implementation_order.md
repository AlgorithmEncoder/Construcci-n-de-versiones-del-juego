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
CONFIGURACIÓN

├── 5.1 Bases: Json, manager y integración
├── 5.2 General
│   ├── Confirmaciones
│   ├── Avisos
│   └── Comportamiento del launcher
│
├── 5.3 Display
│   ├── Resolución
│   ├── Pantalla completa
│   ├── Modo ventana
│   ├── Ajustar a pantalla
│   ├── Tema del launcher
│   ├── Tema del juego
│   └── Tema de computers
│
├── 5.6 Audio
│   ├── Volumen general
│   ├── Música
│   ├── Efectos
│   └── Diálogos
│
├── 5.5 Idioma
│   └── Idioma
│
├── 5.4 Accesibilidad
│   ├── Tamaño de texto
│   ├── Animación de escritura
│   └── Velocidad del texto

## Fase 6 (Sonido)

## Fase 7 (Inventario)