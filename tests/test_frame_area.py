import unittest
from ddt import ddt, data, unpack
from frame_area import FrameArea


@ddt
class TestPosition(unittest.TestCase):


    # X_VALUE
    @data(-1.0, "1", None, [], ["hi"], (), ("hi",), set(), {"hi"}, 1 + 2j, b"",
          b"hi", bytearray(b""), bytearray(b"hi"), range(0))
    def test_frame_area_x_setter_wrong_type(self, value):
        area = FrameArea()
        with self.assertRaises(TypeError):
            area.x = value

    @data(-1, -5, -10, -50, -100, -500, -1_000, -5_000, -10_000, -50_000, -100_000, -500_000, -1_000_000)
    def test_frame_area_x_setter_wrong_value(self, value):
        area = FrameArea()
        with self.assertRaises(ValueError):
            area.x = value

    @data(0, 1, 5, 10, 50, 100, 500, 1_000, 5_000, 10_000, 50_000, 100_000, 500_000, 1_000_000)
    def test_frame_area_x_setter_success(self, value):
        area = FrameArea()
        area.x = value
        self.assertIsInstance(area.x, int)
        self.assertEqual(area.x, value)


    # Y_VALUE
    @data(-1.0, "1", None, [], ["hi"], (), ("hi",), set(), {"hi"}, 1 + 2j, b"",
          b"hi", bytearray(b""), bytearray(b"hi"), range(0))
    def test_frame_area_y_setter_wrong_type(self, value):
        area = FrameArea()
        with self.assertRaises(TypeError):
            area.y = value

    @data(-1, -5, -10, -50, -100, -500, -1_000, -5_000, -10_000, -50_000, -100_000, -500_000, -1_000_000)
    def test_frame_area_y_setter_wrong_value(self, value):
        area = FrameArea()
        with self.assertRaises(ValueError):
            area.y = value

    @data(0, 1, 5, 10, 50, 100, 500, 1_000, 5_000, 10_000, 50_000, 100_000, 500_000, 1_000_000)
    def test_frame_area_y_setter_success(self, value):
        area = FrameArea()
        area.y = value
        self.assertIsInstance(area.y, int)
        self.assertEqual(area.y, value)


    # WIDTH
    @data(-1.0, "1", None, [], ["hi"], (), ("hi",), set(), {"hi"}, 1 + 2j, b"",
          b"hi", bytearray(b""), bytearray(b"hi"), range(0))
    def test_frame_area_width_setter_wrong_type(self, value):
        area = FrameArea()
        with self.assertRaises(TypeError):
            area.width = value

    @data(-1, -5, -10, -50, -100, -500, -1_000, -5_000, -10_000, -50_000, -100_000, -500_000, -1_000_000)
    def test_frame_area_width_setter_wrong_value(self, value):
        area = FrameArea()
        with self.assertRaises(ValueError):
            area.width = value

    @data(0, 1, 5, 10, 50, 100, 500, 1_000, 5_000, 10_000, 50_000, 100_000, 500_000, 1_000_000)
    def test_frame_area_width_setter_success(self, value):
        area = FrameArea()
        area.width = value
        self.assertIsInstance(area.width, int)
        self.assertEqual(area.width, value)

    #HEIGHT
    @data(-1.0, "1", None, [], ["hi"], (), ("hi",), set(), {"hi"}, 1 + 2j, b"",
          b"hi", bytearray(b""), bytearray(b"hi"), range(0))
    def test_frame_area_height_setter_wrong_type(self, value):
        area = FrameArea()
        with self.assertRaises(TypeError):
            area.height = value

    @data(-1, -5, -10, -50, -100, -500, -1_000, -5_000, -10_000, -50_000, -100_000, -500_000, -1_000_000)
    def test_frame_area_height_setter_wrong_value(self, value):
        area = FrameArea()
        with self.assertRaises(ValueError):
            area.height = value

    @data(0, 1, 5, 10, 50, 100, 500, 1_000, 5_000, 10_000, 50_000, 100_000, 500_000, 1_000_000)
    def test_frame_area_height_setter_success(self, value):
        area = FrameArea()
        area.height = value
        self.assertIsInstance(area.height, int)
        self.assertEqual(area.height, value)

    # DIVIDER
    @data(-1.0, "1", None, [], ["hi"], (), ("hi",), set(), {"hi"}, 1 + 2j, b"",
          b"hi", bytearray(b""), bytearray(b"hi"), range(0))
    def test_frame_area_divider_setter_wrong_type(self, value):
        area = FrameArea()
        with self.assertRaises(TypeError):
            area.divider = value

    @data(-1, -5, -10, -50, -100, -500, -1_000, -5_000, -10_000, -50_000, -100_000, -500_000, -1_000_000)
    def test_frame_area_divider_setter_wrong_value(self, value):
        area = FrameArea()
        with self.assertRaises(ValueError):
            area.divider = value

    @data(0, 1, 5, 10, 50, 100, 500, 1_000, 5_000, 10_000, 50_000, 100_000, 500_000, 1_000_000)
    def test_frame_area_divider_setter_success(self, value):
        area = FrameArea()
        area.divider = value
        self.assertIsInstance(area.divider, int)
        self.assertEqual(area.divider, value)


    @data(
        (5, 10, 100, 200),      # Обычные значения
        (0, 0, 0, 0),          # Нулевые размеры
        (1_000_000, 1_000_000, 1_000_000, 1_000_000)  # Большие значения
    )
    @unpack
    def test_frame_area_update_position(self, x, y, width, height):
        area = FrameArea()
        area.update_position(x, y, width, height)
        self.assertEqual(area.x, x)
        self.assertEqual(area.y, y)
        self.assertEqual(area.width, width)
        self.assertEqual(area.height, height)

    @data((640, 480), (800, 600), (1024, 768))
    @unpack
    def test_frame_area_calculate_center(self, width, height):
        area = FrameArea()
        area.update_position(10, 20, width, height)
        center_x, center_y = area.get_center()
        self.assertEqual(center_x, 10 + width // 2)
        self.assertEqual(center_y, 20 + height // 2)



