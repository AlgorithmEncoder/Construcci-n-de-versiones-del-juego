# Diseño de la ventana principal

## Objetivo

La ventana principal representa la estación de trabajo del investigador.
Desde ella se gestionan las incursiones, las notas personales y el
inventario. La interfaz está inspirada en una aplicación de escritorio,
con un diseño limpio y modular.

------------------------------------------------------------------------

# Estructura general

La ventana se divide siempre en tres zonas principales:

``` text
┌──────────────────────────────────────────────────────────────────────────┐
│ Header                                                                   │
├──────────────────────────────────────────────────────────────────────────┤
│ Sidebar              │                 Workspace                         │
│                      │                                                    │
│                      │                                                    │
│                      │                                                    │
│                      │                                                    │
├──────────────────────────────────────────────────────────────────────────┤
│ Footer                                                                   │
└──────────────────────────────────────────────────────────────────────────┘
```

La estructura nunca cambia. Únicamente cambia el contenido mostrado en
la **Sidebar** y en el **Workspace**.

------------------------------------------------------------------------

# Header

Contiene la navegación principal de la aplicación.

## Componentes

-   Título del juego (`DreamWalker` o nombre definitivo).
-   Botón **Principal**.
-   Botón **Perfil**.
-   Botón **Ajustes**.

## Funcionamiento

Los botones del Header **únicamente cambian la Sidebar**.

Cada botón carga un módulo diferente.

------------------------------------------------------------------------

# Footer

Siempre permanece visible.

## Información fija

-   Versión del juego.
-   Autor.

Ejemplo:

``` text
v0.1.0                                     © Alberto
```

## Información dinámica

Campo destinado a mostrar mensajes del sistema.

Ejemplos:

-   Sincronización estable
-   Guardando...
-   Leyendo memoria...
-   Hipótesis registrada
-   Notas guardadas

------------------------------------------------------------------------

# Body

El cuerpo se divide en dos paneles.

## Sidebar

Contiene la navegación del módulo seleccionado.

## Workspace

Zona principal donde se muestra toda la información.

El Workspace se divide internamente en:

``` text
Workspace
│
├── WorkspaceHeader
└── WorkspaceBody
```

------------------------------------------------------------------------

# WorkspaceHeader

Siempre tiene el mismo formato.

``` text
Título de la vista                          [← Volver]
```

## Reglas

-   El título siempre aparece alineado a la izquierda.
-   El botón **Volver** siempre aparece alineado completamente a la
    derecha.
-   El botón únicamente se muestra cuando existe una vista anterior.

------------------------------------------------------------------------

# WorkspaceBody

Aquí se representa el contenido real de la aplicación.

------------------------------------------------------------------------

# Módulo Principal

Al pulsar **Principal** en el Header, la Sidebar pasa a contener:

``` text
🧠 Incursiones

📝 Notas

🎒 Inventario
```

Estos botones **únicamente modifican el Workspace**.

------------------------------------------------------------------------

## Incursiones

### Vista 1 --- Lista

``` text
INCURSIONES

La entrevista

Sueño 2 🔒

Sueño 3 🔒

Sueño 4 🔒
```

Cada incursión puede mostrar:

-   Nombre
-   Estado
-   Duración del sueño
-   Porcentaje de progreso
-   Última incursión

### Vista 2 --- Información de una incursión

``` text
La entrevista                          [← Volver]

Estado:
En investigación

Duración:
10 minutos

Incursiones realizadas:
8

Descripción

...

Objetivo

...

[ Iniciar incursión ]
```

------------------------------------------------------------------------

# Notas

Las notas funcionan como un **explorador de archivos**.

Todo ocurre dentro del Workspace.

## Vista raíz

``` text
Proyecto

📁 Caso 01

📁 Caso 02

📄 General.txt
```

## Vista carpeta

``` text
Caso 01                              [← Volver]

📄 Daniel.txt

📄 Director.txt

📁 Personajes

📁 Correos
```

## Vista archivo

``` text
Daniel.txt                           [← Volver]

----------------------------------------

(Editor de texto)

----------------------------------------
```

## Funcionalidades

El jugador podrá:

-   Crear carpetas.
-   Crear notas (.txt).
-   Editar notas.
-   Renombrar notas.
-   Renombrar carpetas.
-   Eliminar notas.
-   Eliminar carpetas (con todo su contenido).
-   Mover notas entre carpetas.
-   Mover carpetas.
-   Organizar libremente la estructura.

El sistema debe comportarse como un explorador de archivos sencillo.

------------------------------------------------------------------------

# Inventario

## Vista lista

``` text
INVENTARIO

Tarjeta de acceso

USB

Fotografía

Documento roto
```

## Vista objeto

``` text
Fotografía                          [← Volver]

(imagen)

Descripción

...

Observaciones

...
```

------------------------------------------------------------------------

# Perfil

Al pulsar **Perfil**, cambia completamente la Sidebar.

Ejemplo:

``` text
👤 Estadísticas

🏆 Logros

📊 Actividad
```

Cada opción mostrará su correspondiente información en el Workspace.

------------------------------------------------------------------------

# Ajustes

Al pulsar **Ajustes**, la Sidebar cambia a:

``` text
🎮 General

🔊 Audio

🖥 Pantalla

🌐 Idioma
```

Cada opción modificará únicamente el Workspace.

------------------------------------------------------------------------

# Arquitectura de navegación

## Header

-   Cambia el módulo.
-   Cambia la Sidebar.

## Sidebar

-   Cambia la vista del Workspace.

## Workspace

-   Permite navegar dentro de la información del módulo.

------------------------------------------------------------------------

# Navegación interna

Las vistas del Workspace mantienen un historial.

Ejemplo:

``` text
Incursiones

↓

Detalle de incursión

↓

Documento

↓

Imagen
```

El botón **Volver** siempre regresa a la vista inmediatamente anterior.

------------------------------------------------------------------------

# Filosofía de diseño

-   Interfaz limpia y profesional.
-   Inspiración en aplicaciones de escritorio.
-   Sin animaciones complejas.
-   Navegación consistente.
-   Separación clara de responsabilidades:
    -   Header → cambia módulos.
    -   Sidebar → cambia vistas.
    -   Workspace → muestra y edita información.
    -   Footer → información global del sistema.
