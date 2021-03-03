import cv2


def get_image_dimensions(image_path):
    """Gets an image's dimensions from a file path

    Args:
        image_path (str): file path

    Returns:
        tuple: a tuple of form image_width, image_height
    """
    img = cv2.imread(image_path)
    img_height, img_width = img.shape[:2]
    return img_width, img_height
