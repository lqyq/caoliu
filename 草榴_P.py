#路径问题
#
import requests
import re
import os
import multiprocessing
import time
from chardet.universaldetector import UniversalDetector
import chardet
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}


def _1_get_url(page,pic_type):
    if pic_type == '1':
        url = 'https://co.oustrave.com/thread0806.php?fid=7&search=&page=' + page  # 技术交流
    if pic_type == '2':
        url = 'https://co.oustrave.com/thread0806.php?fid=8&search=&page=' + page  # 新時代的我們
    if pic_type == '3':
        url = 'https://co.oustrave.com/thread0806.php?fid=16&search=&page=' + page  # 達蓋爾的旗幟

    # url = 'https://co.oustrave.com/@%E5%9B%9E%E6%94%B6%E8%A1%A8%E5%A6%B9' #注意看好url

    res = requests.get(url, headers=headers)
    code = re.findall('charset=(.*)\"', res.text)[0]
    if not code:
        code=chardet.detect(res.content)['encoding']
    res.encoding = code
    text = res.text
    # print(text)
    a = re.findall('a href="(.*?)html"', text)
    # print('总界面',a)
    return a  # 返回1级页面里面的url




def baocun(url, name):  # 此方法是将图片保存文件到本地 只需要传入图片地址
    n = re.findall('(.*?)[P\-]', name)
    print(n[0][-3:])
    root = '..' + os.sep + "pic" + os.sep + n[0] + os.sep  # 这是根文件所在
    try:
        os.mkdirs(root)
    except:
        pass
    if url[-4] == '.':
        path = root + name + url[-4:]  # 通过’/‘把图片的url分开找到最后的那个就是带.jpg的保存起来
    if url[-5] == '.':
        path = root + name + url[-5:]  # 通过’/‘把图片的url分开找到最后的那个就是带.jpg的保存起来
    if not os.path.exists(root):
        os.mkdir(root)
    if not os.path.exists(path):
        r = requests.get(url)
        r.raise_for_status()
        with open(path, 'wb') as f:  # 式以二进制格式打开一个文件只用于写入。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。一般用于非文本文件如图片等
            f.write(r.content)  # r.content返回二进制，像图片
            print('爬取成功')


def getimgscl(url, name='default'):
    count = 0
    res = requests.get(url, headers=headers)
    code = re.findall('charset=(.*)\"', res.text)[0]
    if not code:
        code = chardet.detect(res.content)['encoding']
    res.encoding = code
    text = res.text
    # print(text)
    # pprint(text)
    a = re.findall('ess-data=\'(.*?)\'', text)#需要修改
    title1 = re.findall('<title>(.*?)\|', text)
    title = re.findall('(.*?)P',title1[0])[0]
    print(title)
    print(code,url)
    if title:
        name = title
    pic_list=[]
    pic_list.append(title)
    for i in a:
        pic_list.append(i)
    return pic_list
def save_pic(url, count,title):

    # extension=re.findall('.*(\..*)',url)[-1]#拓展名不一定是后面的那些
    if '.gif' in url:
        extension='.gif'
    elif '.png' in url:
        extension='.png'
    elif '.jpg' in url:
        extension='.jpg'
    elif '.jpeg' in url:
        extension='.jpeg'
    else:
        extension=re.findall('.*(\..*)',url)[-1]#拓展名不一定是后面的那些
    try:
        os.makedirs('..'+os.sep+'pic' + os.sep + title)#路径
    except:
        pass
    file_name = (".."+os.sep+'pic'+os.sep+title+os.sep+title+str(count + 1) + extension)#路径
    file_name=re.sub(re.compile('[/\:*?"<>|]') , '',file_name)
    res = requests.get(url)
    print(len(res.content) // 1024 // 1024, url)
    with open(file_name, 'wb') as f:
        f.write(res.content)
    print('保存成功')
def process_download(save_pic, url_list,title):
    processes = []
    start = time.time()
    for i in range(len(url_list)):
        # 创建线程
        p = multiprocessing.Process(target=save_pic, args=[url_list[i], i,title])
        p.start()
        processes.append(p)
        # 每个进程按顺序逐个执行
        # p.join()
    # 多进程并发
    # print('process_download',threading.currentThread())

    for p in processes:
        p.join()
    end = time.time()
    print('多进程总耗时：%r' % (end - start))
if __name__ == '__main__':
    pic_type=input('输入类型\n1技术交流\n2新時代的我們\n3達蓋爾的旗幟\n')
    page1 = input("输入start页面")
    page2 = input("end")
    crawled=[]
    try:
        with open('已爬取草榴p.log', 'r') as file:
                for line in file:
                    crawled.append(line[:-1])
    except:
        pass
    for page in range(int(page1), int(page2) + 1):
        a = _1_get_url(str(page),pic_type)
        for i in a:
            if i not in crawled:
                try:
                    with open('已爬取草榴p.log', 'a') as file:
                        file.write(i+'\n')
                    imgs = getimgscl('https://co.oustrave.com/' + i + 'html')
                    title = imgs[0]
                    print(title)
                    del imgs[0]
                    process_download(save_pic, imgs, title)
                except:
                    print('下载失败')

            else:
                print('已爬取，跳过',i)
