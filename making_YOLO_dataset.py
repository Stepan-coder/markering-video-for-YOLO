import os
import cv2
import tqdm
import numpy as np
from pathlib import Path


class Position:
    """
    Class to represent the position and dimensions of a rectangular area.

    Attributes:
        devider (int): Number of divisions for the grid.
        x (int): X-coordinate of the top-left corner of the rectangle.
        y (int): Y-coordinate of the top-left corner of the rectangle.
        width (int): Width of the rectangle.
        height (int): Height of the rectangle.
    """

    def __init__(self, devider: int = 1):
        """
        Initializes the Position with a given divider.

        Args:
            devider (int): The number of divisions for the grid, default is 1.
        """
        self._devider = devider
        self._x = 0
        self._y = 0
        self._width = 0
        self._height = 0

    @property
    def devider(self) -> int:
        """Return the number of divisions."""
        return self._devider

    @property
    def x_step(self) -> int:
        """Return the step size for the x-axis based on width and devider."""
        return int(self._width / self._devider)

    @property
    def y_step(self) -> int:
        """Return the step size for the y-axis based on height and devider."""
        return int(self._height / self._devider)

    @property
    def x(self) -> int:
        """Return the x-coordinate."""
        return self._x

    @x.setter
    def x(self, x: int) -> None:
        """
        Set the x-coordinate.

        Args:
            x (int): The x-coordinate to set.

        Raises:
            TypeError: If x is not an integer.
        """
        if not isinstance(x, int):
            raise TypeError(f"'x' must be 'int', but got {type(x).__name__}")
        self._x = x

    @property
    def y(self) -> int:
        """Return the y-coordinate."""
        return self._y

    @y.setter
    def y(self, y: int) -> None:
        """
        Set the y-coordinate.

        Args:
            y (int): The y-coordinate to set.

        Raises:
            TypeError: If y is not an integer.
        """
        if not isinstance(y, int):
            raise TypeError(f"'y' must be 'int', but got {type(y).__name__}")
        self._y = y

    @property
    def width(self) -> int:
        """Return the width of the rectangle."""
        return self._width

    @width.setter
    def width(self, width: int) -> None:
        """
        Set the width of the rectangle.

        Args:
            width (int): The width to set.

        Raises:
            TypeError: If width is not an integer.
        """
        if not isinstance(width, int):
            raise TypeError(f"'width' must be 'int', but got {type(width).__name__}")
        self._width = width

    @property
    def height(self) -> int:
        """Return the height of the rectangle."""
        return self._height

    @height.setter
    def height(self, height: int) -> None:
        """
        Set the height of the rectangle.

        Args:
            height (int): The height to set.

        Raises:
            TypeError: If height is not an integer.
        """
        if not isinstance(height, int):
            raise TypeError(f"'height' must be 'int', but got {type(height).__name__}")
        self._height = height

def get_video_path() -> os.PathLike:
    """
    Prompt the user for a video file path until a valid one is provided.

    Returns:
        os.PathLike: The valid video file path.

    Raises:
        Exception: If the path is incorrect or not a file.
    """
    while True:
        video_name = input("Please specify the full path to the video you want to annotate: ").strip()

        if not os.path.exists(video_name):
            raise Exception("Path is incorrect!")

        if not os.path.isfile(video_name):
            raise Exception("Path is not a file!")

        return video_name

def get_folder_to_save() -> os.PathLike:
    """
    Prompt the user for a folder path until a valid one is provided.

    Returns:
        os.PathLike: The valid folder path.

    Raises:
        Exception: If the path is incorrect or not a directory.
    """
    while True:
        save_folder = input("Please specify the full path to the folder where images should be saved: ").strip()

        if not os.path.exists(save_folder):
            raise Exception("Path is incorrect!")

        if not os.path.isdir(save_folder):
            raise Exception("Path is not a directory!")

        return save_folder

def get_count_to_skip(max_frames: int) -> int:
    """
    Prompt the user for the number of frames to skip until a valid one is provided.

    Args:
        max_frames (int): The maximum number of frames that can be skipped.

    Returns:
        int: The number of frames to skip.

    Raises:
        Exception: If the value cannot be converted to a number or is out of range.
    """
    while True:
        try:
            frames_to_skip = int(input("How many frames to skip (0 to {}): ".format(max_frames)).strip())
            if not (0 <= frames_to_skip <= max_frames):
                raise Exception(f"The value must be in the range from 0 to {max_frames}.")
            return frames_to_skip
        except ValueError:
            raise Exception("The value you entered could not be converted to a number. Please enter a valid number.")

def draw_grid(new_frame, position: Position, color=(0, 255, 0), thickness=1):
    """
    Draw a grid on the provided frame.

    Args:
        new_frame: The frame on which to draw the grid.
        position (Position): The Position object containing grid parameters.
        color (tuple): Color of the grid lines in BGR format (default green).
        thickness (int): Thickness of the grid lines (default is 1).
    """
    for i in range(position.devider + 1):  # +1 for the boundary
        y = position.y + position.y_step * i
        cv2.line(new_frame, (position.x, y), (position.x + position.width, y), color, thickness)

    for i in range(position.devider + 1):  # +1 for the boundary
        x = position.x + position.x_step * i
        cv2.line(new_frame, (x, position.y), (x, position.y + position.height), color, thickness)

    cv2.rectangle(new_frame,
                  (position.x, position.y),
                  (position.x + position.width, position.y + position.height), color, thickness + 1)

def zoom_image(image: np.ndarray, x: int, y: int, width: int, height: int, factor: float) -> np.ndarray:
    """
    Zooms into a specified area of the image by the given factor.

    Args:
        image (np.ndarray): The original image.
        x (int): X-coordinate of the top-left corner of the area.
        y (int): Y-coordinate of the top-left corner of the area.
        width (int): Width of the area.
        height (int): Height of the area.
        factor (float): Zoom factor (e.g., 2.0 for double size).

    Returns:
        np.ndarray: The zoomed image.
    """

    # Crop the specified area
    cropped = image[y:y + height, x:x + width]

    # Check if the cropped area is valid
    if cropped.size == 0:
        raise ValueError("The specified area exceeds the image boundaries.")

    return cv2.resize(cropped, None, fx=factor, fy=factor, interpolation=cv2.INTER_LINEAR)


video_path = get_video_path()
folder = get_folder_to_save()

name = Path(video_path).name

cap = cv2.VideoCapture(video_path)
frames_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
skip = get_count_to_skip(max_frames=frames_count)

# Инициализация позиции
pos = Position(3)
pos.height = 640
pos.width = 640
is_zoom = False
with tqdm.tqdm(total=frames_count) as pbar:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        height, width = frame.shape[:2]

        if skip > 0:
            skip -= 1
            test = f"frame {pbar.n} of {frames_count}: {name}"
            cv2.putText(frame, test, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(frame, 'SKIPPING', (int(width / 2) - len('SKIPPING') * 15, int(height / 2)),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)

            cv2.imshow('frame', frame)
            if cv2.waitKey(1) == ord('q'):
                break
            pbar.update(1)
            continue

        next_frame_flag = False
        while not next_frame_flag:
            new_frame = frame.copy()
            draw_grid(new_frame, pos, thickness=1 + int(max(width, height) / 1000))
            test = f"frame {pbar.n} of {frames_count}: {name}"
            cv2.putText(new_frame, test, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv2.imshow('frame', new_frame)

            if is_zoom:
                zoomed = zoom_image(image=frame, x=pos.x, y=pos.y, width=pos.width, height=pos.height, factor=3)
                test = f"frame {pbar.n} of {frames_count}: {name}"
                cv2.putText(zoomed, test, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.imshow('zoomed_area', zoomed)
            else:
                cv2.destroyWindow('zoomed_area')

            key = cv2.waitKey(0)
            match key:
                case _ if key == ord('a'):
                    pos.x = max(0, pos.x - pos.x_step)
                case _ if key == ord('d'):
                    pos.x = min(width - pos.width, pos.x + pos.x_step)
                case _ if key == ord('w'):
                    pos.y = max(0, pos.y - pos.y_step)
                case _ if key == ord('s'):
                    pos.y = min(height - pos.height, pos.y + pos.y_step)
                case _ if key == ord('k'):
                    cropped_image = frame[pos.y: pos.y + pos.height, pos.x: pos.x + pos.width]
                    # cv2.imshow('croped', cropped_image)
                    cv2.imwrite(os.path.join(folder, f"{name.split(' ')[0]}_{pbar.n}.png"), cropped_image)
                case _ if key == ord('z'):
                    is_zoom = not is_zoom
                case _ if key == ord(' '):
                    next_frame_flag = True
                case _ if key == ord('q'):
                    exit()
        pbar.update(1)
cap.release()
cv2.destroyAllWindows()


# /Users/stepanborodin/Desktop/Projects/Yan/YanDrone/pythonProject/videos/IMG_8444.MOV
# /Users/stepanborodin/Desktop/Projects/Yan/YanDrone/pythonProject/drones