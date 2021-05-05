from compare_images import *
from image_traits import *

import unittest


class TestStringMethods(unittest.TestCase):

    def test_get_hash(self):
        self.assertEqual(type(get_image_hash("test_elephant1.jpg")), str)

    def test_compare_hash(self):
        hash1 = get_image_hash("test_elephant1.jpg")
        hash2 = get_image_hash("test_elephant2.jpg")
        hash3 = get_image_hash("test_goose1.jpg")
        hash4 = get_image_hash("test_goose2.jpg")

        elephant = compare_hash(hash1, hash2) < compare_hash(hash1, hash3)
        goose = compare_hash(hash3, hash4) < compare_hash(hash2, hash4)
        self.assertTrue(elephant and goose)

    def test_get_paintings(self):
        test_link = "https://allpainters.ru/serov-valentin-01.html"
        self.assertEqual(len(get_paintings(test_link)), 15)


if __name__ == '__main__':
    unittest.main()
