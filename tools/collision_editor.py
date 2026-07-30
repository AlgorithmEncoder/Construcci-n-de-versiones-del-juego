#!/usr/bin/env python3

import json
import sys
from pathlib import Path

import pygame

try:
    import pyperclip
except ImportError:
    pyperclip = None


class Editor:

    def __init__(self, memory_path, image_name):

        pygame.init()

        self.memory_path = Path(memory_path)

        # ---------------------------------------------------------
        # Leer metadata
        # ---------------------------------------------------------

        metadata_file = self.memory_path / "metadata.json"

        with open(metadata_file, "r", encoding="utf8") as f:
            metadata = json.load(f)

        resolution = metadata["resolution"]

        self.window_width = resolution["width"]
        self.window_height = resolution["height"]

        # ---------------------------------------------------------
        # Cargar imagen
        # ---------------------------------------------------------

        image_file = (
            self.memory_path
            / "assets"
            / "rooms"
            / f"{image_name}.png"
        )

        if not image_file.exists():

            raise FileNotFoundError(
                f"No existe la imagen:\n{image_file}"
            )

        # Cargar imagen (sin convertir)
        self.original_img = pygame.image.load(image_file)

        # Tamaño original
        self.original_width = self.original_img.get_width()
        self.original_height = self.original_img.get_height()

        # Calcular escalado
        self.scale_x = self.window_width / self.original_width
        self.scale_y = self.window_height / self.original_height

        # Crear ventana
        info = pygame.display.Info()

        screen_width = int(info.current_w * 0.9)
        screen_height = int(info.current_h * 0.9)

        self.screen = pygame.display.set_mode(
            (
                screen_width,
                screen_height
            ),
            pygame.RESIZABLE
        )
        
        # Escalar imagen
        self.scale = min(
            screen_width / self.window_width,
            screen_height / self.window_height
        )

        world_width = self.window_width * self.scale
        world_height = self.window_height * self.scale

        self.offset_x = (screen_width - world_width) / 2
        self.offset_y = (screen_height - world_height) / 2
        
        self.img = pygame.transform.smoothscale(
            self.original_img,
            (
                int(world_width),
                int(world_height)
            )
        )

        # ---------------------------------------------------------

        info = pygame.display.Info()

        screen_width = int(info.current_w * 0.9)
        screen_height = int(info.current_h * 0.9)

        self.screen = pygame.display.set_mode(
            (
                screen_width,
                screen_height
            ),
            pygame.RESIZABLE
        )

        self.calculate_viewport()

        pygame.display.set_caption(
            "Collision Editor"
        )

        self.font = pygame.font.SysFont(
            None,
            22
        )

        self.origin = None
        self.points = []
        self.drag = None
        
        self.radius = max(4, int(6 * min(self.scale_x, self.scale_y)))

    # ==========================================================
    # Conversión coordenadas
    # ==========================================================

    def screen_to_image(self, pos):

        return (
            int((pos[0] - self.offset_x) / self.scale),
            int((pos[1] - self.offset_y) / self.scale)
        )


    def image_to_screen(self, pos):

        return (
            int(pos[0] * self.scale + self.offset_x),
            int(pos[1] * self.scale + self.offset_y)
        )

    # ==========================================================

    def rel(self, point):

        return [
            point[0] - self.origin[0],
            point[1] - self.origin[1]
        ]

    # ==========================================================

    def export(self):

        data = {

            "position": list(self.origin),

            "polygon": [

                self.rel(p)

                for p in self.points

            ]

        }

        text = json.dumps(
            data,
            indent=4
        )

        print()
        print(text)

        if pyperclip:

            pyperclip.copy(text)

            print()
            print("Copiado al portapapeles.")

    # ==========================================================

    def point_at(self, pos):

        for i, p in enumerate(self.points):

            dx = p[0] - pos[0]
            dy = p[1] - pos[1]

            if dx * dx + dy * dy < (self.radius * 2) ** 2:

                return i

        return None
    
    def calculate_viewport(self):

        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        self.scale = min(
            screen_width / self.window_width,
            screen_height / self.window_height
        )

        world_width = self.window_width * self.scale
        world_height = self.window_height * self.scale

        self.offset_x = (screen_width - world_width) / 2
        self.offset_y = (screen_height - world_height) / 2

        self.img = pygame.transform.smoothscale(
            self.original_img,
            (
                int(world_width),
                int(world_height)
            )
        )

    # ==========================================================

    def draw(self):

        self.screen.fill(
            (40, 40, 40)
        )

        self.screen.fill((0,0,0))

        self.screen.blit(
            self.img,
            (
                int(self.offset_x),
                int(self.offset_y)
            )
        )

        # ------------------------------------------
        # Origen
        # ------------------------------------------

        if self.origin:

            p = self.image_to_screen(
                self.origin
            )

            pygame.draw.line(
                self.screen,
                (0, 255, 0),
                (p[0] - 8, p[1]),
                (p[0] + 8, p[1]),
                2
            )

            pygame.draw.line(
                self.screen,
                (0, 255, 0),
                (p[0], p[1] - 8),
                (p[0], p[1] + 8),
                2
            )

        # ------------------------------------------
        # Polígono
        # ------------------------------------------

        if len(self.points) > 1:

            pygame.draw.lines(

                self.screen,

                (0, 150, 255),

                False,

                [
                    self.image_to_screen(p)
                    for p in self.points
                ],

                2

            )

            mouse = self.screen_to_image(
                pygame.mouse.get_pos()
            )

            pygame.draw.line(

                self.screen,

                (0, 150, 255),

                self.image_to_screen(
                    self.points[-1]
                ),

                self.image_to_screen(
                    mouse
                ),

                1

            )
        
                # ------------------------------------------
        # Cerrar polígono
        # ------------------------------------------

        if len(self.points) > 2:

            pygame.draw.line(

                self.screen,

                (0, 150, 255),

                self.image_to_screen(
                    self.points[-1]
                ),

                self.image_to_screen(
                    self.points[0]
                ),

                2

            )

        # ------------------------------------------
        # Dibujar vértices
        # ------------------------------------------

        for point in self.points:

            pygame.draw.circle(

                self.screen,

                (255, 0, 0),

                self.image_to_screen(point),

                self.radius

            )

        # ------------------------------------------
        # Ayuda
        # ------------------------------------------

        text = self.font.render(

            "1º click: origen | Click: punto | Arrastrar: mover | "
            "Backspace: último | Supr: borrar | C: limpiar | "
            "Enter: exportar | Esc: salir",

            True,

            (255, 255, 255)

        )

        self.screen.blit(
            text,
            (5, 5)
        )

        pygame.display.flip()

    # ==========================================================

    def run(self):

        clock = pygame.time.Clock()

        while True:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    return
                
                # ----------------------------------
                
                if event.type == pygame.VIDEORESIZE:

                    self.screen = pygame.display.set_mode(
                        event.size,
                        pygame.RESIZABLE
                    )

                    self.calculate_viewport()

                    continue

                # ----------------------------------

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        return

                    elif event.key == pygame.K_RETURN:

                        if self.origin:
                            self.export()

                    elif event.key == pygame.K_BACKSPACE:

                        if self.points:
                            self.points.pop()

                    elif event.key == pygame.K_DELETE:

                        mouse = self.screen_to_image(
                            pygame.mouse.get_pos()
                        )

                        index = self.point_at(mouse)

                        if index is not None:
                            self.points.pop(index)

                    elif event.key == pygame.K_c:

                        self.origin = None
                        self.points.clear()

                # ----------------------------------

                elif (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 1
                ):

                    pos = self.screen_to_image(
                        event.pos
                    )

                    if self.origin is None:

                        self.origin = pos

                    else:

                        index = self.point_at(pos)

                        if index is None:

                            self.points.append(pos)

                        else:

                            self.drag = index

                # ----------------------------------

                elif (
                    event.type == pygame.MOUSEBUTTONUP
                    and event.button == 1
                ):

                    self.drag = None

                # ----------------------------------

                elif (
                    event.type == pygame.MOUSEMOTION
                    and self.drag is not None
                ):

                    self.points[self.drag] = (
                        self.screen_to_image(
                            event.pos
                        )
                    )

            self.draw()

            clock.tick(60)


# ==========================================================
# Main
# ==========================================================

def main():

    if len(sys.argv) != 2:

        print()
        print("Uso:")
        print()
        print(
            "python collision_editor.py "
            "data/memories/memory_01"
        )
        print()

        sys.exit(1)

    memory_path = Path(sys.argv[1])

    rooms_file = memory_path / "rooms.json"

    if not rooms_file.exists():

        print(f"No existe: {rooms_file}")
        sys.exit(1)

    with open(rooms_file, "r", encoding="utf8") as f:
        rooms = json.load(f)

    room_list = list(rooms.items())

    print()
    print("Habitaciones disponibles")
    print("-" * 40)

    for i, (room_id, room) in enumerate(room_list, start=1):

        print(f"{i}. {room_id}")

    print()

    while True:

        try:

            option = int(input("Selecciona una habitación: "))

            if 1 <= option <= len(room_list):
                break

        except ValueError:
            pass

        print("Opción no válida.")

    room_id, room = room_list[option - 1]

    background = room["background"]

    Editor(
        memory_path,
        background
    ).run()


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()