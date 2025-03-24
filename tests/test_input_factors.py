# import unittest
# from ddt import ddt, data, unpack
# from making_YOLO_dataset import  get_video_path, get_folder_to_save, \
#     get_screen_resolution
#
#
# @ddt
# class TestInputFunctions(unittest.TestCase):
#     @data("invalid_path.mp4", "non_existing_folder")
#     def test_get_video_path_invalid(self, video_path):
#         with unittest.mock.patch('builtins.input', return_value=video_path):
#             with self.assertRaises(Exception):
#                 get_video_path()
#
#     @data("invalid_folder", "non_existing_path")
#     def test_get_folder_to_save_invalid(self, folder_path):
#         with unittest.mock.patch('builtins.input', return_value=folder_path):
#             with self.assertRaises(Exception):
#                 get_folder_to_save()
#
#     @data("800x641", "1920x1080")
#     def test_get_screen_resolution_valid(self, screen_res):
#         with unittest.mock.patch('builtins.input', return_value=screen_res):
#             width, height = get_screen_resolution()
#             self.assertGreater(width, 640)
#             self.assertGreater(height, 640)
#
#     def test_get_screen_resolution_invalid(self):
#         with unittest.mock.patch('builtins.input', return_value="500x500"):
#             with self.assertRaises(ValueError):
#                 get_screen_resolution()
