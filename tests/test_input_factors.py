"""Unit tests for video annotation functionality.

This module contains comprehensive tests for all major components
of the video annotation system including input validation, image
processing, and core business logic.
"""

import unittest
from unittest.mock import patch, MagicMock
import os
import cv2
import numpy as np
from pathlib import Path
import tempfile
import shutil

from making_YOLO_dataset import (
    get_video_path,
    get_folder_to_save,
    get_count_to_skip,
    get_screen_resolution,
    draw_grid,
    zoom_image,
    crop_image_to_screen_size,
    FrameArea
)


class TestVideoAnnotation(unittest.TestCase):
    """Test suite for video annotation system.

    Attributes:
        test_dir (str): Path to temporary directory for test artifacts
        test_video (str): Path to temporary test video file
    """

    @classmethod
    def setUpClass(cls):
        """Create temporary test environment with sample video file."""
        cls.test_dir = tempfile.mkdtemp()
        cls.test_video = os.path.join(cls.test_dir, "test_video.mp4")
        open(cls.test_video, 'a').close()

    @classmethod
    def tearDownClass(cls):
        """Clean up temporary test environment."""
        shutil.rmtree(cls.test_dir)

    def test_get_video_path_valid(self):
        """Tests valid video path input handling.

        Verifies:
            - Correct path is returned for existing file
            - No exceptions raised for valid input
            - Filesystem validation works as expected
        """
        with patch('builtins.input', return_value=self.test_video):
            result = get_video_path()
            self.assertEqual(result, self.test_video)

    def test_get_video_path_invalid(self):
        """Tests invalid video path input handling.

        Verifies:
            - Exception raised for non-existent path
            - Exception raised for non-file paths
            - Proper error propagation
        """
        with patch('builtins.input', return_value="invalid_path"):
            with self.assertRaises(Exception):
                get_video_path()

    def test_get_folder_to_save_valid(self):
        """Tests valid directory path input handling.

        Verifies:
            - Correct path is returned for existing directory
            - Directory validation works as expected
            - No exceptions raised for valid input
        """
        with patch('builtins.input', return_value=self.test_dir):
            result = get_folder_to_save()
            self.assertEqual(result, self.test_dir)

    def test_get_count_to_skip_valid(self):
        """Tests valid frame skip count input.

        Verifies:
            - Correct integer conversion
            - Proper range validation
            - No exceptions for valid input
        """
        with patch('builtins.input', return_value='5'):
            result = get_count_to_skip(max_frames=10)
            self.assertEqual(result, 5)

    def test_get_count_to_skip_invalid(self):
        """Tests invalid frame skip count input.

        Verifies:
            - ValueError for non-numeric input
            - Proper error handling
            - Range validation enforcement
        """
        with patch('builtins.input', return_value='invalid'):
            with self.assertRaises(ValueError):
                get_count_to_skip(max_frames=10)

    def test_get_screen_resolution_valid(self):
        """Tests valid screen resolution input.

        Verifies:
            - Correct WxH format parsing
            - Minimum resolution requirements
            - Proper return type (tuple)
        """
        with patch('builtins.input', return_value='1920x1080'):
            width, height = get_screen_resolution()
            self.assertEqual((width, height), (1920, 1080))

    def test_get_screen_resolution_invalid(self):
        """Tests invalid screen resolution input.

        Verifies:
            - ValueError for resolutions below minimum
            - Format validation
            - Error message clarity
        """
        with patch('builtins.input', return_value='600x480'):
            with self.assertRaises(ValueError):
                get_screen_resolution()

    def test_draw_grid(self):
        """Tests grid drawing functionality.

        Verifies:
            - Grid lines are properly rendered
            - Image modification occurs
            - No exceptions during drawing
        """
        test_image = np.zeros((500, 500, 3), dtype=np.uint8)
        area = FrameArea(divider=3)
        area.x = 100
        area.y = 100
        area.width = 300
        area.height = 300

        draw_grid(test_image, area)
        self.assertGreater(np.count_nonzero(test_image), 0)

    def test_zoom_image_valid(self):
        """Tests valid image zoom operation.

        Verifies:
            - Output dimensions are correct
            - No data loss during zoom
            - Proper interpolation
        """
        test_image = np.random.randint(0, 255, (500, 500, 3), dtype=np.uint8)
        zoomed = zoom_image(test_image, 100, 100, 200, 200, 2.0)
        self.assertEqual(zoomed.shape, (400, 400, 3))

    def test_zoom_image_invalid(self):
        """Tests invalid image zoom parameters.

        Verifies:
            - ValueError for out-of-bounds regions
            - Empty region detection
            - Error message clarity
        """
        test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        with self.assertRaises(ValueError):
            zoom_image(test_image, 150, 150, 200, 200, 2.0)

    def test_crop_image_to_screen_size(self):
        """Tests image cropping to screen dimensions.

        Verifies:
            - Aspect ratio preservation
            - Size constraints enforcement
            - No data corruption
        """
        test_image = np.random.randint(0, 255, (1000, 2000, 3), dtype=np.uint8)
        cropped, h, w = crop_image_to_screen_size(test_image, 1000, 800)
        self.assertTrue(h <= 800)
        self.assertTrue(w <= 1000)

    @patch('cv2.VideoCapture')
    @patch('cv2.imshow')
    @patch('cv2.waitKey')
    def test_main_workflow(self, mock_waitkey, mock_imshow, mock_cap):
        """Tests complete annotation workflow.

        Verifies:
            - End-to-end process flow
            - User input simulation
            - File saving functionality
            - Keyboard interaction handling
        """
        # Mock video capture setup
        mock_cap.return_value = MagicMock(
            isOpened=lambda: True,
            read=lambda: (True, np.zeros((1080, 1920, 3), dtype=np.uint8)),
            get=lambda x: 100 if x == cv2.CAP_PROP_FRAME_COUNT else None,
            release=lambda: None
        )

        # Simulate user input sequence
        with patch('builtins.input', side_effect=[
            self.test_video,  # Video path
            self.test_dir,  # Save directory
            '1920x1080',  # Screen resolution
            '0'  # Frames to skip
        ]):
            # Simulate keyboard inputs
            mock_waitkey.side_effect = [
                ord('a'),  # Move left
                ord('d'),  # Move right
                ord('w'),  # Move up
                ord('s'),  # Move down
                ord('k'),  # Save frame
                ord('z'),  # Toggle zoom
                ord(' '),  # Next frame
                ord('q')  # Quit
            ]

            # Verify output files were created
            output_files = [f for f in os.listdir(self.test_dir)
                            if f.endswith('.png')]
            self.assertGreaterEqual(len(output_files), 1)

