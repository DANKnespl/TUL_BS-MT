"""
metody hledání změn ve videu
"""
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


def image_load(file):
    """
    loads image and turns it gray
    """
    bgr = cv2.imread(file)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    return gray

def met1(gs1,gs2):
    """
    |CompleteSum(gs1)-CompleteSum(gs2)|
    """
    return abs(np.sum(gs1,dtype="int64")-np.sum(gs2,dtype="int64"))

def met2(gs1,gs2):
    """
    CompleteSum(|gs1-gs2|)
    """
    return np.sum(abs(np.int64(gs1) - np.int64(gs2)),dtype="int64")

def met3(gs1,gs2):
    """
    CompleteSum(|Histogram(gs1)-Histogram(gs2)|)
    """
    return np.sum(abs(np.histogram(gs1,range(256))[0]-np.histogram(gs2,range(256))[0]))

def met4(gs1,gs2,n):
    """
    CompleteSum(|DCTCoeffficients(gs1,n)-DCTCoeffficients(gs2,n)|)
    """
    return np.sum(abs(np.subtract(dct_coeffs(gs1,n), dct_coeffs(gs2,n))))

def dct_coeffs(gs1,n):
    """
    finds highest n dct coefficients
    """
    dct_image = cv2.dct(np.float32(gs1))
    coefficients = abs(dct_image.flatten())
    top_indices = np.argsort(coefficients)[-n:] #argsort - indexy od nejmenšího [-n:] posledních 5
    top_coeffs = np.log(coefficients[top_indices])[::-1] #vrácení v opačném pořadí
    return top_coeffs

def draw_sub(data,title):
    """
    plots subplots for first figure
    """
    enums = list(enumerate(data))
    t = [x[0] for x in enums]
    vec = [x[1] for x in enums]
    plt.title(title)
    plt.axvline(x=208, linewidth=2, color='r')
    plt.axvline(x=268, linewidth=2, color='r')
    plt.plot(t, vec, linewidth=2, color='b')
    plt.axis([min(t), max(t), min(vec), max(vec)])

def draw_fig1(data):
    """
    plots first figure
    """
    plt.subplot(2, 2, 1)
    draw_sub(data[0],"Method #0")
    plt.subplot(2, 2, 2)
    draw_sub(data[1],"Method #1")
    plt.subplot(2, 2, 3)
    draw_sub(data[2],"Method #2")
    plt.subplot(2, 2, 4)
    draw_sub(data[3],"Method #3")


def images_input(path):
    """
    calculates data for fig1 from images folder
    """
    method1_list=[]
    method2_list=[]
    method3_list=[]
    method4_list=[]
    frames=len(os.listdir(path))+1
    for i in range(2,frames):
        gs1=image_load(path+f"/a{(i-1):03d}.bmp")
        gs2=image_load(path+f"/a{i:03d}.bmp")
        method1_list.append(met1(gs1,gs2))
        method2_list.append(met2(gs1,gs2))
        method3_list.append(met3(gs1,gs2))
        method4_list.append(met4(gs1,gs2,5))
    return method1_list,method2_list,method3_list,method4_list

def stream_input(path):
    """
    calculates data for fig1 from stream
    """
    method1_list=[]
    method2_list=[]
    method3_list=[]
    method4_list=[]
    stream = cv2.VideoCapture(path)
    _, bgr = stream.read()
    gs1= cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    j = 1
    while j <  int(stream.get(cv2.CAP_PROP_FRAME_COUNT)):
        _, bgr = stream.read()
        gs2= cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        method1_list.append(met1(gs1,gs2))
        method2_list.append(met2(gs1,gs2))
        method3_list.append(met3(gs1,gs2))
        method4_list.append(met4(gs1,gs2,5))
        j+=1
        gs1=gs2
    stream.release()
    return method1_list,method2_list,method3_list,method4_list

def images_fig2(path,t,vec):
    """
    shows images at times in plot
    """
    fig = plt.figure()
    fig.add_axes([0, 0, 1, 1], frameon=False, xticks=[], yticks=[])
    frames=len(os.listdir(path))+1
    for i in range(1,frames):
        bgr = cv2.imread(path+f"/a{i:03d}.bmp")
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        fig.clear()
        plt.axvline(x=208, linewidth=2, color='r')
        plt.axvline(x=268, linewidth=2, color='r')
        plt.plot(t, vec, linewidth=2, color='b')
        plt.axvline(x=i, linewidth=2, color='g')
        plt.axis([min(t), max(t), min(vec), max(vec)])
        plt.imshow(rgb, aspect='auto', extent = [min(t), max(t), min(vec), max(vec)])
        plt.show(block=False)
        plt.pause(0.000001)

def stream_fig2(path,t,vec):
    """
    shows frames of stream in plot
    """
    fig = plt.figure()
    cap = cv2.VideoCapture(path)
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    for i in range(1, frames):
        _, bgr = cap.read()
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        fig.clear()
        plt.axvline(x=208, linewidth=2, color='r')
        plt.axvline(x=268, linewidth=2, color='r')
        plt.plot(t, vec, linewidth=2, color='b')
        plt.axvline(x=i, linewidth=2, color='g')
        plt.axis([min(t), max(t), min(vec), max(vec)])

        plt.imshow(rgb, aspect='auto', extent = [min(t), max(t), min(vec), max(vec)])
        plt.show(block=False)
        plt.pause(0.000001)
    cap.release()


def draw(method_list,rt_method,path,image_video):
    """
    plots data to two plots, second plot shows after
    first is closed
    """
    draw_fig1(method_list)
    plt.show()
    enums = list(enumerate(method_list[rt_method]))
    t = [x[0] for x in enums]
    vec = [x[1] for x in enums]
    if image_video==0:
        stream_fig2(path,t,vec)
    else:
        images_fig2(path,t,vec)
    plt.show()

def images_full(path,rt_method):
    """
    calculates and shows data from image folder
    with files named like f"/a{n:03d}.bmp",
    starting at /a001.bmp the folder path should not contain the last /
    """
    draw(images_input(path),rt_method,path,1)

def stream_full(path,rt_method):
    """
    calculates and shows data from video file
    """
    draw(stream_input(path),rt_method,path,0)


if __name__=="__main__":
    #images_full("data/Cv08_vid",1)
    stream_full("data/cv08_video.mp4",1)
