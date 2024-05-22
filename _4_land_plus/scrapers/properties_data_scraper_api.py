import asyncio
import aiohttp

from _4_land_plus.settings import API_CHANNEL, API_URL
from scraping.config import USER_AGENT


class PropertiesDataScraperAPI:
    def __init__(self) -> None:
        self.headers = {"user-agent": USER_AGENT}

    @staticmethod
    async def fetch_data(session, url, method="GET", form_data=None) -> dict:
        async with session.request(
            method, url, data=form_data, timeout=10000
        ) as response:
            return await response.json()

    async def get_property_ids(self, session, form_data) -> list:
        property_ids = []
        page = 1

        while True:
            form_data["page"] = page
            response = await self.fetch_data(
                session, API_URL + "search", method="POST", form_data=form_data
            )
            listings = response.get("listings")

            if not listings:
                break

            property_ids.extend([listing.get("id") for listing in listings])
            page += 1
            await asyncio.sleep(0.1)

        return property_ids

    async def get_property_details(self, session, property_ids) -> list:
        results = []
        step = 30

        for i in range(0, len(property_ids), step):
            tasks = [
                self.fetch_data(session, API_URL + f"{property_id}")
                for property_id in property_ids[i : i + step]
            ]
            results.extend(await asyncio.gather(*tasks))
            await asyncio.sleep(0.1)

        return results

    async def get_json_data(self) -> list:
        property_ids = []

        async with aiohttp.ClientSession(headers=self.headers) as session:
            for channel in API_CHANNEL:
                form_data = {
                    "channel": channel,
                    "keyword": "Singapore",
                    "country": "Singapore",
                    "north_east": "1.3610389499982616,103.85122794195556",
                    "south_west": "1.3454650250011437,103.80960005804442",
                    "page": 0,
                }
                property_ids.extend(await self.get_property_ids(session, form_data))

        async with aiohttp.ClientSession(headers=self.headers) as session:
            return await self.get_property_details(session, property_ids)

    def scrape_properties_data(self) -> list:
        return asyncio.run(self.get_json_data())
