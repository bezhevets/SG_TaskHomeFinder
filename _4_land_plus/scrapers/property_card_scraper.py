import json

from bs4 import BeautifulSoup

from _4_land_plus.settings import BASE_URL


class PropertyCardScraper:

    @staticmethod
    def get_operation_type(data: dict) -> str:
        operation_type = data.get("channel")
        if operation_type == "For Sale":
            return "For Buy"
        return operation_type

    @staticmethod
    def get_property_features(data: dict) -> int:
        bedrooms = data.get("bedrooms")
        bathrooms = data.get("bathrooms")
        rooms = 0
        if bedrooms:
            rooms += bedrooms
        if bathrooms:
            rooms += bathrooms
        return rooms

    @staticmethod
    def get_property_type(data: dict) -> str | None:
        property_types = data.get("PropertyTypes")
        if property_types:
            property_type = property_types[0].get("Caption")
            return property_type

    @staticmethod
    def get_property_title(data: dict) -> str | None:
        property_page_title = data.get("PropertyPageTitle")
        if property_page_title:
            property_title = property_page_title.split(" | ")[0]
            return property_title

    @staticmethod
    def get_property_images(soup: BeautifulSoup) -> list:
        media_slider = soup.find("div", id="media-slider")
        data_props = media_slider["data-props"]
        data_props = data_props.replace("&quot;", '"')
        data = json.loads(data_props)
        image_links = [photo["fullnail"] for photo in data["photos"]]
        return image_links

    @staticmethod
    def get_property_area(data: list | None) -> str | None:
        try:
            if data:
                return data[1]
        except IndexError:
            return None

    def get_property_data(self, data: dict) -> dict:
        return {
            "url": f"{BASE_URL}listings/{data.get('id')}",
            "operation_type": self.get_operation_type(data),
            "title": data.get("property_name"),
            "property_type": data.get("category_text"),
            "address": data.get("title_text"),
            "region": None,
            "description": data.get("description"),
            "pictures": [],
            "price": data.get("amount_text"),
            "rooms_cnt": self.get_property_features(data),
            "area": None,
        }
