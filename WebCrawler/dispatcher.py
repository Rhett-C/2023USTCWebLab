import url_manager
import web_parser


def GetWebdata(line, type):
    if type == "movie":
        url_movie = url_manager.GetUrl(line, "movie")
        dataList_movie = web_parser.AnalysisData_movie(url_movie)
        return dataList_movie
    if type == "book":
        url_book = url_manager.GetUrl(line, "book")
        dataList_book = web_parser.AnalysisData_book(url_book)
        return dataList_book


def ProtectCrawler():
    '''在遭遇反爬机制时尝试绕过'''
    # TODO: 更换headers伪装, 或者使用代理IP
    pass


def LineInit():
    url_manager.LineInit()


def LineSave():
    # TODO
    pass


def LineLoad():
    # TODO
    pass


# <--- debug only ---->

def Running(startLine, runTime, type):
    '''
    爬取数据
    startLine: 从第几行开始爬取
    runTime: 爬取多少次
    type: 爬取的类型 (电影或书籍)
    '''
    for time in range(runTime):
        line = startLine + time
        dataList = GetWebdata(line, type)

        print("Crawling: " + str(line))
        print(dataList) # debug only

        # TODO: save dataList in the file?
    # TODO: output the result

if __name__ == "__main__":
    LineInit()
    Running(1, 15, "movie")

