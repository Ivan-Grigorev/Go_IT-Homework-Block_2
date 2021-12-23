import aiohttp_jinja2
import jinja2
import asyncio
import aiohttp

from aiohttp import web


async def get_open_weather(session, url):
    async with session.get(url) as resp:
        open_weather = await resp.json()
        from init_db import db
        await db.open_weather.insert_one(open_weather)
        print("Weather forecast from 'Open Weather' successfully added to database!")


async def get_weather_api(session, url):
    async with session.get(url) as resp:
        weather_api = await resp.json()
        from init_db import db
        await db.weather_api.insert_one(weather_api)
        print("Weather forecast from 'Weather API' successfully added to database!")


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        open_weather_url = f"https://api.openweathermap.org/" \
                           f"data/2.5/weather?q={city}&appid=206c04ecd30711b37b3e460efd0e40d7"
        weather_api_url = f"https://api.weatherapi.com/" \
                          f"v1/current.json?key=ce1a47e57b034d8f853120037211612&q={city}&aqi=yes"
        tasks.append(asyncio.ensure_future(get_open_weather(session, open_weather_url)))
        tasks.append(asyncio.ensure_future(get_weather_api(session, weather_api_url)))

        await asyncio.gather(*tasks)


app = web.Application()
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))


if __name__ == '__main__':
    city = input("Enter the city for search weather forecast:\n>> ").title()
    asyncio.run(main())
    from routes import setup_routes
    setup_routes(app)
    web.run_app(app)
