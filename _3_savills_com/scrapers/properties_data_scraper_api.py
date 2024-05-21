import asyncio
import aiohttp

from _3_savills_com.settings import API_PAYLOAD, HEADERS, API_URL


class PropertiesDataScraperAPI:
    def __init__(self) -> None:
        self.headers = HEADERS

    @staticmethod
    async def fetch_data(session, url, payload) -> dict:
        async with session.post(url, json=payload) as response:
            return await response.json()

    async def get_json_data(self) -> list:
        result = []
        for payload in API_PAYLOAD:

            async with aiohttp.ClientSession(headers=self.headers) as session:
                page = 1
                while True:
                    payload_copy = payload.copy()
                    payload_copy["url"] += f"{page}"
                    responses = await self.fetch_data(session, API_URL, payload_copy)
                    result_responses = responses["Results"]["Properties"]
                    if result_responses:
                        result += result_responses
                        page += 1
                        await asyncio.sleep(0.1)
                    if len(result_responses) == 0:
                        break
        return result

    def scrape_properties_data(self) -> list:
        return asyncio.run(self.get_json_data())
