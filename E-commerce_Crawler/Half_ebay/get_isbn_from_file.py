import xlrd
import os
import re
import datetime


def read_excel(filename):
    '''读取excel表格内容'''
    print ("get_isbns start:", datetime.datetime.now())
    # 打开文件
    workbook = xlrd.open_workbook(filename)

    asin_list = {}
    f = open("./update/isbn/asins1018.txt", "w")

    for i in range(len(workbook.sheets())):
        # 根据sheet索引获取sheet内容
        sheet = workbook.sheet_by_index(i)
        nrows = sheet.nrows
        #     print nrows

        for j in range(nrows):
            # 获取单元格内容
            if j == 0:
                if sheet.cell(j, 0).value.encode('utf-8').isdigit():
                    asin_list[sheet.cell(j, 0).value.encode('utf-8')] = ""
                    f.write(sheet.cell(j, 0).value.encode('utf-8') + "\n")
            else:
                if sheet.cell(j, 0).value.encode('utf-8') not in asin_list:
                    asin_list[sheet.cell(j, 0).value.encode('utf-8')] = ""
                    f.write(sheet.cell(j, 0).value.encode('utf-8') + "\n")
                    #         if i==0:
                    #             if sheet.cell(i,0).value.encode("utf-8").isdigit():
                    #                 asin_list[sheet.cell(i,0).value.encode('utf-8')]=""
                    #                 f.write(sheet.cell(i,0).value.encode('utf-8')+"\n")
                    #             if sheet.cell(i,2).value.encode("utf-8").isdigit():
                    #                 asin_list[sheet.cell(i,2).value.encode('utf-8')]=""
                    #                 f.write(sheet.cell(i,2).value.encode('utf-8')+"\n")
                    #         else:
                    #             if sheet.cell(i,0).value.encode('utf-8') not in asin_list:
                    #                 asin_list[sheet.cell(i,0).value.encode('utf-8')]=""
                    #                 f.write(sheet.cell(i,0).value.encode('utf-8')+"\n")
                    #             if sheet.cell(i,2).value.encode("utf-8") and sheet.cell(i,2).value.encode("utf-8") not in asin_list:
                    #                 asin_list[sheet.cell(i,2).value.encode('utf-8')]=""
                    #                 f.write(sheet.cell(i,2).value.encode('utf-8')+"\n")
    print ("get_isbns end:", datetime.datetime.now())


#     return asin_list


def getFileName(path):
    ''' 获取指定目录下的所有指定后缀的文件名 '''

    f_list = os.listdir(path)
    # print f_list
    for i in f_list:
        # os.path.splitext():分离文件名与扩展名
        if os.path.splitext(i)[1] == '.xls' or os.path.splitext(i)[1] == '.xlsx':
            return i


def get_isbns(path):
    filename = path + "/" + getFileName(path)
    isbns = read_excel(filename)
    #     for i in range(len(isbns)/20+1):
    #        print i,isbns[i*20:(i+1)*20]
    return isbns


if __name__ == '__main__':
    get_isbns(path='./update/isbn')
