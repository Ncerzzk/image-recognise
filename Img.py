from PIL import Image
import os
import sys


class ImgExpection(Exception):
    def __init__(self):
        print("uncorrect input image")


class Img:
    def __init__(self,image=None,fname=None,url=None):
        if image:
            self.image=image
        elif fname:
            self.image=Image.open(fname)
        else:
            self.image=None

    def binary(self): #二值化
        for y in range(self.image.height):
            for x in range(self.image.width):
                pixel=self.image.getpixel((x,y))
                light=pixel[0]*0.299+pixel[1]*0.587+pixel[2]*0.114
                if light>255.0/2:
                    self.image.putpixel((x,y),(255,255,255,255))
                else:
                    self.image.putpixel((x,y),(0,0,0,255))

    def show(self):
        self.image.show()

    def save(self,fname):
        self.image.save(fname)

    def divide(self):  #分割图片
        height=self.image.height
        width=int(self.image.width/4)
        result=[]

        dividers=[]
        for c in range(1,4):
            for i in range(c*width-4,c*width+4):
                for j in range(self.image.height):
                    temp=self.image.getpixel((i,j))
                    if temp[0]==0:
                        break
                else:
                    dividers.append(i)
                    break
            else:
                dividers.append(width*c)
        dividers.append(self.image.width)
        for j,i in enumerate(dividers):
            crop=self.image.crop((0 if not j else dividers[j-1],0,i,height))
            crop=Img(crop)
            crop.binary()
            crop.move_center()
            crop.save(str(j)+".jpg")
            result.append(crop)
        return result

    def get_feature(self): #取特征值,通过特征值的比对来确定结果
        result=""
        for y in range(self.image.height):
            for x in range(self.image.width):
                temp=self.image.getpixel((x,y))
                if temp[0]>0:
                    result+="0"
                else:
                    result+="1"
        return result

    def move_center(self): #将图片移到中心，在divide中调用

        left=self.image.width
        top=self.image.height
        right=0
        bottom=0

        for j in range(self.image.height):
            for i in range(self.image.width):
                temp=self.image.getpixel((i,j))
                if temp[0] == 0:
                    left=min(left,i)
                    top=min(top,j)
                    break
            for i in range(self.image.width-1,0,-1):
                temp=self.image.getpixel((i,j))
                if temp[0] == 0:
                    right=max(right,i)
                    bottom=max(bottom,j)
                    break

        self.image=self.image.crop((left,top,right,bottom))

    def recognise(self): #识别  （注：此时的Img为分割后的四个图片之一）
        count=0
        result=''
        feature=self.get_feature()
        for file in os.listdir(sys.path[0]+"/font"):
            name=os.path.basename(file)
            if name.find('.txt')==-1:
                continue
            name=name.split('-')
            name=name[0]
            f=open("font/"+file)
            tempstr=f.read()
            f.close()
            temp=0
            for i,j in zip(feature,tempstr):
                if i==j:
                    temp+=1
            if temp>count:
                count=temp
                result=name
        return result
