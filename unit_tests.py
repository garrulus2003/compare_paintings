from compare_images import *
from image_traits import *

import unittest
import os.path

hashes = ['0101000011000101100100110111100111100100110111111110001110011000',
          '0010010000000100011110001010111001011101100111101110011101101101',
          '1100110011111100010000100001101011011000110100001110011001100001',
          '0101111010010001111010100110000101010000100101001111100011100000',
          '0110101111101101100010011111011101000110110001110001010010101110',
          '1110101011100101100011011011110001101011010111001001010000011001',
          '1010001011111101001100111111000001110000111001100001101101110000',
          '0101110100011110111000000101011101111001010001010001110000011110',
          '0011010100110100010101011110111010111101111111111111010100011000',
          '0111011110011111010011110110010010100000100000101110010011000011']

compare_hashes = [[0, 33, 32, 29, 30, 30, 29, 38, 27, 32],
                  [33, 0, 27, 32, 37, 33, 36, 37, 22, 35],
                  [32, 27, 0, 27, 38, 32, 31, 34, 35, 30],
                  [29, 32, 27, 0, 33, 37, 30, 31, 40, 25],
                  [30, 37, 38, 33, 0, 24, 29, 28, 37, 32],
                  [30, 33, 32, 37, 24, 0, 31, 34, 31, 36],
                  [29, 36, 31, 30, 29, 31, 0, 37, 34, 35],
                  [38, 37, 34, 31, 28, 34, 37, 0, 31, 36],
                  [27, 22, 35, 40, 37, 31, 34, 31, 0, 31],
                  [32, 35, 30, 25, 32, 36, 35, 36, 31, 0]]

test_link = "https://lenta.ru/"


class TestStringMethods(unittest.TestCase):

    def test_get_hash_normal(self):
        get_image_hash("test_elephant1.jpg")
        get_image_hash("test_elephant2.jpg")
        get_image_hash("test_goose1.jpg")
        get_image_hash("test_goose2.jpg")

    def test_get_hash_type(self):
        self.assertEqual(type(get_image_hash("test_elephant1.jpg")), str)

    def test_get_hash_length(self):
        self.assertEqual(len(get_image_hash("test_elephant1.jpg")), 64)

    def test_compare_hash_easy(self):
        compare_matrix = [list(map(lambda x: compare_hash(x, hash_), hashes))
                          for hash_ in hashes]
        self.assertEqual(compare_matrix, compare_hashes)

    def test_compare_hash_hard(self):
        hash1 = get_image_hash("test_elephant1.jpg")
        hash2 = get_image_hash("test_elephant2.jpg")
        hash3 = get_image_hash("test_goose1.jpg")
        hash4 = get_image_hash("test_goose2.jpg")
        elephant = compare_hash(hash1, hash2) < compare_hash(hash1, hash3)
        goose = compare_hash(hash3, hash4) < compare_hash(hash2, hash4)
        self.assertTrue(elephant and goose)

    def test_download_photo(self):
        content = urllib.request.urlopen(test_link).read()
        img_urls = re.findall('img .*?src="(.*?)"', str(content))
        links = []
        for img in img_urls:
            if img.endswith(".jpg"):
                resource = urllib.request.urlopen(img)
                download_photo(resource.read(), "test_file.jpg")
                break
        self.assertTrue((os.path.exists("test_file.jpg")))

    def test_get_paintings(self):
        self.assertEqual(len(get_paintings(test_link)), 15)


if __name__ == '__main__':
    unittest.main()
