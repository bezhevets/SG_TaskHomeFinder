import asyncio

import aiohttp
from aiohttp import ClientPayloadError
from bs4 import BeautifulSoup

from scraping.config import USER_AGENT
from _1_buycondo_sg.settings import BASE_SEARCH_URLS


class PropertiesLinksScraper:
    def __init__(self) -> None:
        self.headers = {"user-agent": USER_AGENT}

    @staticmethod
    async def fetch_url_content(session, url: str, timeout=10000) -> str:
        async with session.get(url, timeout=timeout) as response:
            return await response.text()

    async def get_properties_links(self, session, page_link) -> list | str:
        try:
            text_response = await self.fetch_url_content(session, page_link)
        except asyncio.TimeoutError:
            return "Error"
        except ClientPayloadError:
            return "Error"

        soup = BeautifulSoup(text_response, "html.parser")

        containers = soup.find_all(
            "h3", {"class": "h4 ellipsis text-transform-none"}
        )

        if not containers:
            return []
        links = [container.find("a").get("href") for container in containers]
        return links

    async def create_coroutines(self) -> list:
        results = []
        async with aiohttp.ClientSession(headers=self.headers) as session:
            index = 1
            while True:
                if index == 1:
                    result = await self.get_properties_links(
                        session, f"{BASE_SEARCH_URLS}"
                    )
                else:
                    result = await self.get_properties_links(
                        session, f"{BASE_SEARCH_URLS}pages/{index}/"
                    )
                if result == "Error":
                    index += 1
                    continue

                if not result:
                    break

                results += result
                index += 1
        return results

    def scrape_properties_links(self) -> list:
        return asyncio.run(self.create_coroutines())
