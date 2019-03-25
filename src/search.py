#!/usr/bin/env python3
from urllib.parse import quote
import aiohttp
import asyncio

from src.config import MOVIE_SITES
from src.logger import logger


async def search(site_name, site_url, keyword):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        url = site_url.format(quote(keyword))
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    logger.debug("{} success, url: {}".format(site_name, url))
                else:
                    logger.debug("{} fail, url: {}".format(site_name, url))
        except:
            logger.debug("{} fail, url: {}".format(site_name, url))


def run():
    """
    启动搜索
    """
    logger.debug("searching...")
    loop = asyncio.get_event_loop()
    tasks = [search(item['name'], item['url'], '肖申克的救赎') for item in MOVIE_SITES]
    if tasks:
        loop.run_until_complete(asyncio.wait(tasks))
    logger.info("completed...")


if __name__ == '__main__':
    run()
