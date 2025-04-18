import httpx

API_URL = "http://127.0.0.1:8000/expenses/"


async def send_expense_to_api(data: dict) -> bool:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(API_URL, json=data)
        return response.status_code == 200
    except Exception as e:
        print("API ERROR:", e)
        return False
