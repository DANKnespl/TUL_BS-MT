
import struct
import cv2
import numpy as np
import matplotlib.pyplot as plt


def parserToRGB(file):
    with open(file, 'rb') as f:
        if str(f.read(2))!="b'BM'":
            raise Exception("Error")
        size=struct.unpack("i",f.read(4))[0]
        f.read(4) #future use
        if str(f.read(8))!="b'6\\x00\\x00\\x00(\\x00\\x00\\x00'":
            raise Exception("error")
        width=struct.unpack("i",f.read(4))[0]
        height=struct.unpack("i",f.read(4))[0]
        planes=struct.unpack("h",f.read(2))[0]
        bpp=struct.unpack("h",f.read(2))[0]
        f.read(4)
        if struct.unpack("i",f.read(4))[0]%4!=0:
            raise Exception("Wrong size")
        f.read(16)
        #data
        Bpp=1
        if bpp>=8:
            Bpp=int(bpp/8)
        ExtraBytes=4-(Bpp*width)%4
        if ExtraBytes==4:
            ExtraBytes=0
        data = [[0 for i in range(width)] for j in range(height)]
        for j in range(height):
            for i in range(width):
                pixel=[]
                for k in range(Bpp):
                    pixel.append(struct.unpack("B",f.read(1))[0])
                data[width-1-j][i]=pixel
            f.read(ExtraBytes)
        rgb = cv2.cvtColor(np.uint8(np.array(data)), cv2.COLOR_BGR2RGB)
        print("Size="+str(size)+" B")
        print("Planes="+str(planes))
        print(str(bpp)+" bits/pixel")
        print("Width="+str(width))
        print("Height="+str(height))
    return(rgb)


def colourFinder(file):
    bgr = cv2.imread(file)
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    width = rgb.shape[1]
    height = rgb.shape[0]
    data = [[0 for i in range(width)] for j in range(height)]
    for j in range(height):
        for i in range(width):
            if (np.uint16(rgb[j][i][0])+rgb[j][i][1]+rgb[j][i][2])==0:
                r=0
            else:
                r=rgb[j][i][0]/(np.uint16(rgb[j][i][0])+rgb[j][i][1]+rgb[j][i][2])
            data[j][i]=rgb[j][i]            
            if r <0.5:
                data[j][i]=[255,255,255]
    return(rgb,data)

def output(rgb,nonwhite,white):
    width = rgb.shape[1]
    height = rgb.shape[0]

    figGS = plt.figure()
    plotsGS = figGS.subplots(1,2)
    plotsGS[0].imshow(rgb)
    plotsGS[1].imshow(cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY), cmap='gray')
    plotsGS[0].title.set_text("RGB")
    plotsGS[1].title.set_text("GRAY")

    hsv=cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    ycbcr=cv2.cvtColor(rgb, cv2.COLOR_RGB2YCR_CB)
    h = [[0 for i in range(width)] for j in range(height)]
    s = [[0 for i in range(width)] for j in range(height)]
    v = [[0 for i in range(width)] for j in range(height)]
    
    y = [[0 for i in range(width)] for j in range(height)]
    cb = [[0 for i in range(width)] for j in range(height)]
    cr = [[0 for i in range(width)] for j in range(height)]
    for j in range(height):
        for i in range(width):
            h[i][j]=hsv[i][j][0]
            s[j][i]=hsv[j][i][1]
            v[j][i]=hsv[j][i][2]
            y[j][i]=ycbcr[j][i][0]
            cr[j][i]=ycbcr[j][i][1]
            cb[j][i]=ycbcr[j][i][2]

    figHSV, axHSV= plt.subplots(2,2)
    a01=axHSV[0,0].imshow(rgb)
    a02=axHSV[0,1].imshow(h, cmap='jet', vmin=0,vmax=150)
    a03=axHSV[1,0].imshow(s, cmap='jet', vmin=100,vmax=255)
    a04=axHSV[1,1].imshow(v, cmap='jet', vmin=100,vmax=255)
    figHSV.colorbar(a02,ax=axHSV[0,1])
    figHSV.colorbar(a03,ax=axHSV[1,0])
    figHSV.colorbar(a04,ax=axHSV[1,1])
    axHSV[0,0].title.set_text("RGB")
    axHSV[0,1].title.set_text("H")
    axHSV[1,0].title.set_text("S")
    axHSV[1,1].title.set_text("V")

    figYCBCR,axYCrCb = plt.subplots(2,2)
    a11=axYCrCb[0,0].imshow(rgb)
    a12=axYCrCb[0,1].imshow(y, cmap='gray', vmin=0,vmax=255)
    a13=axYCrCb[1,0].imshow(cr, cmap='jet', vmin=0,vmax=255)
    a14=axYCrCb[1,1].imshow(cb, cmap='jet', vmin=0,vmax=255)

    figHSV.colorbar(a12,ax=axYCrCb[0,1])
    figHSV.colorbar(a13,ax=axYCrCb[1,0])
    figHSV.colorbar(a14,ax=axYCrCb[1,1])
    axYCrCb[0,0].title.set_text("RGB")
    axYCrCb[0,1].title.set_text("Y")
    axYCrCb[1,0].title.set_text("Cr")
    axYCrCb[1,1].title.set_text("Cb")
    
    figWhite,axWhite = plt.subplots(1,2)
    axWhite[0].imshow(nonwhite, cmap='jet')
    axWhite[1].imshow(white, cmap='jet')
    #plotsGS[1][].imshow()  
    plt.show()


if __name__ == '__main__':
    data=parserToRGB("data/cv03_objekty1.bmp")
    data2a,data2b=colourFinder("data/cv03_red_object.jpg")   
    output(data,data2a,data2b)
