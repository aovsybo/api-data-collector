import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import requests

from validation import Product, Action


class OzonAPIClient:
    def __init__(self, api_key: str, client_id: str):
        self.api_key = api_key
        self.client_id = client_id
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.api_link = "https://api-seller.ozon.ru/v1/"

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
            url=f"{self.api_link}actions"
        )

    async def get_actions_candidates(self, action: Action):
        return await self._send_request_async(
            method=self._send_post_request,
            url=f"{self.api_link}actions/candidates",
            data={"action_id": action.action_id}
        )

    async def activate_actions_products(self, action: Action, products: list[Product]):
        return await self._send_request_async(
            method=self._send_post_request,
            url=f"{self.api_link}actions/products/activate",
            data={
                "action_id": action.action_id,
                "products": [product.dict() for product in products]
            }
        )
