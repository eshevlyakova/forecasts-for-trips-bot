from services.location_service import fetch_location_data, fetch_weather_data
from aiohttp import ClientSession
from html import escape

async def get_weather_report(start, end, intermediate, interval):
    locations = [start] + (intermediate or []) + [end]
    weather_data = ["🌍 <b>Прогноз погоды для городов:</b>", "\n---\n"]

    async with ClientSession() as session:
        for location in locations:
            try:
                location_data = await fetch_location_data(location, session)
                weather = await fetch_weather_data(location_data['Key'], interval, session)

                weather_data.append(f"<b>{escape(location)} 🌆:</b>")
                weather_data.append(escape(weather))
                weather_data.append("\n---\n")
            except Exception as e:
                weather_data.append(f"<b>{escape(location)} 🚫:</b> Ошибка ({escape(str(e))})")
                weather_data.append("\n---\n")

    return "\n".join(weather_data)
