from typing import Tuple


class FrameArea:
    """
    Class to represent the position and dimensions of a rectangular area.

    Attributes:
        divider (int): Number of divisions for the grid.
        x (int): X-coordinate of the top-left corner of the rectangle.
        y (int): Y-coordinate of the top-left corner of the rectangle.
        width (int): Width of the rectangle.
        height (int): Height of the rectangle.
    """

    def __init__(self, divider: int = 1):
        """
        Initializes the FrameArea instance with a given divider.

        Args:
            divider (int): The number of divisions for the grid, default is 1.
        """
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.divider = divider

    @property
    def x(self) -> int:
        """Get the x-coordinate of the rectangle."""
        return self._x

    @x.setter
    def x(self, x: int) -> None:
        """
        Set the x-coordinate of the rectangle.

        Args:
            x (int): The new x-coordinate to set.
        """
        if not isinstance(x, int):
            raise TypeError(f"'x' must be 'int', but got {type(x).__name__}")
        if x < 0:
            raise ValueError(f"Field 'x' should be greater than or equal to zero, but got {x}")
        self._x = x

    @property
    def y(self) -> int:
        """Get the y-coordinate of the rectangle."""
        return self._y

    @y.setter
    def y(self, y: int) -> None:
        """
        Set the y-coordinate of the rectangle.

        Args:
            y (int): The new y-coordinate to set.
        """
        if not isinstance(y, int):
            raise TypeError(f"'y' must be 'int', but got {type(y).__name__}")
        if y < 0:
            raise ValueError(f"Field 'y' should be greater than or equal to zero, but got {y}")
        self._y = y

    @property
    def width(self) -> int:
        """Get the width of the rectangle."""
        return self._width

    @width.setter
    def width(self, width: int) -> None:
        """
        Set the width of the rectangle.

        Args:
            width (int): The new width to set.
        """
        if not isinstance(width, int):
            raise TypeError(f"'width' must be 'int', but got {type(width).__name__}")
        if width < 0:
            raise ValueError(f"Field 'width' should be greater than or equal to zero, but got {width}")
        self._width = width

    @property
    def height(self) -> int:
        """Get the height of the rectangle."""
        return self._height

    @height.setter
    def height(self, height: int) -> None:
        """
        Set the height of the rectangle.

        Args:
            height (int): The new height to set.
        """
        if not isinstance(height, int):
            raise TypeError(f"'height' must be 'int', but got {type(height).__name__}")
        if height < 0:
            raise ValueError(f"Field 'height' should be greater than or equal to zero, but got {height}")
        self._height = height

    @property
    def divider(self) -> int:
        """Get the number of divisions for the grid."""
        return self._divider

    @divider.setter
    def divider(self, divider: int) -> None:
        """
        Set the number of divisions for the grid.

        Args:
            divider (int): The new number of divisions to set.
        """
        if not isinstance(divider, int):
            raise TypeError(f"'divider' must be 'int', but got {type(divider).__name__}")
        if divider < 0:
            raise ValueError(f"Field 'divider' should be greater than or equal to zero, but got {divider}")
        self._divider = divider

    @property
    def x_step(self) -> int:
        """Calculate the step size for the x-axis based on width and divider."""
        return int(self.width / self.divider)

    @property
    def y_step(self) -> int:
        """Calculate the step size for the y-axis based on height and divider."""
        return int(self.height / self.divider)

    def get_center(self) -> Tuple[int, int]:
        """
        Calculate the center point of the rectangle.

        Returns:
            Tuple[int, int]: The x and y coordinates of the center point.
        """
        return self.x + self.width // 2, self.y + self.height // 2

    def update_position(self, x: int, y: int, width: int, height: int) -> None:
        """
        Update the position's attributes.

        Args:
            x (int): The new x-coordinate.
            y (int): The new y-coordinate.
            width (int): The new width.
            height (int): The new height.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
