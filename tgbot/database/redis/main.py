import aiohttp
import json
import xml.etree.ElementTree as ET
from redis.asyncio import Redis


url = 'https://cbr.ru/scripts/XML_daily.asp'

async def fetch_xml(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                xml_content = await response.text()
                return xml_content
            else:
                raise Exception(f"Failed to fetch XML. Status code: {response.status}")


async def update_currency(cache_pool: Redis):
    try:
        xml_content = await fetch_xml(url)
        root = ET.fromstring(xml_content)

        date = root.attrib.get('Date')
        await cache_pool.set(name="date", value=date)
        for valute in root:
            char_code = valute.find('CharCode').text
            d = {}
            d['Name'] = valute.find('Name').text
            d['Nominal'] = valute.find('Nominal').text
            d['Value'] = valute.find('Value').text
            d['VunitRate'] = valute.find('VunitRate').text
            d = json.dumps(d)
            await cache_pool.set(name=char_code, value=d)
    except Exception as e:
        print(e)


async def get_char_codes(cache_pool: Redis) -> list:
    lst: list = await cache_pool.keys()
    lst.remove('date')
    lst.append('RUB')
    return lst


async def get_converted_amount(
    cache_pool: Redis, 
    char_code_in: str, 
    char_code_out: str, 
    amount: str
) -> float:
    if char_code_in != 'RUB':
        currency_in = await cache_pool.get(char_code_in)
        currency_in = json.loads(currency_in)
        amount_in = float(currency_in.get('VunitRate').replace(',', '.'))
    else:
        amount_in = 1
    if char_code_out != 'RUB':
        currency_out = await cache_pool.get(char_code_out)
        currency_out = json.loads(currency_out)
        amount_out = float(currency_out.get('VunitRate').replace(',', '.'))
    else:
        amount_out = 1
    result = round(amount_in * float(amount) / amount_out, 2)
    return result


async def get_currency_info(
    cache_pool: Redis, 
    char_codes: list
) -> list:
    lst = []
    for cc in char_codes:
        d = await cache_pool.get(cc)
        d = json.loads(d)
        lst.append(d)
    return lst
