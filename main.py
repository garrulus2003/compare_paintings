from tkinter import *
import json
import re
import urllib.request
from PIL import Image, ImageTk
from compare_images import get_image_hash, compare_hash

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


    def get_paintings(painter):
        """

        :param painter: str in list artists
        :return: list of links to paintings of this artist
        """
        url = artists[painter]
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
                download_photo(source_list[i].read(), target_file.format(i))
            except:
                pass


    def post_photo(image, x, y):
        """
        posts the image to the root? putting it to a square with left horizontal coordinate x,
        upper vertical y
        :param image: jpg file
        :param x: int
        :param y: int
        :return:
        """
        load = Image.open(image)
        render = ImageTk.PhotoImage(load)
        img = Label(root, image=render)
        img.image = render
        img.place(x=x, y=y)

    def find_similar():
        """
        searches for the smallest hash difference and post less different photos
        :return:
        """
        list1 = get_paintings(artist1.get())
        list2 = get_paintings(artist2.get())
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

        post_photo("img1_{}.jpg".format(i_min), 30, 200)
        post_photo("img2_{}.jpg".format(j_min), 430, 200)


    lbl = Label(text="Многие художники одного времени придерживаются одного стиля.")
    lbl1 = Label(text="В этом можно убедиться на примере художников первой половины XX века.")
    lbl2 = Label(text="Несмотря на то, что искусство этого времени отличается своим разнообразием,")
    lbl3 = Label(text="Вы увидете некоторое сходство.")
    btn = Button(text="Найти похожие картины", command=find_similar)
    choose1 = OptionMenu(root, artist1, *list(artists))
    choose2 = OptionMenu(root, artist2, *list(artists))
    choose1.config(width=50, height=0)
    choose2.config(width=50, height=0)

    graphic_elements = [choose1, choose2, btn, lbl, lbl1, lbl2, lbl3]
    for element in graphic_elements:
        element.pack()

    root.mainloop()
