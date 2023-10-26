import csv
import url_manager
import web_parser


movieSavePath = "./Data/MovieData.csv"
bookSavePath = "./Data/BookData.csv"


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


def LineSave(line, dataList, type, writer):
    if type == "movie":
        # dataList-->   [ [[电影名称], [图片链接]], [简介], [导演], [演职员表], [评分, 评价人数] ]
        # save-->       行数, 电影名称, 简介, 导演, 演职员表, 图片链接, 评分, 评价人数
        if dataList != None and len(dataList) == 5 and len(dataList[0]) == 2 and len(dataList[4]) == 2:
            writeData = [line] + dataList[0][0] + dataList[1] + dataList[2] + dataList[3] + dataList[0][1] + dataList[4]
            writer.writerow(writeData)
        else:
            writeData = [line] + ["fetch webpage failed"]
            writer.writerow(writeData)
    elif type == "book":
        # dataList-->   [ [[书籍名称], [书籍图片地址], [作者]], [书籍外文原名(若有)], [简介], [[书籍评分], [评价人数]] ]
        # save-->       行数, 书籍名称, 书籍外文原名(若有), 作者, 简介, 书籍图片地址, 书籍评分, 评价人数
        if dataList != None and len(dataList) == 4 and len(dataList[0]) == 3 and len(dataList[3]) == 2:
            writeData = [line] + dataList[0][0] + dataList[1] + dataList[0][2] + dataList[2] + dataList[0][1] + dataList[3]
            writer.writerow(writeData)
        else:
            writeData = [line] + ["fetch webpage failed"]
            writer.writerow(writeData)


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
    if type == "movie":
        with open(movieSavePath, "a", newline="", encoding='utf-8') as dataFile:
            writer = csv.writer(dataFile)
            for time in range(runTime):
                line = startLine + time
                print("Crawling: " + str(line))

                dataList = GetWebdata(line, type)
                # print(dataList)
                # debug only

                # save dataList in the file?
                LineSave(line, dataList, type, writer)
    
    elif type == "book":
        with open(bookSavePath, "a", newline="", encoding='utf-8') as dataFile:
            writer = csv.writer(dataFile)
            for time in range(runTime):
                line = startLine + time
                print("Crawling: " + str(line))

                dataList = GetWebdata(line, type)
                # print(dataList)
                # debug only

                # save dataList in the file?
                LineSave(line, dataList, type, writer)


def RunningAll(startLine, type):
    Running(startLine, 1200-startLine+1, type)
    


if __name__ == "__main__":
    LineInit()
    RunningAll(175, "book")

