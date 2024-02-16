from challenges.models import Laptop


def brand_and_price_validator(brand: str, price: float) -> bool:
    """
    Validate the brand and price of a laptop.

    Args:
        brand (str): The brand of the laptop.
        price (float): The price of the laptop.

    Returns:
        bool: True if the brand is valid and the price is greater than 0, otherwise False.
    """
    if price <= 0:
        return False
    for brand_choice in Laptop.BRAND_CHOICES:
        if brand in brand_choice:
            return True
    return False
