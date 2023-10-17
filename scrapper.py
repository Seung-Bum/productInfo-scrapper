import requests
from bs4 import BeautifulSoup
from urllib import parse
from urllib.request import urlopen


def get_product_status(param_list):
    print("- get_product_status START")

    # 메인 카테고리
    mainUrl = f"https://www.gsshop.com/shop/sect/sectM.gs?sectid={param_list[0]}&lsectid={param_list[1]}&msectid={param_list[2]}&lseq={param_list[3]}&gsid={param_list[4]}"
    print("  .mainUrl : " + mainUrl)

    # pageNavigation
    paging = []
    a = urlopen(mainUrl)
    soup = BeautifulSoup(a.read(), 'html.parser')
    attr = soup.select('a')

    # 호출을 그냥 최대 페이지까지 하고 그다음 페이지도 추출했을때 예외가 생기면 그예외 받고 끝내기 무한루프? 로 해보기
    for i in attr:
        print(i)
    # for i in paging:
    #   print('paging : ' + str(paging[i]))

    # 다음 내용을 base64 인코딩 후 endpoint로 붙임
    # {"pageNumber":2,"selected":"opt-page"}7

    # detailList = get_detail_product(mainUrl)
    # return detailList


def get_detail_product(url):
    print("- get_detail_status STRAT")
    rsltList = []
    a = urlopen(url)
    soup = BeautifulSoup(a.read(), 'html.parser')
    buttonTags = soup.find_all('button', 'link-new-tab')
    print('  .buttonTags len : ' + str(len(buttonTags)))

    idx = 0
    for i in buttonTags:
        idx += 1
        orginStr = str(i)
        index1 = int(str(orginStr.find("https")))
        index2 = int(str(orginStr.find("§id")))
        detailUrl = orginStr[index1:index2]
        rsltStatus = extract_Status(detailUrl, idx)
        print(str(idx) + ". ")
        print(rsltStatus)
        rsltList.append(rsltStatus)
    return rsltList


# 상품 url을 받아서 상품의 타이틀과 상태를 리턴한다.
def extract_Status(url, idx):
    print("- extract_Status START")
    a = urlopen(url)
    soup = BeautifulSoup(a.read(), 'html.parser')

    title = soup.find("p", "product-title").text
    print("  .title : " + title)

    status = soup.find("span", "gs-btn red color-only gient").text
    print("  .status : " + status)

    return {
        'idx': idx,
        'title': title,
        'status': status,
        'link': url
    }

    # buttonList = buttonTag.split(',')

    # print(soup.find_all('button', 'link-new-tab'))

    # result = requests.get(url)
    # soup = BeautifulSoup(result.text, "html.parser")
    # pages = soup.find('div', {'class': 'prd-img'})
    # print("pages : " + str(pages))

    # return pages
    # last_page = len(pages)
    # return int(last_page)


# def extract_jobs(last_page, url):
#     jobs = []
#     for page in range(last_page):
#         print(f"Scrapping: page: {page}")
#         result = requests.get(f"{url}{page+1}")
#         soup = BeautifulSoup(result.text, "html.parser")
#         results = soup.find_all("div", {"class": "grid--cell fl1"})
#         for result in results:
#             job = extract_job(result)
#             jobs.append(job)
#     return jobs
