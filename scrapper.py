import requests
from bs4 import BeautifulSoup
from urllib import parse
from urllib.request import urlopen


def extract_Status(html):
    a = urlopen(html)
    soup = BeautifulSoup(a.read(), 'html.parser')

    title = soup.find("p", "product-title").text
    print("title : " + title)

    status = soup.find("span", "gs-btn red color-only gient").text
    print("status : " + status)

    return {
        'title': title,
        'status': status,
        'link': html
    }


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


def get_product_status(param_list):
    # 메인 카테고리
    mainUrl = f"https://www.gsshop.com/shop/sect/sectM.gs?sectid={param_list[0]}&lsectid={param_list[1]}&msectid={param_list[2]}&lseq={param_list[3]}&gsid={param_list[4]}"
    print("mainUrl : " + mainUrl)

    detailUrl = get_detail_status(mainUrl)
    return detailUrl
    # jobs = extract_jobs(last_page, url)
    # return jobs


def get_detail_status(url):
    a = urlopen(url)
    soup = BeautifulSoup(a.read(), 'html.parser')
    buttonTags = soup.find_all('button', 'link-new-tab')
    for i in buttonTags:
        orginStr = str(i)
        index1 = int(str(orginStr.find("https")))
        index2 = int(str(orginStr.find("§id")))
        detailUrl = orginStr[index1:index2]
        print('detail url : ' + detailUrl)
        return detailUrl

    # buttonList = buttonTag.split(',')

    # print(soup.find_all('button', 'link-new-tab'))

    # result = requests.get(url)
    # soup = BeautifulSoup(result.text, "html.parser")
    # pages = soup.find('div', {'class': 'prd-img'})
    # print("pages : " + str(pages))

    # return pages
    # last_page = len(pages)
    # return int(last_page)
