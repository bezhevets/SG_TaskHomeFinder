# Base urls settings
BASE_URL = "https://search.savills.com/"
API_URL = "https://livev6-searchapi.savills.com/Data/SearchByUrl"
API_PAYLOAD = [
    {
        "url": "/sg/en/list?SearchList=Id_1240+Category_RegionCountyCountry&Tenure=GRS_T_R&SortOrder=SO_PCDD&Currency=GBP&Period=Week&Bedrooms=-1&Bathrooms=-1&CarSpaces=-1&Receptions=-1&ResidentialSizeUnit=SquareFeet&LandAreaUnit=Acre&SaleableAreaUnit=SquareMeter&Category=GRS_CAT_RES&Shapes=W10&CurrentPage="
    },
    {
        "url": "/sg/en/list?SearchList=Id_1240+Category_RegionCountyCountry&Tenure=GRS_T_B&SortOrder=SO_PCDD&Currency=SGD&ResidentialSizeUnit=SquareFeet&LandAreaUnit=Acre&SaleableAreaUnit=SquareMeter&Category=GRS_CAT_RES&Shapes=W10&CurrentPage=",
    },
]
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "accept": "application/json, text/plain, */*",
    "content-type": "application/json",
    "gpscountrycode": "sg",
}
