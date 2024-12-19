from dotenv import load_dotenv

load_dotenv()

BASE_URL = 'http://dataservice.accuweather.com/'
WEATHER_API_KEY = 'hcim65SyN9VGqzB0ULKzGBEwR5B0e8rE'

async def fetch_location_data(city_name, session):
    url = f"{BASE_URL}locations/v1/cities/search"
    params = {'apikey': WEATHER_API_KEY, 'q': city_name}
    async with session.get(url, params=params) as response:
        response.raise_for_status()
        data = await response.json()

    if not data:
        raise ValueError(f"Город не найден: {city_name}")

    return data[0]

async def fetch_weather_data(location_key, days, session):
    url = f"{BASE_URL}forecasts/v1/daily/{days}day/{location_key}"
    params = {'apikey': WEATHER_API_KEY, 'details': 'true'}
    async with session.get(url, params=params) as response:
        response.raise_for_status()
        data = await response.json()

    forecasts = data['DailyForecasts']
    result = []

    for day in forecasts:
        day_humidity = day['Day']['RelativeHumidity']['Average']
        night_humidity = day['Night']['RelativeHumidity']['Average']
        avg_humidity = (day_humidity + night_humidity) / 2

        temp_min_f = day['Temperature']['Minimum']['Value']
        temp_max_f = day['Temperature']['Maximum']['Value']
        temp_min_c = (temp_min_f - 32) * 5.0 / 9.0
        temp_max_c = (temp_max_f - 32) * 5.0 / 9.0
        avg_temp_c = (temp_min_c + temp_max_c) / 2

        wind_speed_kmh = day['Day']['Wind']['Speed']['Value'] * 1.60934

        result.append(
            f"🗓 {day['Date'][:10]}:\n"
            f"Температура: {round(avg_temp_c, 2)}°C️\n"
            f"Влажность: {round(avg_humidity, 2)}%\n"
            f"Ветер: {round(wind_speed_kmh, 2)} км/ч️\n"
        )

    return "\n".join(result)
