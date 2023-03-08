# aithe.dev
# github.com/aithedev/opensea-twitter-scraper

import cloudscraper
import random
import bs4
from Terminalia import Color

class Scraper:
    def __init__(self) -> None:
        self.session = cloudscraper.create_scraper()
        self.addresses = open("./addresses.txt", "r").read().splitlines()
        self.proxies = open("./proxies.txt", "r").read().splitlines()


    def scrape(self):
        for address in self.addresses:
            response = self.session.get(
                url = f"https://opensea.io/{address}",
                proxies = {"http": f"http://{random.choice(self.proxies)}", "https": f"http://{random.choice(self.proxies)}"},
                timeout = 20
            )

            if response.status_code == 200:
                if "https://twitter.com/" in response.text:
                    parser = bs4.BeautifulSoup(response.text, "html.parser")
                    for a in parser.find_all('a', {"class": "sc-1f719d57-0 fKAlPV"}):
                        twitter = a.get('href').replace("https://twitter.com/", "")
                    if "@opensea" not in twitter:
                        print(f"{Color.GREEN}[+] {address} -> {twitter}{Color.RESET}")
                        open("./twitters.txt", "a+").write(twitter+"\n")
                    else:
                        print(f"{Color.RED}[-] {address} -> Twitter Not Found{Color.RESET}")
                else:
                    print(f"{Color.RED}[-] {address} -> Twitter Not Found{Color.RESET}")
            else:
                print(response.text)


if __name__ == "__main__":
    Scraper().scrape()
