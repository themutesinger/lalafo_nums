import asyncio
import aiohttp
import csv
from bs4 import BeautifulSoup

# async def get_status(url, session):
#     async with session.get(url, allow_redirects=True) as response:
#         print(response.status)


async def get_phone(page):
    soap = BeautifulSoup(page, 'lxml')
    phone_num = soap.find(class_="phone-wrap").text
    return phone_num


async def get_page(url, headers, session):

    async with session.get(url, allow_redirects=True, headers=headers) as response:
        return await response.text()


async def save_phone(url, headers, file_name, session):
    page = await get_page(url, headers, session)
    try:
        phone = await get_phone(page)
    except:
        phone = 'xxxxx'
    with open(file_name+'.csv', 'a') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([phone, url])


def split_list(a_list, part_count):
    half = int(len(a_list)/part_count)
    parts = []
    for i in range(part_count):
        part = a_list[half*i:half*(i+1)]
        parts.append(part)
    return parts


async def collect(ads_url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,ismage/avif,image/webp,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0"
    }
    file_name = 'numbers'

    # ads_url = ['https://lalafo.kg/karakol/ads/audi-s4-1991-id-100284433']

    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in ads_url:
            # print(url)
            task = asyncio.create_task(save_phone(
                url, headers, file_name, session))
            tasks.append(task)

        await asyncio.gather(*tasks)


def run():
    source = 'ads.csv'
    print('start!!!')
    with open(source, 'r', newline='') as csvfile:
        ads_row = csv.reader(csvfile, delimiter=' ', quotechar='|')
        ads_url = []
        for row in ads_row:
            ads_url.append(row[0])
        lists = split_list(ads_url, 6)
        asyncio.run(collect(lists[0]))
        asyncio.run(collect(lists[1]))
        asyncio.run(collect(lists[2]))
        asyncio.run(collect(lists[3]))
        asyncio.run(collect(lists[4]))
        asyncio.run(collect(lists[4]))
        print("end!!!!")


if __name__ == '__main__':
    run()
