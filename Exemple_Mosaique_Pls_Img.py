from PIL import Image
from PIL import ImageOps
from tqdm import tqdm
from glob import glob
import random
import argparse


parser = argparse.ArgumentParser()
parser.add_argument( '--doss')
parser.add_argument('--img')
argsdeouf = parser.parse_args()
nom_grande_image = argsdeouf.img
nom_images = argsdeouf.doss


#############  Récupérer les images et leur donner une bonne taille  ###########

## On récupère le nom de l'image à faire et on l'ouvre
grande_image = Image.open(nom_grande_image).convert('RGBA')
## On récupère le nom de l'image à utiliser et on l'ouvre
ttes_images = glob(nom_images+"/*")
# on définit un tableau pour nos images
ttes_petites_images = []
for nom_petite_image in ttes_images:
    petite_image = Image.open(nom_petite_image).convert('RGBA')
    ttes_petites_images.append(petite_image)
print(ttes_petites_images)
print(ttes_petites_images[0])

## On recup la largeur et la hauteur de la grande image
# et on la resize en plus petit
W,H = grande_image.size
W /= 2
H /= 2
W = int(W)
H = int(H)
print(W)
print(H)
grande_image = grande_image.resize((W,H))

## On donne une taille fixe à la petite image : 50 par 50
w = 50
h = 50

########################  Créer la mosaique   ##################################

## On récupère la couleur de chaque pixel de la grande image à réaliser
print("On récupère les pixels ->")
pixel_valeur = list(grande_image.getdata())

## on crée une nouvelle image
image_finale = Image.new('RGBA', (w*W,h*H),(255,255,255,0))
print("Nouvelle image créée !")


## On ajoute les petites images à l'image finale
## Et on lui donne la bonne teinte
print("On remplit la nouvelle image ->")


## On parcourt la grande image, ligne par ligne
for y in tqdm(range(0,H,1)):

    for x in range(0,W,1):
        try :
            indice_tableau = y*W + x
            # on définit nos variables pour la position de la petite image
            position_x_gauche = x*w
            position_y_haut = y*h
            position_x_droit = position_x_gauche + w
            position_y_bas = position_y_haut + h
            # On crée une nouvelle image de la taille de la petite image
            # et de la couleur du pixel de la grande image
            filtre_couleur = Image.new('RGBA', (w,h),pixel_valeur[indice_tableau])
            petite_image = random.choice(ttes_petites_images)
            petite_image = petite_image.resize((w,h))
            # On mixe notre petite image avec l'image de la bonne couleur
            petite_image_filtre = Image.blend(petite_image,filtre_couleur,0.5)
            # On ajoute notre petite image de la bonne couleur à l'image finale
            # au bon emplacement
            image_finale.paste(petite_image_filtre,box=(position_x_gauche, position_y_haut, position_x_droit, position_y_bas))
        except:
            print("Fail au x : " + str(x) + " et y : " + str(y))



## On affiche l'image
image_finale.show()

## on sauvegarde
sauvegarde = input("Sauvegarder ? Oui ou Non. ")
if sauvegarde == "Oui":
    image_finale.save("image_mosaique.png")
