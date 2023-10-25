import csv


# 定义文件路径
filepath_movie = "./Data/Movie_tag.csv"
filepath_book = "./Data/Book_tag.csv"

# 定义基础url, 每次拼接最后的id即可
baseurl_movie = "https://movie.douban.com/subject/"
baseurl_book = "https://book.douban.com/subject/"

# 定义一个变量, 用于记录当前爬取到文件的第几行
currectLine_movie = 0
currectLine_book = 0


def LineInit():
    global currectLine_movie
    currectLine_movie = 0

    global currectLine_book
    currectLine_book = 0
    
    return True


def ReadLine_csv(filepath, line):
    f = open(filepath, encoding='UTF8')
    rows = list(f)
    # line 0, also as rows[0], is the title
    # 'Id,Tag\n'
    readData = rows[line].replace('\n', '').split(',')
    f.close()
    return readData


def GetUrl(line, type):
    '''
    定义一个函数, 用于获取电影的url
    type决定获取的url是电影的url还是书籍的url
    '''
    if type == "movie":
        url = baseurl_movie + ReadLine_csv(filepath_movie, line)[0]
    if type == "book":
        url = baseurl_book + ReadLine_csv(filepath_book, line)[0]

    print("GetUrl(): " + url)
    return url
