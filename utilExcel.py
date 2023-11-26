import pandas as pd
import getpass
from openpyxl import Workbook


def makeExcel(category, dataList):
    print("  .MakeExcel Start")
    wb = Workbook()
    ws = wb.active
    ws.title = "dataList"  # 엑셀 시트명 변경
    ws['A1'] = category  # 한 행 입력
    ws.append(['idx', 'title', 'status', 'link'])
    user = getpass.getuser()

    for dict in dataList:
        ws.append([dict['idx'], dict['title'], dict['status'], dict['link']])

    # filename = f'C:\\Users\\{user}\\Desktop\\productScrap.xlsx'
    filename = '.\\productScrap.xlsx'
    wb.save(filename)
    print("  .MakeExcel End")
