import arcade
from colors import *
from pyglet.graphics import Batch

WIDTH = 800
HEIGHT = 600
CAMERA_WIDTH = 50
CAMERA_HEIGHT = 30
CAMERA_BORDER = 2


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
        correct_x = self.left <= x <= self.left + self.width
        correct_y = self.bottom <= y <= self.bottom + self.height

        return correct_x and correct_y


class Camera(Button):
    def __init__(self, left, bottom, bg_color, text, batch, image_path):
        super().__init__(left, bottom, CAMERA_WIDTH, CAMERA_HEIGHT, color)

        self.text = arcade.Text(text, left + 7, bottom + 7, WHITE,
                                font_size=15, anchor_x='left', batch=batch)
        self.bg_color = bg_color
        self.image_path = image_path

    def draw(self):
        arcade.draw_lbwh_rectangle_filled(self.left, self.bottom, self.width,
                                          self.height, self.bg_color)
        arcade.draw_lbwh_rectangle_outline(self.left - 1, self.bottom - 1,
                                           self.width + 2, self.height + 2,
                                           WHITE, CAMERA_BORDER)

    def set_background_color(self, color):
        self.bg_color = color


class CamerasView(arcade.View):
    def __init__(self, old_view):
        super().__init__()
        self.old_view = old_view
        self.background_color = BLACK
        self.batch = Batch()

    def setup(self):
        self.cameras = {
            '1A': Camera(WIDTH - 200, 200, GRAY, '1A', self.batch,
                         'images/Dining-Hall-Empty.png'),
            '1B': Camera(WIDTH - 220, 150, GRAY, '1B', self.batch,
                         'Stage_Bonnie_Chica_Freddy.png')
        }
        self.camera = '1A'
        self.cameras_buttom = Button(WIDTH - 300, 20, 280, 20, WHITE)

        self.camera_view = arcade.Sprite(self.cameras[self.camera].image_path)
        self.camera_view.center_x = WIDTH // 2
        self.camera_view.center_y = HEIGHT // 2
        self.camera_view_list = arcade.SpriteList()
        self.camera_view_list.append(self.camera_view)

    def on_draw(self):
        self.clear()

        self.camera_view_list.draw()

        for camera in self.cameras:
            self.cameras[camera].draw()
        self.batch.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        pressed_on_camera_button = self.cameras_buttom.check_mouse_press(x, y)

        if pressed_on_camera_button:
            self.window.show_view(self.old_view)

        for camera in self.cameras.values():
            pressed_on_camera = camera.check_mouse_press(x, y)
            camera.set_background_color(GREEN if pressed_on_camera else GRAY)


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
