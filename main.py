from tkinter import *
import json
import re
import urllib.request
from PIL import Image, ImageTk
from compare_images import get_image_hash, compare_hash


f = open("artists_links.json", 'r')
root = Tk()
root.title("Поиск похожих картин.")
root.geometry("800x500")
variable = StringVar(root)
variable.set("       Выберите художника")
variable1 = StringVar(root)
variable1.set("       Выберите художника")
A = json.load(f)


def get_paintings(painter):
    url = A[painter]
    content = urllib.request.urlopen(url).read()
    imgUrls = re.findall('img .*?src="(.*?)"', str(content))
    answer = []
    for img in imgUrls:
        if img.endswith(".jpg"):
            try:
                resource = urllib.request.urlopen(img)
                answer.append(resource)
                print(1)
            except Exception as e:
                print(e)
        if len(answer) >= 15:
            break
    return answer


def find_similar():
    list1 = get_paintings(variable.get())
    list2 = get_paintings(variable1.get())

    for i in range(len(list1)):
        try:
            f1 = open("img1_{}.jpg".format(i), 'wb')
            f1.write(list1[i].read())
            f1.close()
        except:
            print(1)

    for i in range(len(list2)):
        try:
            f2 = open("img2_{}.jpg".format(i), 'wb')
            f2.write(list2[i].read())
            f2.close()
        except:
            print(1)

    B = []
    i_min = 0
    j_min = 0
    min_value = 100
    for i in range(len(list1)):
        B.append([])
        for j in range(len(list2)):
            B[i].append(compare_hash(get_image_hash("img1_{}.jpg".format(i)), get_image_hash("img2_{}.jpg".format(j))))
            if B[i][j] < min_value:
                i_min = i
                j_min = j
                min_value = B[i][j]

    print(i_min, j_min)
    load = Image.open("img1_{}.jpg".format(i_min))
    render = ImageTk.PhotoImage(load)
    img = Label(root, image=render)
    img.image = render
    img.place(x=30, y=200)

    load1 = Image.open("img2_{}.jpg".format(j_min))
    render1 = ImageTk.PhotoImage(load1)
    img1 = Label(root, image=render1)
    img1.image = render1
    img1.place(x=430, y=200)


lbl = Label(text="Многие художники одного времени придерживаются одного стиля.")
lbl1 = Label(text="В этом можно убедиться на примере художников первой половины XX века.")
lbl2 = Label(text="Несмотря на то, что искусство этого времени отличается своим разнообразием,")
lbl3 = Label(text="Вы увидете некоторое сходство.")
btn = Button(text="Найти похожие картины", command=find_similar)
w = OptionMenu(root, variable, *list(A))
u = OptionMenu(root, variable1, *list(A))


w.config(width=50, height=0)
u.config(width=50, height=0)

w.pack()
u.pack()

btn.pack()
lbl.pack()
lbl1.pack()
lbl2.pack()
lbl3.pack()

root.mainloop()