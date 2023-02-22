# www.aithe.dev
# github.com/aithedev/opensea-twitter-scraper

from random import choice
from bs4 import BeautifulSoup
from cloudscraper import create_scraper

class Scraper:
    def __init__(self) -> None:
        self.session = create_scraper()
        self.addresses = open('./addresses.txt', 'r').read().splitlines()
        self.proxies = open('./proxies.txt', 'r').read().splitlines()
    
    @property
    def proxy(self) -> dict:
        if self.proxies == []:
            return {}
        _proxy = choice(self.proxies)
        return {'http': f'http://{_proxy}', 'https': f'https://{_proxy}'}


    def scrape(self):
        for address in self.addresses:
            response = self.session.get(
                url=f'https://opensea.io/{address}',
                proxies=self.proxy,
                timeout=20
            )

            if response.status_code == 200:
                    parser = BeautifulSoup(response.text, 'html.parser')
                    for a in parser.find_all('a', {'class': 'sc-1f719d57-0 fKAlPV'}):
                        twitter = a.get('href').replace('https://twitter.com/', '')
                    if '@opensea' not in twitter:
                        print(f'[+] {address} -> {twitter}')
                        with open('twitters.txt', 'a+') as f:
                            f.write(f'{address} -> {twitter}\n')
                    else:
                        print(f'[-] {address} -> Twitter Not Found')
            else:
                print(f'[-] {address} -> Failed getting Twitter | {response.status_code}')


if __name__ == '__main__':
    Scraper().scrape()
