# config.py


# BASE_URL = "https://www.carsome.id/beli-mobil-bekas"
# CSS_SELECTOR = "[class^='list-card__item']"

BASE_URL = "https://www.oto.com/mobil-bekas/jakarta-pusat"
CSS_SELECTOR = "[class^='card splide__slide shadow-light filter-listing-card used-car-card']"


REQUIRED_KEYS = [
    "title",
    "image_url",
    "brand",
    "model",
    "year",
    "km",
    "price",
    "currency", # e.g., IDR, USD
    "transmission",
    "fuel",
    "city",
    "seller_name"
    # "listing_id"
]
