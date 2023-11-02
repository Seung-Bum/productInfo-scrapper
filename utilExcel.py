import pandas as pd
from openpyxl import Workbook


def makeExcel(category, dataList):
    print("MakeExcel Start")
    wb = Workbook()
    ws = wb.active
    ws.title = "dataList"  # 엑셀 시트명 변경
    ws.append([category])  # 한 행 입력
    ws.append(['idx', 'title', 'status', 'link'])

    for dict in dataList:
        ws.append(
            [dict.get('idx', 'null')],
            [dict.get('title', 'null')],
            [dict.get('status', 'null')],
            [dict.get('link', 'null')]
        )

    wb.save("C:\\")

    # raw_data = {
    #     'idx': [dict.get('idx', 'null')],
    #     'title': [dict.get('title', 'null')],
    #     'status': [dict.get('status', 'null')],
    #     'link': [dict.get('link', 'null')]
    # }  # 리스트 자료형으로 생성
    # raw_data1 = pd.DataFrame(raw_data)  # 데이터 프레임으로 전환 및 생성
    # raw_data2 = pd.DataFrame(raw_data)  # 데이터 프레임으로 전환 및 생성
    # xlxs_dir = 'sample.xlsx'  # 경로 및 파일명 설정
    # with pd.ExcelWriter(xlxs_dir) as writer:
    #     # raw_data1 시트에 저장
    #     raw_data1.to_excel(writer, sheet_name='raw_data1')
    #     # raw_data2 시트에 저장
    #     raw_data2.to_excel(writer, sheet_name='raw_data2')
