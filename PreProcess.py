import os
import sys
import math
import time
import argparse
import random
import cv2 as cv
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
PATH = 'D:/edoctordate/Project/all/1/'
saveimgpath='D:/edoctordate/Project/train/1/'

f_list = os.listdir(PATH)
for image in f_list:
    if os.path.splitext(image)[1] == '.jpg':
        img = Image.open(PATH+image).convert("L")
        img = np.array(img)

        # 二值化心电图，去掉表格
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                    if img[i][j]> 100:
                        img[i][j]=255
                    else :
                        img[i][j]=0
        '''
        找出每张心电图的心跳间隔
        心电图的尺寸为1400*690
        故img[0~690][0~1400]
        

        观察心电图，我认为想要找出心跳的频率，需要从波峰入手
        波峰的一般特征：在较短的宽度内，高度发生较大变化
        可以通过判定至少有3条（暂定）在8个像素（暂定）的宽度范围内，竖直方向的连续像素数大于6（暂定）
        '''

        Number=0        #第几次心跳最高峰
        Numcount=0      #竖直条数计数器
        NumWidth=9      #水平宽度计数器
        temp=[[0]*4 for i in range(20)]       #暂存竖线的位置信息，当找到了3条竖线时，取平均大约可以求得心电图某次心跳的最高峰位置
        i=60            #心电图大约在此处开始绘制
        j=0
        signal=0        #因为有多层循环，为跳出中间层循环二创造的变量
        while i< img.shape[1]:
            while j< 150:
                #提高效率 and 避免循环在边缘处发生错误            
                if img[j][i]==0:
                    # 在规定宽度范围（8个像素）内
                    # for width in range(i,i+NumWidth):
                    width=i
                    while width< i+NumWidth:
                        for jj in range(j-10,j+30):
                            if img[jj][width]==0 and img[jj+1][width]==0 and img[jj+2][width]==0 and img[jj+3][width]==0 and img[jj+4][width]==0 and img[jj+5][width]==0:
                                # 发现心电图的右上角的EMG字样会干扰判断
                                # 加限制:须i>30
                                if j>30:
                                    temp[Number][Numcount]=width
                                    Numcount =Numcount+1

                                if Numcount==3:
                                    Numcount=0
                                    temp[Number][0]=(temp[Number][0]+temp[Number][1]+temp[Number][2])//3
                                    temp[Number][3]=jj
                                    Number=Number+1
                                    # 纵坐标
                                    
                                    # 找到了三个竖向直线，
                                    # 心电图波峰确定，为跳出while width<i+NumWidth循环，signal置1
                                    signal=1
                                    # 如果找到了三个连续的竖向直线，意味着这附近有一个心跳的波峰
                                    # 想要寻找下一个波峰，而不受此波峰的竖向直线干扰，须加7（暂定值）
                                    i=i+NumWidth
                                    break
                                #如果遍历了横向7宽度的像素，能执行到这一步，说明宽度范围内没有心跳峰值
                                if width==i+NumWidth-1:
                                    Numcount=0
                                
                                break
                        if signal==1:
                            signal=0
                            break
                        if width==i+NumWidth-1:
                            Numcount=0
                        width=width+1
                j=j+1
            j=0
            i=i+1                   
                                
        '''
        一下代码为横向扫描
        效率高
        但因为横向扫描，会出现重复扫描波峰的情况，未出现
        
        while i< 150:
            while j< img.shape[1]:
                #提高效率 and 避免循环在边缘处发生错误            
                if img[i][j]==0:
                    # 在规定宽度范围（8个像素）内
                    # for width in range(i,i+NumWidth):
                    width=j
                    while width< j+NumWidth:
                        for ii in range(i-10,i+30):
                            if img[ii][width]==0 and img[ii+1][width]==0 and img[ii+2][width]==0 and img[ii+3][width]==0 and img[ii+4][width]==0 and img[ii+5][width]==0:
                                # 发现心电图的右上角的EMG字样会干扰判断
                                # 加限制:须i>30
                                if i>30:
                                    temp[Number][Numcount]=width
                                    Numcount =Numcount+1

                                if Numcount==3:
                                    Numcount=0
                                    temp[Number][0]=(temp[Number][0]+temp[Number][1]+temp[Number][2])//3
                                    Number=Number+1
                                    # 找到了三个竖向直线，
                                    # 心电图波峰确定，为跳出while width<i+NumWidth循环，signal置1
                                    signal=1
                                    # 如果找到了三个连续的竖向直线，意味着这附近有一个心跳的波峰
                                    # 想要寻找下一个波峰，而不受此波峰的竖向直线干扰，须加7（暂定值）
                                    j=j+7
                                    break
                                #在if img[ii][width]==0 ……判断内执行进入下面这步判断，说明相对于初始位置的第七个像素有竖向直线
                                # 但是数量不够三个，故也需要舍弃，即置Numcount=0
                                #在如果遍历了横向7宽度的像素，能执行到这一步，说明宽度范围内没有心跳峰值
                                if width==j+NumWidth-1:
                                    Numcount=0
                                
                                break
                        if signal==1:
                            signal=0
                            break
                        
                        #如果遍历了横向7宽度的像素，能执行到这一步，说明宽度范围内没有心跳峰值
                        if width==j+NumWidth-1:
                            Numcount=0
                        width=width+1
                # 这边j+1操作可能发生在j+7后
                # 我不知道会不会有问题
                j=j+1
            j=0
            i=i+1  
        
        '''

        # temp[][1]和temp[][2]存储的是临时数据
        # 当执行到该步时，temp[][0]时找出的心跳波峰
        # for i in range(Number):
        #     print(temp[i][0])

        for i in range (Number):
            box = (temp[i][0]-64,temp[i][3]-64,temp[i][0]+64,temp[i][3]+64)
            # #这里的参数可以这么认为：从某图的(x,y)坐标开始截，截到(width+x,height+y)坐标
            # #所包围的图像，crop方法与php中的imagecopy方法大为不一样
            # newIm = img.crop(box)
            # newIm=np.zeros((temp[i+1][0]-temp[i][0],120),dtype=np.uint8)
            # newIm=img[temp[i][3]-60:temp[i][3]+60][temp[i][0]:temp[i+1][0]]
            newIm=Image.fromarray(img,mode='L')
            newIm = newIm.crop(box)
            '''
            for ii in range(3):
                for iii in range(3):
                    # 确定X坐标
                    # 裁切上一步生成的128*128的图像为96*96
                    # 然后扩展至128*128
                    # 进一步扩展数据集
                    if ii==0:
                        coorx=0
                    elif ii==1 :
                        coorx=16
                    else :
                        coorx=32
                    # 
                    if iii==0:
                        coory=0
                    elif iii==1 :
                        coory=16
                    else :
                        coory=32
                    smallbox=(coorx,coory,coorx+96,coory+96)
                    smallnewIm=newIm.crop(smallbox)
                    smallnewIm.resize((128,128))
                    smallnewIm.save(saveimgpath+image[0:-4]+'~'+str(i)+'_'+str(ii)+'_'+str(iii)+'.jpg')
            '''
            # newIm.show()
            newIm.save(saveimgpath+image[0:-4]+'(track0)'+str(i)+'.jpg')
        
        # 从上次找到的心跳波峰+50像素处开始找下一道心跳
        # 理论上讲，只要发现黑色像素点，就一定是一下道心跳位置
        # 依旧存入temp[][3]
        for track in range(1,6):
            for first in range(Number):
                for ii in range(temp[first][3]+50,img.shape[0]):
                    if img[ii][temp[first][0]]==0:
                        temp[first][3] = ii
                        # print(ii)
                        break
            
            for i in range (Number):
                box = (temp[i][0]-64,temp[i][3]-64,temp[i][0]+64,temp[i][3]+64)
                # #这里的参数可以这么认为：从某图的(x,y)坐标开始截，截到(width+x,height+y)坐标
                # #所包围的图像，crop方法与php中的imagecopy方法大为不一样
                # newIm = img.crop(box)
                # newIm=np.zeros((temp[i+1][0]-temp[i][0],120),dtype=np.uint8)
                # newIm=img[temp[i][3]-60:temp[i][3]+60][temp[i][0]:temp[i+1][0]]
                newIm=Image.fromarray(img,mode='L')
                newIm = newIm.crop(box)
                '''
                for ii in range(3):
                    for iii in range(3):
                        # 确定X坐标
                        # 裁切上一步生成的128*128的图像为96*96
                        # 然后扩展至128*128
                        # 进一步扩展数据集
                        if ii==0:
                            coorx=0
                        elif ii==1 :
                            coorx=16
                        else :
                            coorx=32
                        # 
                        if iii==0:
                            coory=0
                        elif iii==1 :
                            coory=16
                        else :
                            coory=32
                        smallbox=(coorx,coory,coorx+96,coory+96)
                        smallnewIm=newIm.crop(smallbox)
                        smallnewIm.resize((128,128))
                        smallnewIm.save(saveimgpath+image[0:-4]+'~'+str(i)+'_'+str(ii)+'_'+str(iii)+'.jpg')
                '''
                # newIm.show()
                newIm.save(saveimgpath+image[0:-4]+'(track'+str(track)+')'+str(i)+'.jpg')