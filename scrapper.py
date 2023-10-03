import requests
from bs4 import BeautifulSoup
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
