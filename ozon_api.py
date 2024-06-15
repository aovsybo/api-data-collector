import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import requests

from validation import Product, Action


ACTION_PRICE_LIMIT_PERCENTAGE = 10

class OzonAPIClient:
    def __init__(self, api_key: str, client_id: str):
        self.api_key = api_key
        self.client_id = client_id
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.api_link = "https://api-seller.ozon.ru/"

    def _get_headers(self):
        return {
            'Api-Key': self.api_key,
            'Client-Id': self.client_id,
            'Content-Type': 'application/json'
        }

    def _send_get_request(self, url: str):
        response = requests.get(url, headers=self._get_headers())
        return response.json()

    def _send_post_request(self, url: str, data: dict):
        response = requests.post(url, headers=self._get_headers(), json=data)
        return response.json()

    async def _send_request_async(self, method: callable, url: str, data: dict | None = None):
        loop = asyncio.get_running_loop()
        func = partial(method, url, data) if data else partial(method, url)
        response = await loop.run_in_executor(self.executor, func)
        return response

    async def get_actions(self):
        return await self._send_request_async(
            method=self._send_get_request,
            url=f"{self.api_link}v1/actions"
        )

    async def get_actions_candidates(self, action: Action):
        return await self._send_request_async(
            method=self._send_post_request,
            url=f"{self.api_link}v1/actions/candidates",
            data={"action_id": action.action_id}
        )

    @staticmethod
    def is_action_valid(product: Product, product_prices: dict) -> bool:
        old_price = float(product_prices[product.product_id])
        price_diff = old_price - product.action_price
        return price_diff / old_price * 100 <= ACTION_PRICE_LIMIT_PERCENTAGE

    async def activate_actions_products(self, action: Action, products: list[Product]):
        products_ids = [product.product_id for product in products]
        product_prices = await self.get_product_prices(products_ids=products_ids)
        products_to_activate = [product.dict() for product in products if self.is_action_valid(product, product_prices)]
        return await self._send_request_async(
            method=self._send_post_request,
            url=f"{self.api_link}v1/actions/products/activate",
            data={
                "action_id": action.action_id,
                "products": products_to_activate
            }
        )

    async def get_product_prices(self, products_ids: list[int]):
        product_prices = await self._send_request_async(
            method=self._send_post_request,
            url=f"{self.api_link}v4/product/info/prices",
            data={
                "filter": {
                    "product_id": products_ids,
                    "visibility": "ALL"
                },
                "limit": 100
            }
        )
        return {product["product_id"]: product["price"]["price"] for product in product_prices["result"]["items"]}
