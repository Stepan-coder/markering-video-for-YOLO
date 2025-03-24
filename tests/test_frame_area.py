import unittest
from ddt import ddt, data, unpack
from frame_area import FrameArea
from typing import Any, List, Dict

@ddt
class TestPosition(unittest.TestCase):
    """
    Unit tests for the FrameArea class, covering initialization, setters,
    step calculations, center calculations, and position updates.
    """

    @data(
        (0, 0, 0, 0, 1),  # Default values
        (0, 0, 0, 0, 0),  # Divider = 0
        (0, 0, 10, 20, 1),  # Standard rectangle
        (5, 5, 100, 200, 2),  # Positive values
        (10, 15, 300, 400, 10),  # Larger area
        (0, 0, 1_000_000, 1_000_000, 1),  # Maximum values
        (0, 0, 10, 15, -1),  # Negative divider (should raise exception)
        (-5, -5, 10, 20, 1),  # Negative x and y (should raise exception)
        (5, 10, -1, -1, 1),  # Negative width and height (should raise exception)
        (0, 0, 0, -5, 1)  # Negative height (should raise exception)
    )
    @unpack
    def test_initialization(self, x: int, y: int, width: int, height: int, divider: int):
        """
        Test the initialization of the FrameArea class with various parameters.

        Args:
            x (int): The x-coordinate of the rectangle.
            y (int): The y-coordinate of the rectangle.
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            divider (int): The number of divisions for the grid.

        Raises:
            ValueError: If divider is negative or zero, or if width, height, x, or y are negative.
        """
        if divider < 0:
            with self.assertRaises(ValueError):
                FrameArea(divider=divider)
        else:
            area = FrameArea(divider=divider)
            area.x = x
            area.y = y
            area.width = width
            area.height = height

            # Validate object's state after initialization
            self.assertEqual(area.x, x)
            self.assertEqual(area.y, y)
            self.assertEqual(area.width, width)
            self.assertEqual(area.height, height)
            self.assertEqual(area.divider, divider)

    # Tests for x setter
    @data(-1.0, "1", None, [], ["hi"], (), ("hi",), set(), {"hi"}, 1 + 2j, b"",
          b"hi", bytearray(b""), bytearray(b"hi"), range(0))
    def test_frame_area_x_setter_wrong_type(self, value: Any):
        """
        Test the x setter for incorrect types.

        Args:
            value (Any): The value to be set as the x-coordinate.

        Raises:
            TypeError: If the value is not an integer.
        """
        area = FrameArea()
        with self.assertRaises(TypeError):
            area.x = value

    @data(-1, -5, -10, -50, -100, -500, -1_000, -5_000, -10_000, -50_000, -100_000, -500_000, -1_000_000)
    def test_frame_area_x_setter_wrong_value(self, value: int):
        """
        Test the x setter for negative values.

        Args:
            value (int): The value to be set as the x-coordinate.

        Raises:
            ValueError: If the value is negative.
        """
        area = FrameArea()
        with self.assertRaises(ValueError):
            area.x = value

    @data(0, 1, 5, 10, 50, 100, 500, 1_000, 5_000, 10_000, 50_000, 100_000, 500_000, 1_000_000)
    def test_frame_area_x_setter_success(self, value: int):
        """
        Test the x setter for valid positive values.

        Args:
            value (int): The value to be set as the x-coordinate.
        """
        area = FrameArea()
        area.x = value
        self.assertIsInstance(area.x, int)
        self.assertEqual(area.x, value)

    # Tests for y setter
    @data(-1.0, "1", None, [], ["hi"], (), ("hi",), set(), {"hi"}, 1 + 2j, b"",
          b"hi", bytearray(b""), bytearray(b"hi"), range(0))
    def test_frame_area_y_setter_wrong_type(self, value: Any):
        """
        Test the y setter for incorrect types.

        Args:
            value (Any): The value to be set as the y-coordinate.

        Raises:
            TypeError: If the value is not an integer.
        """
        area = FrameArea()
        with self.assertRaises(TypeError):
            area.y = value

    @data(-1, -5, -10, -50, -100, -500, -1_000, -5_000, -10_000, -50_000, -100_000, -500_000, -1_000_000)
    def test_frame_area_y_setter_wrong_value(self, value: int):
        """
        Test the y setter for negative values.

        Args:
            value (int): The value to be set as the y-coordinate.

        Raises:
            ValueError: If the value is negative.
        """
        area = FrameArea()
        with self.assertRaises(ValueError):
            area.y = value

    @data(0, 1, 5, 10, 50, 100, 500, 1_000, 5_000, 10_000, 50_000, 100_000, 500_000, 1_000_000)
    def test_frame_area_y_setter_success(self, value: int):
        """
        Test the y setter for valid positive values.

        Args:
            value (int): The value to be set as the y-coordinate.
        """
        area = FrameArea()
        area.y = value
        self.assertIsInstance(area.y, int)
        self.assertEqual(area.y, value)

    # Tests for width setter
    @data(-1.0, "1", None, [], ["hi"], (), ("hi",), set(), {"hi"}, 1 + 2j, b"",
          b"hi", bytearray(b""), bytearray(b"hi"), range(0))
    def test_frame_area_width_setter_wrong_type(self, value: Any):
        """
        Test the width setter for incorrect types.

        Args:
            value (Any): The value to be set as the width of the rectangle.

        Raises:
            TypeError: If the value is not an integer.
        """
        area = FrameArea()
        with self.assertRaises(TypeError):
            area.width = value

    @data(-1, -5, -10, -50, -100, -500, -1_000, -5_000, -10_000, -50_000, -100_000, -500_000, -1_000_000)
    def test_frame_area_width_setter_wrong_value(self, value: int):
        """
        Test the width setter for negative values.

        Args:
            value (int): The value to be set as the width of the rectangle.

        Raises:
            ValueError: If the value is negative.
        """
        area = FrameArea()
        with self.assertRaises(ValueError):
            area.width = value

    @data(0, 1, 5, 10, 50, 100, 500, 1_000, 5_000, 10_000, 50_000, 100_000, 500_000, 1_000_000)
    def test_frame_area_width_setter_success(self, value: int):
        """
        Test the width setter for valid positive values.

        Args:
            value (int): The value to be set as the width of the rectangle.
        """
        area = FrameArea()
        area.width = value
        self.assertIsInstance(area.width, int)
        self.assertEqual(area.width, value)

    # Tests for height setter
    @data(-1.0, "1", None, [], ["hi"], (), ("hi",), set(), {"hi"}, 1 + 2j, b"",
          b"hi", bytearray(b""), bytearray(b"hi"), range(0))
    def test_frame_area_height_setter_wrong_type(self, value: Any):
        """
        Test the height setter for incorrect types.

        Args:
            value (Any): The value to be set as the height of the rectangle.

        Raises:
            TypeError: If the value is not an integer.
        """
        area = FrameArea()
        with self.assertRaises(TypeError):
            area.height = value

    @data(-1, -5, -10, -50, -100, -500, -1_000, -5_000, -10_000, -50_000, -100_000, -500_000, -1_000_000)
    def test_frame_area_height_setter_wrong_value(self, value: int):
        """
        Test the height setter for negative values.

        Args:
            value (int): The value to be set as the height of the rectangle.

        Raises:
            ValueError: If the value is negative.
        """
        area = FrameArea()
        with self.assertRaises(ValueError):
            area.height = value

    @data(0, 1, 5, 10, 50, 100, 500, 1_000, 5_000, 10_000, 50_000, 100_000, 500_000, 1_000_000)
    def test_frame_area_height_setter_success(self, value: int):
        """
        Test the height setter for valid positive values.

        Args:
            value (int): The value to be set as the height of the rectangle.
        """
        area = FrameArea()
        area.height = value
        self.assertIsInstance(area.height, int)
        self.assertEqual(area.height, value)

    # Tests for divider setter
    @data(-1.0, "1", None, [], ["hi"], (), ("hi",), set(), {"hi"}, 1 + 2j, b"",
          b"hi", bytearray(b""), bytearray(b"hi"), range(0))
    def test_frame_area_divider_setter_wrong_type(self, value: Any):
        """
        Test the divider setter for incorrect types.

        Args:
            value (Any): The value to be set as the divider for the grid.

        Raises:
            TypeError: If the value is not an integer.
        """
        area = FrameArea()
        with self.assertRaises(TypeError):
            area.divider = value

    @data(-1, -5, -10, -50, -100, -500, -1_000, -5_000, -10_000, -50_000, -100_000, -500_000, -1_000_000)
    def test_frame_area_divider_setter_wrong_value(self, value: int):
        """
        Test the divider setter for negative values.

        Args:
            value (int): The value to be set as the divider for the grid.

        Raises:
            ValueError: If the value is negative.
        """
        area = FrameArea()
        with self.assertRaises(ValueError):
            area.divider = value

    @data(0, 1, 5, 10, 50, 100, 500, 1_000, 5_000, 10_000, 50_000, 100_000, 500_000, 1_000_000)
    def test_frame_area_divider_setter_success(self, value: int):
        """
        Test the divider setter for valid positive values.

        Args:
            value (int): The value to be set as the divider for the grid.
        """
        area = FrameArea()
        area.divider = value
        self.assertIsInstance(area.divider, int)
        self.assertEqual(area.divider, value)

    # Tests for x_step calculation
    @data((10, 5, 2),
          (100, 50, 10),
          (25, 10, 5),
          (0, 0, 1),
          (10, 5, 0))  # (width, height, divider)
    @unpack
    def test_frame_area_x_step_success(self, width: int, height: int, divider: int):
        """
        Test the calculation of the x-axis step size.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            divider (int): The number of divisions for the grid.

        Ensures that the calculation of the x-axis step size is correct.
        """
        area = FrameArea(divider=divider)
        area.width = width
        area.height = height
        self.assertEqual(area.x_step, width // divider)

    # Tests for y_step calculation
    @data((10, 5, 2),
          (100, 50, 10),
          (25, 10, 5),
          (0, 0, 1),
          (10, 5, 0))  # (width, height, divider)
    @unpack
    def test_frame_area_y_step_success(self, width: int, height: int, divider: int):
        """
        Test the calculation of the y-axis step size.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            divider (int): The number of divisions for the grid.

        Ensures that the calculation of the y-axis step size is correct.
        """
        area = FrameArea(divider=divider)
        area.width = width
        area.height = height
        self.assertEqual(area.y_step, height // divider)

    # Tests for center calculation
    @data(
        (0, 0, 0, 0), # center (0, 0)
        (0, 0, 10, 20),        # center (5, 10)
        (10, 10, 0, 0),       # center (10, 10)
        (100, 100, 50, 50),   # center (125, 125)
        (300, 200, 100, 50),  # center (350, 225)
        (50, 75, 30, 30)      # center (65, 90)
    )
    @unpack
    def test_frame_area_get_center_success(self, x: int, y: int, width: int, height: int):
        """
        Test the calculation of the center point of the rectangle.

        Args:
            x (int): The x-coordinate of the rectangle.
            y (int): The y-coordinate of the rectangle.
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.

        Ensures that the center point calculation returns the expected results.
        """
        area = FrameArea()
        area.update_position(x, y, width, height)
        center_x, center_y = area.get_center()
        self.assertEqual(center_x, x + width // 2)
        self.assertEqual(center_y, y + height // 2)

    # Tests for position update
    @data(
        (0, 0, 0, 0),  # Zero sizes
        (10, 20, 30, 40),      # Standard values
        (15, 25, 100, 200),    # Different sizes
        (5, 10, 300, 400),     # Large sizes
        (1_000_000, 1_000_000, 1_000_000, 1_000_000))  # Maximum values
    @unpack
    def test_frame_area_update_position_success(self, x: int, y: int, width: int, height: int):
        """
        Test the update of the rectangle's position and size.

        Args:
            x (int): The new x-coordinate.
            y (int): The new y-coordinate.
            width (int): The new width.
            height (int): The new height.

        Ensures that the position and size are updated correctly.
        """
        area = FrameArea()
        area.update_position(x, y, width, height)
        self.assertEqual(area.x, x)
        self.assertEqual(area.y, y)
        self.assertEqual(area.width, width)
        self.assertEqual(area.height, height)


