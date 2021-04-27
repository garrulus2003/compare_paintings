import cv2


def get_image_hash(file):
    """
    hashes the image
    :param file: jpg file
    :return:
    """
    image = cv2.imread(file)
    resized = cv2.resize(image, (8, 8), interpolation=cv2.INTER_AREA)
    gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    avg = gray_image.mean()
    ret, threshold_image = cv2.threshold(gray_image, avg, 255, 0)

    _hash = ""
    for x in range(8):
        for y in range(8):
            val = threshold_image[x, y]
            _hash += "1" if val == 255 else "0"
    return _hash


def compare_hash(hash1, hash2):
    """
    finds difference between hashes
    :param hash1: str
    :param hash2: str
    :return:
    """
    current_element = 0
    difference = 0
    while current_element < len(hash1):
        difference += 1 if hash1[current_element] != hash2[current_element] else 0
        current_element += 1
    return difference
