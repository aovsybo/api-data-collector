from fastapi import FastAPI, Depends

from ozon_api import OzonAPIClient
from validation import Product, Action
import config


app = FastAPI()


def get_api_client() -> OzonAPIClient:
    return OzonAPIClient(
        api_key=config.API_KEY,
        client_id=config.CLIENT_ID,
    )


@app.get("/get-actions/")
async def send_request(client: OzonAPIClient = Depends(get_api_client)):
    future = client.get_actions()
    result = await future
    return result


@app.post("/get-actions-candidates/")
async def send_request(action: Action, client: OzonAPIClient = Depends(get_api_client)):
    future = client.get_actions_candidates(action)
    result = await future
    return result


@app.post("/activate-actions-products/")
async def send_request(action: Action, products: list[Product], client: OzonAPIClient = Depends(get_api_client)):
    future = client.activate_actions_products(action, products)
    result = await future
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
