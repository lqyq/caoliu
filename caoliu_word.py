#（已失效）
import requests
import re
import os
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}


def _1_get_url(page):

    url = 'https://co.oustrave.com/thread0806.php?fid=20&search=&page=' + page#文学


    res = requests.get(url, headers=headers)
    res.encoding = 'gbk'
    text = res.text
    # print(text)
    a = re.findall('a href="(.*?)html"', text)
    print('总界面',a)
    return a  # 返回1级页面里面的url




def baocun(url, name):  # 此方法是将图片保存文件到本地 只需要传入图片地址
    n = re.findall('(.*?)[P\-]', name)
    print(n[0][-3:])
    root = "D://h_tupian//" + n[0] + '//'  # 这是根文件所在
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


def _2_get_urlanddl(url, name='default'):
    res = requests.get(url, headers=headers)
    res.encoding = 'gbk'
    text = res.text
    soup = BeautifulSoup(text, 'lxml')
    # print(soup)

    tag_title = soup.find('title')
    title = tag_title.text
    title = re.findall('(.*?)-', title)[0]
    content = soup.find(attrs={'class': 'tpc_content do_not_catch'}).text
    recon = re.sub('<.*?>', '', content)
    try:
        with open(title, 'w', encoding='utf-8')as file:
            file.write(content)
        print('保存成功')
    except:
        print('保存失败',url)


if __name__ == '__main__':
    page1 = input("输入start页面")
    page2 = input("end")
    crawled=[]
    try:
        with open('已爬取草榴word.txt', 'r') as file:
                for line in file:
                    crawled.append(line[:-1])
    except:
        pass
    for page in range(int(page1), int(page2) + 1):
        a = _1_get_url(str(page))
        for i in a:
            if i not in crawled:
                try:
                    with open('已爬取草榴word.txt', 'a') as file:
                        file.write(i+'\n')
                    _2_get_urlanddl('https://co.oustrave.com/' + i + 'html')

                except:
                    print('失败')

            else:
                print('已爬取，跳过',i)
