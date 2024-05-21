from _3_savills_com.settings import BASE_URL


class PropertyCardScraper:

    @staticmethod
    def get_operation_type(data: dict) -> str:
        index_type = data["RentBasis"]
        if index_type == 1:
            return "For Rent"
        if index_type == 0:
            return "For Buy"

    @staticmethod
    def get_property_features(data: dict) -> int:
        bedrooms = int(data["Bathrooms"])
        bathrooms = int(data["Bedrooms"])
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
    def get_property_description(data: list | None) -> str | None:
        if data:
            description = data[0].get("Body")
            return description

    @staticmethod
    def get_property_images(data: list | None) -> list:
        if data:
            images = [image_url.get("ImageUrl_L") for image_url in data]
            return images
        return []

    @staticmethod
    def get_property_area(data: list | None) -> str | None:
        try:
            if data:
                return data[1]
        except IndexError:
            return None

    def get_property_data(self, data: dict) -> dict:
        return {
            "url": BASE_URL + data["MetaInformation"]["CanonicalUrl"],
            "operation_type": self.get_operation_type(data),
            "title": self.get_property_title(data),
            "property_type": self.get_property_type(data),
            "address": data.get("AddressLine2"),
            "region": None,
            "description": self.get_property_description(data.get("LongDescription")),
            "pictures": self.get_property_images(data.get("ImagesGallery")),
            "price": data.get("DisplayPriceText"),
            "rooms_cnt": self.get_property_features(data),
            "area": self.get_property_area(data.get("HeaderSizeFormatted")),
        }
