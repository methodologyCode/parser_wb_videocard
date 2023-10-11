from typing import List

from pydantic import BaseModel, model_validator


class Product(BaseModel):
    id: int
    name: str
    salePriceU: int
    brand: str
    rating: int

    @model_validator(mode='before')
    def validate_price(cls, values):
        price = values.get('salePriceU')
        if price is not None:
            values['salePriceU'] = price // 100
        return values


class Products(BaseModel):
    products: List[Product]
