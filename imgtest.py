from Img import *
import urllib.request
import random

opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor, urllib.request.HTTPHandler)
fontpath='font/'

def download_image(url,name="vcode"):
    open(name+".jpg","wb+").write(opener.open(url).read())


def train():
    for i in range(10):
        try:
            os.mkdir(fontpath)
        except:
            print(fontpath+" exist!")
        download_image("http://jwxt.bupt.edu.cn/validateCodeAction.do?random=")
        img=Img(fname="vcode.jpg")
        img.binary()
        img.save("tempBinary.jpg")
        img.show()
        x=input()
        if x=="next":          #如果分割破坏严重或者二值化后图片花了，直接输入next跳过该图片，以免污染字库
            continue
        images=img.divide()

        random.randint(1,100)
        for s,i in zip(x,images):
            f=open(fontpath+s+"-"+str(random.randint(1,100))+".txt","w+")
            f.write(i.get_feature()) #将特征值保存
            f.close()


def train2():
    for i in range(10):
        try:
            os.mkdir(fontpath)
        except:
            print(fontpath+" exist!")
        download_image("http://jwxt.bupt.edu.cn/validateCodeAction.do?random=")
        img=Img(fname="vcode.jpg")
        img.binary()
        img.save("tempBinary.jpg")
        img.show()
        images=img.divide()
        random.randint(1,100)
        for i in images:
            result=i.recognise()
            print("hello:"+result)
            x=input()
            if x=="":   #如果上面识别结果没错，输入回车则保存特征值。否则随意输入其他字符，跳过
                f=open(fontpath+result+"-"+str(random.randint(1,100))+".txt","w+")
                f.write(i.get_feature())
                f.close()

def test():
    download_image("http://jwxt.bupt.edu.cn/validateCodeAction.do?random=",name="hello")
    image=Img(fname="hello.jpg")
    image.binary()
    images=image.divide()

    vcodes=[]
    for temp in images:
        vcodes.append(temp.recognise())
    vcode_result=''.join(vcodes)
    print(vcode_result)

#train()
#本方法适用于重头开始训练，即字库为空或者字库里特征值很少。如果想试试本方法可以将fontpath修改一下，然后调用


#train2() #本方法适用于字库里已经有一定数量的特征值之后，进行快速训练
test()
