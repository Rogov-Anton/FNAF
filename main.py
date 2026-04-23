import arcade
from colors import *
from pyglet.graphics import Batch

WIDTH = 800
HEIGHT = 600
CAMERA_WIDTH = 50
CAMERA_HEIGHT = 30


class Button:
    def __init__(self, left, bottom, width, height, color):
        self.left = left
        self.bottom = bottom
        self.width = width
        self.height = height
        self.color = color

    def draw(self):
        arcade.draw_lbwh_rectangle_outline(self.left, self.bottom, self.width,
                                           self.height, self.color)

    def check_mouse_press(self, x: int, y: int) -> bool:
        correctx = self.left <= x <= self.left + self.width
        correcty = self.bottom <= y <= self.bottom + self.height

        return correctx and correcty


class Camera(Button):
    def __init__(self, left, bottom, color, text, batch):
        super().__init__(left, bottom, CAMERA_WIDTH, CAMERA_HEIGHT, color)
        self.text = arcade.Text(text, left + 7, bottom + 7,
                                arcade.color.WHITE, font_size=15,
                                anchor_x='left', batch=batch)

    def draw(self):
        arcade.draw_lbwh_rectangle_outline(self.left, self.bottom, self.width,
                                           self.height, self.color)


class CamerasView(arcade.View):
    def __init__(self, main_view):
        super().__init__()
        self.main_view = main_view
        self.background_color = BLACK
        self.batch = Batch()

    def setup(self):
        self.cameras = {
            '1A': Camera(WIDTH - 200, 200, WHITE, '1A', self.batch),
            '1B': Camera(WIDTH - 220, 150, WHITE, '1B', self.batch)
        }
        self.camera = '1A'

    def on_draw(self):
        self.clear()

        for camera in self.cameras:
            self.cameras[camera].draw()
        self.batch.draw()


class MainView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = BLACK
        self.batch = Batch()

    def setup(self):
        self.energy = 99
        self.energy_timer = 0.0
        self.energy_text = arcade.Text(f'Power left: {self.energy}%',
                                       20, 20, WHITE, font_size=20,
                                       anchor_x='left', batch=self.batch)
        self.cameras_buttom = Button(WIDTH - 300, 20, 280, 20, WHITE)

    def on_update(self, delta_time):
        self.energy_timer += delta_time
        if self.energy_timer >= 6:
            self.energy -= 1
            self.energy_text.text = f'Power left: {self.energy}%'
            self.energy_timer = 0.0

    def on_draw(self):
        self.clear()
        self.batch.draw()

        self.cameras_buttom.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        pressed_on_camera_button = self.cameras_buttom.check_mouse_press(x, y)

        if pressed_on_camera_button:
            cameras_view = CamerasView(self)
            cameras_view.setup()
            self.window.show_view(cameras_view)


if __name__ == '__main__':
    window = arcade.Window(WIDTH, HEIGHT, 'FNAF')

    main_view = MainView()
    main_view.setup()

    window.show_view(main_view)
    arcade.run()
