"""
popis
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt


def histogramEqualisation(img,q0,qk):
    ImgDataBGR=cv2.imread(img)
    ImgDataYCrCb=cv2.cvtColor(ImgDataBGR,cv2.COLOR_BGR2YCR_CB)
    ImgDataRGB=cv2.cvtColor(ImgDataBGR,cv2.COLOR_BGR2RGB)
    width=ImgDataBGR.shape[1]
    height=ImgDataBGR.shape[0]
    hist = cv2.calcHist([ImgDataYCrCb],[0],None,[256],[0,256])
    data=[[0 for i in range(width)] for j in range(height)]
    FH=hist.cumsum()
    IMGCONST=(qk-q0)/(width*height)
    for j in range(height):
        for i in range(width):
            p=ImgDataYCrCb[j][i][0]
            data[j][i]=[IMGCONST*FH[p]+q0,ImgDataYCrCb[j][i][1],ImgDataYCrCb[j][i][2]]
    data=np.uint8(data)
    print(FH)
    dataHist=cv2.calcHist([data],[0],None,[256],[0,256])
    return ImgDataRGB,hist,cv2.cvtColor(data,cv2.COLOR_YCR_CB2RGB),dataHist

def gammaCorection(withEr,Er):
    withErDataBGR = cv2.imread(withEr)
    ErDataBGR = cv2.imread(Er)
    data3=np.divide(withErDataBGR.astype(float),ErDataBGR.astype(float))*255
    return (cv2.cvtColor(withErDataBGR,cv2.COLOR_BGR2RGB),cv2.cvtColor(ErDataBGR,cv2.COLOR_BGR2RGB),cv2.cvtColor(np.uint8(data3),cv2.COLOR_BGR2RGB))

def output(g1,g2,equal):
    figG1, axG1 = plt.subplots(1, 3)
    axG1[0].imshow(g1[0])
    axG1[1].imshow(g1[1])
    axG1[2].imshow(g1[2])
    figG1.set_figwidth(10)
    figG1.set_figheight(5)
    axG1[0].title.set_text("S chybou")
    axG1[1].title.set_text("Chyba")
    axG1[2].title.set_text("Bez chyby")

    figG2, axG2 = plt.subplots(1, 3)
    axG2[0].imshow(g2[0])
    axG2[1].imshow(g2[1])
    axG2[2].imshow(g2[2])
    axG2[0].title.set_text("S chybou")
    axG2[1].title.set_text("Chyba")
    axG2[2].title.set_text("Bez chyby")
    figG2.set_figwidth(10)
    figG2.set_figheight(5)

    figEq, axEq = plt.subplots(2, 2)
    axEq[0][0].imshow(equal[0])
    axEq[0][1].imshow(equal[2])
    axEq[1][0].plot(equal[1])
    axEq[1][1].plot(equal[3])
    axEq[0][0].title.set_text("Nízký kontrast")
    axEq[0][1].title.set_text("Vysoký kontrast")
    axEq[1][0].title.set_text("LC-Histogram")
    axEq[1][1].title.set_text("HC-Histogram")
    figEq.set_figwidth(8)
    figEq.set_figheight(7)
    plt.show()

if __name__ == '__main__':
    gamma1=gammaCorection("data/Cv04_porucha1.bmp","data/Cv04_porucha1_etalon.bmp")
    gamma2=gammaCorection("data/Cv04_porucha2.bmp","data/Cv04_porucha2_etalon.bmp")
    equal = histogramEqualisation("data/Cv04_rentgen.bmp",0,255)
    output(gamma1,gamma2,equal)


#nest - elsticsearch .net