from bs4 import BeautifulSoup
import re
import web_downloader


# 获取豆瓣*电影*的网页信息

# 定义正则对象获取指定的内容
# 注: 在re.compile()中添加 ,re.S 让'.'特殊字符匹配任何字符, 包括换行符;

# 提取影片名称 e.g. "name": "肖申克的救赎 The Shawshank Redemption",
findMovieTitle = re.compile(r'"name": "(.*)",')

# 提取图片 e.g. "image": "https://img2.doubanio.com/view/photo/s_ratio_poster/public/p480747492.webp",
findMovieImgSrc = re.compile(r'"image": "(.*)",')

# 提取简介 
# 普通简介 e.g. <span property="v:summary" class="">阿甘（汤姆·汉克斯 饰）于二战结束后不久出生在美国南方阿拉巴马州一个闭塞的小镇，他先天弱智，智商只有75，然而他的妈妈是一个性格坚强的女性，她常常鼓励阿甘“傻人有傻福”，要他自强不息。<br />阿甘像普通孩子一样上学，并且认识了一生的朋友和至爱珍妮（罗宾·莱特·潘 饰），在珍妮 和妈妈的爱护下，阿甘凭着上帝赐予的“飞毛腿”开始了一生不停的奔跑。<br />阿甘成为橄榄球巨星、越战英雄、乒乓球外交使者、亿万富翁，但是，他始终忘不了珍妮，几次匆匆的相聚和离别，更是加深了阿甘的思念。<br />有一天，阿甘收到珍妮的信，他们终于又要见面……</span>
# 折叠简介 e.g. <span class="all hidden">一场谋杀案使银行家安迪（蒂姆•罗宾斯 Tim Robbins 饰）蒙冤入狱，谋杀妻子及其情人的指控将囚禁他终生。在肖申克监狱的首次现身就让监狱“大哥”瑞德（摩根•弗里曼 Morgan Freeman 饰）对他另眼相看。瑞德帮助他搞到一把石锤和一幅女明星海报，两人渐成患难 之交。很快，安迪在监狱里大显其才，担当监狱图书管理员，并利用自己的金融知识帮助监狱官避税，引起了典狱长的注意，被招致麾下帮助典狱长洗黑钱。偶然一次，他得知一名新入狱的小偷能够作证帮他洗脱谋杀罪。燃起一丝希望的安迪找到了典狱长，希望他能帮自己翻案。阴险伪善的狱长假装答应安迪，背后却派人杀死小偷，让他唯一能合法出狱的希望泯灭。沮丧的安迪并没有绝望，在一个电闪雷鸣的风雨夜，一场暗藏几十年的越狱计划让他自我救赎，重获自由！老朋友瑞德在他的鼓舞和帮助下，也勇敢地奔向自由。<br />本片获得1995年奥斯卡10项提名，以及金球奖、土星奖等多项提名。</span>
findMovieInq = re.compile(r'<span class="" property="v:summary">(.*)</span>', re.S)
findMovieInqHidden = re.compile(r'<span class="all hidden">(.*)</span>', re.S)

# 提取演职员表 e.g. <meta property="video:actor" content="蒂姆·罗宾斯" />
findDirector = re.compile(r'content="([^"]*)"')
findActor = re.compile(r'content="([^"]*)"')

# 提取影片评分 e.g. <strong class="ll rating_num" property="v:average">9.7</strong>
findMovieRate = re.compile(r'<strong class="ll rating_num" property="v:average">(.*)</strong>')

# 提取影片评价人数 e.g. <span property="v:votes">2924421</span>人评价
findMovieJudgeAmt = re.compile(r'<span property="v:votes">(\d*)</span>人评价')

# 提取相关内容
# TODO: findRelated = re.compile(r'<p class="">(.*)</p>(.*)<div', re.S)


def AnalysisData_movie(url):
    '''
    定义一个函数, 并解析这个网页
    目前可以记录以下信息: [[电影名称, 图片链接], 简介, [导演, 演职员表], [评分, 评价人数]]
    '''

    # 定义一个列表以储存每一部电影的信息
    # databin = []
    dataList = []

    # 获取指定网页
    html = web_downloader.GetHtml(url)

    # 指定解析器解析html, 得到BeautifulSoup对象
    soup = BeautifulSoup(html, "html5lib")

    # 在下面的过程中, 尝试从文档树中取得需要的信息
    # item是bs4.element.Tag对象, 将其转换成字符串来处理
    # data[]定义一个列表以储存每一个电影解析的内容


    # 在script块中定位数据块的位置
    data = []
    for item in soup.find_all('script', type="application/ld+json"):
        item = str(item)

        # 添加标题
        # 例如: 肖申克的救赎 The Shawshank Redemption
        # 电影同时具有中文名称和外文名称时如何处理?
        title = re.findall(findMovieTitle, item)[0]
        data.append(title)
        # databin.append(title)

        # 添加图片链接
        img = re.findall(findMovieImgSrc, item)[0]
        data.append(img)
        # databin.append(img)

    dataList.append(data) # 将电影的信息添加到dataList中

    
    data = []
    for item in soup.find_all('div', class_="indent", id="link-report-intra"):

        inq = []    # 初始化inq

        for child in item.children:
            child = str(child)
            # 查找其中的简介(可能有两种格式, 普通简介和折叠简介)
            temp = re.findall(findMovieInq, child)
            if temp != []:
                inq.append(temp)
                break
        if inq == []:
            # 如果没有找到普通简介, 则查找折叠简介
            for child in item.children:
                child = str(child)
                temp = re.findall(findMovieInqHidden, child)
                if temp != []:
                    inq.append(temp)
                    break

        # 电影可能没有简介
        if inq == []:
            inq = "no film introduction found"
        else:
            # 整理简介的字符串, 取出其中的不必要符号
            # 只收集第一个简介
            inq = re.sub(r' |\n', '', inq[0][0])
            inq = inq.replace(u'\u3000', '').replace(u'<br/>', '')
        data.append(inq)
        # databin.append(inq)

    dataList.append(data) # 将电影的信息添加到dataList中

    
    data = []
    for item in soup.find_all('meta', property="video:director"):
        item = str(item)

        # 添加导演信息
        director = re.findall(findDirector, item)[0]
        data.append("Director:" + director)
        # databin.append(director)
    
    for item in soup.find_all('meta', property="video:actor"):
        item = str(item)

        # 添加演职员表
        actor = re.findall(findActor, item)[0]
        data.append(actor)
        # databin.append(actor)

    dataList.append(data)


    data = []
    for item in soup.find_all('div', class_="rating_self clearfix", typeof="v:Rating"):
        item = str(item)

        # 添加评分
        rate = re.findall(findMovieRate, item)[0]
        data.append(rate)
        # databin.append(rate)

        # 添加评价人数
        judgeAmt = re.findall(findMovieJudgeAmt, item)[0]
        data.append(judgeAmt)
        # databin.append(judgeAmt)

    dataList.append(data) # 将电影的信息添加到dataList中


    return dataList



# 获取豆瓣*书籍*的网页信息

# 定义正则对象获取指定的内容

# 提取书籍名称
# e.g. <meta property="og:title" content="挪威的森林" />
# e.g. <span class="pl">原作名:</span> ノルウェイの森<br/>
findBookTitle = re.compile(r'<meta content="(.*)" property="og:title"/>')
findBookTitleOrigin = re.compile(r'<span class="pl">原作名:</span> (.*)<br/>')

# 提取图片 e.g. <meta property="og:image" content="https://img1.doubanio.com/view/subject/l/public/s1221930.jpg" />
findBookImgSrc = re.compile(r'<meta content="(.*)" property="og:image"/>')

# 提取作者信息
# 作者信息 e.g. <meta property="book:author" content="[日] 村上春树" />
# 译者信息(如果有) e.g. ???
# 作者简介信息 e.g. <div class="intro"><p>村上春树（1949- ），日本小说家。曾在早稻田大学文学部戏剧科就读。1979年，他的第一部小说《听风之歌》问世后，即被搬上了银幕。随后，他的优秀作品《1973年的弹子球》、《寻羊冒险记》、《挪威的森林》等相继发表。他的创作不受传统拘束，构思新奇，行文潇洒自在，而又不流于庸俗浅薄。尤其是在刻画人的孤独无奈方面更有特色，他没有把这种情绪写成负的东西，而是通过内心的心智性操作使之升华为一种优雅的格调，一种乐在其中的境界，以此来为读者，尤其是生活在城市里的人们提供了一种生活模式或生命的体验。</p></div>
findArthor = re.compile(r'<meta content="(.*)" property="book:author"/>')
# TODO: findTranslator = ???
findArthorInq = re.compile(r'<div class="intro"><p>(.*)</p></div>', re.S)

# 提取简介
# e.g. <div class="intro"><p>这是一部动人心弦的、平缓舒雅的、略带感伤的恋爱小说。小说主人公渡边以第一人称展开他同两个女孩间的爱情纠葛。渡边的第一个恋人直子原是他高中要好同学木月的女友，后来木月自杀了。一年后渡边同直子不期而遇并开始交往。此时的直子已变得娴静腼腆，美丽晶莹的眸子里不时掠过一丝难以捕捉的阴翳。两人只是日复一日地在落叶飘零的东京街头漫无目标地或前或后或并肩行走不止。直子20岁生日的晚上两人发生了性关系，不料第二天直子便不知去向。几个月后直子来信说她住进一家远在深山里的精神疗养院。渡边前去探望时发现直子开始带有成熟女性的丰腴与娇美。晚间两人虽同处一室，但渡边约束了自己，分手前表示永远等待直子。返校不久，由于一次偶然相遇，渡边开始与低年级的绿子交往。绿子同内向的直子截然相反，“简直就像迎着春天的晨光蹦跳到世界上来的一头小鹿”。这期间，渡边内心十分苦闷彷徨。一方面念念不忘直子缠绵的病情与柔情，一方面又难以抗拒绿子大胆的表白和迷人的活力。不久传来直子自杀的噩耗，渡边失魂魄地四处徒步旅行。最后，在直子同房病友玲子的鼓励下，开始摸索此后的人生。</p></div>
findBookInq = re.compile(r'<p>(.*)[^>]</p></div>', re.S)

# 提取书籍评分 e.g. <strong class="ll rating_num " property="v:average"> 8.1 </strong>
findBookRate = re.compile(r'<strong class="ll rating_num" property="v:average"> (.*) </strong>')

# 提取书籍评价人数 e.g. <a href="comments" class="rating_people"><span property="v:votes">346576</span>人评价</a>
findBookJudgeAmt = re.compile(r'<span property="v:votes">(\d*)</span>人评价')


def AnalysisData_book(url):
    '''
    定义一个函数, 并解析这个网页
    目前可以记录以下信息: [ [[书籍名称], [书籍图片地址], [作者]], [书籍外文原名(若有)], [简介], [[书籍评分], [评价人数]] ]
    '''

    # 定义一个列表以储存每一部电影的信息
    dataList = []

    # 获取指定网页
    html = web_downloader.GetHtml(url)

    # 指定解析器解析html, 得到BeautifulSoup对象
    soup = BeautifulSoup(html, "html5lib")

    # 在下面的过程中, 尝试从文档树中取得需要的信息
    # item是bs4.element.Tag对象, 将其转换成字符串来处理
    # data[]定义一个列表以储存每一个电影解析的内容


    data = []
    for item in soup.find_all('meta'):
        item = str(item)

        # 添加书籍名称
        title = re.findall(findBookTitle, item)
        if title != []:
            data.append(title)

        # 添加书籍图片链接
        img = re.findall(findBookImgSrc, item)
        if img != []:
            data.append(img)

        # 添加作者信息
        arthor = re.findall(findArthor, item)
        if arthor != []:
            data.append(arthor)

    dataList.append(data) # 将书籍的信息添加到dataList中


    data = []
    for item in soup.find_all('div', id="info", class_=""):
        item = str(item)

        # 添加原作名(可能不存在)
        temp = re.findall(findBookTitleOrigin, item)
        if temp != []:
            titleOrigin = temp[0]
            data.append(titleOrigin)

    if data != []:
        dataList.append(data) # 将书籍的信息添加到dataList中
    else:
        dataList.append(["no original title found"])


    data = []
    for item in soup.find_all('div', class_="indent", id="link-report"):
        item = str(item)

        for child in soup.find_all('div', class_="intro"):
            child = str(child)

            # 添加书籍简介
            temp = re.findall(findBookInq, child)
            if temp != []:
                inq = re.findall(findBookInq, child)[0]
                inq = re.sub(r' |\n', '', inq)
                inq = inq.replace(u'<p>', '').replace(u'</p>', '')
                data.append(inq)

    dataList.append(data) # 将书籍的信息添加到dataList中


    # TODO: 译者信息


    data = []
    for item in soup.find_all('div', class_="rating_self clearfix", typeof="v:Rating"):
        item = str(item)

        # 添加评分
        rate = re.findall(findBookRate, item)
        data.append(rate)

        # 添加评价人数
        judgeAmt = re.findall(findBookJudgeAmt, item)
        data.append(judgeAmt)

    dataList.append(data) # 将书籍的信息添加到dataList中


    return dataList


# <--- debug only ---->
if __name__ == "__main__":
    url = "https://book.douban.com/subject/1084336/"
    print(AnalysisData_book(url))