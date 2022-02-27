import math
import time
from bs4 import BeautifulSoup
import requests
from get_rand_proxy_headers import get_rand_headers, get_rand_proxy
import random


def get_anime_links(_crit=math.inf):
    anime_link_list = []
    limit = 0
    while limit < _crit:
        with requests.Session() as res:
            while True:
                try:
                    anime_list_page = res.get(f"https://myanimelist.net/topanime.php?limit={limit * 50}",
                                              proxies={"http": get_rand_proxy()}, headers=get_rand_headers(),
                                              timeout=100)
                    break
                except Exception:
                    print("scrap_anime_list_page: Change proxy...")
                    time.sleep(0.5)
                    continue

        soup = BeautifulSoup(anime_list_page.text, "html.parser")

        if not soup.find('tr', class_="ranking-list"):
            break

        a_tag_list = soup.find_all('a', class_="fl-l")
        anime_link_list += [link['href'] for link in a_tag_list]

        print(f"scrap_anime_list_page: https://myanimelist.net/people.php?limit={limit * 50}  Success!")
        limit += 1
        time.sleep(round(random.random() * 2, 1))

    print("Successfully get all the links of anime page!")

    return anime_link_list


def test():
    people_list = get_anime_links(2)
    print(len(people_list))
    print(people_list)


if __name__ == "__main__":
    test()
