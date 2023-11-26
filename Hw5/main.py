import platform
from datetime import datetime
import logging

import aiohttp
import asyncio


async def request(url: str):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    r = await resp.json()
                    return r
                logging.error(f"Error status: {resp.status} for {url}")
                return None
        except aiohttp.ClientConnectorError as err:
            logging.error(f"Connection error: {str(err)}")
            return None



async def get_exchange(currency_code: str, date: str):
    result = await request(f'https://api.privatbank.ua/p24api/exchange_rates?date={date}')
    
    if result:
        rates = result.get("exchangeRate")
        exc, = list(filter(lambda element: element["currency"] == currency_code, rates))
        print (f"{currency_code}: buy: {exc['purchaseRateNB']}, sale: {exc['saleRateNB']}. Date: {datetime.now().date()}")
    return "Failed to retrieve data"
    
asyncio.run(get_exchange("USD", "23.11.2023"))
asyncio.run(get_exchange("EUR", "23.11.2023"))