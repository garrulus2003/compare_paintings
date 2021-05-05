from tkinter import *
import json
import re
import urllib.request
from PIL import Image, ImageTk
from compare_images import get_image_hash, compare_hash
from image_traits import post_photo, get_paintings, download_photo, find_similar


def download_list(source_list, target_file):
    """
    downloads all images from the list, does not break in case of exception
    :param source_list: list of jpg files
    :param target_file: a string able to format
    :return:
    """
    for i in range(len(source_list)):
        try:
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


if __name__ == '__main__':
    artists_links = open("artists_links.json", 'r')
    root = Tk()
    root.title("Поиск похожих картин.")
    root.geometry("800x500")

    artist1 = StringVar(root)
    artist1.set("       Выберите художника")
    artist2 = StringVar(root)
    artist2.set("       Выберите художника")
    artists = json.load(artists_links)

    def find_similar_clicked():
        find_similar(get_paintings(artists[artist1.get()]), get_paintings(artists[artist2.get()]), root)


    lbl = Label(text="Многие художники одного времени придерживаются одного стиля.")
    lbl1 = Label(text="В этом можно убедиться на примере художников первой половины XX века.")
    lbl2 = Label(text="Несмотря на то, что искусство этого времени отличается своим разнообразием,")
    lbl3 = Label(text="Вы увидете некоторое сходство.")
    btn = Button(text="Найти похожие картины", command=find_similar_clicked)

    choose1 = OptionMenu(root, artist1, *list(artists))
    choose2 = OptionMenu(root, artist2, *list(artists))
    choose1.config(width=50, height=0)
    choose2.config(width=50, height=0)

    graphic_elements = [choose1, choose2, btn, lbl, lbl1, lbl2, lbl3]
    for element in graphic_elements:
        element.pack()

    root.mainloop()
