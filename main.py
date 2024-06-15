from fastapi import FastAPI, Depends

from ozon_api import OzonAPIClient
from validation import Product, Action, APIClient


app = FastAPI()


def get_api_client(api_client: APIClient) -> OzonAPIClient:
    return OzonAPIClient(
        api_key=api_client.api_key,
        client_id=api_client.client_id
    )


@app.post("/get-actions/")
async def get_actions(client: OzonAPIClient = Depends(get_api_client)):
    return await client.get_actions()


@app.post("/get-actions-candidates/")
async def get_actions_candidates(action: Action, client: OzonAPIClient = Depends(get_api_client)):
    return await client.get_actions_candidates(action)


@app.post("/activate-actions-products/")
async def activate_actions_products(
        action: Action,
        products: list[Product],
        client: OzonAPIClient = Depends(get_api_client)
):
    return await client.activate_actions_products(action, products)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
