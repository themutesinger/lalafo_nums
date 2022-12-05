import asyncio
import aiohttp
import csv
from bs4 import BeautifulSoup

from config import PAGE_COUNT

# async def get_status(url, session):
#     async with session.get(url, allow_redirects=True) as response:
#         print(response.status)


async def get_hrefs(page):
    soap = BeautifulSoup(page, 'lxml')
    allAd = soap.findAll(class_="adTile-mainInfo-link")
    return allAd


async def get_page(url, headers, session):
    async with session.get(
        url, allow_redirects=True,
        headers=headers
    ) as response:
        return await response.text()


async def save_href(url, headers, file_name, session):

    page = await get_page(url, headers, session)
    hrefs = await get_hrefs(page)
    with open(file_name+'.csv', 'a') as csvfile:
        csvwriter = csv.writer(csvfile)
        for ad in hrefs:
            csvwriter.writerow(['https://lalafo.kg'+ad.get("href")])


async def collect():
    url = 'https://lalafo.kg/?page='
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,ismage/avif,image/webp,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0"
    }
    file_name = 'ads'
    page_count = PAGE_COUNT

    tasks = []
    async with aiohttp.ClientSession() as session:
        for i in range(1, page_count+1):

            task = asyncio.create_task(
                save_href(url+str(i), headers, file_name, session))
            tasks.append(task)
            print(i)
        await asyncio.gather(*tasks)


def run():
    asyncio.run(collect())


if __name__ == '__main__':
    run()
