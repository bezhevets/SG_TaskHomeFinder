import asyncio

import aiohttp
from bs4 import BeautifulSoup

from core.schemas import Property
from scraping.config import USER_AGENT
from .property_card_scraper import PropertyCardScraper


class PropertiesScraper(PropertyCardScraper):

    @staticmethod
    async def check_results(results: list[Property]) -> list[Property]:
        return [result for result in results if result]

    @staticmethod
    async def fetch_url_content(session, url: str, timeout=10000) -> str:
        async with session.get(url, timeout=timeout) as response:
            return await response.text()

    async def create_property_instance(self, session, property_link: str) -> Property | None:
        try:
            text_response = await self.fetch_url_content(session, property_link)
        except asyncio.TimeoutError:
            return None

        soup = BeautifulSoup(text_response, "html.parser")

        property_data = self.get_property_data(soup)
        return Property(url=property_link, **property_data)

    async def create_coroutines(self, properties_links: list):
        headers = {"user-agent": USER_AGENT}

        async with aiohttp.ClientSession(headers=headers) as session:
            results = []
            step = 30
            for i in range(0, len(properties_links), step):
                tasks = [
                    self.create_property_instance(session, property_link)
                    for property_link in properties_links[i:i + step]
                ]
                results += await asyncio.gather(*tasks)
                await asyncio.sleep(0.5)

            results = await self.check_results(results)
            return results

    def scrape_properties(self, properties_links: list):
        return asyncio.run(self.create_coroutines(properties_links=properties_links))
