#!/usr/bin/env python3
from urllib.parse import quote
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from src.config import MOVIE_SITES
from src.logger import logger


async def search(site_name, site_url, keyword, selector):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        url = site_url.format(quote(keyword))
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    markup = resp.content
                    soup = BeautifulSoup(markup, "lxml")
                    movies = soup.select(selector)
                    if movies:
                        logger.debug("{} success, url: {}".format(site_name, url))
                else:
                    logger.debug("{} fail, url: {}".format(site_name, url))
        except:
            # logger.debug("{} fail, url: {}".format(site_name, url))
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
