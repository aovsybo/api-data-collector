from pydantic import BaseModel


class Action(BaseModel):
    action_id: int


class Product(BaseModel):
    product_id: int
    action_price: int
    stock: int


class APIClient(BaseModel):
    api_key: str
    client_id: str
