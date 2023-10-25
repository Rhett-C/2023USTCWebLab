import urllib.request, urllib.error


headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

def GetHtml(url):
    "定义一个函数getHtmlByURL, 得到指定url网页的内容"
    # 自定义headers(伪装, 告诉豆瓣服务器, 我们是什么类型的机器, 以免被反爬虫)
    global headers

    # 利用Request类构造自定义头的请求
    req = urllib.request.Request(url, headers=headers)
    # 定义一个用于接受的变量
    html = ""
    try:
        # urlopen()方法的参数, 发送给服务器并接收响应
        resp = urllib.request.urlopen(req)
        # urlopen()获取页面内容, 返回的数据格式为bytes类型, 需要decode()解码, 转换成str类型
        html = resp.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html
