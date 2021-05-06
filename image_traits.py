from tkinter import *
import json
import re
import urllib.request
from PIL import Image, ImageTk
from compare_images import get_image_hash, compare_hash


def post_photo(image, x, y, screen):
    """
    posts the image to the root? putting it to a square with left horizontal coordinate x,
    upper vertical y

    :param screen: tkinter root
    :param image: jpg file
    :param x: int
    :param y: int
    :return:
    """
    load = Image.open(image)
    render = ImageTk.PhotoImage(load)
    img = Label(screen, image=render)
    img.image = render
    img.place(x=x, y=y)


def get_paintings(url):
    """

    :param url: url for the page where paintings are stored
    """
    content = urllib.request.urlopen(url).read()
    img_urls = re.findall('img .*?src="(.*?)"', str(content))
    links = []
    for img in img_urls:
        if img.endswith(".jpg"):
            try:
                resource = urllib.request.urlopen(img)
                links.append(resource)
            except:
                pass
        if len(links) >= 15:
            break
    return links


def download_photo(source_file, target_file):
    """
    downloads a photo from source_file to target_file
    :param source_file: binary read file
    :param target_file: file.jpg
    :return:
    """
    file = open(target_file, 'wb')
    file.write(source_file)
    file.close()


def download_list(source_list, target_file):
    """
    downloads all images from the list, does not break in case of exception
    :param source_list: list of jpg files
    :param target_file: a string able to format
    :return:
    """
    for i in range(len(source_list)):
        try:
            print(source_list[i].read())
            download_photo(source_list[i].read(), target_file.format(i))
        except:
            pass


def find_similar(list1, list2, screen):
    """
    posts two most similar photos
    :param screen: tkinter root
    :param list1: list of links to images
    :param list2: list of links to images
    :return:
    """
    download_list(list1, "img1_{}.jpg")
    download_list(list2, "img2_{}.jpg")

    compare_matrix = [[0]*len(list2)]*len(list1)
    i_min = 0
    j_min = 0
    min_value = 100
    for i in range(len(list1)):
        for j in range(len(list2)):
            compare_matrix[i][j] = compare_hash(get_image_hash("img1_{}.jpg".format(i)),
                                                get_image_hash("img2_{}.jpg".format(j)))
            if compare_matrix[i][j] < min_value:
                i_min = i
                j_min = j
                min_value = compare_matrix[i][j]

    post_photo("img1_{}.jpg".format(i_min), 30, 200, screen)
    post_photo("img2_{}.jpg".format(j_min), 430, 200, screen)
