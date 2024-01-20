from bs4 import BeautifulSoup
import requests


def make_soup(url):
    headers = {
        "User-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        "Accept-Language": 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        "Accept-Encoding": 'gzip, deflate, br',
        "Cache-Control": 'no-cache',
        "Sec-Fetch-Site": 'same-site',
        "Sec-Fetch-Mode": 'no-cors',
        "Sec-Fetch-Dest": 'script',
    }
    req = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(req.text, "lxml")
    return soup
