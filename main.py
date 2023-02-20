import cloudscraper
import re

class Scraper:
    def __init__(self) -> None:
        self.session = cloudscraper.create_scraper()
        self.addresses = open("./addresses.txt", "r").read().splitlines()
        self.proxies =  open("./proxies.txt", "r").read().splitlines() 

    def start(self):
        for address in self.addresses:
            response = self.session.get(
                url = f"https://opensea.io/{address}",
                proxies = self.proxies if self.proxies != '' else None,
                timeout = 20
            )

            if response.status_code == 200:
                if "https://twitter.com/" in response.text:
                    twitter = re.search('<a class="sc-1f719d57-0 fKAlPV" href="https://twitter.com/(.*)" rel="nofollow noopener" target="_blank">', response.text).group(1)
                    if "@opensea" not in twitter:
                        print(f"[+] {address} -> {twitter}")
                        open("./twitters.txt", "a+").write(twitter+"\n")
                    else:
                        print(f"[-] {address} -> Twitter Not Found")
                else:
                    print(f"[-] {address} -> Twitter Not Found")
            else:
                print(response.text)

if __name__ == "__main__":
    Scraper().start()