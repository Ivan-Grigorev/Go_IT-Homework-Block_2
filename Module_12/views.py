import aiohttp_jinja2

from datetime import datetime

from init_db import db


@aiohttp_jinja2.template('show_weather.html')
async def index(request):
    cursor_ow = db.open_weather.find().sort([['_id', -1]]).limit(1)
    for document_ow in await cursor_ow.to_list(length=None):
        response = aiohttp_jinja2.render_template('show_weather.html', request, {
            'ow_name': document_ow['name'],
            'ow_temp_c': (document_ow['main']['temp'] - 273.15).__round__(1),
            'ow_temp_f': ((document_ow['main']['temp'] - 273.15) * 9 / 5 + 32).__round__(1),
            'ow_clouds': document_ow['clouds']['all'],
            'ow_wind_kmh': (document_ow['wind']['speed'] * 3.6).__round__(1),
            'ow_wind_mh': (document_ow['wind']['speed'] * 2.237).__round__(1),
            'ow_visibility_km': (document_ow['visibility'] / 1000).__round__(1),
            'ow_visibility_m': (document_ow['visibility'] / 1609).__round__(1),
            'ow_pressure': document_ow['main']['pressure'],
            'ow_humidity': document_ow['main']['humidity'],
            'ow_dt': datetime.fromtimestamp(document_ow['dt'])
        })
        return response

    cursor_wi = db.weather_api.find().sort([['_id', -1]]).limit(1)
    for document_wi in await cursor_wi.to_list(length=None):
        response = aiohttp_jinja2.render_template('show_weather.html', request, {
            'wi_name': document_wi['location']['name'],
            'wi_temp_c': document_wi['current']['temp_c'],
            'wi_temp_f': document_wi['current']['temp_f'],
            'wi_cloud': document_wi['current']['cloud'],
            'wi_wind_kph': document_wi['current']['wind_kph'],
            'wi_wind_mph': document_wi['current']['wind_mph'],
            'wi_vis_km': document_wi['current']['vis_km'],
            'wi_vis_miles': document_wi['current']['vis_miles'],
            'wi_pressure': document_wi['current']['pressure_mb'],
            'wi_humidity': document_wi['current']['humidity'],
            'wi_dt': datetime.fromtimestamp(document_wi['current']['last_updated_epoch'])
        })
        return response
