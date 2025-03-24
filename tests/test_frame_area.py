import unittest
from ddt import ddt, data, unpack
from frame_area import FrameArea
from typing import Any, List, Dict

@ddt
class TestPosition(unittest.TestCase):


    # X_VALUE
    @data(-1.0, "1", None, [], ["hi"], (), ("hi",), set(), {"hi"}, 1 + 2j, b"",
          b"hi", bytearray(b""), bytearray(b"hi"), range(0))
    def test_frame_area_x_setter_wrong_type(self, value: Any):
        area = FrameArea()
        with self.assertRaises(TypeError):
            area.x = value

    @data(-1, -5, -10, -50, -100, -500, -1_000, -5_000, -10_000, -50_000, -100_000, -500_000, -1_000_000)
    def test_frame_area_x_setter_wrong_value(self, value: int):
        area = FrameArea()
        with self.assertRaises(ValueError):
            area.x = value

    @data(0, 1, 5, 10, 50, 100, 500, 1_000, 5_000, 10_000, 50_000, 100_000, 500_000, 1_000_000)
    def test_frame_area_x_setter_success(self, value: int):
        area = FrameArea()
        area.x = value
        self.assertIsInstance(area.x, int)
        self.assertEqual(area.x, value)


    # Y_VALUE
    @data(-1.0, "1", None, [], ["hi"], (), ("hi",), set(), {"hi"}, 1 + 2j, b"",
          b"hi", bytearray(b""), bytearray(b"hi"), range(0))
    def test_frame_area_y_setter_wrong_type(self, value: Any):
        area = FrameArea()
        with self.assertRaises(TypeError):
            area.y = value

    @data(-1, -5, -10, -50, -100, -500, -1_000, -5_000, -10_000, -50_000, -100_000, -500_000, -1_000_000)
    def test_frame_area_y_setter_wrong_value(self, value: int):
        area = FrameArea()
        with self.assertRaises(ValueError):
            area.y = value

    @data(0, 1, 5, 10, 50, 100, 500, 1_000, 5_000, 10_000, 50_000, 100_000, 500_000, 1_000_000)
    def test_frame_area_y_setter_success(self, value: int):
        area = FrameArea()
        area.y = value
        self.assertIsInstance(area.y, int)
        self.assertEqual(area.y, value)


    # WIDTH
    @data(-1.0, "1", None, [], ["hi"], (), ("hi",), set(), {"hi"}, 1 + 2j, b"",
          b"hi", bytearray(b""), bytearray(b"hi"), range(0))
    def test_frame_area_width_setter_wrong_type(self, value: Any):
        area = FrameArea()
        with self.assertRaises(TypeError):
            area.width = value

    @data(-1, -5, -10, -50, -100, -500, -1_000, -5_000, -10_000, -50_000, -100_000, -500_000, -1_000_000)
    def test_frame_area_width_setter_wrong_value(self, value: int):
        area = FrameArea()
        with self.assertRaises(ValueError):
            area.width = value

    @data(0, 1, 5, 10, 50, 100, 500, 1_000, 5_000, 10_000, 50_000, 100_000, 500_000, 1_000_000)
    def test_frame_area_width_setter_success(self, value: int):
        area = FrameArea()
        area.width = value
        self.assertIsInstance(area.width, int)
        self.assertEqual(area.width, value)

    #HEIGHT
    @data(-1.0, "1", None, [], ["hi"], (), ("hi",), set(), {"hi"}, 1 + 2j, b"",
          b"hi", bytearray(b""), bytearray(b"hi"), range(0))
    def test_frame_area_height_setter_wrong_type(self, value: Any):
        area = FrameArea()
        with self.assertRaises(TypeError):
            area.height = value

    @data(-1, -5, -10, -50, -100, -500, -1_000, -5_000, -10_000, -50_000, -100_000, -500_000, -1_000_000)
    def test_frame_area_height_setter_wrong_value(self, value: int):
        area = FrameArea()
        with self.assertRaises(ValueError):
            area.height = value

    @data(0, 1, 5, 10, 50, 100, 500, 1_000, 5_000, 10_000, 50_000, 100_000, 500_000, 1_000_000)
    def test_frame_area_height_setter_success(self, value: int):
        area = FrameArea()
        area.height = value
        self.assertIsInstance(area.height, int)
        self.assertEqual(area.height, value)

    # DIVIDER
    @data(-1.0, "1", None, [], ["hi"], (), ("hi",), set(), {"hi"}, 1 + 2j, b"",
          b"hi", bytearray(b""), bytearray(b"hi"), range(0))
    def test_frame_area_divider_setter_wrong_type(self, value: Any):
        area = FrameArea()
        with self.assertRaises(TypeError):
            area.divider = value

    @data(-1, -5, -10, -50, -100, -500, -1_000, -5_000, -10_000, -50_000, -100_000, -500_000, -1_000_000)
    def test_frame_area_divider_setter_wrong_value(self, value: int):
        area = FrameArea()
        with self.assertRaises(ValueError):
            area.divider = value

    @data(0, 1, 5, 10, 50, 100, 500, 1_000, 5_000, 10_000, 50_000, 100_000, 500_000, 1_000_000)
    def test_frame_area_divider_setter_success(self, value: int):
        area = FrameArea()
        area.divider = value
        self.assertIsInstance(area.divider, int)
        self.assertEqual(area.divider, value)

    # X_STEP
    @data((10, 5, 2),
          (100, 50, 10),
          (25, 10, 5),
          (0, 0, 1),
          (10, 5, 0))
    @unpack
    def test_frame_area_x_step_success(self, width: int, height: int, divider: int):
        area = FrameArea(divider=divider)
        area.width = width
        area.height = height
        self.assertEqual(area.x_step, width // divider)

    # X_STEP
    @data((10, 5, 2),
          (100, 50, 10),
          (25, 10, 5),
          (0, 0, 1),
          (10, 5, 0))  # (width, height, divider)
    @unpack
    def test_frame_area_y_step_success(self, width: int, height: int, divider: int):
        area = FrameArea(divider=divider)
        area.width = width
        area.height = height
        self.assertEqual(area.y_step, height // divider)

    # GET_CENTER
    @data(
        (0, 0, 0, 0), # center (0, 0)
        (0, 0, 10, 20),        # center (5, 10)
        (10, 10, 0, 0),       # center (10, 10)
        (100, 100, 50, 50),   # center (125, 125)
        (300, 200, 100, 50),   # center (350, 225)
        (50, 75, 30, 30))      # center (65, 90)

    @unpack
    def test_frame_area_get_center_success(self, x: int, y: int, width: int, height: int):
        area = FrameArea()
        area.update_position(x, y, width, height)
        center_x, center_y = area.get_center()
        self.assertEqual(center_x, x + width // 2)
        self.assertEqual(center_y, y + height // 2)

    # UPDATE_POSITION
    @data(
        (0, 0, 0, 0),  # Нулевые размеры
        (10, 20, 30, 40),      # Обычные значения
        (15, 25, 100, 200),    # Разные размеры
        (5, 10, 300, 400),      # Дефицит размера
        (1_000_000, 1_000_000, 1_000_000, 1_000_000))  # Максимальные значения
    @unpack
    def test_frame_area_update_position_success(self, x: int, y: int, width: int, height: int):
        area = FrameArea()
        area.update_position(x, y, width, height)
        self.assertEqual(area.x, x)
        self.assertEqual(area.y, y)
        self.assertEqual(area.width, width)
        self.assertEqual(area.height, height)



