import unittest
from unittest import mock
from ddt import ddt, data, unpack
from making_YOLO_dataset import FrameArea, get_video_path, get_folder_to_save, \
    get_screen_resolution  # Импортируйте ваши функции и классы


@ddt
class TestPosition(unittest.TestCase):

    @data((640, 480), (800, 600), (1024, 768))
    @unpack
    def test_calculate_center(self, width, height):
        area = FrameArea()
        area.update_position(10, 20, width, height)
        center_x, center_y = area.get_center()
        self.assertEqual(center_x, 10 + width // 2)
        self.assertEqual(center_y, 20 + height // 2)

    @data(-1.0, "1", None, [], ["hi"], (), ("hi",), set(), {"hi"}, 1 + 2j, b"",
          b"hi", bytearray(b""), bytearray(b"hi"), range(0), )
    def test_x_setter_type_error(self, value):
        area = FrameArea()
        with self.assertRaises(TypeError):
            area.x = value

    @data(-1.0, "1", None, [], ["hi"], (), ("hi",), set(), {"hi"}, 1 + 2j, b"",
          b"hi", bytearray(b""), bytearray(b"hi"), range(0), )
    def test_x_setter_type_error(self, value):
        area = FrameArea()
        with self.assertRaises(TypeError):
            area.y = value

    @data(-1.0, "1", None, [], ["hi"], (), ("hi",), set(), {"hi"}, 1 + 2j, b"",
          b"hi", bytearray(b""), bytearray(b"hi"), range(0), )
    def test_width_setter_type_error(self, value):
        area = FrameArea()
        with self.assertRaises(TypeError):
            area.width = "string"

    @data(-1.0, "1", None, [], ["hi"], (), ("hi",), set(), {"hi"}, 1 + 2j, b"",
          b"hi", bytearray(b""), bytearray(b"hi"), range(0), )
    def test_width_setter_type_error(self, value):
        area = FrameArea()
        with self.assertRaises(TypeError):
            area.height = value

    @data(
        (5, 10, 100, 200),      # Обычные значения
        (0, 0, 0, 0),          # Нулевые размеры
        (1_000_000, 1_000_000, 1_000_000, 1_000_000)  # Большие значения
    )
    @unpack
    def test_update_position(self, x, y, width, height):
        area = FrameArea()
        area.update_position(x, y, width, height)
        self.assertEqual(area.x, x)
        self.assertEqual(area.y, y)
        self.assertEqual(area.width, width)
        self.assertEqual(area.height, height)


@ddt
class TestInputFunctions(unittest.TestCase):
    @data("invalid_path.mp4", "non_existing_folder")
    def test_get_video_path_invalid(self, video_path):
        with unittest.mock.patch('builtins.input', return_value=video_path):
            with self.assertRaises(Exception):
                get_video_path()

    @data("invalid_folder", "non_existing_path")
    def test_get_folder_to_save_invalid(self, folder_path):
        with unittest.mock.patch('builtins.input', return_value=folder_path):
            with self.assertRaises(Exception):
                get_folder_to_save()

    @data("800x641", "1920x1080")
    def test_get_screen_resolution_valid(self, screen_res):
        with unittest.mock.patch('builtins.input', return_value=screen_res):
            width, height = get_screen_resolution()
            self.assertGreater(width, 640)
            self.assertGreater(height, 640)

    def test_get_screen_resolution_invalid(self):
        with unittest.mock.patch('builtins.input', return_value="500x500"):
            with self.assertRaises(ValueError):
                get_screen_resolution()


