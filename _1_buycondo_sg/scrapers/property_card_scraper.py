import re

from bs4 import BeautifulSoup


class PropertyCardScraper:

    @staticmethod
    def get_property_characteristics(soup: BeautifulSoup) -> dict:
        info_block = soup.find("div", {"class": "procontent"})
        info_table = info_block.find("table", {"class": "table"})
        try:
            rows_table = info_table.find_all("td")
        except AttributeError:
            return {}
        rows_text = [row.get_text(strip=True) for row in rows_table]

        characteristics = {}
        for i in range(0, len(rows_text), 2):
            characteristics[rows_text[i].replace(":", "")] = rows_text[i + 1]
        return characteristics

    @staticmethod
    def get_property_title(soup: BeautifulSoup) -> str | None:
        try:
            title = soup.find("h1", {"class": "with-view-position"}).get_text(
                strip=True
            )
            result = re.sub(r"\d+views", "", title)
            return result
        except AttributeError:
            return None

    @staticmethod
    def get_property_description(soup: BeautifulSoup) -> str | None:
        description_parts = []
        try:
            description_block = soup.find("div", {"class": "procontent"}).find_all(
                recursive=False
            )
        except AttributeError:
            return None

        for tag in description_block:
            if tag.name == "table":
                continue
            description_parts.append(tag)

        description = "\n".join(
            [part.get_text(strip=True) for part in description_parts]
        )
        return description

    @staticmethod
    def get_property_address(soup: BeautifulSoup) -> str | None:
        try:
            return soup.find("li", {"class": "v_address"}).get_text(strip=True)
        except AttributeError:
            return None

    @staticmethod
    def get_property_price(soup: BeautifulSoup) -> str | None:
        price = soup.find("div", {"class": "porprice for-rent"})
        if price:
            return price.get_text().replace("S$", "$")

        price = soup.find("div", {"class": "single-p_price_on_ask"})
        if price:
            return price.get_text(strip=True)
        return None

    @staticmethod
    def get_property_images(soup: BeautifulSoup) -> list:
        image_block = soup.find("div", {"class": "gallerylist"})
        if image_block:
            image_tags = image_block.find("div", {"id": "gallery"}).find_all("img")
            img_list = [img_url.get("data-image") for img_url in image_tags]
            return img_list
        return []

    def get_property_type(self, soup: BeautifulSoup) -> str | None:
        block_property_type = soup.find(
            "ul",
            {"class": "listprope listpor singlepro"},
        )
        property_type = block_property_type.find("li", {"class": "v_home"})
        try:
            if property_type:
                property_type = property_type.get_text(strip=True)
                property_type_list = property_type.split("/")
                if "Condo" in property_type or "Apt" in property_type_list:
                    return "Apartment"
                return self.get_property_characteristics(soup).get("Property Type")
            return None
        except AttributeError:
            return None

    @staticmethod
    def get_property_features(soup: BeautifulSoup) -> int:
        block_info = soup.find("ul", {"class": "listprope listpor singlepro"})
        bedrooms = block_info.find("li", {"class": "v_bedrooms"})
        bathrooms = block_info.find("li", {"class": "v_bathrooms"})
        rooms = 0
        if bedrooms:
            rooms += int(bedrooms.get_text(strip=True)[0])
        if bathrooms:
            rooms += int(bathrooms.get_text(strip=True)[0])
        return rooms

    @staticmethod
    def get_property_area(soup: BeautifulSoup) -> str | None:
        try:
            return soup.find("li", {"class": "v_sqft"}).get_text(strip=True)
        except AttributeError:
            return None

    @staticmethod
    def get_operation_type(soup: BeautifulSoup) -> str | None:
        price = soup.find("div", {"class": "porprice for-rent"})
        if price:
            return "For Rent"
        return "For Buy"

    def get_property_data(self, soup: BeautifulSoup) -> dict:
        property_block_info = soup.find("ul", {"class": "listprope listpor singlepro"})
        return {
            "title": self.get_property_title(soup),
            "property_type": self.get_property_type(soup),
            "operation_type": self.get_operation_type(soup),
            "address": self.get_property_address(property_block_info),
            "region": None,
            "description": self.get_property_description(soup),
            "pictures": self.get_property_images(soup),
            "price": self.get_property_price(soup),
            "rooms_cnt": self.get_property_features(soup),
            "area": self.get_property_area(property_block_info),
        }
