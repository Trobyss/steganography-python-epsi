from PIL import Image


# Génère une chaîne de 0 et 1 à partir d'une image.
# C'est vraiment une mauvaise idée de faire ça.
def genDataFromImage(image):
    data = ''
    # Extracts pixel
    imgdata = iter(image.getdata())

    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                  imgdata.__next__()[:3] +
                  imgdata.__next__()[:3]]
        # string of binary data
        print(pixels)

        # Parcours des tableaux de 3 trio rgb en entiers, soit taille 9 de 0 à 8
        for i in pixels[:8]:
            print(i)
            data += '{0:08b}'.format(i)
        # binstr = format(ord(i), '08b')
        print(data)
        # Check the eighth pixel reader information
        if (pixels[-1] % 2 != 0):
            return data


# A compléter
def convert_rgb_256_to_bit(data_256):
    bits = ['', '', '']
    i = 0
    for value in data_256:
        bits[i] = '{0:08b}'.format(value)
        i += 1
    return bits


# A compléter
def convert_rgb_bit_to_256(data_bit):
    return []


# Méthode à réaliser
def encode_hidden_into_carrying(img_carrying, img_hidden):
    # indice de parcours u,v dans carrying
    # indice de parcours x,y dans hidden
    img_carrying_data = iter(img_carrying.getdata())
    img_hidden_data = iter(img_hidden.getdata())

    # DEBUT BOUCLE ITERANT SUR PIXELS IMAGE CACHEE
    while (True):
        # Il va falloir controler les tailles dees images pour éviter les out of bound ex
        # pour chaque pixel x,y de l'hidden, récupération de [r,g,b] de x et y en base 256
        pix_hidden = [values_256 for values_256 in img_hidden_data.__next__()[:3]]  # tableau de trois valeurs 256
        pix_hidden_binary = convert_rgb_256_to_bit(pix_hidden)  # tableau de trois valeurs bit format string 10010101

        # Récupération de [r,g,b] de u,v et des 7 suivants en base 256
        # C'est une matrice : en colonne, les rgb, en ligne les 8 pixels sélectionnés
        pix_carrying = [values_256 for values_256 in img_carrying_data.__next__()[:3] +
                        img_carrying_data.__next__()[:3] +
                        img_carrying_data.__next__()[:3] +
                        img_carrying_data.__next__()[:3] +
                        img_carrying_data.__next__()[:3] +
                        img_carrying_data.__next__()[:3] +
                        img_carrying_data.__next__()[:3] +
                        img_carrying_data.__next__()[:3]]
        # transformation de [r,g,b] des 8 pixels en calcant le bit de poids faible sur la valeur binaire associée de x,y

        # Index dans la matrice pix_carrying
        mx = 0  # max 2, trois valeurs rgb pour 8 pixels, taille max 3*8 -1 = 23

        for pix_binary_one_color_as_string in pix_hidden_binary[:]:  # pour chaque couleur
            for character in list(pix_binary_one_color_as_string):  # pour chaque caractere binaire de la couleur
                if character == '0' and pix_carrying[mx] % 2 != 0:
                    pix_carrying[mx] -= 1

                elif character == '1' and pix_carrying[mx] % 2 == 0:
                    if pix_carrying[mx] != 0:
                        pix_carrying[mx] -= 1
                    else:
                        pix_carrying[mx] += 1

                # Iteration dans la matrice actuelle
                if mx < 23:
                    mx += 1

    # FIN BOUCLE ITERANT SUR PIXELS IMAGE CACHEE


# Convert encoding data into 8-bit binary ASCII
def genData(data):
    newd = []

    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd


# Pixels are modified according to the 8-bit binary ASCII
def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):

        # Extracting 3 pixels at a time
        pix = [value for value in imdata.__next__()[:3] +
               imdata.__next__()[:3] +
               imdata.__next__()[:3]]

        # Pixel value should be made odd for 1 and even for 0
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j] % 2 != 0):
                pix[j] -= 1

            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if (pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1
                # pix[j] -= 1

        # Eighth pixel of every set tells whether to stop ot read further.
        # 0 => keep reading / 1 => message is over.
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if (pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1

        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]


def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):

        # Putting modified pixels in the new image
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1


# Encode data into image
def encode_text():
    img = input("Chemin relatif de l'image (.png) : ")
    image = Image.open(img, 'r')

    data = input("Texte à encoder : ")
    if (len(data) == 0):
        raise ValueError('Le texte ne peut être vide')

    newimg = image.copy()
    encode_enc(newimg, data)

    new_img_name = input("Entrer le nom de la nouvelle image (.png) : ")
    newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))


# Decode the data in the image
def decode_text():
    img = input("Chemin relatif de l'image (.png) : ")
    image = Image.open(img, 'r')

    data = ''
    # Extracts pixel
    imgdata = iter(image.getdata())

    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                  imgdata.__next__()[:3] +
                  imgdata.__next__()[:3]]

        # string of binary data
        binstr = ''

        # split by 8 pixel (for ASCII)
        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        data += chr(int(binstr, 2))
        # Check the eighth pixel reader information
        if (pixels[-1] % 2 != 0):
            return data


def encode_image():
    img = input("Chemin relatif de l'image porteuse (.png) : ")
    image_carrying = Image.open(img, 'r')
    img = input("Chemin relatif de l'image cachée (.png) : ")
    image_hidden = Image.open(img, 'r')

    newimg = image_carrying.copy()
    encode_hidden_into_carrying(newimg, image_hidden)

    new_img_name = input("Entrer le nom de la nouvelle image (.png) : ")
    newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))


def decode_image():
    img = input("Chemin relatif de l'image porteuse (.png) : ")
    image_carrying = Image.open(img, 'r')

    data = ''

    newimg = image_carrying.copy()

    new_img_name = input("Entrer le nom de la nouvelle image (.png) : ")
    newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))


def main():
    a = int(input(":: Politique & Sécurité des données ::\n"
                  "1. Encode some text\n2. Decode some test\n"
                  "3. Encode some image\n4. Decode some image\n"))
    if (a == 1):
        encode_text()

    elif (a == 2):
        print("Mots décodés :  " + decode_text())

    if (a == 3):
        encode_image()

    if (a == 4):
        decode_image()

    else:
        raise Exception("Erreur d'entrée")


if __name__ == '__main__':
    # Calling main function
    main()
