from pydantic import BaseModel


class Venue(BaseModel):
    """
    Represents the data structure of a Venue.
    """

    title: str
    image_url: str
    brand: str
    model: str
    year: int
    km: int # Kilometers
    price: str # Use string to capture original format (e.g., "Rp 150.000.000")
    currency: str
    transmission: str
    fuel: str
    city: str
    seller_name: str
    # listing_id: str
