import os
import cv2
import tqdm
import numpy as np
from frame_area import FrameArea
from pathlib import Path
from typing import Tuple


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
                raise ValueError(f"The value must be in the range from 0 to {max_frames}.")
            return frames_to_skip
        except ValueError:
            raise ValueError("The value you entered could not be converted to a number. Please enter a valid number.")

def get_screen_resolution() -> Tuple[int, int]:
    """
    Get the screen resolution from user input.

    Returns:
        Tuple[int, int]: A tuple containing the width and height of the screen.

    Raises:
        ValueError: If the input resolution is less than or equal to 640 for width
                     or height or if the input format is incorrect.
    """
    resolution = input("Enter the resolution of your screen in the format WxH, for example, 1920x1080: ").lower().strip()
    width = int(resolution.split('x')[0])
    height = int(resolution.split('x')[1])
    if width <= 640:
        raise ValueError("The width value must be greater than 640.")
    if height <= 640:
        raise ValueError("The height value must be greater than 640.")
    return width, height


def draw_grid(new_frame: np.ndarray, position: FrameArea, color=(0, 255, 0), thickness: int = 1, k: float = 1.0):
    """
    Draw a grid on the provided frame.

    Args:
        new_frame (np.ndarray): The frame on which to draw the grid.
        position (Position): The Position object containing grid parameters.
        color (tuple): Color of the grid lines in BGR format (default is green).
        thickness (int): Thickness of the grid lines (default is 1).
        k (float): Scaling factor for the grid size (default is 1.0).
    """
    for i in range(position.divider + 1):  # +1 for the boundary
        y = int(position.y * k + position.y_step * k * i)
        cv2.line(new_frame,
                 (int(position.x * k), y),
                 (int(position.x * k + position.width * k), y),
                 color, thickness)

    for i in range(position.divider + 1):  # +1 for the boundary
        x = int(position.x * k + position.x_step * k * i)
        cv2.line(new_frame,
                 (x, int(position.y * k)),
                 (x, int(position.y * k + position.height * k)), color, thickness)

    cv2.rectangle(new_frame,
                  (int(position.x * k), int(position.y * k)),
                  (int(position.x * k + position.width * k),
                   int(position.y * k + position.height * k)), color, thickness + 1)

def zoom_image(image: np.ndarray, x: int, y: int, width: int, height: int, factor: float) -> np.ndarray:
    """
    Zoom into a specified area of the image by the given factor.

    Args:
        image (np.ndarray): The original image.
        x (int): X-coordinate of the top-left corner of the area.
        y (int): Y-coordinate of the top-left corner of the area.
        width (int): Width of the area.
        height (int): Height of the area.
        factor (float): Zoom factor (e.g., 2.0 for double size).

    Returns:
        np.ndarray: The zoomed image.

    Raises:
        ValueError: If the specified area exceeds the image boundaries.
    """

    # Crop the specified area
    cropped = image[y:y + height, x:x + width]

    # Check if the cropped area is valid
    if cropped.size == 0:
        raise ValueError("The specified area exceeds the image boundaries.")

    return cv2.resize(cropped, None, fx=factor, fy=factor, interpolation=cv2.INTER_LINEAR)

def crop_image_to_screen_size(frame: np.ndarray, to_width: int, to_height: int) -> Tuple[np.ndarray, int, int]:
    """
    Crop the image to fit within the specified width and height.

    Args:
        frame (np.ndarray): The original image frame.
        to_width (int): The target width.
        to_height (int): The target height.

    Returns:
        Tuple[np.ndarray, int, int]: The resized image and its new dimensions (height, width).
    """
    if frame.shape[1] > to_width:
        frame = cv2.resize(frame,
                           (to_width, int(frame.shape[0] * to_width / frame.shape[1])),
                           interpolation=cv2.INTER_LINEAR)

    if frame.shape[0] > to_height:
        frame = cv2.resize(frame,
                           (int(frame.shape[1] * to_height / frame.shape[0]), to_height),
                           interpolation=cv2.INTER_LINEAR)
    return frame, frame.shape[0], frame.shape[1]


area = FrameArea(divider=3)
area.height = 640
area.width = 640
is_zoom = False

video_path = get_video_path()
folder = get_folder_to_save()
screen_width, screen_height = get_screen_resolution()

cap = cv2.VideoCapture(video_path)
name = Path(video_path).name
frames_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
skip = get_count_to_skip(max_frames=frames_count)
with tqdm.tqdm(total=frames_count) as pbar:
    while cap.isOpened():
        ret, frame = cap.read()

        sub_frame, height, width = crop_image_to_screen_size(frame=frame.copy(),
                                                             to_width=screen_width,
                                                             to_height=screen_height)

        if skip > 0:
            skip -= 1
            test = f"frame {pbar.n} of {frames_count}: {name}"
            cv2.putText(sub_frame, test, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(sub_frame, 'SKIPPING', (int(width / 2) - len('SKIPPING') * 15, int(height / 2)),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)

            cv2.imshow('frame', sub_frame)
            if cv2.waitKey(1) == ord('q'):
                break
            pbar.update(1)
            continue

        next_frame_flag = False
        while not next_frame_flag:
            new_frame = sub_frame.copy()
            draw_grid(new_frame, area, thickness=1 + int(max(width, height) / 1000), k=width/frame.shape[1])
            test = f"frame {pbar.n} of {frames_count}: {name}"
            cv2.putText(new_frame, test, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv2.imshow('frame', new_frame)

            if is_zoom:
                zoomed = zoom_image(image=frame, x=area.x, y=area.y, width=area.width, height=area.height, factor=3)
                test = f"frame {pbar.n} of {frames_count}: {name}"
                cv2.putText(zoomed, test, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.imshow('zoomed_area', zoomed)
            else:
                try:
                    cv2.destroyWindow('zoomed_area')
                except:
                    pass

            key = cv2.waitKey(0)
            match key:
                case _ if key == ord('a'):
                    area.x = max(0, area.x - area.x_step)
                case _ if key == ord('d'):
                    area.x = min(frame.shape[1] - area.width, area.x + area.x_step)
                case _ if key == ord('w'):
                    area.y = max(0, area.y - area.y_step)
                case _ if key == ord('s'):
                    area.y = min(frame.shape[0] - area.height, area.y + area.y_step)
                case _ if key == ord('k'):
                    cropped_image = frame[area.y: area.y + area.height, area.x: area.x + area.width]
                    cv2.imwrite(f"{name.split(' ')[0]}_{pbar.n}.png", cropped_image)
                case _ if key == ord('z'):
                    is_zoom = not is_zoom
                case _ if key == ord(' '):
                    next_frame_flag = True
                case _ if key == ord('q'):
                    exit()
        pbar.update(1)
cap.release()
cv2.destroyAllWindows()
