#!/usr/bin/env python3
from urllib.parse import quote
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from src.config import MOVIE_SITES
from src.logger import logger

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}


async def search(site_name, site_url, keyword, selector):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False), headers=headers) as session:
        url = site_url.format(quote(keyword))
        try:
            async with session.get(url, timeout=5) as resp:
                if resp.status == 200:
                    markup = await resp.text()
                    soup = BeautifulSoup(markup, "lxml")
                    movies = soup.select(selector)
                    if movies:
                        logger.info("site_name: {}, url: {}".format(site_name, url))
                        return {'site_name': site_name, 'url': url}
        except Exception as e:
            pass

def run():
    """
    启动搜索
    """
    logger.debug("searching...")
    loop = asyncio.get_event_loop()
    tasks = [search(item['name'], item['url'], '肖申克的救赎', item['selector']) for item in MOVIE_SITES]
    if tasks:
        loop.run_until_complete(asyncio.wait(tasks))
    logger.info("completed...")


if __name__ == '__main__':
    run()
