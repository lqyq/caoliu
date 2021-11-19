#（已失效）
import requests
import re
import os


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}


def _1_get_url(page):
    url = 'https://co.oustrave.com/thread0806.php?fid=16&search=&page=' + page#達蓋爾的旗幟
    # url='https://cc.yta1.icu/thread0806.php?fid=7&search=565227&page='+page#gif
    # url="https://cc.yta1.icu/thread0806.php?fid=7&search=483423"#gif
    # url = 'https://co.oustrave.com/@%E5%9B%9E%E6%94%B6%E8%A1%A8%E5%A6%B9' #注意看好url

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
    count = 0
    res = requests.get(url, headers=headers)
    res.encoding = 'gbk'
    text = res.text
    # print(text)
    # pprint(text)
    a = re.findall('ess-data=\'(.*?)\'', text)#需要修改
    title1 = re.findall('<title>(.*?)\|', text)
    title = title1[0]
    print(title)
    if title:
        name = title
    for i in a:
        count = count + 1
        baocun(i, name + '(' + str(count) + ')')
        print("保存成功", count)


if __name__ == '__main__':
    page1 = input("输入start页面")
    page2 = input("end")
    crawled=[]
    try:
        with open('已爬取草榴p.txt', 'r') as file:
                for line in file:
                    crawled.append(line[:-1])
    except:
        pass
    for page in range(int(page1), int(page2) + 1):
        a = _1_get_url(str(page))
        for i in a:
            if i not in crawled:
                try:
                    with open('已爬取草榴p.txt', 'a') as file:
                        file.write(i+'\n')
                    _2_get_urlanddl('https://co.oustrave.com/' + i + 'html')

                except:
                    print('失败')

            else:
                print('已爬取，跳过',i)
# _2_get_urlanddl('https://cc.yta1.icu/htm_data/2106/7/4546562.html')
# def download_pic2(img_lists, dir_name):#下载img_lists里的内容到dir_name
#     print("一共有{num}张照片".format(num=len(img_lists)))
#
#     # 标记下载进度
#     index = 1
#
#     for image_url in img_lists:
#         file_name = dir_name + os.sep + basename(urlsplit(image_url)[2])#basename()就是直接把’/‘之前的全删掉，只保留最后一个‘/’后面的内容
#
#         # 已经下载的文件跳过
#         if os.path.exists(file_name):
#             print("文件{file_name}已存在。".format(file_name=file_name))
#             index += 1
#             continue
#
#         # 重试次数
#         retry_time = 3
#         auto_download(image_url, file_name, retry_time)
#
#         print("下载{pic_name}完成！({index}/{sum})".format(pic_name=file_name, index=index, sum=len(img_lists)))
#         index += 1
#
#     # 打印下载出错的文件
#     if len(failed_image_list):
#         print("以下文件下载失败：")
#         for failed_image_url in failed_image_list:
#             print(failed_image_url)
#
#
# #递归下载文件，直到文件下载成功
# def auto_download(image_url, file_name, retry_time):#递归下载文件，直到文件下载成功
#     # 递归下载，直到文件下载成功
#     try:
#         # 判断剩余下载次数是否小于等于0，如果是，就跳过下载
#         if retry_time <= 0:
#             print("下载失败，请检查{image_url}链接是否正确（必要时可以手动下载）")
#             failed_image_list.append(image_url)
#             return
#
#         # 下载文件
#         urllib.request.urlretrieve(image_url, file_name)#下载文件
#
#     except urllib.request.ContentTooShortError:
#         print("文件下载不完整，尝试重新下载，剩余尝试次数{retry_time}".format(retry_time=retry_time))
#         retry_time -= 1
#         auto_download(image_url, file_name, retry_time)
#
#     except urllib.request.URLError as e:
#         print("网络连接出错，尝试重新下载，剩余尝试次数{retry_time}".format(retry_time=retry_time))
#         retry_time -= 1
#         auto_download(image_url, file_name, retry_time)