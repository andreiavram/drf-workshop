import mock
import string
from unittest import TestCase

from PIL import Image

from work.tasks import get_picture_average_color


class TestWorkUnitTestCase(TestCase):

    def test_get_picture_average_color_returns_hex_color_code(self):
        with mock.patch('work.tasks.download_image') as download_image_mock:
            image_object = Image.open('work/tests/test_image.png')

            # Mock download_image to return a default image
            download_image_mock.return_value = image_object

            color_code = get_picture_average_color('https://i.imgur.com/KOi8eXo.png')

            # Color code is a string
            self.assertIsInstance(color_code, str)

            # Color code starts with a #
            self.assertTrue(color_code.startswith('#'))

            # Color code has length 7, e.g. #2D5817
            self.assertEqual(len(color_code), 7)

            # Color code has only letters, numbers and the character #
            self.assertEqual(
                set(color_code) - set(string.ascii_letters + string.digits + '#'),
                set()
            )
