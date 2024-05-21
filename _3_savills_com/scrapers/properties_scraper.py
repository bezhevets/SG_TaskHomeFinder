import asyncio

from core.schemas import Property
from .property_card_scraper import PropertyCardScraper


class PropertiesScraper(PropertyCardScraper):

    def create_property_instance(self, property_data: dict) -> Property:
        property_data = self.get_property_data(property_data)
        return Property(**property_data)

    async def create_coroutines(self, properties_data: list) -> list:

        list_properties = []
        for property_data in properties_data:
            list_properties.append(self.create_property_instance(property_data))

        return list_properties

    def scrape_properties(self, properties_data: list):
        return asyncio.run(self.create_coroutines(properties_data=properties_data))
