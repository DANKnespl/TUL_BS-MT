"""
PCA of image
"""
import math
import cv2
import numpy as np
import matplotlib.pyplot as plt

def draw(data_pca,data_gray):
    """
    plots chosen pca component and grayscale to be compared
    """
    plt.subplot(2,2,1)
    plt.title("PCA")
    plt.imshow(data_pca,cmap="gray")
    plt.subplot(2,2,2)
    plt.title("BGR2GRAY")
    plt.imshow(data_gray,cmap="gray")
    plt.subplot(2,2,3)
    plt.hist(data_pca.flatten(),256,[0,256])
    plt.subplot(2,2,4)
    plt.hist(data_gray.flatten(),256,[0,256])
    plt.show()

def draw2(data_pca1,data_pca2,data_pca3,data_gray):
    """
    plots all pca components and grayscale to be compared
    """
    plt.subplot(2,4,1)
    plt.title("PCA1")
    plt.imshow(data_pca1,cmap="gray")
    plt.subplot(2,4,5)
    plt.hist(data_pca1.flatten(),256,[0,256])

    plt.subplot(2,4,2)
    plt.title("PCA2")
    plt.imshow(data_pca2,cmap="gray")
    plt.subplot(2,4,6)
    plt.hist(data_pca2.flatten(),256,[0,256])

    plt.subplot(2,4,3)
    plt.title("PCA3")
    plt.imshow(data_pca3,cmap="gray")
    plt.subplot(2,4,7)
    plt.hist(data_pca3.flatten(),256,[0,256])

    plt.subplot(2,4,4)
    plt.title("BGR2GRAY")
    plt.imshow(data_gray,cmap="gray")
    plt.subplot(2,4,8)
    plt.hist(data_gray.flatten(),256,[0,256])
    plt.show()

def get_pca_component(image_data,component):
    """
    returns (component+1)-th component of image_data
    """
    b,g,r = [],[],[]
    rgb=[]
    for _,i in enumerate(image_data):
        for _,j in enumerate(i):
            b.append(j[0]/255)
            g.append(j[1]/255)
            r.append(j[2]/255)
    m_vector = (np.array(b)+np.array(g)+np.array(r))/3
    b=np.array(b)-m_vector
    g=np.array(g)-m_vector
    r=np.array(r)-m_vector
    wt=np.matrix([r,g,b])
    #wt=np.matrix([b,g,r])
    w=np.transpose(wt)
    c=np.matmul(wt,w)
    print(c)
    eigenvalues, eigenvectors = np.linalg.eig(c)
    ep = ([x for _, x in sorted(zip(eigenvalues.tolist(),eigenvectors.tolist()))])
    ep.reverse()
    ep=np.matrix(ep)
    e=np.matmul(w,ep)
    line=[]
    for i,item in enumerate(e):
        list_item=item.tolist()[0]
        line.append(math.floor((list_item[component]+m_vector[i])*255))
        if len(line)==len(image_data[0]):
            rgb.append(line)
            line=[]
    rgb=np.array(rgb)
    return rgb

if __name__=="__main__":
    bgr=cv2.imread("data/Cv09_obr.bmp")
    gray=cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    pca=get_pca_component(bgr,0)
    #draw2(get_pca_component(bgr,0),get_pca_component(bgr,1),get_pca_component(bgr,2),gray)
    draw(pca,gray)
