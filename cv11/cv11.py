"""
cv10/11 ?
"""

import math
import cv2
import numpy as np
import matplotlib.pyplot as plt


def hough_circle(path):
    """
    funkce pro vytvoření obrázku s počtem kružnic
    """
    bgr=cv2.imread(path)
    gray=cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,2.6,10)
    circles = np.uint16(np.around(circles))
    cv2.putText(bgr,str(len(circles[0,:])),(78,180),0, 5,(255,0,255),6)
    return bgr

def hough_circle_draw(imgs):
    """
    metoda pro vykreslování výsledků funkce HoughCircle
    """
    plt.subplot(2,3,1)
    plt.xticks(color='white')
    plt.yticks(color='white')
    plt.imshow(imgs[0])

    plt.subplot(2,3,2)
    plt.xticks(color='white')
    plt.yticks(color='white')
    plt.imshow(imgs[1])

    plt.subplot(2,3,3)
    plt.xticks(color='white')
    plt.yticks(color='white')
    plt.imshow(imgs[2])

    plt.subplot(2,3,4)
    plt.xticks(color='white')
    plt.yticks(color='white')
    plt.imshow(imgs[3])

    plt.subplot(2,3,5)
    plt.xticks(color='white')
    plt.yticks(color='white')
    plt.imshow(imgs[4])

    plt.subplot(2,3,6)
    plt.xticks(color='white')
    plt.yticks(color='white')
    plt.imshow(imgs[5])

    plt.show()

def znacky_encode(imgsrc):
    """
    funkce pro zjištění: značek, využité matice pro erozi, tvaru původního obrázku,
    obrázku značek a šedotónového obrázku
    """
    img=cv2.imread(imgsrc)
    gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray=np.divide(gray,255)
    kernel = np.ones((3, 3), np.uint8)
    n=[-1,-1]
    image_post_erode=[]
    eroding1 = img[:math.floor(len(img)/2)]
    eroding2 = img[-math.ceil(len(img)/2):]
    while np.sum(eroding1)>0:
        eroding1=cv2.erode(eroding1, kernel)
        n[0]+=1
    #erroding1=cv2.dilate(erroding1,np.ones((3, 3), np.uint8))
    while np.sum(eroding2)>0:
        eroding2=cv2.erode(eroding2, kernel)
        n[1]+=1
    #erroding2=cv2.dilate(erroding2,np.ones((3, 3), np.uint8))
    eroding1 = img[:math.floor(len(img)/2)]
    eroding2 = img[-math.ceil(len(img)/2):]
    eroding1=cv2.erode(eroding1, kernel,iterations=n[0])
    eroding2=cv2.erode(eroding2, kernel,iterations=n[1])
    #erroding1=np.array(erroding1).flatten()
    eroding1 = cv2.cvtColor(eroding1,cv2.COLOR_RGB2GRAY)/255
    eroding2 = cv2.cvtColor(eroding2,cv2.COLOR_RGB2GRAY)/255
    image_post_erode.extend(eroding1)
    image_post_erode.extend(eroding2)
    hits=[]
    n_counter=0
    for y,row in enumerate(image_post_erode):
        for x,column in enumerate(row):
            if column==1:
                hits.append([y,x,n[n_counter]])
                n_counter+=1
    return hits, kernel, gray.shape, image_post_erode, gray

def znacky_decode(znacky,kernel,img_shape):
    """
    funkce pro dekodování na obrázek ze značek, použité matice a tvaru původního obrázku
    """
    img = np.zeros(img_shape)
    for _,zn in enumerate(znacky):
        img[zn[0]][zn[1]]=255
    dilation1 = img[:math.floor(len(img)/2)]
    dilation2 = img[-math.ceil(len(img)/2):]
    dilation1=cv2.dilate(dilation1, kernel,iterations=znacky[0][2])
    dilation2=cv2.dilate(dilation2, kernel,iterations=znacky[1][2])
    img_post_dilate=[]
    img_post_dilate.extend(dilation1)
    img_post_dilate.extend(dilation2)
    return img_post_dilate

def znacky_plot(source,encoded,decoded, znacky):
    """
    metoda pro vykreslování výsledků značkování a výpis značek do konzole
    """
    print("\nZnačky:")
    for znacka in znacky:
        print("    x: "+str(znacka[1])+", y: "+str(znacka[0])+", počet erozí: "+str(znacka[2]))
    plt.subplot(1,3,1)
    plt.imshow(source, cmap="gray")
    plt.title("Pre eroze")
    plt.axis('off')
    plt.subplot(1,3,2)
    plt.title("značky")
    plt.axis('off')
    plt.imshow(encoded, cmap="gray")
    plt.subplot(1,3,3)
    plt.title("Post dilatace")
    plt.axis('off')
    plt.imshow(decoded, cmap="gray")
    plt.show()


if __name__=="__main__":
    imgs=[]
    imgs.append(hough_circle("data/img/Cv11_c01.bmp"))
    imgs.append(hough_circle("data/img/Cv11_c02.bmp"))
    imgs.append(hough_circle("data/img/Cv11_c03.bmp"))
    imgs.append(hough_circle("data/img/Cv11_c04.bmp"))
    imgs.append(hough_circle("data/img/Cv11_c05.bmp"))
    imgs.append(hough_circle("data/img/Cv11_c06.bmp"))
    hough_circle_draw(imgs)

    znacky,matrix,shape, imge, imgs = znacky_encode("data/img/Cv11_merkers.bmp")
    imgd = znacky_decode(znacky,matrix,shape)
    znacky_plot(imgs,imge,imgd, znacky)
