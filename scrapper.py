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


def get_product_status(endpoint):
    asisUrl = f"https://www.gsshop.com/shop/sect/sectM.gs?sectid={endpoint}"
    # tobeUrl = parse.urlparse(asisUrl)
    # query = parse.parse_qs(tobeUrl.query)
    # result = parse.urlencode(query, doseq=True)
    # print("asisUrl : " + asisUrl)
    # print("tobeUrl : " + tobeUrl)

    last_page = get_last_page(asisUrl)
    return last_page
    # jobs = extract_jobs(last_page, url)
    # return jobs


def get_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("nav", {"class": "paging"}).find("a", "data-index")
    print("pages : " + pages)
    return pages
    # last_page = len(pages)
    # return int(last_page)
