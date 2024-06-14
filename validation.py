from pydantic import BaseModel


class Action(BaseModel):
    action_id: int


class Product(BaseModel):
    product_id: int
    action_price: int
    stock: int
