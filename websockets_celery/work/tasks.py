from PIL import Image

from celery import shared_task


def download_image(pic_url):
    """Return the image from pic_url as an image object."""
    raise NotImplementedError


def get_picture_average_color(pic_url):
    """Return the average color computed from all pixels

    Download the image from pic_url, compute the average color and return
    the resulting color as hex.

    :param str pic_url: the URL of an image
    :return str: the average color computed from all pixels, returned as a hex
        color code e.g. '#2D5817'
    """
    raise NotImplementedError
