from PIL import Image
import pytesseract,urllib.request,time,re,threading,shutil,os,socket
import myImgUrlData,sameImg,Timer

myImgUrlData.save_cookit() #保存cookie
regString = r"[裸]+|私我|要看妹|自?慰|加我|微?信|加?妹?妹|妹?Q|妹?q|看?发?表|1?岁|哥*哥|不约|[看果徵]|[0-9]{7,20}"
myId = [999999,1178456,1076081,1086930,1084036,1000216,1683209,1627049,1384660,1302915]
def save_img(img_url,file_name="1",file_path='img'):
    #保存图片到磁盘文件夹 file_path中，默认为当前脚本运行目录下的 book\img文件夹
    try:
        #获得图片后缀
        file_suffix = os.path.splitext(img_url)[1]
        #拼接图片名（包含路径）
        filename = '{}{}{}{}'.format(file_path,os.sep,file_name,file_suffix)
       #下载图片，并保存到文件夹中
        socket.setdefaulttimeout(30)
        urllib.request.urlretrieve(img_url,filename=filename)
        files = filename
    except IOError as e:
        files = '1.jpg'
    return files

def img_to_str(imgFile):
    try:
        text = pytesseract.image_to_string(Image.open(imgFile),lang='chi_sim').strip()
        text = text.replace("\n", "")
        if len(text)>6:
            print ("try识别模式结束文字为：%s"%text)
    except Exception as e:
        text = "12"
    return text

def idarr(uid):  #返回所有id
    posturl = '/admin/audit' #请求地址只留下后缀了
    data = {'page': "",'r_id': "",'date': "",'title': "",'content': "",'status':"all",'uid': uid}
    #  print (post(posturl, data))  #打印post请求返回数据
    return myImgUrlData.getIdArr(posturl,data)

def killAllNode(arr):
    for val in arr:
        myImgUrlData.killOneNode(val)

def max_same_num(img_file):
    numarr = []
    for x in range(2,6):
        image1 = Image.open("a_img/%s.jpg"%x)
        image2 = Image.open(img_file)
        num = sameImg.classfiy_histogram_with_split(image1, image2)
        numarr.append(num)
    return max(numarr)


def round_img():
    all_img = myImgUrlData.main()
    # print (all_img)
    for i in all_img:
        saveimg = save_img(i)
        sameNum = max_same_num(saveimg)
        if sameNum >= 80:
            uid = i[i.index("_1")+1:i.index("_1")+8]
            int_uid = int(uid)
            if uid not in myId and int_uid >1900000:
                myImgUrlData.killOneNode(idarr(uid)[0])
                myImgUrlData.forbidden(uid)
                print ("相识删除%suid%s"%(sameNum,uid))
        text = img_to_str(saveimg)
        if len(text)>=10:
            #这里是正则匹配
            pattern = re.compile(regString)
            match = pattern.findall(text)
            #这里是正则匹配
            if match:
                uid = i[i.index("_")+1:i.index("_")+8]
                int_uid = int(uid)
                #myImgUrlData.killOneNode(idarr(uid)[0])
                if uid not in myId and int_uid >1900000:
                    myImgUrlData.forbidden(uid)
                    killAllNode(idarr(uid))
                    print ("============================================================")
                    print ("禁用了用户%s的帖子"%uid)
                    print ("============================================================")
        if all_img.index(i) == len(all_img)-1:
            print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "结束，开始新的循环\n\n")
            #timer = threading.Timer(150, round_img)
            #timer.start()

def main():
    t = Timer.LoopTimer(152,round_img)
    t.start()
if __name__ == '__main__':
    #round_img()
    main()
    # print(idarr(1252096))
    # killAllNode(idarr(1252096))
